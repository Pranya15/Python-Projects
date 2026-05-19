import argparse
import re
from pathlib import Path


EMAIL_PATTERN = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")


def extract_emails(input_path: Path) -> list[str]:
    text = input_path.read_text(encoding="utf-8")
    matches = EMAIL_PATTERN.findall(text)

    # Preserve order while removing duplicates.
    unique_emails = list(dict.fromkeys(matches))
    return unique_emails


def save_emails(output_path: Path, emails: list[str]) -> None:
    output_path.write_text("\n".join(emails), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract email addresses from a text file and save them to another file."
    )
    parser.add_argument("input_file", help="Path to the input .txt file")
    parser.add_argument("output_file", help="Path to the output file")
    args = parser.parse_args()

    input_path = Path(args.input_file)
    output_path = Path(args.output_file)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    emails = extract_emails(input_path)
    save_emails(output_path, emails)

    print(f"Found {len(emails)} unique email(s).")
    print(f"Saved output to: {output_path}")


if __name__ == "__main__":
    main()
