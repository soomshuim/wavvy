#!/usr/bin/env python3
"""Read-only exact filter replay, full PCM residual and held-out local gain audit."""
import hashlib,importlib.util,json,subprocess,time
from pathlib import Path
import numpy as np
from scipy import signal
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('integrated160',P/'render-160.py');R=importlib.util.module_from_spec(s);s.loader.exec_module(R)
SR=48000

def rms(x):return float(np.sqrt(np.mean(np.asarray(x,float)**2)))
def db(v):return float(20*np.log10(max(float(v),1e-30)))
def cosine(x,y):
    x=np.asarray(x,float).ravel();y=np.asarray(y,float).ravel()
    return float(np.dot(x,y)/max(np.linalg.norm(x)*np.linalg.norm(y),1e-30))
def exact_read(pipe,size):
    chunks=[];left=size
    while left:
        b=pipe.read(left)
        if not b:break
        chunks.append(b);left-=len(b)
    return b''.join(chunks)
def gain_fit(x,y,block):
    n=len(x)//block*block;x=np.asarray(x[:n],float).reshape(-1,block,2);y=np.asarray(y[:n],float).reshape(-1,block,2)
    # Fit one common stereo gain on even samples; test on unseen odd samples.
    tx=x[:,::2];ty=y[:,::2];den=np.sum(tx*tx,axis=(1,2));valid=den/(tx.shape[1]*2)>1e-10
    gain=np.sum(tx*ty,axis=(1,2))/np.maximum(den,1e-30)
    vx=x[:,1::2];vy=y[:,1::2];residual=vy-vx*gain[:,None,None]
    good=gain[valid];err=rms(residual[valid]) if np.any(valid) else None
    return {'block_samples':block,'block_ms':block*1000/SR,'valid_blocks':int(np.sum(valid)),
       'gain_values':good.tolist(),'gain_p05_p50_p95':np.quantile(good,[.05,.5,.95]).tolist() if len(good) else None,
       'gain_coefficient_of_variation':float(np.std(good)/max(abs(np.mean(good)),1e-30)) if len(good) else None,
       'heldout_residual_rms_dbfs':db(err) if err is not None else None,
       'heldout_error_snr_db':db(rms(vy[valid]))-db(err) if err is not None else None,
       'informational_only':'Gain fits explain varying loudness; acceptance uses exact filter replay, not a fitted-gain threshold.'}

def main():
    before=time.monotonic();enc=json.loads((P/'encode-record.json').read_text());tr=json.loads((P/'transform-record.json').read_text());tl=json.loads((P/'timeline.json').read_text())
    src=R.ROOT/tr['output_path'];wav=R.ROOT/enc['wav_path'];aac=R.ROOT/enc['aac_path']
    for f,h in [(src,tr['output_sha256']),(wav,enc['wav_sha256']),(aac,enc['aac_sha256'])]:assert R.sha(f)==h
    graph=enc['command'][enc['command'].index('-filter_complex')+1]
    assert graph.startswith('[0:a]') and graph.endswith(',asplit=2[w][a]')
    af=graph[len('[0:a]'):-len(',asplit=2[w][a]')]
    # This emits analysis-only float bytes to stdout. No WAV/AAC is written.
    commands={
      'replayed_normalized_float':['ffmpeg','-hide_banner','-nostdin','-nostats','-i',str(src),'-af',af,'-c:a','pcm_f32le','-f','f32le','-'],
      'final_wav_float':['ffmpeg','-v','error','-nostdin','-i',str(wav),'-c:a','pcm_f32le','-f','f32le','-'],
      'unprocessed_intermediate_float':['ffmpeg','-v','error','-nostdin','-i',str(src),'-c:a','pcm_f32le','-f','f32le','-']}
    locations=[('transition',t['number'],(t['start_sample']+t['end_sample'])//2-SR//2) for t in tl['transitions']]
    locations += [('body',n,(tl['entries'][n-1]['mix_start_sample']+tl['entries'][n-1]['mix_end_sample'])//2-SR//2) for n in [1,4,11,16,20,21,40]]
    windows=[{'kind':k,'number':n,'start_sample':a,'data':{label:np.zeros((SR,2),np.float32) for label in commands}} for k,n,a in locations]
    procs={};logs={};digests={label:hashlib.sha256() for label in commands};count=0;maxdiff=0.;diff2=0.;value2=0.
    try:
        for label,cmd in commands.items():
            logs[label]=(R.W/f'replay-{label}.stderr.log').open('wb')
            procs[label]=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=logs[label])
        while count<R.OUTPUT_N:
            length=min(10*SR,R.OUTPUT_N-count);data={}
            for label,p in procs.items():
                raw=exact_read(p.stdout,length*8);assert len(raw)==length*8,(label,count,len(raw),length*8)
                digests[label].update(raw);data[label]=np.frombuffer(raw,'<f4').reshape(-1,2)
                assert np.isfinite(data[label]).all()
                for w in windows:
                    left=max(count,w['start_sample']);right=min(count+length,w['start_sample']+SR)
                    if right>left:w['data'][label][left-w['start_sample']:right-w['start_sample']]=data[label][left-count:right-count]
            expected=data['replayed_normalized_float'].astype(float);actual=data['final_wav_float'].astype(float)
            delta=actual-expected;maxdiff=max(maxdiff,float(np.max(abs(delta))));diff2+=float(np.sum(delta*delta));value2+=float(np.sum(expected*expected));count+=length
        for label,p in procs.items():assert p.stdout.read(1)==b'' and p.wait()==0,label
    finally:
        for p in procs.values():
            if p.poll() is None:p.terminate();p.wait()
        for f in logs.values():f.close()
    rows=[]
    for w in windows:
        x=w['data']['unprocessed_intermediate_float'];expected=w['data']['replayed_normalized_float'];actual=w['data']['final_wav_float']
        em=expected.astype(float).mean(axis=1);am=actual.astype(float).mean(axis=1)
        if rms(em)>1e-6:
            cc=signal.correlate(am,em,mode='full',method='fft');c=len(em)-1;lag=int(np.argmax(cc[c-96:c+97])-96)
            corr=cosine(em,am)
        else:lag=None;corr=None
        a10=gain_fit(x,actual,480);a1=gain_fit(x,actual,48);a1.pop('gain_values')
        rows.append({'kind':w['kind'],'number':w['number'],'start_sample':w['start_sample'],'frames':SR,
          'unprocessed_to_final_mono_correlation':cosine(x.mean(axis=1),actual.mean(axis=1)),
          'replay_to_final_mono_correlation':corr,'replay_to_final_lag_samples':lag,
          'replay_to_final_maximum_absolute_difference':float(np.max(abs(actual-expected))),
          'replay_to_final_residual_rms_dbfs':db(rms(actual-expected)),
          'local_gain_10ms':a10,'local_gain_1ms_heldout':a1})
    threshold=2**-22 # Two signed24-bit quantization steps after float->PCM24.
    passed=maxdiff<=threshold and all((r['replay_to_final_lag_samples'] in [None,0]) and (r['replay_to_final_mono_correlation'] is None or r['replay_to_final_mono_correlation']>.999999) for r in rows)
    j={'schema':'wavvy.exact_loudnorm_replay_qa.v1','passed':bool(passed),'audio_files_modified':False,'audio_files_reencoded':False,
       'source_intermediate_path':R.relative(src),'source_intermediate_sha256':R.sha(src),'final_wav_path':enc['wav_path'],'final_wav_sha256':R.sha(wav),'final_aac_sha256':R.sha(aac),
       'encode_record_path':R.relative(P/'encode-record.json'),'encode_record_sha256':R.sha(P/'encode-record.json'),
       'exact_replayed_filter':af,'commands':commands,'full_stream_frames':count,
       'full_stream_float_sha256':{label:d.hexdigest() for label,d in digests.items()},
       'maximum_absolute_pcm_difference':maxdiff,'permitted_pcm_difference':threshold,
       'pcm_difference_basis':'Two signed24-bit quantization steps; no lowered content correlation threshold and no fitted gain used for acceptance.',
       'whole_pcm_residual_rms_dbfs':db(np.sqrt(diff2/(count*2))),
       'whole_pcm_error_snr_db':10*np.log10(value2/max(diff2,1e-60)),
       'windows':rows,'direct_listening':False,'elapsed_seconds':time.monotonic()-before,
       'stderr_logs':[{'path':R.relative(R.W/f'replay-{label}.stderr.log'),'sha256':R.sha(R.W/f'replay-{label}.stderr.log')} for label in commands]}
    assert R.sha(src)==tr['output_sha256'] and R.sha(wav)==enc['wav_sha256'] and R.sha(aac)==enc['aac_sha256']
    R.save(P/'loudnorm-replay-qa.json',j)
    print(json.dumps({'passed':passed,'frames':count,'maximum_pcm_difference':maxdiff,'threshold':threshold,'seconds':j['elapsed_seconds']}),flush=True)
    assert passed,'Exact normalization replay mismatch; stop and report without changing thresholds.'

if __name__=='__main__':main()
