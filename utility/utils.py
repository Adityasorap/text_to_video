import os
from datetime import datetime
import json

# Log types (modify as needed)
LOG_TYPE_GPT = "GPT"
LOG_TYPE_BING = 'bing'  
LOG_TYPE_BING_VIDEO = 'bing_video'


  # Adjust the path as needed
DIRECTORY_LOG_BING = '/path/to/your/logs/bing'    # Add this line with the correct path
DIRECTORY_LOG_GPT = '/path/to/your/logs/gpt'      # Adjust if necessary


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
        if not os.path.exists(DIRECTORY_LOG_BING):
            os.makedirs(DIRECTORY_LOG_BING)
    else:
        # Handle other potential log types
        pass

    # Build filename and filepath
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{log_type}.txt"
    filepath = os.path.join(eval(f"DIRECTORY_LOG_{log_type}"), filename)  # Dynamic directory selection

    # Write log entry to file
    with open(filepath, "w") as outfile:
        outfile.write(json.dumps(log_entry) + '\n')
