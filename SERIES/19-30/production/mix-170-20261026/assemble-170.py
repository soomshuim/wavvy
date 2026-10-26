#!/usr/bin/env python3
"""Whole-source two-cycle assembly, one loudnorm pass, shared PCM WAV/AAC outputs."""
import argparse, hashlib, importlib.util, json, math, subprocess, time
from pathlib import Path
import numpy as np
from scipy import signal
ROOT=Path(__file__).resolve().parents[4]; PROD=Path(__file__).resolve().parent
WORK=ROOT/'work/mix-170-20261026';OUT=ROOT/'SERIES/19-30/output/mix-170-20261026';SR=48000
spec=importlib.util.spec_from_file_location('producer170',PROD/'render-170.py');R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R)
sha=R.sha;save=R.save;read=R.read;relative=R.relative

def parsed_loudness(stderr):
    return json.JSONDecoder().raw_decode(stderr[stderr.rfind('{'):])[0]

def measure(p):
    cmd=['ffmpeg','-hide_banner','-nostdin','-i',str(p),'-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-']
    r=R.run(cmd); d=parsed_loudness(r.stderr)
    return {'integrated_lufs':float(d['input_i']),'true_peak_dbtp':float(d['input_tp']),
            'loudness_range_lu':float(d['input_lra']),'raw':d,'command':cmd}

def load():
    sources=[];audio={}
    for n in range(1,21):
        p=PROD/'corrected'/f'{n:02d}.json';j=json.loads(p.read_text());f=ROOT/j['output_path']
        assert sha(f)==j['output_sha256'];assert j['source_start_preserved'] and j['source_end_preserved']
        x=read(f);assert len(x)==j['output_samples'];audio[n]=x
        sources.append(j)
    return sources,audio

def prepare():
    sources,audio=load();entries=[];transitions=[];b0=sources[0]['first_grid_beat_sample']
    for n,s in enumerate(sources*2):
        order=n%20+1;cycle=n//20+1
        loud_path=PROD/'loudness'/f'{order:02d}.json'
        if loud_path.exists():loud=json.loads(loud_path.read_text())
        else:
            loud=measure(ROOT/s['output_path']);save(loud_path,loud)
        gain_db=-16-loud['integrated_lufs']
        if n==0:start=0
        else:
            prev=entries[-1];desired=prev['mix_end_sample']-R.quarter_sample(4)
            beat_index=round((desired+s['first_grid_beat_sample']-b0)*17/288000)
            start=b0+R.quarter_sample(beat_index)-s['first_grid_beat_sample']
            length=prev['mix_end_sample']-start
            assert R.quarter_sample(3)<length<R.quarter_sample(5)
            residual=(start+s['first_grid_beat_sample']-b0)-R.quarter_sample(beat_index)
            assert residual==0
            transitions.append({'number':n,'outgoing_entry':n,'incoming_entry':n+1,
                'outgoing_order':prev['order'],'incoming_order':order,'outgoing_cycle':prev['cycle'],
                'incoming_cycle':cycle,'repeat_boundary_20_to_1':prev['order']==20 and order==1,
                'start_sample':start,'end_sample':prev['mix_end_sample'],'overlap_samples':length,
                'overlap_seconds':length/SR,'grid_phase_residual_samples':residual,
                'bar_phase_confidence':'unconfirmed; quarter-path phase estimate only',
                'outgoing_corrected_frames':[start-prev['mix_start_sample'],prev['samples']],
                'incoming_corrected_frames':[0,length],
                'source0_and_natural_end_retained':True,
                'caveat':'Whole intros/tails retained. A quiet intro may contain no audible beat during overlap.'})
        entries.append({'entry':n+1,'cycle':cycle,'order':order,'song_id':s['song_id'],'title':s['title'],
            'mix_start_sample':start,'mix_end_sample':start+len(audio[order]),'samples':len(audio[order]),
            'mix_start_seconds':start/SR,'mix_end_seconds':(start+len(audio[order]))/SR,
            'corrected_source_frames':[0,len(audio[order])],'source_gain_db':gain_db,
            'corrected_sha256':s['output_sha256'],'corrected_path':s['output_path'],
            'first_grid_beat_sample_global':start+s['first_grid_beat_sample']})
    assert len(entries)==40 and len(transitions)==39
    assert [(e['cycle'],e['order']) for e in entries]==[(c,i) for c in [1,2] for i in range(1,21)]
    assert sum(t['repeat_boundary_20_to_1'] for t in transitions)==1
    plan={'schema':'wavvy.capture_170_whole_source_repeat2_plan.v1','target_bpm':170,
          'repeat_count':2,'additional_repeats':0,'sample_rate':SR,'sources':sources,
          'entries':entries,'transitions':transitions,'samples':entries[-1]['mix_end_sample'],
          'duration_seconds':entries[-1]['mix_end_sample']/SR,'source_gain_target_lufs':-16,
          'musical_source_trimmed':False,'listener_approved':False}
    save(PROD/'mix-plan.json',plan)
    print(json.dumps({'stage':'mix_plan','entries':40,'transitions':39,'duration_seconds':plan['duration_seconds']}),flush=True)
    return plan,audio

def stream(plan,audio):
    # Non-overlap body remains constant gain. Only first/last~one-bar edges fade.
    for start in range(0,plan['samples'],10*SR):
        end=min(start+10*SR,plan['samples']);out=np.zeros((end-start,2),np.float32)
        for k,e in enumerate(plan['entries']):
            a=max(start,e['mix_start_sample']);b=min(end,e['mix_end_sample'])
            if b<=a:continue
            local=np.arange(a-e['mix_start_sample'],b-e['mix_start_sample'])
            weights=np.ones(len(local))
            if k:
                length=plan['transitions'][k-1]['overlap_samples']
                phase=np.clip(local/max(1,length-1),0,1);weights*=np.sin(phase*np.pi/2)
            if k<39:
                length=plan['transitions'][k]['overlap_samples'];first=e['samples']-length
                phase=np.clip((local-first)/max(1,length-1),0,1);weights*=np.cos(phase*np.pi/2)
            out[a-start:b-start]+=np.asarray(audio[e['order']][local[0]:local[-1]+1])*weights[:,None]*10**(e['source_gain_db']/20)
        assert np.isfinite(out).all()
        yield out

def pipe(cmd,plan,audio,logpath):
    h=hashlib.sha256();count=0;peak=0
    with logpath.open('wb') as log:
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
        try:
            for x in stream(plan,audio):
                raw=x.astype('<f4').tobytes();h.update(raw);peak=max(peak,float(np.max(abs(x))));count+=len(x);p.stdin.write(raw)
            p.stdin.close();assert p.wait()==0,logpath.read_text()[-5000:]
        finally:
            if p.poll() is None:p.terminate();p.wait()
    assert count==plan['samples'];return {'sha256':h.hexdigest(),'samples':count,'peak_linear':peak}

def assembly_analysis():
    plan,audio=prepare()
    cmd=['ffmpeg','-hide_banner','-nostdin','-f','f32le','-ar',str(SR),'-ac','2','-i','pipe:0',
         '-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-']
    log=WORK/'assembly-loudnorm-pass1.log';stats=pipe(cmd,plan,audio,log)
    d=parsed_loudness(log.read_text());save(PROD/'assembled-loudness.json',{'command':cmd,'raw':d,'input_pcm':stats})
    print(json.dumps({'stage':'assembled_loudness','raw':d,'pcm':stats}),flush=True)

def encode():
    plan=json.loads((PROD/'mix-plan.json').read_text());_,audio=load()
    measured=json.loads((PROD/'assembled-loudness.json').read_text());d=measured['raw']
    af=(f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={d['input_i']}:measured_LRA={d['input_lra']}:"
        f"measured_TP={d['input_tp']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}:"
        "linear=true:print_format=json,aresample=48000")
    # Encode AAC once, from the SAME normalized PCM that feeds the WAV encoder.
    # asplit explicitly makes both output encoders consume identical frames.
    wav=OUT/'continuous-mix-1930-repeat2.wav';aac=OUT/'continuous-mix-1930-repeat2.m4a'
    assert not wav.exists() and not aac.exists()
    cmd=['ffmpeg','-hide_banner','-nostdin','-n','-f','f32le','-ar',str(SR),'-ac','2','-i','pipe:0',
         '-filter_complex',f'[0:a]{af},asplit=2[w][a]',
         '-map','[w]','-c:a','pcm_s24le',str(wav),'-map','[a]','-c:a','aac','-b:a','320k','-movflags','+faststart',str(aac)]
    stats=pipe(cmd,plan,audio,WORK/'final-encode.log');assert stats['sha256']==measured['input_pcm']['sha256']
    save(PROD/'encode-record.json',{'schema':'wavvy.capture_170_repeat2_encode.v1','command':cmd,
        'pre_normalization_pcm':stats,'one_final_loudnorm_application':True,
        'normalization_actual_report':parsed_loudness((WORK/'final-encode.log').read_text()),
        'wav_path':relative(wav),'wav_sha256':sha(wav),'aac_path':relative(aac),'aac_sha256':sha(aac),
        'aac_encode_generations':1,'same_normalized_pcm_split_to_both_encoders':True,'direct_listening':False})
    print(json.dumps({'stage':'encoded','wav':relative(wav),'m4a':relative(aac)}),flush=True)

def decode_window(path,start,length=SR):
    # A direct AAC input seek can expose decoder warm-up transients in the
    # first samples of a comparison window. Decode two seconds of history,
    # then select exactly the requested samples. This changes no audio file.
    # One/two-second history was compared with full sequential decoding in
    # transition16-decoder-preroll-audit.json; the selected PCM is identical.
    history=min(start,2*SR)
    cmd=['ffmpeg','-v','error','-nostdin','-ss',f'{(start-history)/SR:.12f}','-i',str(path),
         '-af',f'atrim=start_sample={history}:end_sample={history+length},asetpts=N/SR/TB',
         '-t',f'{length/SR:.12f}','-ar',str(SR),'-ac','2','-f','f32le','-']
    x=np.frombuffer(subprocess.check_output(cmd),'<f4').reshape(-1,2)
    assert len(x)==length,(path,start,len(x),length)
    return x,cmd

def verify():
    plan=json.loads((PROD/'mix-plan.json').read_text());enc=json.loads((PROD/'encode-record.json').read_text());_,source_audio=load()
    wav=ROOT/enc['wav_path'];aac=ROOT/enc['aac_path'];assert sha(wav)==enc['wav_sha256'] and sha(aac)==enc['aac_sha256']
    probes={};loud={}
    for label,p in [('wav',wav),('m4a',aac)]:
        probes[label]=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)],text=True))
        s=probes[label]['streams'][0];assert s['sample_rate']=='48000' and s['channels']==2
        assert abs(float(probes[label]['format']['duration'])-plan['duration_seconds'])<.1
        if label=='wav':assert s['codec_name']=='pcm_s24le' and s['bits_per_sample']==24
        else:assert s['codec_name']=='aac' and s['profile']=='LC'
        actual_path=PROD/'final-actual-loudness.json'
        actual=json.loads(actual_path.read_text()) if actual_path.exists() else {}
        cached=actual.get('measurements',{}).get('wav' if label=='wav' else 'aac',{})
        if cached.get('sha256')==sha(p):loud[label]=cached['measurement']
        else:loud[label]=measure(p)
        assert abs(loud[label]['integrated_lufs']+14)<.2 and loud[label]['true_peak_dbtp']<=-1.0,loud[label]
    checks=[]
    locations=[('body',e['entry'],(e['mix_start_sample']+e['mix_end_sample'])//2-SR//2) for e in plan['entries']]
    locations += [('transition',t['number'],(t['start_sample']+t['end_sample'])//2-SR//2) for t in plan['transitions']]
    for kind,n,start in locations:
        x,cmdw=decode_window(wav,start);y,cmda=decode_window(aac,start)
        mx=x.astype(float).mean(axis=1);my=y.astype(float).mean(axis=1)
        energy=float(np.sqrt(np.mean(mx*mx)))
        if energy<1e-6:
            corr=None;lag=None;assert float(np.max(abs(y-x)))<1e-4
        else:
            corr=float(np.dot(mx,my)/(np.linalg.norm(mx)*np.linalg.norm(my)))
            cc=signal.correlate(my,mx,mode='full',method='fft');center=len(mx)-1
            lag=int(np.argmax(cc[center-96:center+97])-96)
            assert corr>.95 and abs(lag)<=2,(kind,n,corr,lag)
        # Independently tie actual normalized output to the declared corrected
        # source identities and whole-source transition geometry. Gain may vary
        # through loudnorm; content and sample timing must still agree.
        ref=np.zeros((SR,2),float)
        for ek,e in enumerate(plan['entries']):
            left=max(start,e['mix_start_sample']);right=min(start+SR,e['mix_end_sample'])
            if right<=left:continue
            loc=np.arange(left-e['mix_start_sample'],right-e['mix_start_sample']);w=np.ones(len(loc))
            if ek:
                ln=plan['transitions'][ek-1]['overlap_samples'];w*=np.sin(np.clip(loc/(ln-1),0,1)*np.pi/2)
            if ek<39:
                ln=plan['transitions'][ek]['overlap_samples'];w*=np.cos(np.clip((loc-(e['samples']-ln))/(ln-1),0,1)*np.pi/2)
            ref[left-start:right-start]+=np.asarray(source_audio[e['order']][loc[0]:loc[-1]+1])*w[:,None]*10**(e['source_gain_db']/20)
        rm=ref.mean(axis=1)
        if np.linalg.norm(rm)>1e-6:
            identity=float(np.dot(rm,mx)/(np.linalg.norm(rm)*np.linalg.norm(mx)))
            cross=signal.correlate(mx,rm,mode='full',method='fft');ctr=len(rm)-1
            identity_lag=int(np.argmax(cross[ctr-96:ctr+97])-96)
            assert identity>.98 and abs(identity_lag)<=2,('Declared-source identity/timing mismatch',kind,n,identity,identity_lag)
        else:identity=None;identity_lag=None
        checks.append({'declared_source_waveform_correlation':identity,'declared_source_lag_samples':identity_lag,
                       'kind':kind,'number':n,'start_sample':start,'frames':SR,'wav_aac_correlation':corr,
                       'best_lag_samples':lag,'reference_rms_dbfs':20*np.log10(max(energy,1e-30)),
                       'commands':[cmdw,cmda]})
    # Full decoded sample count; WAV must equal planned, AAC may contain one codec padding frame.
    counts={}
    for label,p in [('wav',wav),('m4a',aac)]:
        cmd=['ffprobe','-v','error','-select_streams','a:0','-show_frames','-show_entries','frame=nb_samples','-of','csv=p=0',str(p)]
        n=sum(int(l.split(',')[0]) for l in subprocess.check_output(cmd,text=True).splitlines() if l.strip());counts[label]=n
    assert counts['wav']==plan['samples'];assert 0<=counts['m4a']-plan['samples']<1024
    originals=[]
    for t,a,c,ap in R.records():
        actual=sha(ROOT/a['source']['raw_path']);assert actual==t['raw_sha256']
        originals.append({'song_id':t['song_id'],'sha256':actual,'unchanged':True})
    result={'schema':'wavvy.capture_170_repeat2_technical_validation.v1','passed':True,
            'probes':probes,'final_loudness':loud,'decoded_samples':counts,
            'planned_samples':plan['samples'],'aac_tail_padding_samples':counts['m4a']-plan['samples'],
            'content_timing_checks':checks,'source_hash_checks':originals,'direct_listening':False,
            'aac_metadata_only_remux':{'path':relative(PROD/'aac-pts-repair.json'),'sha256':sha(PROD/'aac-pts-repair.json')},
            'decoder_preroll_audit':{'path':relative(PROD/'transition16-decoder-preroll-audit.json'),
                                    'sha256':sha(PROD/'transition16-decoder-preroll-audit.json')},
            'listener_approved':False,'scope':'audio only; no video/source-final/archive gate claim'}
    save(PROD/'final-technical-validation.json',result)
    manifest={'schema':'wavvy.capture_170_whole_source_repeat2.v1','series':'19-30',
        'status':'rendered_technical_checks_pass_listening_pending','target_bpm':170,
        'repeat_count':2,'additional_repeats':0,'entry_count':40,'transition_count':39,
        'source_count':20,'sample_rate':SR,'musical_source_trimmed':False,
        'duration_seconds':plan['duration_seconds'],'samples':plan['samples'],
        'mix_plan_path':relative(PROD/'mix-plan.json'),'mix_plan_sha256':sha(PROD/'mix-plan.json'),
        'encode_record_path':relative(PROD/'encode-record.json'),'encode_record_sha256':sha(PROD/'encode-record.json'),
        'validation_path':relative(PROD/'final-technical-validation.json'),'validation_sha256':sha(PROD/'final-technical-validation.json'),
        'wav_path':enc['wav_path'],'wav_sha256':enc['wav_sha256'],'aac_path':enc['aac_path'],'aac_sha256':enc['aac_sha256'],
        'final_loudness':loud,'entries':plan['entries'],'transitions':plan['transitions'],
        'listener_approved':False,'originals_preserved':True,
        'independent_output_measurements':[{'order':k,'path':relative(PROD/'independent-beats'/f'{k:02d}.json'),
          'sha256':sha(PROD/'independent-beats'/f'{k:02d}.json'),
          'alias_diagnosis_path':relative(PROD/'model-alias-diagnosis'/f'{k:02d}.json'),
          'alias_diagnosis_sha256':sha(PROD/'model-alias-diagnosis'/f'{k:02d}.json')} for k in range(1,21)],
        'tracklist_path':relative(PROD/'tracklist.md'),'tracklist_sha256':sha(PROD/'tracklist.md'),
        'producer_code':[{'path':relative(PROD/name),'sha256':sha(PROD/name)} for name in
            ['render-170.py','render-rubberband-170.py','assemble-170.py','fix-aac-packet-timestamps.py',
             'measure-rubberband-beats.py','diagnose-model-beats.py']],
        'aac_metadata_only_remux':{'path':relative(PROD/'aac-pts-repair.json'),'sha256':sha(PROD/'aac-pts-repair.json')},
        'limitations':['Inferred quarter-path phase and sparse-section speed interpolation are not verified audible beats at every instant.',
            'Exact bar downbeats are unconfirmed. Late drum entrances and original quiet tails remain.',
            'Dancing Tears half/full metrical ambiguity remains explicitly documented in the source time map.',
            'Technical measurements do not constitute direct listening approval. No video or source-final state promotion.',
            'Raw valid song boundaries inherit UI/PTS estimates with uncalibrated audio output latency.']}
    save(PROD/'manifest.json',manifest)
    print(json.dumps({'stage':'verified','seconds':plan['duration_seconds'],'counts':counts,'loudness':loud,
                      'content_checks':len(checks)},ensure_ascii=False),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['analyze','encode','verify']);a=p.parse_args()
    {'analyze':assembly_analysis,'encode':encode,'verify':verify}[a.stage]()
