# py-foundations

[![CI](https://github.com/ChideraaN/py-foundations/actions/workflows/ci.yml/badge.svg)](https://github.com/ChideraaN/py-foundations/actions/workflows/ci.yml)

A small Python project that reads a CSV of bag reports, validates every row with [Pydantic](https://docs.pydantic.dev/), and writes two JSON files: the rows that passed and the rows that failed, each with the reason. All data is synthetic.

It is the first project in a larger study plan, and focuses on Python fundamentals: type hints, Pydantic models and validators, testable function design, pytest, linting, type checking and CI.

## What it does

`bag_reports.csv` has 30 rows with these columns:

| Column | Rule |
| --- | --- |
| `report_id` | Required. Whitespace is stripped, and empty or whitespace-only values are rejected. |
| `colour` | Required. Same rule as `report_id`. |
| `bag_form` | Required. Must be `suitcase`, `backpack` or `duffel`. |
| `shell` | Optional. Must be `hard` or `soft`. A blank cell becomes `null`. |
| `brand` | Optional. A blank cell becomes `null`. |
| `weight_kg` | Optional. A blank cell becomes `null`. Otherwise must be a number from 0 to 32 (inclusive). `nan` and non-numeric text are rejected. |

Running the script produces:

- `valid.json`: a single array of the 24 valid reports, with blanks converted to `null` and weights as numbers.
- `rejects.json`: a single array of the 6 rejected rows. Each keeps its original values and adds a `failure_reason` field with the validation message.

Example entry from `valid.json`:

```json
{
  "report_id": "R-1003",
  "colour": "red",
  "bag_form": "backpack",
  "shell": null,
  "brand": "Osprey",
  "weight_kg": 8.2
}
```

The six rejected rows in the sample data are: an empty colour (R-1025), the bag form `banana` (R-1026), a weight of 400 (R-1027), a weight of -3 (R-1028), a weight of `heavy` (R-1029), and a row with no report ID.

## Getting started

You need [uv](https://docs.astral.sh/uv/) and Python 3.10 or newer. The repo pins Python 3.12 in `.python-version`.

```bash
git clone https://github.com/ChideraaN/py-foundations.git
cd py-foundations
uv sync
uv run python main.py
```

The script can be run from any folder. It finds the CSV and writes the JSON files next to `main.py`.

## Development

```bash
uv run pytest                  # run the tests
uv run ruff check .            # lint
uv run ruff format --check .   # check formatting
uv run pyright                 # type check
```

## Project layout

```
main.py                  # read the CSV, validate rows, write the JSON files
bag.py                   # the Bag Pydantic model and its validators
bag_reports.csv          # sample input (30 rows)
valid.json               # output: valid reports
rejects.json             # output: rejected rows with failure_reason
tests/test_bag.py        # unit tests for the Bag model
tests/test_validation.py # tests for reading, validating and writing
tests/test_reports.csv   # small CSV used by the reader test
.github/workflows/ci.yml # CI workflow
```

## Design notes

- **Importable without side effects.** Importing `main` does nothing. The work happens only when the script is run directly, behind `if __name__ == "__main__":`.
- **Functions take input and return output.** `read_csv_to_dict`, `validate_bag_reports_csv` and `write_reports` take their inputs and paths as arguments, so tests can call them with small fake data and write to a temporary folder.
- **Paths are relative to the file**, not to the current working directory.
- **Tests cover the edges.** Boundary weights (0 and 32), blank-to-`null` conversion, each rejection reason, and the full pipeline on the real CSV (24 valid, 6 rejected, and the exact rejected IDs).

## Continuous integration

GitHub Actions runs on every push to `main` and on pull requests. For Python 3.10, 3.12 and 3.13 it installs the locked dependencies with uv, then runs ruff (lint and format check), pyright and pytest.