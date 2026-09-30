# Event taxonomy

| Canonical type | Subtypes | Key interpretation |
|---|---|---|
| earnings_guidance | results, outlook increase/reduction, trading update | Actual vs timestamped consensus; guidance midpoint and margin revisions |
| government_contracts | funded award, ceiling, framework, extension, initial order | Obligated value differs from maximum potential value |
| drug_trials_approvals | phases I–III, interim/topline, approval, CRL, AdCom, label | Clinical effect and safety differ from statistical significance |
| ipos | filing, range change, pricing, first trade, lock-up | Offer-to-market return differs from executable secondary-market return |
| uk_announcements | profit warning, placing, takeover, director dealing, dividends, leadership, operations | AIM/liquidity, dilution and exact release time matter |
| economic_releases | CPI/PCE, payrolls, GDP, PMI, rates, guidance | Surprise and revised prior differ from headline level |

One permanent event ID identifies one release occurrence. Overlapping classifications may be attributes; avoid duplicating the same economic release in training. Each engine requires its own extraction rules, feature schema, eligibility and validation. Only daily exploratory market-response calculations are currently executable; the taxonomy does not imply six trained engines.
