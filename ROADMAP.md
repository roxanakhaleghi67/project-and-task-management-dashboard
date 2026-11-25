# Roadmap

Priorities for the Project Performance Dashboard, in order.

| # | Item | Effort | Done when |
| --- | --- | --- | --- |
| 1 | Input validation for the project file | Small | A file with missing columns shows a clear message and the app stops instead of raising `KeyError`. **Done.** |
| 2 | Fix the project-only upload path | Small | Uploading only the project file renders the indicators and builds a synthetic S-curve without crashing. **Done.** |
| 3 | Export the report | Medium | The user can download the indicators and the task table as Excel and a one-page PDF. **Done.** |
| 4 | Tests for the core calculations | Medium | `pytest` covers SPI, CPI, SV, CV, EAC and VAC against `examples/project_sample.csv`. |
| 5 | Explicit budget definitions | Small | BAC and the reporting-date assumptions are configurable and documented in the UI. |
| 6 | Hosted demo | Large | A Streamlit Community Cloud (or similar) deployment is linked from the README. |
| 7 | English interface option | Medium | A language switch renders the labels in English as well as Persian. |

## Known limitations

- The UI is Persian only.
- Multi-series daily aggregation is not implemented; the S-curve reads one project-level series.
- `BAC` is currently derived from total `PV`.
- No automated tests or CI yet.