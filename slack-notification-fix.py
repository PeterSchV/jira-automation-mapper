import json
import logging
from datetime import datetime

def setup_logging():
    log_filename = f"logs/log_slack_fix_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(message)s"
    )
    return log_filename

def fix_slack_webhook(json_file, output_file):
    log_file = setup_logging()
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    fixed_count = 0
    
    def update_slack_actions(obj):
        nonlocal fixed_count
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "type" and value == "slack.notification" and "value" in obj:
                    slack_value = obj["value"]
                    if isinstance(slack_value, dict) and "webhookUrl" in slack_value:
                        webhook = slack_value["webhookUrl"]
                        if isinstance(webhook, dict) and "key" in webhook:
                            fixed_count += 1
                            logging.info(f"Fixing Slack notification action of webhookURL {webhook['key']}")
                            slack_value["webhookUrl"] = webhook["key"]
                update_slack_actions(value)
        elif isinstance(obj, list):
            for item in obj:
                update_slack_actions(item)
    
    update_slack_actions(data)
    
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    
    logging.info(f"Fixed {fixed_count} actions.")
    print(f"Fixing completed. Logs saved to {log_file}")

# Example usage
fix_slack_webhook("fixes/slack-input/slack.json", "fixes/slack-output/slack-fixed.json")
