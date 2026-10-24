#!/usr/bin/env python3
"""Reproduce the authorized 20-track mix with guarded static atempo blocks.

Reuses the controller's separately measured static-block actuator. No runtime
tempo commands. Bar anchors are independent-model candidates corroborated by
source attacks; neither this script nor its measurements certify listening.
"""
import json
from pathlib import Path
import subprocess
import numpy as np
from scipy import signal
from scipy.io import wavfile
import hashlib
import math
import re
import shutil
import argparse
import wave

R=Path(__file__).resolve().parents[1]
CONFIG=R/'SERIES/06-30/production/continuous-mix-20261024.json'
CFG=json.loads(CONFIG.read_text())
PRE={'tracks':CFG['sources']}
W=R/'work/0630-continuous-mix-20261024/production-render'
OUTPUT=R/'SERIES/06-30/output/continuous-mix-20261024'
SR=48000
N=16;CONTEXT=16;GUARD=.25;FADE=.005
APPROVAL=R/'.ai/validation/2026-10-24-0630-continuous-mix-listening-approval.json'
# The user's exception is byte-specific and never turns a technical fail into a
# pass. Only these measured timing failures may use that listening decision.
APPROVED={
    '09-10':('1620e27c344adac9f00615ee36ca127db6a8ccdad7878e43063b9faa665625df',
             ['out independent internal attack residual']),
    '10-11':('526f9dccd3eafebf78faa3bbe7713cc1191d5361125256f18baaf8e8143be90f',
             ['cross-source quarter phase residual']),
}
APPROVED_PAIR_SHA={
    '09-10':'251b316f117122dd252173215e7cf8c59980e0822e712b762d2998a02b279543',
    '10-11':'581d11854b66246b0ec44ccc9298641a31e93d10b25bc71833c4f6e674061a5a',
}

def object_sha(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()


def read(path):
    rate,a=wavfile.read(path,mmap=True)
    assert rate==SR and a.ndim==2 and a.shape[1]==2
    return a

class PCM24:
    """Bounded reads of packed 24-bit PCM; scipy cannot mmap 3-byte samples."""
    dtype=np.dtype(np.int32)
    def __init__(self,path,start=0,stop=None):
        self.path=Path(path)
        with wave.open(str(path),'rb') as f:
            assert (f.getframerate(),f.getnchannels(),f.getsampwidth())==(SR,2,3)
            frames=f.getnframes()
        self.start=start;self.stop=frames if stop is None else stop
        assert 0<=self.start<=self.stop<=frames
    def __len__(self):return self.stop-self.start
    def view(self,start,stop):return PCM24(self.path,self.start+start,self.start+stop)
    def __getitem__(self,key):
        assert isinstance(key,slice) and key.step in (None,1)
        lo,hi,_=key.indices(len(self))
        with wave.open(str(self.path),'rb') as f:
            f.setpos(self.start+lo);raw=f.readframes(hi-lo)
        b=np.frombuffer(raw,dtype=np.uint8).reshape(-1,3).astype(np.uint32)
        # SciPy represents 24-bit PCM left-aligned in a signed int32 container.
        return ((b[:,0]<<8)|(b[:,1]<<16)|(b[:,2]<<24)).view(np.int32).reshape(-1,2)

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def db(x):return float(20*np.log10(max(float(x),1e-12)))

def envelope(audio,band):
    from scipy import ndimage
    mono=np.asarray(audio,float).mean(axis=1)
    x=signal.resample_poly(mono,1,3)
    limits={'low':(30,180),'mid':(180,1800),'high':(1800,7000)}[band]
    y=signal.sosfiltfilt(signal.butter(4,limits,btype='bandpass',fs=16000,output='sos'),x)
    e=np.sqrt(np.mean(y[:len(y)//32*32].reshape(-1,32)**2,axis=1))
    e=ndimage.gaussian_filter1d(e,1.5)
    attack=np.maximum(e-np.roll(e,3),0);attack[:3]=0
    return attack

def save(path,data):
    with path.open('x') as f:json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')

def run(args,log):
    r=subprocess.run(args,capture_output=True,text=True,cwd=R)
    log.write_text(r.stderr)
    assert r.returncode==0,r.stderr[-2000:]

def stats(values):
    x=np.asarray(values,float)
    return {'count':len(x),'median_ms':float(np.median(x)*1000),'p90_abs_ms':float(np.quantile(abs(x),.9)*1000),'max_abs_ms':float(np.max(abs(x))*1000)} if len(x) else {'count':0}

def observed(audio,band):
    env=envelope(audio,band);peaks,_=signal.find_peaks(env,distance=45,prominence=.11*np.percentile(env,99))
    return peaks/500,env

def actual_anchors(g):
    matches=g['source_eighth_matches']
    return np.array([matches[k]['observed_source_seconds'] if matches[k]['observed_source_seconds'] is not None else matches[k]['grid_source_seconds'] for k in range(0,N*2+1,8)])

def waveform_location(source,raw,sa,predicted,margin_seconds=.065):
    # Search around the expected source event, not a prominence-suppressed peak.
    # A 60ms original waveform around the actual attack observes WSOLA delay.
    ss=round((sa-.025)*SR);se=round((sa+.035)*SR)
    template=np.asarray(source[ss:se],float).mean(axis=1)
    guess=round((predicted-.025)*SR);margin=round(margin_seconds*SR)
    lo=max(0,guess-margin);hi=min(len(raw),guess+len(template)+margin)
    target=np.asarray(raw[lo:hi],float).mean(axis=1)
    cc=signal.correlate(target,template,mode='valid',method='fft')
    norms=np.sqrt(np.convolve(target*target,np.ones(len(template)),mode='valid'))*np.linalg.norm(template)
    normalized=cc/(norms+1e-30);k=int(np.argmax(normalized))
    matched=(lo+k+(round(sa*SR)-ss))/SR
    return matched,float(normalized[k])

def align_anchor(source,raw,sa,ca,ratio,band):
    predicted=(sa-ca/SR)/ratio
    events,_=observed(raw,band);event=events[np.argmin(abs(events-predicted))]
    matched,correlation=waveform_location(source,raw,sa,predicted)
    assert correlation>.9,('unreliable anchor waveform correlation',correlation)
    return matched,{'predicted_raw_anchor_s':predicted,'observed_raw_onset_s':float(event),
        'waveform_observed_raw_anchor_s':matched,'normalized_waveform_correlation':correlation,
        'waveform_minus_predicted_ms':(matched-predicted)*1000,'waveform_minus_envelope_peak_ms':(matched-event)*1000}

def stem(folder,g,target,prefix,total):
    side=g['side'];sourcepath=R/g['source_path'];source=read(sourcepath)
    anchors=actual_anchors(g);blocks=[];pieces=[]
    if side=='out':
        body_source_start=round((anchors[0]-prefix)*SR)
        assert body_source_start>=0
        pieces.append({'kind':'unchanged-body-pre','path':sourcepath,'offset':-body_source_start})
    for k in range(4):
        a,b=anchors[k:k+2];ta,tb=target[k:k+2]
        ca=max(0,round((a-GUARD)*SR));cb=min(len(source),round((b+GUARD)*SR))
        ratio=(b-a)/(tb-ta)
        rawpath=folder/f'{side}-bar-{k+1:02d}-raw.wav'
        cmd=['ffmpeg','-hide_banner','-nostdin','-v','error','-n','-i',str(sourcepath),'-af',
             f'atrim=start_sample={ca}:end_sample={cb},asetpts=PTS-STARTPTS,atempo={ratio:.16f},asetpts=N/SR/TB',
             '-c:a','pcm_f32le',str(rawpath)]
        run(cmd,folder/f'{side}-bar-{k+1:02d}.log')
        raw=read(rawpath)
        observed_anchor,alignment=align_anchor(source,raw,float(a),ca,float(ratio),g['measurement_band'])
        offset=round(ta*SR)-round(observed_anchor*SR)
        pieces.append({'kind':'static-atempo','path':rawpath,'offset':offset})
        blocks.append({'bar':k+1,'source_anchor_seconds':[float(a),float(b)],'target_anchor_seconds':[float(ta),float(tb)],
            'tempo_factor':float(ratio),'source_guard_seconds':GUARD,'offset_samples':offset,'alignment':alignment,
            'ffmpeg_command':cmd,'raw_sha256':sha(rawpath)})
    if side=='in':
        offset=round(target[-1]*SR)-round(anchors[-1]*SR)
        pieces.append({'kind':'unchanged-body-post','path':sourcepath,'offset':offset})
    # Cuts are a quarter beat before bar attacks, with 5ms protective overlaps.
    internal=target[1:-1]-.0625*np.diff(target)[:-1]
    if side=='out':cuts=np.r_[0,target[0]-.25*g['quarter_period_seconds'],internal,target[-1]+.15]
    else:cuts=np.r_[target[0]-.15,internal,target[-1]+.25*g['quarter_period_seconds'],total]
    assert len(cuts)==len(pieces)+1,(side,len(cuts),len(pieces))
    args=['ffmpeg','-hide_banner','-nostdin','-v','error','-n'];graph=[]
    for i,piece in enumerate(pieces):
        args+=['-i',str(piece['path'])]
        lo=round((cuts[i]-(FADE/2 if i else 0))*SR)
        hi=round((cuts[i+1]+(FADE/2 if i+1<len(pieces) else 0))*SR)
        trimlo=lo-piece['offset'];trimhi=hi-piece['offset']
        assert trimlo>=0,(side,i,trimlo)
        length=(hi-lo)/SR
        chain=f'[{i}:a]atrim=start_sample={trimlo}:end_sample={trimhi},asetpts=PTS-STARTPTS'
        if i:chain+=f',afade=t=in:st=0:d={FADE}:curve=tri'
        if i+1<len(pieces):chain+=f',afade=t=out:st={length-FADE:.12f}:d={FADE}:curve=tri'
        graph.append(chain+f',adelay={lo}S:all=1[a{i}]')
    count=round(total*SR)
    graph.append(''.join(f'[a{i}]' for i in range(len(pieces)))+f'amix=inputs={len(pieces)}:normalize=0:dropout_transition=0,apad=whole_len={count},atrim=end_sample={count},asetpts=N/SR/TB[out]')
    ffgraph=folder/f'{side}-static-blocks.ffgraph.txt';ffgraph.write_text(';\n'.join(graph)+'\n')
    output=folder/f'{side}-aligned-stem.wav'
    args+=['-filter_complex_script',str(ffgraph),'-map','[out]','-c:a','pcm_f32le',str(output)]
    run(args,folder/f'{side}-assemble.log')
    audio=read(output);events,_=observed(audio,g['measurement_band'])
    # Source attacks that do not exist are not demanded in the output.
    checked=[]
    for match in g['source_eighth_matches']:
        s=match['observed_source_seconds']
        if s is None:continue
        k=min(3,int(match['eighth_index']//8))
        a,b=anchors[k:k+2];ta,tb=target[k:k+2]
        expected=ta+(s-a)*(tb-ta)/(b-a)
        j=int(np.argmin(abs(events-expected)))
        measured,correlation=waveform_location(source,audio,float(s),float(expected),.04)
        error=float(measured-expected)
        checked.append({'eighth_index':match['eighth_index'],'role':match['role'],'source_actual_event_s':s,
                        'mapped_expected_s':float(expected),'output_actual_event_s':measured if abs(error)<.04 and correlation>.65 else None,
                        'actuator_error_ms':error*1000 if abs(error)<.04 and correlation>.65 else None,
                        'waveform_correlation':correlation,'nearest_prominent_envelope_peak_s':float(events[j]),
                        'prominent_envelope_peak_minus_waveform_ms':float((events[j]-measured)*1000)})
    matched=[x for x in checked if x['output_actual_event_s'] is not None]
    errors=[x['actuator_error_ms']/1000 for x in matched]
    if side=='out':
        boundary=round((cuts[1]-FADE)*SR)
        before=np.asarray(source[body_source_start:body_source_start+boundary])
        bodydiff=float(np.max(abs(audio[:boundary]-before)))
        body={'side':'pre','output_interval_samples':[0,boundary],'source_interval_samples':[body_source_start,body_source_start+boundary],'max_sample_difference':bodydiff,'tempo_factor':1.}
    else:
        boundary=round((cuts[-2]+FADE)*SR);offset=pieces[-1]['offset']
        after=np.asarray(source[boundary-offset:len(audio)-offset])
        bodydiff=float(np.max(abs(audio[boundary:]-after)))
        body={'side':'post','output_interval_samples':[boundary,len(audio)],'source_interval_samples':[boundary-offset,len(audio)-offset],'max_sample_difference':bodydiff,'tempo_factor':1.}
    factors=np.array([x['tempo_factor'] for x in blocks])
    validation={'order':g['order'],'side':side,'path':str(output.relative_to(R)),'sha256':sha(output),
      'source_actual_bar_anchors_seconds':anchors.tolist(),'target_bar_anchors_seconds':target.tolist(),
      'actual_body_sample_comparison':body,'source_observed_event_count':len(checked),'output_matched_event_count':len(matched),
      'source_events_without_output_match':[x for x in checked if x['output_actual_event_s'] is None],
      'actuator_source_to_output_error':stats(errors),'mapped_source_event_pairs':checked,
      'actual_duration_seconds':len(audio)/SR,'expected_duration_seconds':total,'duration_error_ms':(len(audio)/SR-total)*1000,
      'static_block_factors':factors.tolist(),'max_factor_step':float(max(abs(np.diff(factors)))),
      'pitch_method':'FFmpeg static atempo, original sample rate; unchanged body samples compared directly',
      'block_join_crossfade_seconds':FADE,'block_join_cuts_seconds':cuts.tolist(),'blocks':blocks,
      'peak_abs':float(np.max(abs(audio))),'clipped_samples':int(np.count_nonzero(abs(audio)>=1)),
      'finite':bool(np.isfinite(audio).all())}
    save(folder/f'{side}-stem-validation.json',validation)
    return audio,validation

def waveform_evidence(source,out,sa,expected):
    ss=round((sa-.025)*SR);se=round((sa+.035)*SR)
    template=np.asarray(source[ss:se],float).mean(axis=1)
    lo=max(0,round((expected-.065)*SR));hi=min(len(out),round((expected+.075)*SR))
    target=np.asarray(out[lo:hi],float).mean(axis=1)
    cc=signal.correlate(target,template,mode='valid',method='fft')
    den=np.sqrt(np.convolve(target*target,np.ones(len(template)),mode='valid'))*np.linalg.norm(template)
    nc=cc/(den+1e-30);k=int(np.argmax(nc))
    peaks,_=signal.find_peaks(nc,distance=round(.002*SR))
    rivals=[int(j) for j in peaks if abs(j-k)>=round(.002*SR)]
    second=max(rivals,key=lambda j:nc[j]) if rivals else None
    actual=(lo+k+round(sa*SR)-ss)/SR
    return {'expected_search_interval_seconds':[expected-.04,expected+.04],
        'observed_seconds':actual,'expected_seconds':expected,'error_ms':(actual-expected)*1000,
        'maximum_correlation':float(nc[k]),'second_correlation':float(nc[second]) if second is not None else None,
        'best_minus_second_correlation':float(nc[k]-nc[second]) if second is not None else None,
        'second_minus_best_lag_ms':float((second-k)/SR*1000) if second is not None else None}

def verify_stem(g,a,v):
    source=read(R/g['source_path']);matches=[]
    for event in v['mapped_source_event_pairs']:
        m=waveform_evidence(source,a,event['source_actual_event_s'],event['mapped_expected_s'])
        m.update({'source_eighth_index':event['eighth_index'],'source_event_seconds':event['source_actual_event_s'],
                  'role':event['role'],'construction_anchor':event['eighth_index']%8==0,
                  'prominent_envelope_peak_seconds':event['nearest_prominent_envelope_peak_s']})
        matches.append(m)
    internal=[m for m in matches if not m['construction_anchor']]
    byid={m['source_eighth_index']:m for m in matches};periods=[]
    for k in range(0,32,2):
        if k in byid and k+2 in byid:
            aa,bb=byid[k],byid[k+2]
            periods.append({'start_quarter_index':k/2,
                'observed_period_seconds':bb['observed_seconds']-aa['observed_seconds'],
                'expected_mapped_source_period_seconds':bb['expected_seconds']-aa['expected_seconds'],
                'actuator_period_error_ms':bb['error_ms']-aa['error_ms']})
    return {'order':g['order'],'side':g['side'],'matches':matches,'quarter_periods':periods,
      'source_supported_event_count':len(matches),'internal_attack_count':len(internal),
      'internal_attack_error':stats([m['error_ms']/1000 for m in internal]),
      'quarter_period_error':stats([m['actuator_period_error_ms']/1000 for m in periods]),
      'minimum_waveform_correlation':min(m['maximum_correlation'] for m in matches),
      'minimum_best_minus_second_correlation':min(m['best_minus_second_correlation'] for m in matches if m['best_minus_second_correlation'] is not None),
      'body_comparison':v['actual_body_sample_comparison']}

def source_hashes():
    rows=[{'order':x['order'],'expected':x['sha256'],'actual':sha(R/x['path'])} for x in CFG['sources']]
    assert all(x['expected']==x['actual'] for x in rows),'source hash mismatch'
    return rows

def geometry(pair):
    po=pair['outgoing']['quarter_period_seconds'];pi=pair['incoming']['quarter_period_seconds']
    prefix=CONTEXT*po;duration=N*(po+pi)/2;total=prefix+duration+CONTEXT*pi
    k=np.arange(0,N+1,4)
    target=prefix+po*k+(pi-po)*(k**3/N**2-.5*k**4/N**3)
    return prefix,duration,total,target

def timeline():
    handle=round(.25*SR);cursor=0;chunks=[];entries=[{'order':1,'mix_entry_sample':0,'mix_entry_seconds':0.}]
    for i,row in enumerate(CFG['sources']):
        start=0 if i==0 else round(actual_anchors(CFG['boundaries'][i-1]['incoming'])[-1]*SR)+handle
        stop=row['frames'] if i==19 else round(actual_anchors(CFG['boundaries'][i]['outgoing'])[0]*SR)-handle
        assert 0<=start<stop<=row['frames']
        chunks.append({'kind':'body','order':row['order'],'source_start_sample':start,'source_end_sample':stop,
            'samples':stop-start,'mix_start_sample':cursor,'mix_end_sample':cursor+stop-start,
            'gain_db':row['gain_db']})
        cursor+=stop-start
        if i<19:
            pair=CFG['boundaries'][i];prefix,duration,total,target=geometry(pair)
            lo=round(prefix*SR)-handle;hi=round((prefix+duration)*SR)+handle
            chunks.append({'kind':'transition','label':pair['label'],'preview_start_sample':lo,'preview_end_sample':hi,
                'samples':hi-lo,'mix_start_sample':cursor,'mix_end_sample':cursor+hi-lo,
                'overlap_mix_start_sample':cursor+handle,'overlap_mix_end_sample':cursor+hi-lo-handle})
            entries.append({'order':i+2,'mix_entry_sample':cursor+handle,'mix_entry_seconds':(cursor+handle)/SR,
                'meaning':'nominal start of incoming fade/beat grid; gain begins at zero, no audibility certification'})
            cursor+=hi-lo
    return {'expected_samples':cursor,'expected_seconds':cursor/SR,'chunks':chunks,'track_entries':entries,
        'first_source_starts_at_zero':True,'last_source_ends_at_full_length':True}

def prepare():
    assert not OUTPUT.exists(),'output directory already exists; refusing overwrite'
    assert not W.exists(),'scratch directory already exists; refusing overwrite'
    OUTPUT.mkdir(parents=True);W.mkdir(parents=True)
    (OUTPUT/'transitions').mkdir();(W/'chunks-final').mkdir()
    hashes=source_hashes();plan=timeline()
    save(W/'frozen-config-final.json',CFG);save(W/'timeline-plan-final.json',plan)
    save(W/'sources-before.json',hashes)
    print(json.dumps({'stage':'preflight','expected_seconds':plan['expected_seconds'],
        'free_bytes':shutil.disk_usage(R).free,'source20_unchanged':True}),flush=True)

def render_boundary(pair,folder=None,output=None):
    gates=CFG['gates']
    label=pair['label'];folder=folder or W/f'transition-{label}';folder.mkdir()
    outgoing,incoming=pair['outgoing'],pair['incoming']
    prefix,duration,total,target=geometry(pair)
    a,va=stem(folder,outgoing,target,prefix,total);b,vb=stem(folder,incoming,target,prefix,total)
    ai=verify_stem(outgoing,a,va);bi=verify_stem(incoming,b,vb)
    output=output or OUTPUT/'transitions'/f'{label}.wav'
    u=f'clip((t-{prefix:.12f})/{duration:.12f},0,1)'
    go=10**(outgoing['gain_db']/20);gi=10**(incoming['gain_db']/20)
    graph=(f"[0:a]volume='{go:.15f}*cos({u}*PI/2)^2':eval=frame[a];"
           f"[1:a]volume='{gi:.15f}*sin({u}*PI/2)^2':eval=frame[b];"
           f'[a][b]amix=inputs=2:normalize=0:dropout_transition=0,atrim=end_sample={round(total*SR)},asetpts=N/SR/TB[out]')
    graphfile=folder/'mix.ffgraph.txt';graphfile.write_text(graph+'\n')
    run(['ffmpeg','-hide_banner','-nostdin','-v','error','-n','-i',va['path'],'-i',vb['path'],
        '-filter_complex_script',str(graphfile),'-map','[out]','-c:a','pcm_f32le',str(output)],folder/'mix.log')
    mixed=read(output)
    am={m['source_eighth_index']:m for m in ai['matches']};bm={m['source_eighth_index']:m for m in bi['matches']}
    common=sorted(set(am)&set(bm));quarters=[k for k in common if k%2==0];bars=[k for k in common if k%8==0]
    diff=lambda ks:[am[k]['observed_seconds']-bm[k]['observed_seconds'] for k in ks]
    phase=stats(diff(quarters));barphase=stats(diff(bars))
    ov=mixed[round(prefix*SR):round((prefix+duration)*SR)]
    minrms=min(db(np.sqrt(np.mean(x.astype(float)**2))) for x in np.array_split(ov,max(1,round(duration*10))))
    failures=[]
    if len(quarters)<gates['minimum_shared_observed_quarter_attacks']:failures.append('too few source-supported shared quarter attacks')
    if phase['p90_abs_ms']>gates['quarter_phase_p90_ms_max'] or phase['max_abs_ms']>gates['quarter_phase_max_ms_max']:failures.append('cross-source quarter phase residual')
    for side,v in [('out',ai),('in',bi)]:
        if v['internal_attack_error']['p90_abs_ms']>gates['independent_internal_actuator_p90_ms_max'] or v['internal_attack_error']['max_abs_ms']>gates['independent_internal_actuator_max_ms_max']:failures.append(side+' independent internal attack residual')
        if v['minimum_waveform_correlation']<gates['minimum_waveform_correlation']:failures.append(side+' ambiguous waveform match')
        if v['body_comparison']['max_sample_difference']!=0:failures.append(side+' native body changed')
    if not np.isfinite(mixed).all() or np.max(abs(mixed))>=1:failures.append('nonfinite or clipped mix')
    if minrms<gates['minimum_overlap_100ms_rms_dbfs']:failures.append('weak/silent 100ms overlap window')
    if abs(len(mixed)-round(total*SR))>gates['max_duration_error_samples']:failures.append('duration mismatch')
    result={'label':label,'quarter_beats':16,'bar_intent':4,'shared_observed_eighth_count':len(common),
        'shared_observed_quarter_count':len(quarters),'shared_observed_bar_anchor_count':len(bars),
        'quarter_phase_difference':phase,'bar_candidate_phase_difference':barphase,
        'preview_path':str(output.relative_to(R)),'preview_sha256':sha(output),
        'expected_duration_seconds':total,'actual_duration_seconds':len(mixed)/SR,
        'duration_error_samples':len(mixed)-round(total*SR),'overlap_timeline_seconds':[prefix,prefix+duration],
        'peak_abs':float(np.max(abs(mixed))),'clipped_samples':int(np.count_nonzero(abs(mixed)>=1)),
        'minimum_overlap_100ms_rms_dbfs':minrms,'out':ai,'in':bi,
        'failures':failures,'technical_gate_pass':not failures,
        'musical_downbeat_status':'MODEL_PLUS_ACTUAL_ATTACK_CANDIDATES_NOT_CERTIFIED',
        'listening_status':'NOT_LISTENED','bass_processing':'no extra EQ; complementary fades, four-bar overlap'}
    save(folder/'validation.json',result)
    print(json.dumps({k:result[k] for k in ['label','technical_gate_pass','failures','quarter_phase_difference','bar_candidate_phase_difference','shared_observed_quarter_count','peak_abs']}),flush=True)
    return result

def render_transitions():
    prepare();results=[]
    for pair in CFG['boundaries']:
        results.append(render_boundary(pair))
    report={'all19_technical_gates_pass':all(r['technical_gate_pass'] for r in results),
        'configuration_sha256':sha(CONFIG),'results':results,'sources_after':source_hashes()}
    save(W/'transition-results.json',report)
    acceptance=validate_acceptance(results)
    save(W/'transition-acceptance-final.json',acceptance)
    report['acceptance']=acceptance
    save(W/'transition-results-final.json',report)

def validate_acceptance(results):
    """Fail closed for changed audio, cues, safety checks or unapproved failures."""
    assert len(results)==19 and [r['label'] for r in results]==[p['label'] for p in CFG['boundaries']]
    approval=json.loads(APPROVAL.read_text())
    assert sha(APPROVAL)==CFG['listening_approval']['sha256'],'listening decision record changed'
    assert approval['answer_quote']=='둘 다 이대로 사용'
    selected={x['boundary']:x for x in approval['approved_previews']}
    assert set(selected)==set(APPROVED)
    frozen={x['label']:x for x in CFG['frozen_previews']}
    gates=CFG['gates'];checks=[]
    for r,pair in zip(results,CFG['boundaries']):
        label=r['label'];f=frozen[label];path=R/r['preview_path']
        assert r['preview_path']==f['path'] and sha(path)==r['preview_sha256']==f['sha256'],('changed preview',label)
        assert object_sha(pair)==f['pair_sha256'],('changed source cue configuration',label)
        audio=read(path);_,_,expected,_=geometry(pair)
        assert len(audio)==round(expected*SR) and r['duration_error_samples']==0,('preview duration',label)
        assert np.isfinite(audio).all() and np.max(abs(audio))<1 and r['clipped_samples']==0,('preview clipping/nonfinite',label)
        assert r['minimum_overlap_100ms_rms_dbfs']>=gates['minimum_overlap_100ms_rms_dbfs'],('preview silence',label)
        failures=[]
        if r['shared_observed_quarter_count']<gates['minimum_shared_observed_quarter_attacks']:failures.append('too few source-supported shared quarter attacks')
        phase=r['quarter_phase_difference']
        if phase['p90_abs_ms']>gates['quarter_phase_p90_ms_max'] or phase['max_abs_ms']>gates['quarter_phase_max_ms_max']:failures.append('cross-source quarter phase residual')
        for side in ['out','in']:
            v=r[side];e=v['internal_attack_error']
            if e['p90_abs_ms']>gates['independent_internal_actuator_p90_ms_max'] or e['max_abs_ms']>gates['independent_internal_actuator_max_ms_max']:failures.append(side+' independent internal attack residual')
            assert v['minimum_waveform_correlation']>=gates['minimum_waveform_correlation'],('ambiguous waveform match',label,side)
            assert v['body_comparison']['max_sample_difference']==0,('native body changed',label,side)
        assert failures==r['failures'] and r['technical_gate_pass']==(not failures),('technical evidence disagrees',label)
        user_approved=False
        if failures:
            assert label in APPROVED,('unapproved technical failure',label,failures)
            exact,allowed=APPROVED[label]
            assert failures==allowed and sha(path)==exact and object_sha(pair)==APPROVED_PAIR_SHA[label],('outside exact user approval',label)
            record=selected[label]
            assert record['path']==r['preview_path'] and record['sha256']==exact and record['user_selected_acceptance'] is True
            user_approved=True
        checks.append({'label':label,'technical_gate_pass':r['technical_gate_pass'],
            'technical_failures':failures,'user_listening_approved':user_approved,
            'exact_preview_sha256':r['preview_sha256'],'accepted_for_master':not failures or user_approved})
    assert sum(c['technical_gate_pass'] for c in checks)==17
    assert sum(c['user_listening_approved'] for c in checks)==2
    return {'all19_technical_gates_pass':False,'technical_pass_count':17,'exact_user_approved_exception_count':2,
        'all19_accepted_for_master':True,'approval_path':str(APPROVAL.relative_to(R)),
        'approval_sha256':sha(APPROVAL),'checks':checks}

def meter(path,log):
    cmd=['ffmpeg','-hide_banner','-nostdin','-v','info','-xerror','-err_detect','explode','-i',str(path),'-af','ebur128=peak=true:framelog=verbose','-f','null','-']
    r=subprocess.run(cmd,capture_output=True,text=True);log.write_text(r.stderr)
    assert r.returncode==0,r.stderr[-1000:]
    tail=r.stderr[r.stderr.rfind('Summary:'):]
    return {'integrated_lufs':float(re.search(r'I:\s+(-?[0-9.]+) LUFS',tail)[1]),
        'true_peak_dbtp':float(re.search(r'Peak:\s+(-?[0-9.]+) dBFS',tail)[1]),
        'full_decode_exit_code':r.returncode,'command':cmd,'log_path':str(log.relative_to(R))}

def compare_original_crop(audio,chunk):
    """All samples against the direct source/gain or float preview crop."""
    if chunk['kind']=='body':
        row=CFG['sources'][chunk['order']-1];path=R/row['path']
        start=chunk['source_start_sample'];gain=10**(row['gain_db']/20)
    else:
        path=OUTPUT/'transitions'/f'{chunk["label"]}.wav'
        start=chunk['preview_start_sample'];gain=1.
    original=read(path);worst=0.
    for offset in range(0,len(audio),SR*10):
        count=min(SR*10,len(audio)-offset)
        actual=np.asarray(audio[offset:offset+count],float)/2147483648
        expected=np.asarray(original[start+offset:start+offset+count],float)*gain
        worst=max(worst,float(np.max(abs(actual-expected))))
    assert worst<2/8388608,('direct source/gain or preview mismatch',chunk,worst)
    return {'reference_path':str(path.relative_to(R)),'reference_sha256':sha(path),
        'reference_start_sample':start,'samples_compared':len(audio),'channels_compared':2,
        'gain_db':chunk.get('gain_db',0),'maximum_sample_error':worst,'quantization_bound':2/8388608,
        'all_samples_within_quantization_bound':True,'tempo_factor':1 if chunk['kind']=='body' else None}

def probe(path):
    cmd=['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]
    return json.loads(subprocess.check_output(cmd,text=True))

def render_master():
    report_path=W/'transition-results-final.json'
    if not report_path.exists():report_path=W/'transition-results.json'
    report=json.loads(report_path.read_text())
    acceptance=validate_acceptance(report['results'])
    assert report['configuration_sha256']==sha(CONFIG),'configuration changed after transition verification'
    source_hashes();plan=timeline();free=shutil.disk_usage(R).free
    assert free>4*1024**3,('insufficient scratch/master reserve',free)
    print(json.dumps({'stage':'before-master','expected_seconds':plan['expected_seconds'],
        'all19_technical_gates_pass':False,'technical_pass_count':17,
        'exact_user_approved_exception_count':2,'all19_accepted_for_master':True,'free_bytes':free}),flush=True)
    assert object_sha(json.loads((W/'frozen-config-final.json').read_text()))==object_sha(CFG)
    assert json.loads((W/'timeline-plan-final.json').read_text())==plan
    concat=[];appearance=plan['track_entries'];bodychecks=[];stagingchecks=[]
    chunkdir=W/'chunks-final';chunkdir.mkdir(exist_ok=True)
    for idx,chunk in enumerate(plan['chunks']):
        output=chunkdir/f'{idx:02d}-{chunk["kind"]}.wav'
        if chunk['kind']=='body':
            row=CFG['sources'][chunk['order']-1];source=R/row['path']
            filt=f'atrim=start_sample={chunk["source_start_sample"]}:end_sample={chunk["source_end_sample"]},asetpts=PTS-STARTPTS,volume={10**(row["gain_db"]/20):.15f}'
        else:
            source=OUTPUT/'transitions'/f'{chunk["label"]}.wav'
            filt=f'atrim=start_sample={chunk["preview_start_sample"]}:end_sample={chunk["preview_end_sample"]},asetpts=PTS-STARTPTS'
        cmd=['ffmpeg','-hide_banner','-nostdin','-v','error','-n','-i',str(source),'-af',filt,'-ar',str(SR),'-ac','2','-c:a','pcm_s24le',str(output)]
        run(cmd,chunkdir/f'{idx:02d}.log');a=PCM24(output)
        assert len(a)==chunk['samples'],(idx,'chunk length mismatch')
        check=compare_original_crop(a,chunk)
        stagingchecks.append({'kind':chunk['kind'],'label':chunk.get('label'),'order':chunk.get('order'),**check})
        if chunk['kind']=='body':bodychecks.append({'order':chunk['order'],**check})
        concat.append(output)
    concatfile=W/'master-concat.txt'
    concatfile.write_text(''.join("file '"+str(path).replace("'","'\\''")+"'\n" for path in concat))
    master=OUTPUT/'continuous-mix-0630.wav'
    run(['ffmpeg','-hide_banner','-nostdin','-v','error','-n','-f','concat','-safe','0','-i',str(concatfile),'-c:a','copy',str(master)],W/'master-concat.log')
    a=PCM24(master);assert a.dtype==np.int32 and len(a)==plan['expected_samples']
    final_crop_checks=[]
    for chunk,path in zip(plan['chunks'],concat):
        staged=PCM24(path)
        actual=a.view(chunk['mix_start_sample'],chunk['mix_end_sample'])
        # Every sample, all 39 chunks, proves the final concat uses the exact
        # verified transition crop and source/gain body crop, without drift.
        same=all(np.array_equal(actual[k:k+SR*10],staged[k:k+SR*10]) for k in range(0,len(actual),SR*10))
        assert same,('final master differs from staged crop',chunk)
        direct=compare_original_crop(actual,chunk)
        final_crop_checks.append({'kind':chunk['kind'],'label':chunk.get('label'),'order':chunk.get('order'),
            'mix_interval_samples':[chunk['mix_start_sample'],chunk['mix_end_sample']],
            'staging_chunk_path':str(path.relative_to(R)),'staging_sha256':sha(path),'all_samples_identical':same,
            'transition_preview_crop_samples':[chunk['preview_start_sample'],chunk['preview_end_sample']] if chunk['kind']=='transition' else None,
            'direct_original_gain_or_preview_comparison':direct})
    peak=0;clipped=0;joinchecks=[]
    for start in range(0,len(a),SR*60):
        x=np.asarray(a[start:start+SR*60]);peak=max(peak,int(np.max(abs(x.astype(np.int64)))));clipped+=int(np.count_nonzero((x==2147483392)|(x==-2147483648)))
    for left,right in zip(plan['chunks'][:-1],plan['chunks'][1:]):
        cut=left['mix_end_sample'];x=np.asarray(a[max(0,cut-2400):cut+2400],float)/2147483648
        jump=float(np.max(abs(x[2400]-x[2399])));rms=db(np.sqrt(np.mean(x*x)))
        assert rms>-40,('silent master body/transition join',cut/SR)
        joinchecks.append({'sample':cut,'seconds':cut/SR,'100ms_rms_dbfs':rms,'adjacent_sample_delta':jump})
    assert clipped==0
    # Full interior scan. Native quiet passages are reported as source content;
    # all39 direct crop comparisons rule out any newly inserted silent samples.
    quiet=[];minimum_interior=0.;digital_zero_windows=0
    for start in range(2*SR,len(a)-2*SR,SR//10):
        x=np.asarray(a[start:start+SR//10],float)/2147483648
        level=db(np.sqrt(np.mean(x*x)));minimum_interior=min(minimum_interior,level)
        if not np.any(x):digital_zero_windows+=1
        if level<-60:
            owner=next(c for c in plan['chunks'] if c['mix_start_sample']<=start<c['mix_end_sample'])
            quiet.append({'start_seconds':start/SR,'duration_seconds':len(x)/SR,'rms_dbfs':level,
                'kind':owner['kind'],'order':owner.get('order'),'label':owner.get('label'),
                'classification':'identical to source/gain' if owner['kind']=='body' else 'identical to verified preview'})
    silencecheck={'window_seconds':.1,'threshold_dbfs':-60,'excluded_natural_first_last_seconds':2,
        'minimum_interior_100ms_rms_dbfs':minimum_interior,'digital_zero_100ms_window_count':digital_zero_windows,
        'quiet_windows':quiet,'no_added_silence_proven_by_all39_direct_sample_comparisons':True}
    assert digital_zero_windows==0,'unexpected complete interior 100ms digital silence'
    wavmeter=meter(master,W/'master-loudness.log');assert wavmeter['true_peak_dbtp']<=CFG['gates']['max_final_true_peak_dbtp'],wavmeter
    listening=OUTPUT/'continuous-mix-0630.m4a'
    run(['ffmpeg','-hide_banner','-nostdin','-v','error','-n','-i',str(master),'-c:a','aac','-b:a','320k','-ar',str(SR),'-movflags','+faststart',str(listening)],W/'master-aac.log')
    aacmeter=meter(listening,W/'master-aac-loudness.log');assert aacmeter['true_peak_dbtp']<=CFG['gates']['max_final_true_peak_dbtp'],aacmeter
    montage=[];preview_artifacts=[]
    for row in report['results']:
        wav=R/row['preview_path'];m4a=wav.with_suffix('.m4a')
        run(['ffmpeg','-hide_banner','-nostdin','-v','error','-n','-i',str(wav),'-c:a','aac','-b:a','256k',str(m4a)],W/f'{row["label"]}-aac.log')
        run(['ffmpeg','-hide_banner','-nostdin','-v','error','-xerror','-err_detect','explode','-i',str(m4a),'-f','null','-'],W/f'{row["label"]}-aac-decode.log')
        preview_artifacts.append({'label':row['label'],'wav_path':str(wav.relative_to(R)),
            'wav_sha256':sha(wav),'wav_duration_seconds':row['actual_duration_seconds'],
            'm4a_path':str(m4a.relative_to(R)),'m4a_sha256':sha(m4a),
            'm4a_container_duration_seconds':float(probe(m4a)['format']['duration']),
            'm4a_full_decode_exit_code':0,'technical_gate_pass':row['technical_gate_pass'],
            'user_listening_approved':row['label'] in APPROVED})
        center=sum(row['overlap_timeline_seconds'])/2;piece=W/f'montage-{row["label"]}.wav'
        run(['ffmpeg','-hide_banner','-nostdin','-v','error','-n','-i',str(wav),'-af',f'atrim=start={center-1:.12f}:end={center+1:.12f},asetpts=PTS-STARTPTS,afade=t=in:d=0.05,afade=t=out:st=1.95:d=0.05','-c:a','pcm_s24le',str(piece)],W/f'{row["label"]}-montage.log')
        montage.append(piece)
    montagefile=W/'montage-concat.txt';montagefile.write_text(''.join("file '"+str(x)+"'\n" for x in montage))
    montageout=OUTPUT/'transition-montage.m4a'
    run(['ffmpeg','-hide_banner','-nostdin','-v','error','-n','-f','concat','-safe','0','-i',str(montagefile),'-c:a','aac','-b:a','256k',str(montageout)],W/'montage.log')
    run(['ffmpeg','-hide_banner','-nostdin','-v','error','-xerror','-err_detect','explode','-i',str(montageout),'-f','null','-'],W/'montage-decode.log')
    masterprobe=probe(master);aacprobe=probe(listening)
    assert masterprobe['streams'][0]['codec_name']=='pcm_s24le' and masterprobe['streams'][0]['bits_per_sample']==24
    aacduration=float(aacprobe['format']['duration'])
    assert abs(aacduration-len(a)/SR)<.1,'AAC container duration differs unexpectedly'
    title_by_order={x['order']:x['path'].split('__')[1] for x in CFG['sources']}
    for item in appearance:
        item['title']=title_by_order[item['order']]
        item['source_path']=CFG['sources'][item['order']-1]['path']
    def timestamp(seconds):
        milliseconds=round(seconds*1000);h,rem=divmod(milliseconds,3600000);m,rem=divmod(rem,60000);s,ms=divmod(rem,1000)
        return f'{h:02d}:{m:02d}:{s:02d}.{ms:03d}'
    tracklist=OUTPUT/'tracklist.txt'
    with tracklist.open('x') as f:
        f.write('06-30 continuous mix — current 20-track order, one appearance each\n')
        f.write('Times mark the incoming fade/beat-grid start; the gain starts at zero.\n\n')
        for item in appearance:f.write(f'{timestamp(item["mix_entry_seconds"])}  {item["order"]:02d}. {item["title"]}\n')
    final={'scope':'independent audio mix, no release-state/report replacement','configuration_path':str(CONFIG.relative_to(R)),
        'configuration_sha256':sha(CONFIG),'script_sha256':sha(Path(__file__)),'source20_sha256_unchanged':True,'source_hashes':source_hashes(),
        'master':{'path':str(master.relative_to(R)),'sha256':sha(master),'sample_rate_hz':SR,'channels':2,'pcm_bits':24,
            'expected_samples':plan['expected_samples'],'actual_samples':len(a),'expected_duration_seconds':plan['expected_seconds'],
            'actual_duration_seconds':len(a)/SR,'duration_error_samples':len(a)-plan['expected_samples'],
            'peak_abs':peak/2147483648,'clipped_samples':clipped,'loudness':wavmeter},
        'listening_copy':{'path':str(listening.relative_to(R)),'sha256':sha(listening),'loudness':aacmeter,
            'container_duration_seconds':aacduration,'container_minus_master_seconds':aacduration-len(a)/SR},
        'transition_montage':{'path':str(montageout.relative_to(R)),'sha256':sha(montageout),'duration_seconds':float(probe(montageout)['format']['duration'])},
        'track_entries':appearance,'tracklist_path':str(tracklist.relative_to(R)),'timeline':plan,
        'transition_previews':preview_artifacts,
        'body_gain_adjusted_sample_checks':bodychecks,'master_body_transition_join_checks':joinchecks,
        'staging_all39_direct_crop_comparisons':stagingchecks,'final_master_all39_crop_comparisons':final_crop_checks,
        'full_interior_silence_check':silencecheck,'master_ffprobe':masterprobe,'listening_ffprobe':aacprobe,
        'all19_transition_technical_gates_pass':False,'transition_acceptance':acceptance,
        'transition_results_path':str(report_path.relative_to(R)),'transition_results_sha256':sha(report_path),
        'frozen_config_path':str((W/'frozen-config-final.json').relative_to(R)),
        'frozen_config_sha256':sha(W/'frozen-config-final.json'),
        'timeline_path':str((W/'timeline-plan-final.json').relative_to(R)),'timeline_sha256':sha(W/'timeline-plan-final.json'),
        'listening_status':'EXACT_09-10_AND_10-11_USER_APPROVED; WHOLE_MASTER_NOT_LISTENED',
        'musical_downbeat_status':'AUTOMATIC_MODEL_PLUS_ACTUAL_ATTACK_CANDIDATES_NOT_CERTIFIED',
        'limitations':CFG['limitations'],'free_disk_bytes_after':shutil.disk_usage(R).free}
    save(OUTPUT/'manifest.json',final)
    save(R/'.ai/validation/2026-10-24-0630-continuous-mix-final-worker-check.json',final)
    print(json.dumps({'stage':'master-complete','master':final['master'],'track_entries':appearance,'free_disk_bytes':final['free_disk_bytes_after']},ensure_ascii=False),flush=True)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage',choices=['transitions','master'],required=True)
    args=parser.parse_args()
    if args.stage=='transitions':render_transitions()
    else:render_master()

if __name__=='__main__':main()

