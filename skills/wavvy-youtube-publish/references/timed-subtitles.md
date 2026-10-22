# Timed subtitles for an existing Wavvy video

Use this path when the requested change is subtitles on an already uploaded video. Confirm the target video and the approved lyric source. Keep its title, description, visibility, video, and comments unchanged unless separately requested. A subtitle follow-up does not require a new title approval or video upload.

## Build from evidence

- The approved lyrics control the words. Automatic speech recognition (ASR) can suggest timing or reveal a sung repeat, but its misheard text must not overwrite the lyrics. Keep the source unchanged. Add a displayed repeat only when the same approved words are supported by actual source evidence; retain that mapping.
- Compare the whole song structure and each repeated pass, not only lines with weak ASR matches. Use the render report's actual track starts and repeat offsets, including crossfades. Rounded chapters and a simple sum of WAV durations are not reliable subtitle offsets.
- Anchor the lines to observed vocal intervals. Do not interpolate across a long instrumental or silent stretch, or place an inferred start outside the supporting observation without flagging and resolving it. Short music-only clips can produce ASR hallucinations; check sufficient surrounding context and retain the raw timing evidence. Do not claim human listening that did not happen.
- Produce a UTF-8 SRT with consecutive cue numbers and `HH:MM:SS,mmm --> HH:MM:SS,mmm` times. Check approved wording and order, evidence-backed extra repeats, positive and readable cue lengths, no overlaps, and bounds within the video. For repeated audio, verify the same text and the actual repeat offset. Timing inferred from ASR remains an estimate, even after these checks.

## Publish and verify

Use the browser product and connection method 젠 specified. In the existing video's subtitle editor, upload the SRT **with timing** and check that timed lines appear before publishing. Publish once and then verify both Studio's manual-language status (`게시됨`) and the public watch page's manual-language option and visible text at sampled positions. Keep an automatically generated language track separate from the manual track. When available, download the published manual SRT and compare its content and times with the validated file; a trailing newline may differ.

If the same error recurs without changed evidence or conditions, stop repeated identical clicks and record the observed result. A different evidence-based method within the user's existing approval may be used. An unresolved error is not publication.

[YouTube's subtitle upload help](https://support.google.com/youtube/answer/2734796?hl=en-CA) describes the timed-file route and does not recommend automatic transcript synchronization for videos over one hour. That guidance does not establish the cause of any particular upload error. [YouTube's supported-file help](https://support.google.com/youtube/answer/2734698?hl=en-CA) lists plain UTF-8 SRT as a supported format.
