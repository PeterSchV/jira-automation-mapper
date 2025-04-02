import json
import csv
import os
import logging
from datetime import datetime

def setup_logging():
    os.makedirs("logs", exist_ok=True)
    log_filename = f"logs/log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    logging.basicConfig(
        filename=log_filename,
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

def load_json(json_path):
    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)

def load_csv(csv_path):
    csv_data = {}
    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            csv_data[row["serverId"]] = {
                "cloudId": row["cloudId"],
                "name": row.get("name", None),
            }
    return csv_data

def update_json(json_data, csv_data):
    for key, records in json_data.items():
        for record in records:
            server_id = record.get("serverId", "")
            
            # Handle custom fields specifically
            if server_id.startswith("customfield_"):
                numeric_id = server_id.replace("customfield_", "")
            else:
                numeric_id = server_id
            
            if numeric_id in csv_data:
                cloud_id = csv_data[numeric_id]["cloudId"]
                
                # Maintain customfield formatting
                if server_id.startswith("customfield_"):
                    record["cloudId"] = f"customfield_{cloud_id}"
                else:
                    record["cloudId"] = cloud_id
                
                # Populate name if available
                if "name" in csv_data[numeric_id] and csv_data[numeric_id]["name"]:
                    record["name"] = csv_data[numeric_id]["name"]
            
            elif record.get("cloudId"):
                logging.warning(f"Record of serverId '{server_id}' already contains the associated cloudId '{record['cloudId']}'.")
            else:
                logging.warning(f"Record of serverId '{server_id}' could not be found in the provided CSV.")

def save_json(json_data, output_path):
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_file = f"output/updated_{timestamp}.json"
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(json_data, file, indent=4)
    print(f"Updated JSON saved to {output_file}")

def main(json_file, csv_file):
    setup_logging()
    json_data = load_json(json_file)
    csv_data = load_csv(csv_file)
    update_json(json_data, csv_data)
    save_json(json_data, "output/updated.json")

if __name__ == "__main__":
    main("input/input.json", "input/input.csv")
