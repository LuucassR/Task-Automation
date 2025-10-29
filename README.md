# Task-Automation
name: "Task Automation - Python CSV Reports"
description: |
  This project automates the generation of sales reports from CSV files. It allows you to:
    - Read a CSV containing employees, their departments, and sales.
    - Add new records via CLI or interactively.
    - Generate summaries per department, including a ranking of top sellers.
    - Export a CSV report with complete statistics.

usage:
  interactive: |
    Run the script without arguments (interactive mode):
    ```bash
    python generate_report.py
    ```
    - The script will ask if you want to add a new record.
    - If you choose 'yes', it will prompt for name, department, and sales.
    - After that, it will display the summary and automatically generate a CSV report.

  cli_arguments: |
    Run the script with CLI arguments:
    ```bash
    python generate_report.py <name> <department> <sales>
    ```
    Example:
    ```bash
    python generate_report.py John Sales 1300
    ```
    - Adds the record directly to the CSV.
    - Then displays the summary and generates a report.

notes: |
  - sales must be a positive integer.
  - Reports are saved in data/reports/ with timestamped filenames.
  - If input_data.csv does not exist, it will be created automatically with example data.

testing: |
  A basic test script is included in test_generate_report.py to validate that:
    - The CSV can be read.
    - A new record can be added.
    - Summaries are generated correctly.

  To run the test:
  ```bash
  python test_generate_report.py
