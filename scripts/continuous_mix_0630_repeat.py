#!/usr/bin/env python3
"""Two cycles from the preserved single-cycle PCM and one verified repeat seam.

No large repeat WAV is stored. Three independently decoded crops are compared
sample-for-sample to the PCM feeding a single AAC encode, with SHA256 evidence.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import numpy as np
from scipy import signal

R=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('continuous_mix_base',R/'scripts/continuous_mix_0630.py')
B=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(B)
CONFIG=R/'SERIES/06-30/production/continuous-mix-20261024-repeat2.json'
C=json.loads(CONFIG.read_text());SR=48000
W=R/'work/0630-continuous-mix-20261024/repeat2-render'
OUT=R/'SERIES/06-30/output/continuous-mix-20261024/repeat2'
SEAM=OUT/'transitions/20-01.wav'

def pinned_base():
    for key in ['base_script','base_config','base_manifest']:
        row=C[key];assert B.sha(R/row['path'])==row['sha256'],('changed baseline',key)
    base=json.loads((R/C['base_manifest']['path']).read_text())
    assert B.sha(R/C['base_master']['path'])==C['base_master']['sha256']
    report=json.loads((R/base['transition_results_path']).read_text())
    B.validate_acceptance(report['results']);B.source_hashes()
    return base

def validate_seam(result):
    g=C['gates'];pair=C['repeat_seam']['pair'];a=B.read(SEAM)
    assert result['technical_gate_pass'] is True and result['failures']==[]
    assert B.sha(SEAM)==result['preview_sha256']==C['repeat_seam']['preview_sha256']
    assert len(a)==round(B.geometry(pair)[2]*SR) and result['duration_error_samples']==0
    assert np.isfinite(a).all() and np.max(abs(a))<1 and result['clipped_samples']==0
    assert result['minimum_overlap_100ms_rms_dbfs']>=g['minimum_overlap_100ms_rms_dbfs']
    assert result['shared_observed_quarter_count']>=g['minimum_shared_observed_quarter_attacks']
    q=result['quarter_phase_difference']
    assert q['p90_abs_ms']<=g['quarter_phase_p90_ms_max'] and q['max_abs_ms']<=g['quarter_phase_max_ms_max']
    for side in ['out','in']:
        row=result[side];e=row['internal_attack_error']
        assert e['p90_abs_ms']<=g['independent_internal_actuator_p90_ms_max']
        assert e['max_abs_ms']<=g['independent_internal_actuator_max_ms_max']
        assert row['minimum_waveform_correlation']>=g['minimum_waveform_correlation']
        assert row['body_comparison']['max_sample_difference']==0

def prepare_seam():
    pinned_base()
    assert not W.exists() and not OUT.exists(),'refusing to replace prior repeat artifacts'
    W.mkdir(parents=True);(OUT/'transitions').mkdir(parents=True)
    pilot=R/C['repeat_seam']['pilot_preview_path'];validation=R/C['repeat_seam']['pilot_validation_path']
    if pilot.exists() and validation.exists():
        assert B.sha(pilot)==C['repeat_seam']['preview_sha256']
        with SEAM.open('xb') as f:f.write(pilot.read_bytes())
        result=json.loads(validation.read_text())
        result['reused_pilot_validation_path']=str(validation.relative_to(R))
        result['preview_path']=str(SEAM.relative_to(R))
    else:
        result=B.render_boundary(C['repeat_seam']['pair'],folder=W/'seam',output=SEAM)
    validate_seam(result)
    B.save(W/'seam-results.json',result);B.save(W/'frozen-config.json',C)

def timeline(base):
    chunks=[];entries=[];cursor=0
    def append(chunk):
        nonlocal cursor
        if chunk['kind']=='transition':
            chunk['overlap_mix_start_sample']=cursor+12000
            chunk['overlap_mix_end_sample']=cursor+chunk['samples']-12000
        chunk['mix_start_sample']=cursor;cursor+=chunk['samples'];chunk['mix_end_sample']=cursor
        chunks.append(chunk)
    for cycle in [1,2]:
        if cycle==1:entries.append({'cycle':1,'order':1,'mix_entry_sample':0})
        for original in base['timeline']['chunks']:
            c=copy.deepcopy(original);lo=c['mix_start_sample'];hi=c['mix_end_sample']
            if cycle==1 and c['kind']=='body' and c['order']==20:
                hi=C['three_crops'][0]['end_sample']
                c['source_end_sample']=c['source_start_sample']+hi-lo
            if cycle==2 and c['kind']=='body' and c['order']==1:
                lo=C['three_crops'][2]['start_sample'];c['source_start_sample']+=lo-original['mix_start_sample']
            c['samples']=hi-lo;c['cycle']=cycle;c['crop_index']=0 if cycle==1 else 2
            c['reference_base_master_samples']=[lo,hi]
            if c['kind']=='transition':
                c['preview_path']=str((B.OUTPUT/'transitions'/f'{c["label"]}.wav').relative_to(R))
                entries.append({'cycle':cycle,'order':int(c['label'].split('-')[1]),'mix_entry_sample':cursor+12000})
            append(c)
        if cycle==1:
            c=C['three_crops'][1]
            entries.append({'cycle':2,'order':1,'mix_entry_sample':cursor+12000})
            append({'kind':'transition','label':'20-01','cycle':1,'incoming_cycle':2,'crop_index':1,
                'samples':c['end_sample']-c['start_sample'],'preview_start_sample':c['start_sample'],
                'preview_end_sample':c['end_sample'],'preview_path':str(SEAM.relative_to(R))})
    assert cursor==C['expected_samples'] and len(chunks)==79 and len(entries)==40
    assert [(x['cycle'],x['order']) for x in entries]==[(cycle,i) for cycle in [1,2] for i in range(1,21)]
    for e in entries:
        source=B.CFG['sources'][e['order']-1];e.update({'mix_entry_seconds':e['mix_entry_sample']/SR,
            'title':source['path'].split('__')[1],'source_path':source['path'],
            'meaning':'incoming fade/beat-grid start; gain begins at zero, not a certified first audible sample'})
    return {'expected_samples':cursor,'expected_seconds':cursor/SR,'chunks':chunks,'track_entries':entries}

def crop_filter(c):
    return f'atrim=start_sample={c["start_sample"]}:end_sample={c["end_sample"]},asetpts=PTS-STARTPTS,aformat=sample_fmts=s32:sample_rates=48000:channel_layouts=stereo'

def read_exact(pipe,count):
    parts=[];remaining=count
    while remaining:
        b=pipe.read(remaining)
        assert b,('unexpected end of PCM pipe',remaining)
        parts.append(b);remaining-=len(b)
    return b''.join(parts)

def unpack24(data):
    b=np.frombuffer(data,np.uint8).reshape(-1,3).astype(np.uint32)
    return ((b[:,0]<<8)|(b[:,1]<<16)|(b[:,2]<<24)).view(np.int32).reshape(-1,2)

def reference(chunk):
    if chunk['kind']=='body':
        row=B.CFG['sources'][chunk['order']-1]
        return B.read(R/row['path']),chunk['source_start_sample'],10**(row['gain_db']/20),row['path']
    return B.read(R/chunk['preview_path']),chunk['preview_start_sample'],1.,chunk['preview_path']

def stream_encode(plan):
    graph=';'.join(f'[{i}:a]{crop_filter(c)}[p{i}]' for i,c in enumerate(C['three_crops']))
    graph+=';[p0][p1][p2]concat=n=3:v=0:a=1,asetpts=N/SR/TB,asplit=3[hash][verify][aac]'
    graphfile=W/'repeat2.ffgraph.txt';graphfile.write_text(graph+'\n')
    listening=OUT/'continuous-mix-0630-repeat2.m4a';hashfile=W/'lossless-stream.sha256'
    cmd=['ffmpeg','-hide_banner','-nostdin','-v','error','-n']
    for c in C['three_crops']:cmd+=['-i',str(R/c['path'])]
    cmd+=['-filter_complex_script',str(graphfile),'-map','[hash]','-c:a','pcm_s24le','-f','hash','-hash','sha256',str(hashfile),
        '-map','[verify]','-c:a','pcm_s24le','-f','s24le','pipe:1',
        '-map','[aac]','-c:a','aac','-b:a','320k','-ar','48000','-movflags','+faststart',str(listening)]
    B.save(W/'render-command.json',cmd)
    h=hashlib.sha256();independent_hash=hashlib.sha256();checks=[];independent_commands=[]
    peak=0;clipped=0;total=0;proc=None;expected=None;crop_index=None
    with (W/'stream-encode.log').open('wb') as log:
        try:
            proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=log,cwd=R)
            for c in plan['chunks']:
                if c['crop_index']!=crop_index:
                    if expected is not None:
                        assert expected.stdout.read(1)==b'';assert expected.wait()==0
                    crop_index=c['crop_index'];crop=C['three_crops'][crop_index]
                    ecmd=['ffmpeg','-hide_banner','-nostdin','-v','error','-i',str(R/crop['path']),'-af',crop_filter(crop),'-c:a','pcm_s24le','-f','s24le','pipe:1']
                    independent_commands.append(ecmd)
                    expected=subprocess.Popen(ecmd,stdout=subprocess.PIPE,stderr=log,cwd=R)
                source,start,gain,sourcepath=reference(c);worst=0.;part_hash=hashlib.sha256()
                for offset in range(0,c['samples'],SR*10):
                    count=min(SR*10,c['samples']-offset);actual=read_exact(proc.stdout,count*6);want=read_exact(expected.stdout,count*6)
                    assert actual==want,('rendered PCM differs from independent source crop',c,offset)
                    h.update(actual);independent_hash.update(want);part_hash.update(actual);total+=count
                    raw=unpack24(actual);peak=max(peak,int(np.max(abs(raw.astype(np.int64)))))
                    clipped+=int(np.count_nonzero((raw==2147483392)|(raw==-2147483648)))
                    expected_float=np.asarray(source[start+offset:start+offset+count],float)*gain
                    err=float(np.max(abs(raw.astype(float)/2147483648-expected_float)));worst=max(worst,err)
                    assert err<2/8388608,('direct source gain/preview comparison failed',c,offset,err)
                checks.append({'kind':c['kind'],'label':c.get('label'),'order':c.get('order'),'cycle':c['cycle'],
                    'mix_interval_samples':[c['mix_start_sample'],c['mix_end_sample']],'samples_compared':c['samples'],
                    'rendered_pcm_sha256':part_hash.hexdigest(),'all_samples_equal_to_independent_base_or_seam_crop':True,
                    'direct_reference_path':sourcepath,'direct_reference_start_sample':start,
                    'maximum_direct_source_gain_or_preview_error':worst,'quantization_bound':2/8388608})
            assert expected.stdout.read(1)==b'' and expected.wait()==0
            assert proc.stdout.read(1)==b'' and proc.wait()==0
        finally:
            for p in [proc,expected]:
                if p is not None and p.poll() is None:p.terminate();p.wait()
    muxhash=hashfile.read_text().strip().split('=')[1].lower()
    assert total==plan['expected_samples'] and clipped==0
    assert muxhash==h.hexdigest()==independent_hash.hexdigest()
    result={'pcm_encoding':'signed little-endian packed24,48kHz,stereo','total_samples':total,
        'hash_muxer_sha256':muxhash,'verified_pipe_sha256':h.hexdigest(),'independent_three_crop_sha256':independent_hash.hexdigest(),
        'all79_full_crop_checks':checks,'sample_peak_abs':peak/2147483648,'clipped_samples':clipped,
        'render_command_path':str((W/'render-command.json').relative_to(R)),
        'independent_sequential_commands':independent_commands,'no_repeat_wav_written':True}
    B.save(W/'lossless-stream-validation.json',result)
    return listening,result

def aac_transition_samples(listening,plan):
    checks=[]
    for c in plan['chunks']:
        if c['kind']!='transition':continue
        start=c['mix_start_sample']+c['samples']//2-SR//2
        local=c['preview_start_sample']+start-c['mix_start_sample']
        ref=np.asarray(B.read(R/c['preview_path'])[local:local+SR],float)
        cmd=['ffmpeg','-hide_banner','-nostdin','-v','error','-ss',f'{start/SR:.12f}','-i',str(listening),
            '-af',f'atrim=end_sample={SR},asetpts=PTS-STARTPTS','-c:a','pcm_f32le','-f','f32le','pipe:1']
        actual=np.frombuffer(subprocess.check_output(cmd),np.float32).reshape(-1,2).astype(float)
        assert actual.shape==ref.shape
        x=ref.mean(axis=1);y=actual.mean(axis=1);den=np.linalg.norm(x)*np.linalg.norm(y)
        corr=float(np.dot(x,y)/den);cc=signal.correlate(y,x,mode='full',method='fft')
        center=len(x)-1;lags=np.arange(-96,97);best=int(lags[np.argmax(cc[center-96:center+97])])
        rms=np.sqrt(np.mean(ref*ref));error=np.sqrt(np.mean((actual-ref)**2));snr=B.db(rms/max(error,1e-30))
        assert corr>=.95 and abs(best)<=2,('AAC transition timing/content mismatch',c['label'],c['cycle'],corr,best)
        checks.append({'label':c['label'],'cycle':c['cycle'],'master_start_sample':start,'samples':SR,
            'reference_preview_path':c['preview_path'],'reference_start_sample':local,
            'zero_lag_waveform_correlation':corr,'best_lag_samples_in_plus_minus_2ms':best,
            'lossy_snr_db':snr,'command':cmd})
    assert len(checks)==39
    return checks

def codec_timing(listening,expected_samples):
    packetcmd=['ffprobe','-v','error','-select_streams','a:0','-read_intervals','%+#1',
        '-show_packets','-of','json',str(listening)]
    first=json.loads(subprocess.check_output(packetcmd,text=True))['packets'][0]
    framecmd=['ffprobe','-v','error','-select_streams','a:0','-show_frames',
        '-show_entries','frame=nb_samples','-of','csv=p=0',str(listening)]
    decoded=0;frames=0
    with (W/'aac-decoded-sample-count.log').open('w') as log:
        proc=subprocess.Popen(framecmd,stdout=subprocess.PIPE,stderr=log,text=True)
        for line in proc.stdout:
            if line.strip():decoded+=int(line.strip().split(',')[0]);frames+=1
        assert proc.wait()==0
    padding=decoded-expected_samples
    assert 0<=padding<1024,('unexpected AAC decoded tail padding',decoded,expected_samples)
    result={'expected_pcm_samples':expected_samples,'actual_decoded_samples':decoded,'decoded_frame_count':frames,
        'decoded_minus_pcm_tail_padding_samples':padding,'tail_padding_seconds':padding/SR,
        'first_packet':first,'first_packet_command':packetcmd,'full_decode_frame_count_command':framecmd,
        'timing_interpretation':'AAC priming is described by first-packet skip_samples; decoded tail may contain frame padding. All39 interior waveform samples have zero observed lag.'}
    B.save(W/'aac-codec-timing.json',result)
    return result

def render_master():
    base=pinned_base();seam=json.loads((W/'seam-results.json').read_text());validate_seam(seam)
    assert B.object_sha(json.loads((W/'frozen-config.json').read_text()))==B.object_sha(C)
    plan=timeline(base);B.save(W/'timeline-plan.json',plan)
    expected_aac=round(C['expected_duration_seconds']*40000*1.03);free=shutil.disk_usage(R).free
    assert free>=expected_aac+C['disk_minimum_reserve_bytes'],('insufficient AAC plus1GiB reserve',free,expected_aac)
    print(json.dumps({'stage':'before-repeat-encode','expected_samples':plan['expected_samples'],
        'expected_seconds':plan['expected_seconds'],'expected_aac_bytes':expected_aac,'free_bytes':free,
        'technical_transition_occurrences':35,'exact_user_approved_transition_occurrences':4}),flush=True)
    listening,lossless=stream_encode(plan)
    meter=B.meter(listening,W/'aac-loudness-full-decode.log')
    assert meter['true_peak_dbtp']<=C['gates']['max_final_true_peak_dbtp']
    metadata=B.probe(listening);duration=float(metadata['format']['duration'])
    assert abs(duration-plan['expected_seconds'])<.1
    silencecmd=['ffmpeg','-hide_banner','-nostdin','-v','info','-xerror','-err_detect','explode','-i',str(listening),
        '-af','silencedetect=noise=-60dB:d=0.1','-f','null','-']
    B.run(silencecmd,W/'aac-full-silence-decode.log')
    text=(W/'aac-full-silence-decode.log').read_text();starts=[float(x) for x in re.findall(r'silence_start: ([0-9.]+)',text)]
    interior=[x for x in starts if 2<x<plan['expected_seconds']-2]
    assert not interior,('unexpected interior quiet interval',interior)
    aacchecks=aac_transition_samples(listening,plan);B.save(W/'aac-39-transition-sample-checks.json',aacchecks)
    timing=codec_timing(listening,plan['expected_samples'])
    preview=SEAM.with_suffix('.m4a')
    B.run(['ffmpeg','-hide_banner','-nostdin','-v','error','-n','-i',str(SEAM),'-c:a','aac','-b:a','256k',str(preview)],W/'seam-aac.log')
    tracklist=OUT/'tracklist.txt'
    with tracklist.open('x') as f:
        f.write('06-30 — exactly two cycles / 40 occurrences\nTimes mark incoming fade/beat-grid starts.\n\n')
        for e in plan['track_entries']:
            ms=round(e['mix_entry_seconds']*1000);h,rem=divmod(ms,3600000);m,rem=divmod(rem,60000);s,ms=divmod(rem,1000)
            f.write(f'{h:02d}:{m:02d}:{s:02d}.{ms:03d}  cycle {e["cycle"]} / {e["order"]:02d}. {e["title"]}\n')
    # This command can produce a WAV later when disk space permits; not executed.
    wavgraph=';'.join(f'[{i}:a]{crop_filter(c)}[p{i}]' for i,c in enumerate(C['three_crops']))+';[p0][p1][p2]concat=n=3:v=0:a=1[out]'
    wavcommand=['ffmpeg','-hide_banner','-nostdin','-n']
    for c in C['three_crops']:wavcommand+=['-i',str(R/c['path'])]
    wavcommand+=['-filter_complex',wavgraph,'-map','[out]','-c:a','pcm_s24le','continuous-mix-0630-repeat2.wav']
    final={'scope':C['scope'],'configuration_path':str(CONFIG.relative_to(R)),'configuration_sha256':B.sha(CONFIG),
        'youtube_input_policy':'Already contains all20 songs exactly twice. Do not apply repeat2 again during video production (would make four cycles).',
        'script_path':str(Path(__file__).relative_to(R)),'script_sha256':B.sha(Path(__file__)),
        'baseline_manifest_path':C['base_manifest']['path'],'baseline_manifest_sha256':C['base_manifest']['sha256'],
        'repeat_count':2,'track_occurrences':40,'transition_occurrences':39,
        'transition_acceptance':{'technical_pass_occurrences':35,'exact_user_approved_occurrences':4,
            'all39_technical_pass':False,'all39_accepted':True,'baseline_exact_approval':base['transition_acceptance'],
            'new_repeat_seam_technical_pass':True,'full_repeat_listening_approved':False},
        'listening_copy':{'path':str(listening.relative_to(R)),'sha256':B.sha(listening),'file_bytes':listening.stat().st_size,
            'expected_samples':plan['expected_samples'],'expected_pcm_seconds':plan['expected_seconds'],
            'container_seconds':duration,'container_minus_pcm_seconds':duration-plan['expected_seconds'],
            'metadata':metadata,'loudness_full_decode':meter,'codec_timing':timing},
        'lossless_pcm_stream_validation':lossless,'timeline':plan,'tracklist_path':str(tracklist.relative_to(R)),
        'timeline_path':str((W/'timeline-plan.json').relative_to(R)),'timeline_sha256':B.sha(W/'timeline-plan.json'),
        'three_exact_crops':C['three_crops'],'repeat_seam_preview':{'wav_path':str(SEAM.relative_to(R)),
            'wav_sha256':B.sha(SEAM),'m4a_path':str(preview.relative_to(R)),'m4a_sha256':B.sha(preview),
            'validation_path':str((W/'seam-results.json').relative_to(R))},
        'aac39_transition_samples':aacchecks,'aac_silence_check':{'threshold_dbfs':-60,'minimum_duration_seconds':.1,
            'quiet_starts_seconds':starts,'unexpected_interior_quiet_starts':interior,'full_decode_exit_code':0,'command':silencecmd},
        'source20_hashes_after':B.source_hashes(),'one_cycle_master_after_sha256':B.sha(R/C['base_master']['path']),
        'two_cycle_wav_saved':False,'reason':'Available disk space; verified lossless PCM streamed without writing another large WAV',
        'optional_lossless_wav_reproduction_command_not_executed':wavcommand,
        'limitations':C['limitations'],'free_bytes_after':shutil.disk_usage(R).free}
    assert final['one_cycle_master_after_sha256']==C['base_master']['sha256']
    B.save(OUT/'manifest.json',final)
    B.save(R/'.ai/validation/2026-10-24-0630-continuous-mix-repeat2-worker-check.json',final)
    print(json.dumps({'stage':'repeat2-complete','listening_copy':final['listening_copy'],
        'lossless_pcm_sha256':lossless['verified_pipe_sha256'],'free_bytes_after':final['free_bytes_after']},ensure_ascii=False),flush=True)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--stage',required=True,choices=['seam','master'])
    args=parser.parse_args()
    if args.stage=='seam':prepare_seam()
    else:render_master()

if __name__=='__main__':main()
