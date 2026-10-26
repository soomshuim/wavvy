#!/usr/bin/env python3
"""Limited paired pulse audit; preserve aliases rather than force target BPM."""
import importlib.util,json
from pathlib import Path
import numpy as np
from scipy import signal
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('integrated160',P/'render-160.py');R=importlib.util.module_from_spec(s);s.loader.exec_module(R)

def fft_peaks(env):
    e=env-np.mean(env);n=2**int(np.ceil(np.log2(len(e)*8)))
    spec=abs(np.fft.rfft(e*np.hanning(len(e)),n=n))**2;freq=np.fft.rfftfreq(n,1/500)
    ids,_=signal.find_peaks(spec);ids=ids[(freq[ids]>=50/60)&(freq[ids]<=220/60)]
    ids=sorted(ids,key=lambda k:spec[k],reverse=True)[:8]
    return [{'bpm':float(freq[k]*60),'relative_power':float(spec[k]/max(np.max(spec),1e-30))} for k in ids]

rows=[]
for order in [1,4,11,16,20]:
    folder=R.W/'checks'/f'body-{order:02d}';sources={}
    for label,name in [('source_170','170.wav'),('output_160','160.wav')]:
        p=folder/name;env=R.B.R.MEASURE.envelopes(p)
        sources[label]={'path':R.relative(p),'sha256':R.sha(p),'attack_autocorrelation':R.pulse(p),
                        'broad_attack_fft_peaks_50_to220_bpm':{b:fft_peaks(env[b]) for b in ['mid','high']}}
    rows.append({'order':order,'paired_evidence':sources})
result={'schema':'wavvy.integrated_160_pulse_family_audit.v1','pairs':rows,
        'source_frequency_to_output_multiplier':16/17,'direct_listening':False,
        'interpretation':'Raw AC/FFT estimates retain subdivisions, harmonics and mixed patterns. No estimate is forced to160. Paired attack timing and exact duration separately test the uniform map.',
        'limitation':'Short-window pulse dominance can differ by band and window edge; full/half meter remains inherited.'}
R.save(P/'pulse-family-audit.json',result)
print(json.dumps([{'order':r['order'],'source_ac':r['paired_evidence']['source_170']['attack_autocorrelation']['mid_high_bpm_median'],
  'output_ac':r['paired_evidence']['output_160']['attack_autocorrelation']['mid_high_bpm_median'],
  'source_high_fft_top3':r['paired_evidence']['source_170']['broad_attack_fft_peaks_50_to220_bpm']['high'][:3],
  'output_high_fft_top3':r['paired_evidence']['output_160']['broad_attack_fft_peaks_50_to220_bpm']['high'][:3]} for r in rows]))
