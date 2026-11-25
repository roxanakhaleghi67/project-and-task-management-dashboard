# Changelog

## Unreleased

### Added
- Input validation for the required columns, with a clear error message.
- Excel and PDF export of the indicators and the task table.
- `examples/` sample data and a project `ROADMAP.md`.

### Fixed
- Crash on the project-only upload path (a `None` value was indexed).
- Removed the deprecated `fillna(method="ffill")` call.

### Changed
- `requirements.txt` now pins versions and includes `reportlab`.
