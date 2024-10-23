import os
from datetime import datetime
import json

# Log types (modify as needed)
LOG_TYPE_GPT = "GPT"
LOG_TYPE_BING_VIDEO = "BING_VIDEO"  # New log type for Bing Video

# Log directory paths
DIRECTORY_LOG_GPT = ".logs/gpt_logs"
DIRECTORY_LOG_BING_VIDEO = ".logs/bing_video_logs"  # New directory

# Method to log response
def log_response(log_type, query, response):
    log_entry = {
        "query": query,
        "response": response,
        "timestamp": datetime.now().isoformat()
    }

    # Create directory if it doesn't exist
    if log_type == LOG_TYPE_GPT:
        if not os.path.exists(DIRECTORY_LOG_GPT):
            os.makedirs(DIRECTORY_LOG_GPT)
    elif log_type == LOG_TYPE_BING_VIDEO:
        if not os.path.exists(DIRECTORY_LOG_BING_VIDEO):
            os.makedirs(DIRECTORY_LOG_BING_VIDEO)
    else:
        # Handle other potential log types
        pass

    # Build filename and filepath
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{log_type}.txt"
    filepath = os.path.join(eval(f"DIRECTORY_LOG_{log_type}"), filename)  # Dynamic directory selection

    # Write log entry to file
    with open(filepath, "w") as outfile:
        outfile.write(json.dumps(log_entry) + '\n')