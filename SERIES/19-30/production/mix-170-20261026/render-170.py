#!/usr/bin/env python3
"""170 BPM capture-only producer. Reuses 07:00 guarded atempo/anchor code.
No cue trims, source mutation, synthetic drums, archive promotion or listening claim.
"""
import argparse
import hashlib
import importlib.util
import json
import subprocess
import time
from pathlib import Path
import numpy as np
from scipy import ndimage, signal
from scipy.io import wavfile

ROOT = Path(__file__).resolve().parents[4]
PROD = Path(__file__).resolve().parent
WORK = ROOT/'work/mix-170-20261026'
SR = 48000
TARGET = 170
BLOCK = 16
GUARD = .4
SEAM = .012

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

OLD = module('guarded_0700', ROOT/'SERIES/07-00/production/render-180bpm.py')
MEASURE = module('envelopes_0700', ROOT/'SERIES/07-00/production/analyze-180bpm.py')
sha = OLD.sha
read = OLD.read

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')

def relative(path): return str(Path(path).resolve().relative_to(ROOT))
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    assert r.returncode == 0, {'command':cmd, 'stderr':r.stderr}
    return r

def quarter_sample(index):
    # 48k * 60/170 = 288000/17. Round cumulative position, never sum one beat.
    return (int(index)*288000+8)//17

def records():
    seq_path = ROOT/'SERIES/19-30/production/capture-analysis-20261026/sequence.json'
    seq = json.loads(seq_path.read_text())
    comp_path = ROOT/'work/2026-10-26-1930-current20-capture/analysis/comparison.json'
    comps = {t['song_id']: t for t in json.loads(comp_path.read_text())['tracks']}
    result=[]
    for t in seq['tracks']:
        a_path = (seq_path.parent/t['analysis_path']).resolve()
        a = json.loads(a_path.read_text())
        assert a['song_id']==t['song_id'] and a['title']==t['title']
        result.append((t, a, comps[t['song_id']], a_path))
    assert len(result)==20 and len({t[0]['song_id'] for t in result})==20
    return result

def source(order):
    t,a,c,ap=records()[order-1]
    raw=ROOT/a['source']['raw_path']; assert sha(raw)==t['raw_sha256']==a['source']['raw_sha256']
    out=WORK/'source'/f'{order:02d}.wav'
    out.parent.mkdir(parents=True, exist_ok=True)
    start,end=a['source']['valid_raw_frames']
    if not out.exists():
        x=read(raw); assert x.dtype==np.float32
        assert end-start==round(t['duration_seconds']*SR)
        wavfile.write(out,SR,np.asarray(x[start:end])); del x
    x=read(out)
    assert len(x)==end-start and x.dtype==np.float32
    return t,a,c,ap,out

def path_for(order):
    t,a,c,ap,p=source(order)
    dest=PROD/'source-time-maps'/f'{order:02d}.json'
    if dest.exists():
        j=json.loads(dest.read_text()); assert sha(p)==j['valid_source_sha256'];return j
    before=time.monotonic()
    # Existing independent 20-second mid/high estimates select source pulse family.
    # 170 itself is never used to choose half/double interpretation.
    trace=[]
    for w in c['native_pulse_trace']:
        vals=w['mid_high_bpm']
        if w['within_family_supported'] and vals:
            trace.append({'center_seconds':float(np.mean(w['range_seconds'])),
                          'median_bpm':float(np.median(vals))})
    assert len(trace)>=3, (order,'insufficient existing independent pulse evidence')
    envs=MEASURE.envelopes(p)
    beats,combined=MEASURE.quarter_path(envs,trace)
    indices=list(range(0,len(beats)-1,BLOCK))
    if indices[-1]!=len(beats)-1:indices.append(len(beats)-1)
    anchors=beats[indices]
    local=60*np.diff(indices)/np.diff(anchors)
    prior=np.interp((anchors[:-1]+anchors[1:])/2,
                    [w['center_seconds'] for w in trace],[w['median_bpm'] for w in trace])
    assert np.max(abs(local/prior-1))<.09, (order,'pulse path contradicts independent source family',local,prior)
    result={'schema':'wavvy.capture_170_source_time_map.v1','order':order,
            'song_id':t['song_id'],'title':t['title'],'raw_path':relative(ROOT/a['source']['raw_path']),
            'raw_sha256':t['raw_sha256'],'raw_valid_frames':a['source']['valid_raw_frames'],
            'raw_valid_seconds':a['source']['valid_raw_seconds'],
            'source_analysis_path':relative(ap),'source_analysis_sha256':sha(ap),
            'valid_source_path':relative(p),'valid_source_sha256':sha(p),
            'source_duration_seconds':len(read(p))/SR,
            'source_pulse_prior':trace,'quarter_beat_seconds':beats.tolist(),
            'block_anchor_indices':indices,'block_source_bpm':local.tolist(),
            'independent_prior_bpm':prior.tolist(),'preferred_pulse_reference_bpm':c['preferred_pulse_reference_bpm'],
            'half_pulse_alternative_bpm':c['half_pulse_bpm_alternative'],
            'intro_relative_energy_end_seconds':c['intro_relative_energy_end_candidate_seconds'],
            'tail_relative_energy_start_seconds':c['tail_relative_energy_start_candidate_seconds'],
            'source_pulse_confidence':c['pulse_confidence'],
            'method':'07:00 multiband attack dynamic path, guided by existing independent mid/high source tempo trace',
            'direct_listening':False,'original_modified':False,'musical_source_trimmed':False,
            'limitations':['Estimated quarter pulse; exact first bar and downbeat not listener confirmed.',
                'Sparse intro/tail pulse is inferred, not evidence of an audible drum on every grid point.',
                'Dancing Tears full/half metrical ambiguity persists; full pulse is supported by source mid/high repetitions, not by proximity to170.',
                'Warm Pixels late body uses multiband attacks independently of the incomplete Beat This path.'],
            'elapsed_seconds':time.monotonic()-before}
    save(dest,result)
    print(json.dumps({'stage':'time_map','order':order,'title':t['title'],'beats':len(beats),
                      'source_bpm_p10_p50_p90':np.quantile(local,[.1,.5,.9]).tolist(),
                      'elapsed_seconds':result['elapsed_seconds']},ensure_ascii=False),flush=True)
    return result

def block_audio(j,k,folder,cache):
    src=ROOT/j['valid_source_path']; x=read(src)
    ids=j['block_anchor_indices']; beats=j['quarter_beat_seconds']
    ia,ib=ids[k:k+2]; sa,sb=beats[ia],beats[ib]
    interval=(quarter_sample(ib)-quarter_sample(ia))/SR
    ratio=(sb-sa)/interval
    guard = .45 if (j['order'], k)==(20,20) else GUARD
    ca=0 if k==0 else max(0,round((sa-guard)*SR))
    cb=len(x) if k==len(ids)-2 else min(len(x),round((sb+GUARD)*SR))
    dest=folder/f'block-{k:03d}.wav'; assert not dest.exists(),dest
    cmd=['ffmpeg','-hide_banner','-v','error','-nostdin','-n','-i',str(src),
         '-af',f'atrim=start_sample={ca}:end_sample={cb},asetpts=PTS-STARTPTS,atempo={ratio:.16f},asetpts=N/SR/TB',
         '-c:a','pcm_f32le',str(dest)]
    run(cmd); y=read(dest)
    la,cca,ea=OLD.locate(x,y,sa,(sa-ca/SR)/ratio,cache)
    lb,ccb,eb=OLD.locate(x,y,sb,(sb-ca/SR)/ratio,cache)
    error=lb-la-interval
    assert abs(error)<.020, ('Block end error exceeds20ms',j['order'],k,error)
    record={'block':k,'source_beat_indices':[ia,ib],'source_anchors_seconds':[sa,sb],
            'tempo_factor':ratio,'guard_seconds':guard,'source_guard_frames':[ca,cb],
            'located_block_anchors_seconds':[la,lb],'waveform_correlations':[cca,ccb],
            'waveform_anchor_evidence':[ea,eb],'observed_end_error_ms':error*1000,
            'render_sha256':sha(dest),'ffmpeg_command':cmd}
    return y,record,dest

def pilot(order,near):
    begin=time.monotonic();j=path_for(order);x=read(ROOT/j['valid_source_path'])
    cache={'mono':x.astype(float).mean(axis=1)}
    anchors=np.array(j['quarter_beat_seconds'])[j['block_anchor_indices']]
    k=int(np.argmin(abs((anchors[:-1]+anchors[1:])/2-near)))
    folder=WORK/'pilots'/f'{order:02d}'/('guard-045' if order==20 else 'guard-040');folder.mkdir(parents=True,exist_ok=True)
    y,b,p=block_audio(j,k,folder,cache)
    assert np.isfinite(y).all() and float(np.max(abs(y)))<1.02
    out={'schema':'wavvy.capture_170_pilot.v1','order':order,'song_id':j['song_id'],'title':j['title'],
         'passed':True,'block':b,'audio_path':relative(p),'audio_sha256':sha(p),
         'elapsed_seconds':time.monotonic()-begin,'direct_listening':False}
    save(PROD/'pilots'/f'{order:02d}.json',out)
    print(json.dumps({'stage':'pilot','order':order,'passed':True,'elapsed_seconds':out['elapsed_seconds'],
                      'anchor_correlations':b['waveform_correlations'],'end_error_ms':b['observed_end_error_ms']},ensure_ascii=False),flush=True)

def render(order):
    before=time.monotonic();j=path_for(order); dest=WORK/'corrected'/f'{order:02d}.wav'
    record_path=PROD/'corrected'/f'{order:02d}.json'
    if record_path.exists():
        saved=json.loads(record_path.read_text());assert sha(dest)==saved['output_sha256'];return
    assert not dest.exists(),dest
    x=read(ROOT/j['valid_source_path']);cache={'mono':x.astype(float).mean(axis=1)}
    beats=np.array(j['quarter_beat_seconds']);ids=j['block_anchor_indices'];anchors=beats[ids]
    first_ratio=(anchors[1]-anchors[0])/((quarter_sample(ids[1])-quarter_sample(ids[0]))/SR)
    estimated=anchors[0]/first_ratio+quarter_sample(ids[-1])/SR+(len(x)/SR-anchors[-1])/first_ratio+10
    output=np.zeros((round(estimated*SR),2),np.float32); weight=np.zeros(len(output),np.float32)
    folder=WORK/'blocks'/f'{order:02d}';folder.mkdir(parents=True,exist_ok=True)
    blocks=[];actual_end=0;first_grid=None
    for k in range(len(ids)-1):
        y,b,p=block_audio(j,k,folder,cache)
        la,lb=b['located_block_anchors_seconds']
        if k==0:first_grid=round(la*SR) # offset0 preserves source0, including its intentional quiet intro.
        ta=first_grid+quarter_sample(ids[k]);tb=first_grid+quarter_sample(ids[k+1])
        offset=ta-round(la*SR)
        assert k or offset==0
        left=0 if k==0 else ta-round(SEAM*SR)
        right=offset+len(y) if k==len(ids)-2 else tb+round(SEAM*SR)
        left=max(left,offset,0);right=min(right,offset+len(y),len(output));assert right>left
        pos=np.arange(left,right)
        w=np.ones(len(pos))
        if k:w*=.5-.5*np.cos(np.pi*np.clip((pos-(ta-SEAM*SR))/(2*SEAM*SR),0,1))
        if k<len(ids)-2:w*=.5+.5*np.cos(np.pi*np.clip((pos-(tb-SEAM*SR))/(2*SEAM*SR),0,1))
        output[left:right]+=np.asarray(y[left-offset:right-offset])*w[:,None];weight[left:right]+=w
        actual_end=max(actual_end,right)
        b.update({'target_anchor_samples':[ta,tb],'output_offset_samples':offset,
                  'retained_output_frames':[left,right]})
        blocks.append(b);del y;p.unlink()
    output=output[:actual_end];weight=weight[:actual_end]
    assert np.min(weight)>.99, ('uncovered output',order,float(np.min(weight)))
    output/=weight[:,None]
    assert np.isfinite(output).all() and float(np.max(abs(output)))<1.02
    dest.parent.mkdir(parents=True,exist_ok=True);wavfile.write(dest,SR,output)
    result={'schema':'wavvy.capture_170_corrected_source.v1','order':order,'song_id':j['song_id'],
            'title':j['title'],'raw_path':j['raw_path'],'raw_sha256':j['raw_sha256'],
            'source_time_map_path':relative(PROD/'source-time-maps'/f'{order:02d}.json'),
            'source_time_map_sha256':sha(PROD/'source-time-maps'/f'{order:02d}.json'),
            'source_valid_frames':j['raw_valid_frames'],'source_duration_seconds':len(x)/SR,
            'output_path':relative(dest),'output_sha256':sha(dest),'output_samples':len(output),
            'output_duration_seconds':len(output)/SR,'output_peak_linear':float(np.max(abs(output))),
            'first_grid_beat_sample':first_grid,'grid_beat_count':len(beats),'target_bpm':170,
            'target_sample_formula':'first_grid_sample+round(k*288000/17)',
            'source_start_preserved':blocks[0]['source_guard_frames'][0]==0 and blocks[0]['output_offset_samples']==0,
            'source_end_preserved':blocks[-1]['source_guard_frames'][1]==len(x),
            'internal_overlap_seconds':2*SEAM,'pitch_processing':'FFmpeg atempo; no resampling pitch shift',
            'direct_listening':False,'producer_script_sha256':sha(Path(__file__)),
            'elapsed_seconds':time.monotonic()-before,'blocks':blocks}
    save(record_path,result)
    print(json.dumps({'stage':'corrected','order':order,'title':j['title'],'duration':len(output)/SR,
                      'max_anchor_error_ms':max(abs(b['observed_end_error_ms']) for b in blocks),
                      'elapsed_seconds':result['elapsed_seconds']},ensure_ascii=False),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['pilot','render','prepare']);p.add_argument('--orders',type=int,nargs='+')
    a=p.parse_args()
    if a.stage=='pilot':
        for order,near in [(1,80),(3,170),(20,150)]:
            if a.orders is None or order in a.orders:pilot(order,near)
        assert all(json.loads((PROD/'pilots'/f'{n:02d}.json').read_text())['passed'] for n in [1,3,20])
        save(PROD/'pilots/validation.json',{'passed':True,'orders':[1,3,20],'tests':3,'direct_listening':False})
    else:
        for n in a.orders or range(1,21):
            (render if a.stage=='render' else path_for)(n)
