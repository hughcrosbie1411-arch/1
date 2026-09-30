# Data dictionary

| Table | Meaning and important fields |
|---|---|
| source_documents | Provider, URL/identifier, publication/ingestion time, SHA-256 and raw reference; immutable provenance target |
| securities | Stable identity, ticker/exchange, geography, sector, currency, valid listing dates |
| events | Permanent UUID, canonical type/subtype, security, event/announcement times, session, source, JSON attributes/flags, superseding ID |
| market_bars | Security/time/interval/adjustment/source identity; positive OHLC and nonnegative volume constraints |
| feature_snapshots | Event, prediction cutoff, dataset/code versions; sealed after forecast |
| feature_values | Feature JSON value, classification, observation/publication/ingestion/effective/available timestamps, provenance and flags |
| model_registry | Algorithm/features/parameters, dataset/code/seed, chronological windows, metrics and artifact identity |
| predictions | Immutable snapshot/model/time/horizon/output and live vs historical label |
| outcomes | Entry/exit time, raw/benchmark/abnormal returns, label method, observed time, dataset and correction link |
| model_promotions | Append-only explicit decision, prior model, evidence and approver |
| research_ledger | Question, dataset/code, method/parameters, result and limitations |

Returns are decimal fractions (0.05 = 5%); UI may format percentages. SQL timestamps are timezone-aware UTC instants; sessions require exchange-local calendars upstream. Unknown values are NULL or explicitly flagged, never zero-filled. `available_at` is the earliest verified time the system could actually use the value and cannot precede ingestion or publication. In retrospective research this conservative rule excludes late-ingested records unless reconstructed from verifiable historical vintages using a distinct, documented workflow. JSON event attributes vary by type; every training feature still needs independently auditable availability.
