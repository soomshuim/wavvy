#!/usr/bin/env python3
"""Uniform pitch-preserving 17/16 stretch of the approved integrated 170 WAV."""
import argparse, hashlib, importlib.util, json, subprocess, sys, time
from pathlib import Path
import numpy as np
from scipy import signal
from scipy.io import wavfile

P=Path(__file__).resolve().parent;ROOT=P.parents[3];W=ROOT/'work/mix-160-20261026'
O=ROOT/'SERIES/19-30/output/mix-160-20261026';OLD=P.parent/'mix-170-20261026';SR=48000
def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
A=module('assembly170',OLD/'assemble-170.py');B=module('rubber170',OLD/'render-rubberband-170.py')
sha=A.sha;save=A.save;relative=A.relative
SOURCE=ROOT/'SERIES/19-30/output/mix-170-20261026/continuous-mix-1930-repeat2.wav'
SOURCE_SHA='aff7601654e6a1212050dd082df85ac8aa3d2a9d15fa6e375bac0f5cd0671aec'
INPUT_N=299829124;OUTPUT_N=(INPUT_N*17+8)//16
RB='/opt/homebrew/bin/rubberband'

def scaled(n):return (int(n)*17+8)//16
def probe(p):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)],text=True))
def frames(p):return int(probe(p)['streams'][0]['duration_ts'])
def excerpt(path,start,length,dest):
    x,cmd=A.decode_window(path,int(start),int(length));dest.parent.mkdir(parents=True,exist_ok=True)
    wavfile.write(dest,SR,x);return x,cmd
def transform(src,out,expected,log):
    assert not out.exists();out.parent.mkdir(parents=True,exist_ok=True)
    cmd=[RB,'-3','-p','0','-t','1.0625',str(src),str(out)]
    before=time.monotonic()
    with log.open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
    assert r.returncode==0,log
    assert 'NaN or Inf' not in log.read_text();assert frames(out)==expected,(frames(out),expected)
    return {'command':cmd,'rubberband_version':subprocess.check_output([RB,'--version'],stderr=subprocess.STDOUT,text=True).strip(),
            'binary_sha256':sha(RB),'output_path':relative(out),'output_sha256':sha(out),'output_frames':expected,
            'log_path':relative(log),'log_sha256':sha(log),'elapsed_seconds':time.monotonic()-before}

def attack_check(src,out,input_n,output_n):
    es=B.R.MEASURE.envelopes(src);eo=B.R.MEASURE.envelopes(out)
    # Separately extracted mid/high attacks, evaluated on the uniform map.
    tout=np.arange(.5,output_n/SR-.5,.002);tin=tout*16/17;rows={}
    for band in ['mid','high']:
        ref=np.interp(tin*500,np.arange(len(es[band])),es[band]);scores=[]
        for lag in range(-30,31):
            obs=np.interp((tout+lag/500)*500,np.arange(len(eo[band])),eo[band])
            scores.append(0. if min(np.std(ref),np.std(obs))<1e-12 else float(np.corrcoef(ref,obs)[0,1]))
        k=int(np.argmax(scores));rows[band]={'lag_ms':(k-30)*2,'correlation':scores[k]}
    reliable=[r for r in rows.values() if r['correlation']>.4]
    return {'bands':rows,'reliable_band_count':len(reliable),'status':'measured' if reliable else 'sparse_or_ambiguous',
            'passed':all(abs(r['lag_ms'])<=30 for r in reliable),
            'caveat':'An empty reliable set is explicitly unmeasurable, not evidence of an audible beat.'}

def pulse(path):
    env=B.R.MEASURE.envelopes(path);rows=B.R.MEASURE.local_tempos(env)
    vals=[np.median([r['band_bpm']['mid'],r['band_bpm']['high']]) for r in rows]
    return {'windows':rows,'mid_high_bpm_median':float(np.median(vals)),
            'method':'Independent output multiband attack autocorrelation, 145–220 BPM neighborhood; not a universal meter detector.'}

def pitch(src,out,input_n):
    # The reused spectral checker samples between its interior map points.
    mx=np.array([0,2*SR,input_n-2*SR,input_n]);my=np.array([scaled(n) for n in mx])
    return B.pitch_check(src,out,mx,my)

def pilot():
    W.mkdir(parents=True,exist_ok=True);O.mkdir(parents=True,exist_ok=True)
    assert sha(SOURCE)==SOURCE_SHA and frames(SOURCE)==INPUT_N
    src=W/'pilot-input.wav';out=W/'pilot-output.wav';x,cmd=excerpt(SOURCE,60*SR,30*SR,src)
    n=scaled(len(x))
    if out.exists():
        # Resume the already completed pilot after the recorded checker-call
        # exception. No second stretch and no waveform replacement.
        assert frames(out)==n and 'NaN or Inf' not in (W/'pilot-rubberband.log').read_text()
        produced={'command':[RB,'-3','-p','0','-t','1.0625',str(src),str(out)],
           'output_path':relative(out),'output_sha256':sha(out),'output_frames':n,
           'log_path':relative(W/'pilot-rubberband.log'),'log_sha256':sha(W/'pilot-rubberband.log'),
           'reused_completed_pilot_after_checker_call_exception':True,'elapsed_seconds':None}
    else:produced=transform(src,out,n,W/'pilot-rubberband.log')
    qa=attack_check(src,out,len(x),n);tempo=pulse(out)
    pitched=pitch(src,out,len(x))
    result={'source_range_seconds':[60,90],'source_sha256':SOURCE_SHA,'extract_command':cmd,'producer':produced,
            'attack':qa,'pulse':tempo,'pitch':pitched,'passed':qa['passed'] and qa['reliable_band_count']>0 and abs(tempo['mid_high_bpm_median']-160)<2 and pitched['passed'],
            'direct_listening':False}
    save(P/'pilot.json',result);print(json.dumps({'stage':'pilot','passed':result['passed'],'bpm':tempo['mid_high_bpm_median'],
       'pitch_cents':pitched['median_shift_cents'],'attack':qa,'elapsed_seconds':produced['elapsed_seconds']}),flush=True)
    assert result['passed'],result

def render():
    assert json.loads((P/'pilot.json').read_text())['passed'];assert sha(SOURCE)==SOURCE_SHA
    out=W/'uniform-160.wav';j=transform(SOURCE,out,OUTPUT_N,W/'full-rubberband.log')
    assert sha(SOURCE)==SOURCE_SHA
    j.update({'schema':'wavvy.integrated_170_to_160_transform.v1','input_path':relative(SOURCE),'input_sha256':SOURCE_SHA,
              'input_frames':INPUT_N,'ratio_numerator':17,'ratio_denominator':16,'rounding_error_frames':OUTPUT_N-INPUT_N*17/16,
              'pitch_semitones':0,'original_170_unchanged':True,'whole_input_preserved':True,
              'first_and_last_output_sample':{'first':A.decode_window(out,0,1)[0][0].tolist(),
                 'last':A.decode_window(out,OUTPUT_N-1,1)[0][0].tolist()}})
    save(P/'transform-record.json',j);timeline()
    print(json.dumps({'stage':'full_transform','samples':OUTPUT_N,'seconds':OUTPUT_N/SR,'elapsed_seconds':j['elapsed_seconds']}),flush=True)

def stamp(n):
    ms=round(n*1000/SR);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02d}:{m:02d}:{s:02d}.{ms:03d}'

def timeline():
    old=json.loads((OLD/'mix-plan.json').read_text());entries=[];transitions=[]
    for e in old['entries']:
        q=dict(e)
        q['upstream_170_mix_frames']=[e['mix_start_sample'],e['mix_end_sample']]
        q['mix_start_sample']=scaled(e['mix_start_sample']);q['mix_end_sample']=scaled(e['mix_end_sample'])
        q['mix_start_seconds']=q['mix_start_sample']/SR;q['mix_end_seconds']=q['mix_end_sample']/SR
        q['samples']=q['mix_end_sample']-q['mix_start_sample'];q['first_grid_beat_sample_global']=scaled(e['first_grid_beat_sample_global'])
        q['upstream_170_entry']=e;entries.append(q)
    for t in old['transitions']:
        q={'number':t['number'],'outgoing_entry':t['outgoing_entry'],'incoming_entry':t['incoming_entry'],
           'repeat_boundary_20_to_1':t['repeat_boundary_20_to_1'],'upstream_170_frames':[t['start_sample'],t['end_sample']],
           'start_sample':scaled(t['start_sample']),'end_sample':scaled(t['end_sample']),
           'bar_phase_confidence':'unchanged unconfirmed quarter-path estimate, uniformly stretched'}
        q['overlap_samples']=q['end_sample']-q['start_sample'];q['overlap_seconds']=q['overlap_samples']/SR;transitions.append(q)
    assert len(entries)==40 and len(transitions)==39 and entries[-1]['mix_end_sample']==OUTPUT_N
    j={'schema':'wavvy.integrated_160_timeline.v1','source_170_plan_path':relative(OLD/'mix-plan.json'),
       'source_170_plan_sha256':sha(OLD/'mix-plan.json'),'ratio':[17,16],'samples':OUTPUT_N,'entries':entries,'transitions':transitions}
    save(P/'timeline.json',j)
    text='# 19:30 · 160 BPM · 전체20곡 순서2회\n\n전체 길이: '+stamp(OUTPUT_N)+' · 40진입/39연결\n\n170 통합 음원을17/16배 늘렸어요. 시각은 기존 겹침 진입점의 변환 위치이며 확정된 첫마디가 아니에요.\n\n| 진입 | 회차 | 순서 | 시작 | 제목 | 표본 위치 |\n|---:|---:|---:|---|---|---:|\n'
    for e in entries:text+=f"| {e['entry']} | {e['cycle']} | {e['order']} | {stamp(e['mix_start_sample'])} | {e['title']} | {e['mix_start_sample']} |\n"
    (P/'tracklist.md').write_text(text);(O/'tracklist.md').write_text(text)

def encode():
    tr=json.loads((P/'transform-record.json').read_text());src=ROOT/tr['output_path'];assert sha(src)==tr['output_sha256']
    loudpath=P/'transformed-loudness.json'
    if loudpath.exists():
        loud=json.loads(loudpath.read_text())
        # The preceding completed measurement is reusable only for this
        # immutable, hash-verified intermediate and its recorded input command.
        assert loud['command'][loud['command'].index('-i')+1]==str(src)
        assert loud.get('source_sha256',tr['output_sha256'])==tr['output_sha256']
    else:loud=A.measure(src)
    loud['source_sha256']=tr['output_sha256'];save(loudpath,loud)
    # A constant gain suffices when both the mean target and AAC headroom fit.
    gain=min(-14-loud['integrated_lufs'],-1.5-loud['true_peak_dbtp'])
    norm_count=0
    if abs(loud['integrated_lufs']+gain+14)<=.2:
        if abs(gain)<.005:gain=0.
        af=(f'volume={gain:.8f}dB,' if gain else '')
    else:
        # Root-authorized fallback: one final loudnorm application, using this
        # measured integrated source. No threshold relaxation or extra stretch.
        d=loud['raw'];gain=None;norm_count=1
        af=(f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={d['input_i']}:measured_LRA={d['input_lra']}:"
            f"measured_TP={d['input_tp']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}:"
            "linear=true:print_format=json,aresample=48000,")
    af+='aformat=sample_fmts=flt:sample_rates=48000,asetpts=N/SR/TB'
    wav=O/'continuous-mix-1930-160-repeat2.wav';aac=O/'continuous-mix-1930-160-repeat2.m4a';assert not wav.exists() and not aac.exists()
    cmd=['ffmpeg','-hide_banner','-nostdin','-n','-i',str(src),'-filter_complex',f'[0:a]{af},asplit=2[w][a]',
         '-map','[w]','-c:a','pcm_s24le',str(wav),'-map','[a]','-c:a','aac','-b:a','320k','-movflags','+faststart',str(aac)]
    before=time.monotonic()
    with (W/'final-encode.log').open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
    assert r.returncode==0
    save(P/'encode-record.json',{'schema':'wavvy.integrated_160_encode.v1','input_path':relative(src),'input_sha256':tr['output_sha256'],
       'command':cmd,'constant_gain_db':gain,'additional_loudnorm_applications':norm_count,'same_final_pcm_split':True,'aac_encode_generations':1,
       'pre_encode_measurement_path':relative(loudpath),'pre_encode_measurement_sha256':sha(loudpath),
       'wav_path':relative(wav),'wav_sha256':sha(wav),'aac_path':relative(aac),'aac_sha256':sha(aac),'elapsed_seconds':time.monotonic()-before})
    print(json.dumps({'stage':'encoded','gain_db':gain,'elapsed_seconds':time.monotonic()-before}),flush=True)

def numerical():
    tr=json.loads((P/'transform-record.json').read_text());out=ROOT/tr['output_path'];tl=json.loads((P/'timeline.json').read_text())
    body_entries=[1,4,11,16,20];locations=[]
    for t in tl['transitions']:locations.append(('transition',t['number'],sum(t['upstream_170_frames'])//2,6))
    old=json.loads((OLD/'mix-plan.json').read_text())
    for n in body_entries:
        e=old['entries'][n-1];locations.append(('body',n,(e['mix_start_sample']+e['mix_end_sample'])//2,20))
    rows=[]
    for kind,n,center,seconds in locations:
        a=center-seconds*SR//2;b=a+seconds*SR;ta=scaled(a);tb=scaled(b);folder=W/'checks'/f'{kind}-{n:02d}'
        src=folder/'170.wav';dst=folder/'160.wav';_,cs=excerpt(SOURCE,a,b-a,src);_,co=excerpt(out,ta,tb-ta,dst)
        align=attack_check(src,dst,b-a,tb-ta);row={'kind':kind,'number':n,'source_170_frames':[a,b],'output_160_frames':[ta,tb],
             'attack_alignment':align,'commands':[cs,co]}
        if kind=='body':
            row['pulse']=pulse(dst);row['pitch']=pitch(src,dst,b-a)
        rows.append(row)
    reliable=[b for r in rows for b in r['attack_alignment']['bands'].values() if b['correlation']>.4]
    bpms=[r['pulse']['mid_high_bpm_median'] for r in rows if r['kind']=='body']
    passed=all(r['attack_alignment']['passed'] for r in rows) and abs(np.median(bpms)-160)<2 and all(r['pitch']['passed'] for r in rows if r['kind']=='body')
    result={'schema':'wavvy.integrated_160_numerical_checks.v1','passed':bool(passed),'checks':rows,'body_pulse_bpm_values':bpms,
       'attack_abs_lag_p90_ms':float(np.quantile([abs(b['lag_ms']) for b in reliable],.9)),
       'unmeasurable_attack_windows':[{'kind':r['kind'],'number':r['number']} for r in rows if not r['attack_alignment']['reliable_band_count']],
       'direct_listening':False,'limitation':'Inherited full/half and downbeat uncertainty. Sparse attacks can be unmeasurable; no every-instant beat guarantee.'}
    save(P/'numerical-checks.json',result);assert passed,result
    print(json.dumps({'stage':'numerical','passed':passed,'pulse_bpm':bpms,'lag_p90_ms':result['attack_abs_lag_p90_ms']}),flush=True)

def verify():
    enc=json.loads((P/'encode-record.json').read_text());tl=json.loads((P/'timeline.json').read_text());tr=json.loads((P/'transform-record.json').read_text())
    wav=ROOT/enc['wav_path'];aac=ROOT/enc['aac_path'];assert sha(wav)==enc['wav_sha256'] and sha(aac)==enc['aac_sha256']
    assert sha(SOURCE)==SOURCE_SHA and sha(ROOT/tr['output_path'])==tr['output_sha256']
    replay=None;replay_windows={}
    if enc['additional_loudnorm_applications']:
        replay=json.loads((P/'loudnorm-replay-qa.json').read_text())
        assert replay['passed'] and replay['full_stream_frames']==OUTPUT_N
        assert replay['encode_record_sha256']==sha(P/'encode-record.json')
        assert replay['final_wav_sha256']==enc['wav_sha256'] and replay['final_aac_sha256']==enc['aac_sha256']
        assert replay['source_intermediate_sha256']==tr['output_sha256']
        assert replay['maximum_absolute_pcm_difference']<=replay['permitted_pcm_difference']
        replay_windows={(r['kind'],r['number'],r['start_sample']):r for r in replay['windows']}
    probes={label:probe(f) for label,f in [('wav',wav),('m4a',aac)]};assert frames(wav)==OUTPUT_N
    for label,q in probes.items():
        s=q['streams'][0];assert s['sample_rate']=='48000' and s['channels']==2
        assert (s['codec_name']=='pcm_s24le' and s['bits_per_sample']==24) if label=='wav' else (s['codec_name']=='aac' and s['profile']=='LC')
    packet_cmd=['ffprobe','-v','error','-select_streams','a:0','-show_packets','-show_entries','packet=pts,dts,duration,side_data_list','-of','json',str(aac)]
    packets=json.loads(subprocess.check_output(packet_cmd,text=True))['packets']
    gaps=[{'index':i,'gap_samples':int(b['pts'])-int(a['pts'])-int(a['duration'])} for i,(a,b) in enumerate(zip(packets,packets[1:]),1) if int(b['pts'])!=int(a['pts'])+int(a['duration'])]
    pkt={'command':packet_cmd,'packet_count':len(packets),'first_packet':packets[0],'last_packet':packets[-1],'gaps':gaps,
         'stream_end_sample':int(packets[-1]['pts'])+int(packets[-1]['duration'])}
    save(P/'aac-packet-validation.json',pkt);assert not gaps and pkt['stream_end_sample']==OUTPUT_N,pkt
    loudpath=P/'final-loudness.json'
    cached=json.loads(loudpath.read_text()) if loudpath.exists() else {};loud={}
    for label,f in [('wav',wav),('m4a',aac)]:
        prior=cached.get(label)
        if prior and prior['command'][prior['command'].index('-i')+1]==str(f) and prior.get('source_sha256',sha(f))==sha(f):
            loud[label]=prior
        else:loud[label]=A.measure(f)
        loud[label]['source_sha256']=sha(f);save(loudpath,loud)
        assert abs(loud[label]['integrated_lufs']+14)<=.2 and loud[label]['true_peak_dbtp']<=-1,loud[label]
    checks=[];locs=[('transition',t['number'],(t['start_sample']+t['end_sample'])//2-SR//2) for t in tl['transitions']]
    locs += [('body',n,(tl['entries'][n-1]['mix_start_sample']+tl['entries'][n-1]['mix_end_sample'])//2-SR//2) for n in [1,4,11,16,20,21,40]]
    intermediate=ROOT/tr['output_path']
    for kind,n,start in locs:
        x,cx=A.decode_window(wav,start);y,cy=A.decode_window(aac,start);z,cz=A.decode_window(intermediate,start)
        def compare(left,right):
            m=left.astype(float).mean(axis=1);n=right.astype(float).mean(axis=1)
            if np.linalg.norm(m)<1e-6:return {'correlation':None,'lag_samples':None,'maximum_absolute_difference':float(np.max(abs(left-right)))}
            corr=float(np.dot(m,n)/(np.linalg.norm(m)*np.linalg.norm(n)));cc=signal.correlate(n,m,mode='full',method='fft');c=len(m)-1
            return {'correlation':corr,'lag_samples':int(np.argmax(cc[c-96:c+97])-96)}
        ca=compare(x,y);cs=compare(z,x)
        if ca['correlation'] is None:assert ca['maximum_absolute_difference']<1e-4
        else:assert ca['correlation']>.95 and abs(ca['lag_samples'])<=2,(kind,n,'aac',ca)
        if replay is not None:
            # Content identity is proven by exact normalization replay, not a
            # lowered similarity threshold on dynamically changed gain.
            proof=replay_windows[(kind,n,start)]
            assert proof['replay_to_final_maximum_absolute_difference']<=replay['permitted_pcm_difference']
            assert proof['replay_to_final_lag_samples'] in [None,0]
            assert proof['replay_to_final_mono_correlation'] is None or proof['replay_to_final_mono_correlation']>.999999
            identity_method='Exact encoded loudnorm filter replay; full PCM quantization residual and zero lag'
        else:
            if cs['correlation'] is None:assert cs['maximum_absolute_difference']<1e-4
            else:assert cs['correlation']>.999 and abs(cs['lag_samples'])<=2,(kind,n,'constant-gain source',cs)
            identity_method='Constant-gain waveform identity'
        checks.append({'kind':kind,'number':n,'start_sample':start,'wav_aac':ca,'transformed_pcm_wav':cs,
                       'source_identity_method':identity_method,'commands':[cx,cy,cz]})
    countcmd=['ffprobe','-v','error','-select_streams','a:0','-show_frames','-show_entries','frame=nb_samples','-of','csv=p=0',str(aac)]
    count=sum(int(x.split(',')[0]) for x in subprocess.check_output(countcmd,text=True).splitlines() if x.strip())
    assert 0<=count-OUTPUT_N<1024
    numeric=json.loads((P/'numerical-checks.json').read_text());assert numeric['passed']
    assert [(e['cycle'],e['order']) for e in tl['entries']]==[(c,o) for c in [1,2] for o in range(1,21)]
    assert len({e['song_id'] for e in tl['entries']})==20 and tl['entries'][0]['title']=='Goodbye'
    val={'schema':'wavvy.integrated_160_technical_validation.v1','passed':True,'source_170_unchanged':True,
         'source_170_sha256':sha(SOURCE),'expected_samples':OUTPUT_N,'actual_wav_samples':frames(wav),'actual_aac_decoded_samples':count,
         'aac_padding_samples':count-OUTPUT_N,'probes':probes,'final_loudness':loud,'content_checks':checks,'exact_sequence_twice':True,
         'entry_count':40,'transition_count':39,'repeat_boundary_count':sum(t['repeat_boundary_20_to_1'] for t in tl['transitions']),
         'packet_validation_path':relative(P/'aac-packet-validation.json'),'numerical_checks_path':relative(P/'numerical-checks.json'),
         'exact_loudnorm_replay_path':relative(P/'loudnorm-replay-qa.json') if replay is not None else None,
         'exact_loudnorm_replay_sha256':sha(P/'loudnorm-replay-qa.json') if replay is not None else None,
         'direct_listening':False,'listener_approved':False}
    save(P/'final-technical-validation.json',val)
    man={'schema':'wavvy.integrated_170_to_160_delivery.v1','target_bpm':160,'ratio_numerator':17,'ratio_denominator':16,
         'samples':OUTPUT_N,'duration_seconds':OUTPUT_N/SR,'duration_hms':stamp(OUTPUT_N),'sample_rate':SR,'channels':2,
         'source_170_path':relative(SOURCE),'source_170_sha256':SOURCE_SHA,'source_170_preserved':True,
         'source_170_manifest_path':relative(OLD/'manifest.json'),'source_170_manifest_sha256':sha(OLD/'manifest.json'),
         'whole_integrated_master_stretched_once':True,'original_twenty_sources_rerendered':False,'pitch_semitones':0,
         'repeat_count':2,'additional_repeats':0,'entry_count':40,'transition_count':39,'entries':tl['entries'],'transitions':tl['transitions'],
         'wav_path':enc['wav_path'],'wav_sha256':enc['wav_sha256'],'aac_path':enc['aac_path'],'aac_sha256':enc['aac_sha256'],
         'aac_encode_generations':1,'additional_loudnorm_applications':enc['additional_loudnorm_applications'],'constant_gain_db':enc['constant_gain_db'],'final_loudness':loud,
         'evidence':[{'path':relative(P/name),'sha256':sha(P/name)} for name in ['render-plan.md','render-160.py','pilot.json','transform-record.json','encode-record.json','timeline.json','numerical-checks.json','pulse-family-audit.py','pulse-family-audit.json','loudnorm-replay-qa.py','loudnorm-replay-qa.json','aac-packet-validation.json','final-technical-validation.json','tracklist.md']],
         'direct_listening':False,'listener_approved':False,'scope':'audio-only; no video/source-final/archive claim',
         'limitations':['Uniform conversion inherits the upstream170 quarter-path and half/full metrical uncertainty.',
           'Sparse intros/tails are retained and do not guarantee an audible beat at every grid point.',
           'R3 changes waveform shape; numerical pitch/attack checks are not direct listening approval.']}
    save(P/'manifest.json',man);save(P/'final-premixed-audio.json',{'schema':'wavvy.integrated_160_audio_pointer.v1','manifest_path':relative(P/'manifest.json'),'manifest_sha256':sha(P/'manifest.json'),'target_bpm':160,'wav_path':enc['wav_path'],'wav_sha256':enc['wav_sha256'],'aac_path':enc['aac_path'],'aac_sha256':enc['aac_sha256'],'audio_only':True})
    print(json.dumps({'stage':'verified','samples':OUTPUT_N,'seconds':OUTPUT_N/SR,'aac_padding_samples':count-OUTPUT_N,'loudness':loud,'content_windows':len(checks)}),flush=True)

def replay():
    subprocess.check_call([sys.executable,str(P/'loudnorm-replay-qa.py')])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['pilot','render','encode','numerical','replay','verify','all']);a=p.parse_args()
    if a.stage=='all':
        for f in [pilot,render,encode,numerical,replay,verify]:f()
    else:globals()[a.stage]()
