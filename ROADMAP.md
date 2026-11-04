# Dashboard development plan

## Execution and input handling

- [ ] Fix the project-only path: it currently indexes `df_daily` when it is `None`.
- [ ] Validate required columns before calculations; show missing column names in the UI.
- [ ] Report invalid numeric cells, empty files, and invalid dates without an unhandled exception.
- [ ] Handle an empty or single-date daily dataset before creating the date slider.
- [ ] Define whether daily inputs are incremental or cumulative; use one documented convention.
- [ ] Decide how multiple activity series are aggregated by reporting date.

## Calculation correctness

- [ ] Separate PV at the reporting date from the full budget at completion (BAC).
- [ ] Define progress independently from SPI when using partial project snapshots.
- [ ] Extract calculation functions from the UI.
- [ ] Check zero PV, zero AC, missing values, and the supplied sample arithmetic.
- [ ] Make unavailable metrics display as unavailable instead of as successful results.

## Portfolio readiness

- [ ] Run the documented commands from a new environment and record the Python/dependency versions.
- [ ] Verify no input, project only, both inputs, and malformed input flows.
- [ ] Add two screenshots from the actual running application.
- [ ] Publish a demo with synthetic data and add its real URL to the repository About field.
- [ ] Implement and verify Docker if it remains part of the project.

Ready to feature when another person can follow the README, use the sample inputs, and explain the displayed indicators without additional setup help.
