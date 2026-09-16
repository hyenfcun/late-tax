# Week 3 — Midnight Finding Robustness Check

## Question

Is the elevated Yellow-N midnight reliability risk driven only by the frequently observed 24:08 scheduled departure?

## Segment Comparison

| Segment | Trips | Avg Arrival Delay | Median Arrival Delay | Avg Departure Delay | Avg Travel Delta | >=5 min Late |
|---|---:|---:|---:|---:|---:|---:|
| Yellow-N 24:08 | 250 | 4.26 | 3.90 | 3.02 | 1.24 | 30.4% |
| Yellow-N other midnight | 48 | 4.01 | 3.13 | 3.55 | 0.46 | 22.9% |
| Yellow-N non-midnight | 349 | 1.28 | 1.48 | 0.80 | 0.48 | 0.6% |
| All trips except Yellow-N 24:08 | 1,563 | 1.39 | 1.12 | 1.24 | 0.15 | 2.9% |

## Result

- The 24:08 departure is the largest component of the target segment and shows elevated reliability risk.
- However, the other Yellow-N midnight departures also show a 22.9% rate of lateness of at least five minutes.
- Yellow-N non-midnight trips show only a 0.6% rate of lateness of at least five minutes.
- Therefore, the observed pattern is not solely an artifact of the 24:08 scheduled departure.

## Interpretation

The evidence supports describing the finding as an elevated reliability pattern among observed Yellow-N trips scheduled shortly after midnight, rather than attributing the pattern to Yellow-N service generally or to the 24:08 departure alone.

## Guardrails

- This is a descriptive robustness check, not a causal test.
- The other-midnight comparison contains fewer observations than the 24:08 group, so its estimates should be interpreted with greater uncertainty.
