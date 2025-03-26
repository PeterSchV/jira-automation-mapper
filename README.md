# JSON-CSV Mapper

## Overview
This script processes a JSON file and a CSV file to update `cloudId` values in the JSON based on `serverId` mappings found in the CSV. Any missing mappings or pre-filled values are logged for reference.

## Directory Structure
```
json_csv_mapper/
│── input/               # Store input files (JSON and CSV)
│   ├── input.json
│   ├── input.csv
│── output/              # Stores the updated JSON file
│── logs/                # Stores log files
│── main.py              # The main Python script
│── README.md            # Documentation
│── requirements.txt     # Dependencies (if any)
```

## Installation
Ensure you have Python 3 installed. Clone or download the repository, then navigate to the project directory.

```sh
cd json_csv_mapper
```

## Usage
1. Place the input JSON and CSV files in the `input/` directory. Make sure they are named `input.json` and `input.csv` respectively.
2. Run the script:

```sh
python main.py
```

3. The updated JSON file will be saved in `output/updated.json`.
4. Logs will be saved in `logs/process.log`.

## Input File Formats

### JSON Format (Example)
```json
{
    "projects": [
        {
            "name": "",
            "serverId": "11111",
            "cloudId": ""
        }
    ]
}
```

### CSV Format (Example)
```
entityType,serverId,cloudId
jira/classic:project,11111,10101
jira/classic:project,22222,20202
```

## Logging
- **Missing `serverId` in CSV** → `WARNING: Record of serverId '<serverId>' could not be found in the provided CSV.`
- **Pre-filled `cloudId`** → `WARNING: Record of serverId '<serverId>' already contains the associated cloudId '<cloudId>'.`

## Dependencies
This script only uses built-in Python libraries (`json`, `csv`, `os`, and `logging`), so no external dependencies are required. You do not need a `requirements.txt` file unless you plan to extend the script with third-party libraries.

## Current Limitations
- **Name field remains unchanged**: The script does not currently look up or populate the `name` field in the JSON based on CSV data.
- **Fixed file paths**: The script expects the JSON and CSV files to be named `input.json` and `input.csv`, respectively, and does not support dynamic file selection.
- **Single-Level Processing**: The script processes only one level of records under a key (e.g., `projects`). If the JSON structure changes significantly, the script may not work correctly.
- **No Data Validation**: The script assumes valid JSON and CSV formats. It does not validate the integrity of the data beyond simple existence checks.


## License
This project is open-source and available for modification and use.

