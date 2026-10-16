# A4 paper-evidence pack

CPU analysis of committed caches plus the real G1-03 score hashes.
Historical B5 rows stay leaked / diagnostic. `results.json` is written by:

```
python scripts/analyze_cached_rows.py --seed 0 --output paper_evidence/results.json
```

Inputs (hashed into the JSON):

- `evidence/a4_realdata/rows_two_sided.json`
- `evidence/a4_realdata/gt_subset.json`
- `evidence/a4_realdata/detections_raw_conf.json`

`g1_03` now cites `evaluation_result_v1.json` SHA-256
`2ee47322225175fe2b30f981a2a0ac90870ac91a10fe046d48395f26fad63605`.
Do not promote 11.026 as a leak-free headline.
