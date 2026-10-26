#!/usr/bin/env python3
"""Approved capture-preserving R3 offline time-map producer and numerical checks."""
import argparse, importlib.util, json, subprocess, time
from pathlib import Path
import numpy as np
from scipy import signal, ndimage
from scipy.io import wavfile
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('r170',P/'render-170.py');R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R)
ROOT=R.ROOT;WORK=R.WORK;SR=R.SR;save=R.save;sha=R.sha;relative=R.relative;read=R.read
RB='/opt/homebrew/bin/rubberband'

def map_for(order):
    j=R.path_for(order);beats=np.asarray(j['quarter_beat_seconds'])
    good=beats[(beats>=j['intro_relative_energy_end_seconds']) & (beats<=j['tail_relative_energy_start_seconds'])]
    assert len(good)>64
    first_ratio=(R.quarter_sample(16)/SR)/(good[16]-good[0])
    last_ratio=(R.quarter_sample(16)/SR)/(good[-1]-good[-17])
    first=round(good[0]*SR*first_ratio)
    source=np.rint(good*SR).astype(np.int64)
    target=first+np.array([R.quarter_sample(k) for k in range(len(good))])
    n=round(j['source_duration_seconds']*SR)
    end=round(target[-1]+(n-source[-1])*last_ratio)
    assert 0<source[0]<source[-1]<n and 0<target[0]<target[-1]<end
    assert np.all(np.diff(source)>0) and np.all(np.diff(target)>0)
    result={'schema':'wavvy.capture_170_rubberband_time_map.v1','order':order,'song_id':j['song_id'],'title':j['title'],
        'input_frames':n,'output_frames':end,'first_grid_beat_sample':int(target[0]),'grid_beat_count':len(good),
        'key_frames_input':source.tolist(),'key_frames_output':target.tolist(),
        'complete_map_input':[0]+source.tolist()+[n], 'complete_map_output':[0]+target.tolist()+[end],
        'implicit_origin_and_terminal_duration':True,'input_source0_through_natural_end':True,
        'sparse_regions_input_frames':[[0,int(source[0])],[int(source[-1]),n]],
        'sparse_edge_time_ratios':[first_ratio,last_ratio],
        'source_time_map_path':relative(P/'source-time-maps'/f'{order:02d}.json'),
        'source_time_map_sha256':sha(P/'source-time-maps'/f'{order:02d}.json'),
        'valid_source_path':j['valid_source_path'],'valid_source_sha256':j['valid_source_sha256'],
        'raw_path':j['raw_path'],'raw_sha256':j['raw_sha256'],'raw_valid_frames':j['raw_valid_frames'],
        'pitch_semitones':0,'engine':'Rubber Band4.0.0 R3 fine offline',
        'limitations':['Quarter path is an inferred pulse, not listener-confirmed meter.',
         'Sparse intro/tail use adjacent body tempo; audible170 beats are not certified in those regions.',
         'Dancing full/half metrical uncertainty remains; selected source family follows existing independent mid/high measurements.']}
    save(P/'rubberband-time-maps'/f'{order:02d}.json',result)
    return result

def pitch_check(src,out,mx,my):
    # Matched local log spectra, not musical key/chord or listener judgment.
    sx=read(src).astype(float).mean(axis=1);sy=read(out).astype(float).mean(axis=1)
    rows=[]
    freq=np.geomspace(80,6000,4096)
    for center in np.linspace(max(2,mx[1]/SR),min(len(sx)/SR-2,mx[-2]/SR),5):
        target=np.interp(center*SR,mx,my)/SR
        a=sx[round((center-1)*SR):round((center+1)*SR)]
        b=sy[max(0,round((target-1)*SR)):min(len(sy),round((target+1)*SR))]
        f,px=signal.welch(a,SR,nperseg=16384);_,py=signal.welch(b,SR,nperseg=16384)
        lx=np.log(np.maximum(np.interp(freq,f,px),1e-16));lx-=ndimage.gaussian_filter1d(lx,30)
        scores=[];shifts=np.arange(-100,101,2)
        for cents in shifts:
            ly=np.log(np.maximum(np.interp(freq*2**(cents/1200),f,py),1e-16));ly-=ndimage.gaussian_filter1d(ly,30)
            scores.append(float(np.corrcoef(lx,ly)[0,1]))
        best=int(np.argmax(scores));rows.append({'source_center_seconds':float(center),'output_center_seconds':float(target),
            'best_frequency_shift_cents':int(shifts[best]),'spectral_correlation':scores[best]})
    median=float(np.median([r['best_frequency_shift_cents'] for r in rows]))
    return {'method':'five matched two-second Welch spectra, whitened log-frequency correlation, ±100cent search',
            'windows':rows,'median_shift_cents':median,'passed':abs(median)<=20,
            'caveat':'Polyphonic spectral proxy, not exact note transcription or auditory quality approval.'}

def checks(src,out,mx,my):
    x=read(src);y=read(out)
    assert len(x)==mx[-1] and len(y)==my[-1],(len(x),mx[-1],len(y),my[-1])
    assert np.isfinite(y).all() and np.max(abs(y))<=1
    es=R.MEASURE.envelopes(src);eo=R.MEASURE.envelopes(out)
    align=[]
    for center in np.arange(4,len(x)/SR-3,4):
        # Source and output attack envelopes are separately measured. Their clocks
        # are compared through the supplied map, never by raw PCM similarity.
        tout=np.arange(np.interp((center-2)*SR,mx,my)/SR,np.interp((center+2)*SR,mx,my)/SR,.002)
        tin=np.interp(tout*SR,my,mx)/SR
        byband={}
        for band in ['mid','high']:
            warped=np.interp(tin*500,np.arange(len(es[band])),es[band])
            vals=[]
            for lag in range(-30,31):
                actual=np.interp((tout+lag/500)*500,np.arange(len(eo[band])),eo[band])
                if np.std(warped)<1e-12 or np.std(actual)<1e-12:vals.append(0.)
                else:vals.append(float(np.corrcoef(warped,actual)[0,1]))
            k=int(np.argmax(vals));byband[band]={'lag_ms':(k-30)*2,'correlation':vals[k]}
        align.append({'source_center_seconds':float(center),'bands':byband})
    reliable=[b for w in align for b in w['bands'].values() if b['correlation']>.4]
    assert reliable, 'No measurable source/output attack alignment'
    lag90=float(np.quantile([abs(b['lag_ms']) for b in reliable],.9))
    # Independent output autocorrelation, no use of source time-map beat points.
    tempos=R.MEASURE.local_tempos(eo)
    middle=[w for w in tempos if 5<w['center_seconds']<len(y)/SR-5]
    midhigh=[np.median([w['band_bpm']['mid'],w['band_bpm']['high']]) for w in middle]
    median=float(np.median(midhigh))
    pitch=pitch_check(src,out,mx,my)
    return {'schema':'wavvy.rubberband_output_numerical_check.v1','passed':lag90<=30 and abs(median-170)<2 and pitch['passed'],
       'expected_output_frames':int(my[-1]),'actual_output_frames':len(y),'length_error_samples':len(y)-int(my[-1]),
       'finite':True,'peak_linear':float(np.max(abs(y))),'source_output_attack_alignment':align,
       'reliable_alignment_windows':len(reliable),'attack_abs_lag_p90_ms':lag90,
       'independent_output_tempo_windows':tempos,'mid_high_output_bpm_median':median,
       'pitch':pitch,'direct_listening':False,
       'boundary_samples':{'input_first':x[0].tolist(),'input_last':x[-1].tolist(),
         'output_first':y[0].tolist(),'output_last':y[-1].tolist(),
         'meaning':'Boundary amplitudes need not equal after phase-vocoder transformation; map origin0/end plus complete input and exact output length preserve temporal extent.'}}

def transform(src,out,mx,my,mapfile,log):
    assert not out.exists(),out;out.parent.mkdir(parents=True,exist_ok=True)
    inner=[(int(a),int(b)) for a,b in zip(mx,my) if 0<a<mx[-1] and 0<b<my[-1]]
    mapfile.parent.mkdir(parents=True,exist_ok=True);mapfile.write_text(''.join(f'{a} {b}\n' for a,b in inner))
    cmd=[RB,'-3','-p','0','--timemap',str(mapfile),'-D',f'{my[-1]/SR:.14f}',str(src),str(out)]
    before=time.monotonic();r=subprocess.run(cmd,capture_output=True,text=True);log.write_text(r.stdout+r.stderr)
    assert r.returncode==0,(r.returncode,log)
    assert 'NaN or Inf' not in r.stderr and 'no time stretch' not in r.stderr,r.stderr
    return {'command':cmd,'rubberband_version':subprocess.check_output([RB,'--version'],stderr=subprocess.STDOUT,text=True).strip(),
            'binary_sha256':sha(RB),'timemap_sha256':sha(mapfile),'elapsed_seconds':time.monotonic()-before,
            'log_path':relative(log),'log_sha256':sha(log)}

def pilot(order,start,end):
    m=map_for(order);x=read(ROOT/m['valid_source_path']);a,b=round(start*SR),round(end*SR)
    mx=np.array(m['complete_map_input']);my=np.array(m['complete_map_output'])
    ta,tb=round(np.interp(a,mx,my)),round(np.interp(b,mx,my))
    mask=(mx>a)&(mx<b);sx=np.r_[0,mx[mask]-a,b-a];sy=np.r_[0,my[mask]-ta,tb-ta]
    folder=WORK/'rubberband-pilots'/f'{order:02d}';folder.mkdir(parents=True,exist_ok=True)
    src=folder/'source.wav';wavfile.write(src,SR,np.asarray(x[a:b]));out=folder/'output.wav'
    produced=transform(src,out,sx,sy,folder/'timemap.txt',folder/'rubberband.log')
    qa=checks(src,out,sx,sy);save(P/'rubberband-pilots'/f'{order:02d}.json',{
      'order':order,'song_id':m['song_id'],'title':m['title'],'source_range_seconds':[start,end],
      'source_path':relative(src),'source_sha256':sha(src),'output_path':relative(out),'output_sha256':sha(out),
      'producer':produced,'qa':qa})
    print(json.dumps({'stage':'rubberband_pilot','order':order,'title':m['title'],'qa_passed':qa['passed'],
       'lag_p90_ms':qa['attack_abs_lag_p90_ms'],'tempo':qa['mid_high_output_bpm_median'],
       'pitch_cents':qa['pitch']['median_shift_cents'],'length_error':qa['length_error_samples'],
       'elapsed_seconds':produced['elapsed_seconds']},ensure_ascii=False),flush=True)
    assert qa['passed'],('Pilot numerical checks failed',order,qa)

def render(order):
    m=map_for(order);src=ROOT/m['valid_source_path'];out=WORK/'corrected'/f'{order:02d}.wav';folder=WORK/'rubberband'/f'{order:02d}';folder.mkdir(parents=True,exist_ok=True)
    mx=np.array(m['complete_map_input']);my=np.array(m['complete_map_output'])
    rec=P/'corrected'/f'{order:02d}.json'
    if rec.exists():
        saved=json.loads(rec.read_text());assert sha(out)==saved['output_sha256'];return
    produced=transform(src,out,mx,my,folder/'timemap.txt',folder/'rubberband.log')
    qa=checks(src,out,mx,my);save(P/'rubberband-qa'/f'{order:02d}.json',qa)
    # Full-song quiet sections can yield 145/220 family aliases; body model audit
    # is recorded separately before final acceptance. Strict duration/finite/pitch remain.
    assert qa['length_error_samples']==0 and qa['finite'] and qa['pitch']['passed'],('Full source duration/pitch check',order,qa)
    j={'schema':'wavvy.capture_170_rubberband_corrected_source.v1','order':order,'song_id':m['song_id'],'title':m['title'],
       'raw_path':m['raw_path'],'raw_sha256':m['raw_sha256'],'source_valid_frames':m['raw_valid_frames'],
       'source_time_map_path':relative(P/'rubberband-time-maps'/f'{order:02d}.json'),
       'source_time_map_sha256':sha(P/'rubberband-time-maps'/f'{order:02d}.json'),
       'source_duration_seconds':m['input_frames']/SR,'output_path':relative(out),'output_sha256':sha(out),
       'output_samples':len(read(out)),'output_duration_seconds':len(read(out))/SR,
       'first_grid_beat_sample':m['first_grid_beat_sample'],'grid_beat_count':m['grid_beat_count'],
       'source_start_preserved':True,'source_end_preserved':True,'target_bpm':170,
       'pitch_processing':'Rubber Band R3 offline, pitch0, variable sample-frame time map',
       'direct_listening':False,'producer':produced,'output_qa_path':relative(P/'rubberband-qa'/f'{order:02d}.json'),
       'output_qa_sha256':sha(P/'rubberband-qa'/f'{order:02d}.json'),'producer_script_sha256':sha(Path(__file__))}
    save(rec,j)
    print(json.dumps({'stage':'rubberband_corrected','order':order,'title':m['title'],'duration':j['output_duration_seconds'],
       'lag_p90_ms':qa['attack_abs_lag_p90_ms'],'tempo':qa['mid_high_output_bpm_median'],
       'pitch_cents':qa['pitch']['median_shift_cents'],'elapsed_seconds':produced['elapsed_seconds']},ensure_ascii=False),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['pilot','render']);p.add_argument('--orders',type=int,nargs='+');a=p.parse_args()
    if a.stage=='pilot':
        for order,start,end in [(1,60,100),(3,150,190),(20,140,180)]:
            if not a.orders or order in a.orders:pilot(order,start,end)
    else:
        for n in a.orders or range(1,21):render(n)
