async function captureSong(track) {
  const order=track.order, id=track.id, title=track.title;
  const p=order===10?"10-retry1":String(order).padStart(2,"0");
  const url=`https://suno.com/song/${id}`;
  const root="/Users/zenkim_office/Project/wavvy";
  const work="work/2026-10-22-selected-audio-capture";
  const mediaCode="console.log(JSON.stringify(await page.evaluate(()=>({time:new Date().toISOString(),url:location.href,title:document.title,audio:[...document.querySelectorAll('audio')].map(a=>({currentTime:a.currentTime,duration:a.duration,paused:a.paused,ended:a.ended,readyState:a.readyState})),playButtonPresent:!!document.querySelector('button[aria-label=Play]')}))));";
  function parseLast(result) {
    if(result.isError) throw Error(JSON.stringify(result.content));
    const lines=result.content.filter(c=>c.type==="text").map(c=>c.text).join("\n").split("\n");
    const line=lines.reverse().find(s=>s.trim().startsWith("{"));
    if(!line) throw Error("missing JSON browser observation");
    return JSON.parse(line);
  }
  let session=null, stopped=false, report=null;
  try {
    const nav=await tools.mcp__aside__repl({title:`${order}번 대상 확인`,code:`await page.goto('${url}'); var ps${order}=await snapshot(page,{interactive:true}); for(var readiness${order}=0;readiness${order}<20 && !(await page.evaluate(()=>!!document.querySelector('button[aria-label=Play]')));readiness${order}++){await sleep(500);ps${order}=await snapshot(page,{interactive:true});} console.log(ps${order}.tree.slice(0,4000)); ${mediaCode}`});
    const pre=parseLast(nav);
    if(pre.url!==url || pre.title!==`${title} by Wavvy | Suno` || !pre.playButtonPresent || !pre.audio[0].paused || pre.audio[0].currentTime!==0) throw Error("preflight ID/title/player mismatch: "+JSON.stringify(pre));
    const max=Math.min(360,Math.ceil(track.approxSeconds+35));
    const started=await tools.exec_command({cmd:`./${work}/capture-song record 640 ${max} ${work}/${p}-raw.wav ${work}/${p}.stop 2>&1 | tee ${work}/${p}-capture.log`,workdir:root,tty:true,yield_time_ms:1000,max_output_tokens:1000});
    session=started.session_id;
    if(!session) throw Error("capture process returned no session: "+JSON.stringify(started));
    let readyOutput=started.output||"";
    for(let readyPoll=0;readyPoll<6 && !(readyOutput.includes("capture_started") && readyOutput.includes("microphone=false"));readyPoll++) {
      const chunk=await tools.write_stdin({session_id:session,chars:"",yield_time_ms:1000,max_output_tokens:1000});
      readyOutput+=chunk.output||"";
      if(chunk.exit_code!==undefined) break;
    }
    if(!readyOutput.includes("capture_started") || !readyOutput.includes("microphone=false")) throw Error("capture not READY after bounded wait: "+JSON.stringify({initial:started,readyOutput}));
    notify(`${order}번 capture READY`);
    const played=await tools.mcp__aside__repl({title:`${order}번 0초 재생`,code:`${mediaCode} await page.getByRole('button',{name:'Play',exact:true}).click(); var ac${order}=await snapshot(page,{selector:'button[aria-label^="Playbar:"]',interactive:true}); console.log(ac${order}.tree); ${mediaCode}`});
    if(played.isError) throw Error(JSON.stringify(played.content));
    const playLines=played.content.filter(c=>c.type==="text").map(c=>c.text).join("\n").split("\n").filter(s=>s.trim().startsWith("{")).map(s=>JSON.parse(s));
    const before=playLines[0], afterClick=playLines.at(-1);
    if(before.url!==url || before.audio[0].currentTime!==0 || !before.audio[0].paused) throw Error("not at 0 before Play");
    await new Promise(r=>setTimeout(r,2000));
    let r=await tools.mcp__aside__repl({title:`${order}번 재생 확인`,code:mediaCode});
    let first=parseLast(r);
    if(first.url!==url || first.audio[0].paused || !(first.audio[0].duration>100)) throw Error("play not confirmed: "+JSON.stringify(first));
    const duration=first.audio[0].duration;
    const samples=[first];
    notify(`${order}번 시작 ${first.audio[0].currentTime.toFixed(1)}/${duration.toFixed(2)}초`);
    let switchReason=null, previous=first;
    for(let count=0;count<45;count++) {
      const delay=previous.audio[0].currentTime<duration-20?30000:2000;
      await new Promise(resolve=>setTimeout(resolve,delay));
      r=await tools.mcp__aside__repl({title:`${order}번 재생 진행`,code:mediaCode});
      const sample=parseLast(r);
      samples.push(sample);
      if(sample.url!==url) throw Error("song URL changed during playback");
      const a=sample.audio[0];
      notify(`${order}번 ${a.currentTime.toFixed(1)}/${a.duration?.toFixed(2)}초`);
      if((previous.audio[0].currentTime>duration-3 && a.currentTime<30 && a.currentTime<previous.audio[0].currentTime) || (a.duration && Math.abs(a.duration-duration)>1 && a.currentTime<30)) { switchReason="media_switched";break; }
      if(a.paused && a.ended) {switchReason="natural_end";break;}
      if(a.paused && !a.ended) throw Error("playback unexpectedly paused");
      previous=sample;
    }
    if(!switchReason) throw Error("song end not observed");
    const stopUi=await tools.mcp__aside__repl({title:`${order}번 후속 재생 정지`,code:`var pe${order}=await snapshot(page,{selector:'button[aria-label^="Playbar:"]',interactive:true}); console.log(pe${order}.tree); if(await page.evaluate(()=>!!document.querySelector('button[aria-label="Playbar: Pause button"]'))) await page.getByRole('button',{name:'Playbar: Pause button'}).click(); ${mediaCode}`});
    const pause=parseLast(stopUi);
    if(!pause.audio[0].paused) throw Error("player did not pause");
    const marker=await tools.exec_command({cmd:`touch ${work}/${p}.stop`,workdir:root,max_output_tokens:1000});
    const closed=await tools.write_stdin({session_id:session,chars:"",yield_time_ms:1000,max_output_tokens:1000});
    stopped=true;
    if(closed.exit_code!==0 || !closed.output.includes("write_error=none")) throw Error("capture failed to close: "+JSON.stringify(closed));
    const scanR=await tools.exec_command({cmd:`python3 ${work}/raw-scan.py ${order} ${work}/${p}-raw.wav`,workdir:root,max_output_tokens:4000});
    if(scanR.exit_code!==0) throw Error("raw scan failed: "+scanR.output);
    const scan=JSON.parse(scanR.output.trim());
    report={candidate_id:id,title,url,browser_tool:"mcp__aside__repl",capture:"ScreenCaptureKit Aside PID640 app-only, captureMicrophone=false",capture_started:readyOutput,ui_duration_seconds:duration,before,after_click:afterClick,samples,stop_reason:switchReason,paused_after:pause,capture_stopped:closed.output,raw_scan:scan,pts_recorded:false};
    for(const [name,obj] of [["ui-timeline",report],["ui-start",{candidate_id:id,title,url,capture_started:readyOutput,before,after_click:afterClick,play_confirmed:first}],["ui-after",{candidate_id:id,title,url,last_selected_sample:samples.at(-2),switch_sample:samples.at(-1),paused_after:pause,capture_stopped:closed.output}]]) {
      const patch=`*** Begin Patch\n*** Add File: ${root}/${work}/${p}-${name}.json\n+${JSON.stringify(obj,null,2).split("\n").join("\n+")}\n*** End Patch`;
      await tools.apply_patch(patch);
    }
    text(JSON.stringify({order,title,id,ui_duration_seconds:duration,stop_reason:switchReason,raw_scan:scan,evidence_prefix:`${work}/${p}`,capture_closed:true}));
  } catch(error) {
    notify(`${order}번 오류: ${String(error)}`);
    if(session && !stopped) {
      await tools.mcp__aside__repl({title:`${order}번 오류 후 플레이어 정지`,code:`var errSnap=await snapshot(page,{selector:'button[aria-label^="Playbar:"]',interactive:true}); if(await page.evaluate(()=>!!document.querySelector('button[aria-label="Playbar: Pause button"]'))) await page.getByRole('button',{name:'Playbar: Pause button'}).click(); console.log(errSnap.tree);`});
      await tools.exec_command({cmd:`touch ${work}/${p}.stop`,workdir:root,max_output_tokens:1000});
      await tools.write_stdin({session_id:session,chars:"",yield_time_ms:1000,max_output_tokens:1000});
    }
    throw error;
  }
}
