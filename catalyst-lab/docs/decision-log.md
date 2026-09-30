# Decision log

| Decision | Alternatives | Reason | Risk / revisit condition |
|---|---|---|---|
| Offline snapshots first | Live paid pipelines | Genuine Longbridge data is available; avoids unsupported services | Staleness; revisit when scheduled/licensed access is configured |
| NKE vs SPY daily exploration | All sectors and intraday | Available captured data provides a reproducible working path | Selection/benchmark bias; expand to verified panel |
| No trained probabilities | Fit on unverified events/current consensus | Historical event timing and consensus missing | Limited utility; revisit after point-in-time dataset passes QA |
| Six explicit taxonomy engines | Universal black-box | Economic mechanisms differ | More data work; implement independently with shared infrastructure |
| PostgreSQL append-only audit contract | One giant JSON record | Provenance and feature cutoff are independently enforceable | Migration remains untested; validate before provisioning |
| Chronological research core | Random train/test split | Reduce temporal leakage | Issuer dependence remains; require clustered evaluation |
| No autonomous promotion/trading | Automated orders and retraining promotion | Research evidence is insufficient and task excludes execution | Revisit model promotion only with held-out evidence, never trade execution |
| Local reproducible delivery | Claim deployment | Vercel capabilities/account absent in inspection | No hosted URL; revisit once deployment access exists |

Dated 2026-09-30. Decisions describe the implemented foundation and explicit next-stage boundaries.
