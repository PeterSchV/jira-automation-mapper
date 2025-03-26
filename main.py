import json
import csv
import os
import logging

def setup_logging():
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        filename="logs/process.log",
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

def load_json(json_path):
    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)

def load_csv(csv_path):
    server_to_cloud = {}
    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            if len(row) >= 3:
                _, server_id, cloud_id = row
                server_to_cloud[server_id] = cloud_id
    return server_to_cloud

def update_json(json_data, server_to_cloud):
    for key, records in json_data.items():
        for record in records:
            server_id = record.get("serverId", "")
            cloud_id = record.get("cloudId", "")
            
            if cloud_id:  # Already has a cloudId
                logging.warning(f"Record of serverId '{server_id}' already contains the associated cloudId '{cloud_id}'.")
            elif server_id in server_to_cloud:
                record["cloudId"] = server_to_cloud[server_id]
            else:
                logging.warning(f"Record of serverId '{server_id}' could not be found in the provided CSV.")
    return json_data

def save_json(json_data, output_path):
    os.makedirs("output", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(json_data, file, indent=4)

def main(json_file, csv_file, output_file):
    setup_logging()
    json_data = load_json(json_file)
    server_to_cloud = load_csv(csv_file)
    updated_json = update_json(json_data, server_to_cloud)
    save_json(updated_json, output_file)

if __name__ == "__main__":
    main("input/input.json", "input/input.csv", "output/updated.json")
