# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Document output type is now accessible to executable Python code in the
  document via the global variable document_output_format.
  [#19](https://github.com/gbingersoll/sciengdox/issues/19)
- Allow incorporating interactive Plotly plots in HTML output and the SVG
  version of the same in PDF output.
  [#10](https://github.com/gbingersoll/sciengdox/issues/10)

### Fixed
- PythonRunner now uses the same python executable as is used to run the pandoc
  filter.  This fixes an issue when running in a venv and necessary packages for
  your doc aren't installed globally.
  [#18](https://github.com/gbingersoll/sciengdox/issues/18)

## [0.7.0] - 2020-12-09
### Changed
- Updated citeproc handling for pandoc >=2.11.  Default is now to use the
  `--citeproc` flag on the `pandoc` command line internally.
- Various changes in example template for pandoc >=2.11.

### Fixed
- matplotlib is no longer required to build.  The example still uses it, but
  you don't have to have it to do a basic document build anymore.
  [#16](https://github.com/gbingersoll/sciengdox/issues/16)

## [0.6.3] - 2020-05-27
### Fixed
- Blank lines in code listings are no longer dropped in HTML output.
  [#14](https://github.com/gbingersoll/sciengdox/issues/14)

## [0.6.2] - 2020-05-27
### Fixed
- Moved `colorama` library to `install_requires` in `setup.py`.

## [0.6.1] - 2020-05-27
### Fixed
- Added `MANIFEST.in` to make sure `sciengdox/units/unit_defs.txt`, providing
  custom pint units definitions, is included in the output package.

## [0.6.0] - 2020-05-27
Initial public release

[Unreleased]: https://github.com/gbingersoll/sciengdox/compare/v0.7.0...HEAD
[0.7.0]: https://github.com/gbingersoll/sciengdox/compare/v0.6.3...v0.7.0
[0.6.3]: https://github.com/gbingersoll/sciengdox/compare/v0.6.2...v0.6.3
[0.6.2]: https://github.com/gbingersoll/sciengdox/compare/v0.6.1...v0.6.2
[0.6.1]: https://github.com/gbingersoll/sciengdox/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/gbingersoll/sciengdox/releases/tag/v0.6.0
