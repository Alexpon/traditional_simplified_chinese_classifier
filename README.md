# TC/SC Classification

This project provides tools and scripts for classifying and mapping Traditional Chinese (TC) and Simplified Chinese (SC) characters and phrases. It leverages data from sources such as Unihan and OpenCC to build mappings and analyze differences between TC and SC.

## Project Structure

- `analyze_file.py` — Analyze mapping or data files.
- `classify_st.py` — Script for classifying simplified/traditional characters.
- `tcsc_builder.py` — Builds TC/SC mapping sets.
- `compare_mapping_opencc.csv` — CSV file comparing mappings.
- `map/` — Contains mapping results and subsets:
  - `both.txt`, `only_simp.txt`, `only_trad.txt`, `punctuation.txt`
  - `opencc_only/` and `unihan_only/` — Source-specific mappings
- `raw_data/` — Raw data sources:
  - `Unihan.zip` — Unihan database
  - `OpenCC/` — OpenCC dictionary files
- `source_data/` — Source JSON data files

## Usage

1. Place required raw data in the `raw_data/` directory.
2. Use the provided Python scripts to process, classify, and analyze TC/SC data.
3. Generated mappings and results will be available in the `map/` directory.

## Requirements

- Python 3.10+
- No external dependencies required for basic usage (unless specified in scripts)

## License

Specify your license here.

## Author

Add your name or organization here.
