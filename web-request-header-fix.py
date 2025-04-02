import json

def fix_headers(json_file, output_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    def update_headers(obj):
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
                update_headers(value)
        elif isinstance(obj, list):
            for item in obj:
                update_headers(item)
    
    update_headers(data)
    
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# Example usage
fix_headers("fixes/input/headers.json", "fixes/output/headers.json")