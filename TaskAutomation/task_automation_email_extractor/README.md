# Task Automation with Python Scripts

This project automates a small real-life task:

Extract all email addresses from a `.txt` file and save them to another file.

## Python concepts used

- `re` for finding email patterns
- file handling for reading and writing files
- `argparse` for command-line input
- `pathlib` for working with file paths

## Project files

- `email_extractor.py` - main Python script
- `sample_input.txt` - sample text file for testing
- `output_emails.txt` - generated output file after running the script

## How to run

```bash
python email_extractor.py sample_input.txt output_emails.txt
```

## Example output

```text
support@example.com
sales@example.org
admin@example.com
```
