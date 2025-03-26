import json
import csv
import os
import logging
from datetime import datetime

# Function to get a timestamp for unique filenames
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Setup paths with timestamp
def get_output_file_name():
    timestamp = get_timestamp()
    return f"output/updated_{timestamp}.json"

def get_log_file_name():
    timestamp = get_timestamp()
    return f"logs/process_{timestamp}.log"

# Load the JSON file
def load_json(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"File {json_path} not found.")
        raise

# Load the CSV file
def load_csv(csv_path):
    csv_data = {}
    try:
        with open(csv_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['serverId']:
                    csv_data[row['serverId']] = row['cloudId']
        return csv_data
    except FileNotFoundError:
        logging.error(f"File {csv_path} not found.")
        raise

# Process the JSON data
def process_json(json_data, csv_data):
    updated_json = {}
    for key, value in json_data.items():
        updated_value = []
        for record in value:
            server_id = record.get("serverId")
            cloud_id = record.get("cloudId")
            
            if cloud_id:  # Skip if already filled
                logging.warning(f"WARNING: Record of serverId '{server_id}' already contains the associated cloudId '{cloud_id}'.")
                updated_value.append(record)
            elif server_id and server_id in csv_data:  # Look up serverId in CSV
                record["cloudId"] = csv_data[server_id]
                updated_value.append(record)
                logging.info(f"CloudId for serverId '{server_id}' filled from CSV.")
            else:
                updated_value.append(record)
                logging.warning(f"WARNING: Record of serverId '{server_id}' could not be found in the provided CSV.")
        updated_json[key] = updated_value
    return updated_json

# Save the updated JSON data to a new file
def save_json(data, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    logging.info(f"Updated JSON saved to {output_file}")

# Log the process
def log_process(updated_json):
    logging.info("Process completed successfully.")
    # Additional logging could be added based on conditions in the future

# Main function
def main(json_file, csv_file, output_file):
    json_data = load_json(json_file)
    csv_data = load_csv(csv_file)
    updated_json = process_json(json_data, csv_data)
    save_json(updated_json, output_file)
    log_process(updated_json)

if __name__ == "__main__":
    json_file = "input/input.json"
    csv_file = "input/input.csv"
    output_file = get_output_file_name()  # Dynamic output file with timestamp
    log_file = get_log_file_name()  # Dynamic log file with timestamp
    
    # Configure logging
    logging.basicConfig(filename=log_file, level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

    main(json_file, csv_file, output_file)
