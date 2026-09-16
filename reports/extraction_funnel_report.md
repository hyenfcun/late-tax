# Week 2 — Extraction Funnel Audit

This report identifies where historical observations are lost between the raw 511 source and the final Daly City → Powell analytical dataset.

| Month | Scheduled Trip IDs | BART Obs Rows | BART Dates | Valid Trip Rows | Valid Dates | Origin Rows | Destination Rows | Matched Rows | Matched Dates |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2025-06 | 1364 | 63200 | 30 | 10517 | 30 | 130 | 145 | 102 | 23 |
| 2025-07 | 3249 | 67485 | 31 | 10079 | 31 | 76 | 115 | 72 | 26 |
| 2025-08 | 1886 | 78778 | 31 | 22457 | 31 | 432 | 765 | 421 | 30 |
| 2025-09 | 620 | 90205 | 30 | 35387 | 30 | 485 | 1456 | 464 | 30 |
| 2025-10 | 1066 | 81191 | 31 | 25383 | 30 | 291 | 939 | 270 | 30 |
| 2025-11 | 1547 | 64715 | 30 | 10495 | 29 | 154 | 193 | 130 | 29 |
| 2025-12 | 2161 | 66625 | 31 | 10621 | 30 | 135 | 163 | 94 | 30 |
| 2026-01 | 2420 | 67905 | 31 | 10807 | 31 | 126 | 169 | 100 | 31 |
| 2026-02 | 1240 | 62080 | 28 | 10423 | 28 | 135 | 160 | 95 | 27 |
| 2026-03 | 1240 | 67904 | 31 | 11031 | 31 | 142 | 165 | 98 | 30 |
| 2026-04 | 1400 | 65974 | 30 | 10407 | 30 | 108 | 153 | 87 | 30 |
| 2026-05 | 2273 | 67486 | 31 | 11055 | 31 | 141 | 177 | 112 | 30 |
| 2026-06 | 1974 | 67955 | 30 | 10694 | 30 | 166 | 173 | 124 | 29 |
| 2026-07 | 3106 | 70542 | 31 | 11054 | 31 | 174 | 178 | 123 | 30 |
| 2026-08 | 4617 | 69448 | 31 | 11127 | 31 | 177 | 184 | 135 | 30 |

## Diagnostic Logic

- If BART Dates are already low, the historical observation source itself is sparse.
- If BART Dates are high but Valid Dates drop sharply, the scheduled-trip matching logic is the bottleneck.
- If Valid Dates remain high but Matched Dates drop sharply, the Daly City/Powell origin-destination merge requires review.