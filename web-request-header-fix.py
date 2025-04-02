import json
import logging
from datetime import datetime

def setup_logging():
    log_filename = f"logs/log_headers_fix_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(message)s"
    )
    return log_filename

def fix_headers(json_file, output_file):
    log_file = setup_logging()
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    fixed_count = 0
    
    def update_headers(obj):
        nonlocal fixed_count
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "headers" and isinstance(value, list):
                    for header in value:
                        if isinstance(header, dict) and "value" in header and isinstance(header["value"], dict):
                            if "keyOrValue" in header["value"]:
                                header["value"] = header["value"]["keyOrValue"]
                            if "secret" in header["value"]:
                                header["headerSecure"] = header["value"].pop("secret")
                            else:
                                header["headerSecure"] = False  # Default to False if missing
                            
                            logging.info(f"Fixing header of ID {header.get('id', 'Unknown')}")
                            fixed_count += 1
                update_headers(value)
        elif isinstance(obj, list):
            for item in obj:
                update_headers(item)
    
    update_headers(data)
    
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    
    logging.info(f"Fixed {fixed_count} headers.")
    print(f"Fixing completed. Logs saved to {log_file}")


# Example usage
fix_headers("fixes/webhook-input/headers.json", "fixes/webhook-output/headers-fixed.json")
