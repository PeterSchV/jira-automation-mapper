import json

def split_jira_rules(input_file, enabled_output, disabled_output):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if not isinstance(data, dict) or 'rules' not in data:
        raise ValueError("Invalid JSON structure. Expected a dictionary with a 'rules' key.")
    
    rules = data['rules']
    
    enabled_rules = [rule for rule in rules if rule.get('state') == 'ENABLED']
    disabled_rules = [rule for rule in rules if rule.get('state') == 'DISABLED']
    
    enabled_data = {**data, 'rules': enabled_rules}
    disabled_data = {**data, 'rules': disabled_rules}
    
    with open(enabled_output, 'w', encoding='utf-8') as file:
        json.dump(enabled_data, file, indent=4)
    
    with open(disabled_output, 'w', encoding='utf-8') as file:
        json.dump(disabled_data, file, indent=4)
    
    print(f"Split completed: {len(enabled_rules)} enabled rules, {len(disabled_rules)} disabled rules.")

# Example usage
split_jira_rules('fixed20250401.json', 'separator-output/enabled_rules.json', 'separator-output/disabled_rules.json')
