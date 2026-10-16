"""Multi-seed replication of paper 07's misalignment study (read-only use of the
product package; writes only to the job tmp dir)."""
import json, sys
import numpy as np
sys.path.insert(0, "../products/amodal-counting/src")  # adjust to the amodal-counting checkout
from amodal.calibrate import fit_detectability, fit_interval_scale, inference_aligned_pairs, labeled_pairs_from_scenes
from amodal.estimator import corrected_count
from amodal.synth import generate_scenes
from amodal.visibility import estimate_visibilities

def mae(scenes, curve):
    e = []
    for s in scenes:
        est = estimate_visibilities([d.box for d in s.detections], s.occluders, s.image_size)
        e.append(abs(corrected_count(est, curve).estimate - s.true_count))
    return float(np.mean(e)), e

rows = []
for crowding in (0.3, 0.6, 0.8):
    for seed in range(10):
        tr = generate_scenes(60, seed=seed + 1, crowding=crowding)
        ev = generate_scenes(40, seed=seed + 2, crowding=crowding)
        naive = float(np.mean([abs(s.detected_count - s.true_count) for s in ev]))
        t = fit_interval_scale(tr, fit_detectability(*labeled_pairs_from_scenes(tr)))
        a = fit_interval_scale(tr, fit_detectability(*inference_aligned_pairs(tr)))
        tm, _ = mae(ev, t); am, _ = mae(ev, a)
        rows.append(dict(crowding=crowding, seed=seed, naive=naive, truth=tm, aligned=am))
        print(crowding, seed, round(naive, 3), round(tm, 3), round(am, 3), flush=True)
json.dump(rows, open(sys.argv[1] if len(sys.argv) > 1 else "align_multiseed.json", "w"), indent=1)
for c in (0.3, 0.6, 0.8):
    r = [x for x in rows if x["crowding"] == c]
    n = np.mean([x["naive"] for x in r]); t = np.mean([x["truth"] for x in r]); a = np.mean([x["aligned"] for x in r])
    print(f"crowding {c}: mean naive {n:.3f} truth {t:.3f} aligned {a:.3f} | truth>naive in {sum(x['truth']>x['naive'] for x in r)}/10 | aligned<truth in {sum(x['aligned']<x['truth'] for x in r)}/10 | aligned<naive in {sum(x['aligned']<x['naive'] for x in r)}/10")
