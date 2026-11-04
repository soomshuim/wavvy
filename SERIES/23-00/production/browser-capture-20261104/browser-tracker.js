// Own DOM instrumentation only. Browser control remains with Aside MCP.
// Call after the selected song has been paused and sought to zero.
(expected) => {
  if (window.__wavvy2300Timer) clearInterval(window.__wavvy2300Timer);
  if (window.__wavvy2300PlayGuard) {
    document.removeEventListener('play', window.__wavvy2300PlayGuard, true);
  }
  const audio = [...document.querySelectorAll('audio')].find(a => a.duration > 100);
  const title = document.querySelector('h1')?.innerText;
  if (location.pathname !== '/song/' + expected.id || title !== expected.title) {
    throw Error('Selected song URL/title mismatch');
  }
  if (!audio || !audio.paused || audio.currentTime > 0.02 || audio.playbackRate !== 1) {
    throw Error('Selected audio is not paused at zero at rate one');
  }
  const state = {
    schema_version: 1, song_id: expected.id, title, url: location.href,
    prepared_at: new Date().toISOString(), duration: audio.duration,
    done: false, events: [], samples: []
  };
  window.__wavvy2300Capture = state;
  const take = type => ({
    type, unix_ms: Date.now(), performance_ms: performance.now(),
    currentTime: audio.currentTime, duration: audio.duration,
    paused: audio.paused, ended: audio.ended, readyState: audio.readyState,
    playbackRate: audio.playbackRate, muted: audio.muted, volume: audio.volume
  });
  for (const name of ['play', 'playing', 'pause', 'waiting', 'stalled',
                       'seeking', 'seeked', 'ratechange', 'ended', 'error']) {
    audio.addEventListener(name, event => {
      state.events.push(take(event.type));
      if (event.type === 'ended') {
        state.done = true;
        state.ended_event = take('ended');
        for (const media of document.querySelectorAll('audio,video')) media.pause();
        clearInterval(window.__wavvy2300Timer);
      }
    });
  }
  window.__wavvy2300PlayGuard = event => {
    if (window.__wavvy2300Capture?.done && event.target instanceof HTMLMediaElement) {
      event.target.pause();
    }
  };
  document.addEventListener('play', window.__wavvy2300PlayGuard, true);
  window.__wavvy2300Timer = setInterval(() => {
    state.samples.push(take('poll'));
    if (location.pathname !== '/song/' + expected.id) state.unexpected_navigation = true;
  }, 250);
  return { prepared: true, song_id: expected.id, duration: audio.duration };
}
