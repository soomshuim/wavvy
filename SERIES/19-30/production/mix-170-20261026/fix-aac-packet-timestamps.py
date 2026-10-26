#!/usr/bin/env python3
"""Approved metadata-only AAC PTS repair. Compressed audio payload is untouched."""
import hashlib,importlib.util,json,subprocess,time
from pathlib import Path
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('r170',P/'render-170.py');R=importlib.util.module_from_spec(s);s.loader.exec_module(R)
ROOT=R.ROOT;WORK=R.WORK;OUT=ROOT/'SERIES/19-30/output/mix-170-20261026'

def packets(path):
    cmd=['ffprobe','-v','error','-select_streams','a:0','-show_packets','-show_data_hash','sha256',
         '-show_entries','packet=pts,dts,duration,data_hash,side_data_list','-of','json',str(path)]
    return json.loads(subprocess.check_output(cmd,text=True))['packets'],cmd

def pcm_hash(path):
    cmd=['ffmpeg','-v','error','-nostdin','-i',str(path),'-map','0:a:0','-ar','48000','-ac','2','-c:a','pcm_f32le','-f','f32le','-']
    proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);h=hashlib.sha256();count=0
    for b in iter(lambda:proc.stdout.read(1024*1024),b''):h.update(b);count+=len(b)
    err=proc.stderr.read();assert proc.wait()==0,err
    return {'sha256':h.hexdigest(),'bytes':count,'frames':count//8,'command':cmd}

def main():
    before=time.monotonic();current=OUT/'continuous-mix-1930-repeat2.m4a';original=WORK/'continuous-mix-1930-repeat2-pre-pts-fix.m4a'
    assert current.exists() and not original.exists();oldsha=R.sha(current);current.rename(original)
    oldlog=WORK/'final-verification.log'
    if oldlog.exists():oldlog.rename(WORK/'final-verification-pre-remux.log')
    cmd=['ffmpeg','-hide_banner','-v','error','-nostdin','-n','-i',str(original),'-map','0:a:0','-c:a','copy',
         '-bsf:a',r'setts=pts=(N-1)*1024:dts=(N-1)*1024:duration=min(DURATION\,1024):time_base=1/48000',
         '-movflags','+faststart',str(current)]
    R.run(cmd)
    a,ca=packets(original);b,cb=packets(current)
    assert len(a)==len(b);ha=[x['data_hash'] for x in a];hb=[x['data_hash'] for x in b];assert ha==hb
    assert a[0]['side_data_list']==b[0]['side_data_list'] and int(a[0]['pts'])==int(b[0]['pts'])==-1024
    assert int(a[-1]['duration'])==int(b[-1]['duration'])==900
    gaps=[]
    for x,y in zip(b,b[1:]):
        gap=int(y['pts'])-int(x['pts'])-int(x['duration'])
        if gap:gaps.append(gap)
    assert not gaps
    assert int(b[-1]['pts'])+int(b[-1]['duration'])==299829124
    pa=pcm_hash(original);pb=pcm_hash(current);assert pa['sha256']==pb['sha256'] and pa['frames']==pb['frames']==299829248
    result={'schema':'wavvy.metadata_only_aac_pts_repair.v1','passed':True,
      'original_path':R.relative(original),'original_sha256':oldsha,'final_path':R.relative(current),'final_sha256':R.sha(current),
      'remux_command':cmd,'codec':'copy; zero new AAC encodes','packet_count':len(a),
      'packet_payload_hash_lists_identical':True,'ordered_packet_payload_digest':hashlib.sha256('\n'.join(ha).encode()).hexdigest(),
      'original_first_packet':a[0],'final_first_packet':b[0],'original_last_packet':a[-1],'final_last_packet':b[-1],
      'final_pts_gaps_samples':gaps,'final_stream_end_sample':int(b[-1]['pts'])+int(b[-1]['duration']),
      'full_decoded_pcm_original':pa,'full_decoded_pcm_final':pb,'decoded_pcm_identical':True,
      'packet_probe_commands':[ca,cb],'elapsed_seconds':time.monotonic()-before}
    R.save(P/'aac-pts-repair.json',result)
    ep=P/'encode-record.json';e=json.loads(ep.read_text());assert e['aac_sha256']==oldsha
    e['first_encoded_aac_path']=R.relative(original);e['first_encoded_aac_sha256']=oldsha
    e['aac_sha256']=result['final_sha256'];e['aac_metadata_only_remux_path']=R.relative(P/'aac-pts-repair.json');e['aac_metadata_only_remux_sha256']=R.sha(P/'aac-pts-repair.json');e['aac_encode_generations']=1;e['additional_aac_encodes_after_first']=0
    R.save(ep,e);print(json.dumps({'passed':True,'packet_count':len(a),'final_sha256':e['aac_sha256'],'decoded_frames':pb['frames'],'elapsed_seconds':result['elapsed_seconds']}),flush=True)
if __name__=='__main__':main()
