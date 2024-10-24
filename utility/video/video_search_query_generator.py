from openai import OpenAI
import os
import json
import re
from utility.utils import log_response, LOG_TYPE_GPT

# Client Initialization
if len(os.environ.get("GROQ_API_KEY", "")) > 30:
    from groq import Groq
    model = "llama3-70b-8192"
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
else:
    model = "gpt-4o"
    OPENAI_API_KEY = os.environ.get('OPENAI_KEY')
    client = OpenAI(api_key=OPENAI_API_KEY)

log_directory = ".logs/gpt_logs"

prompt = """# Instructions

Given the following video script and timed captions, extract three visually concrete and specific keywords for each time segment that can be used to search for background videos...
"""

def fix_json(json_str):
    json_str = json_str.replace("’", "'")
    json_str = json_str.replace("“", "\"").replace("”", "\"").replace("‘", "\"").replace("’", "\"")
    return json_str

def getVideoSearchQueriesTimed(script, captions_timed):
    end = captions_timed[-1][0][1]
    try:
        out = [[[0, 0], ""]]
        while out[-1][0][1] != end:
            content = call_OpenAI(script, captions_timed).replace("'", '"')
            try:
                out = json.loads(content)
            except Exception as e:
                print("Invalid JSON content: \n", content)
                print("Error:", e)
                content = fix_json(content.replace("```json", "").replace("```", ""))
                out = json.loads(content)
        return out
    except Exception as e:
        print("Error in response:", e)
    return None

def call_OpenAI(script, captions_timed):
    user_content = """Script: {}
Timed Captions:{}
""".format(script, "".join(map(str, captions_timed)))
    print("Content", user_content)
    
    response = client.chat.completions.create(
        model=model,
        temperature=1,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_content}
        ]
    )
    
    text = response.choices[0].message.content.strip()
    text = re.sub(r'\s+', ' ', text)
    print("Text", text)
    log_response(LOG_TYPE_GPT, script, text)  # Ensure proper logging
    return text

def merge_empty_intervals(segments):
    if segments is None:
        print("No segments to merge.")
        return []  # Handle None case gracefully

    merged = []
    i = 0
    while i < len(segments):
        interval, url = segments[i]
        if url is None:
            # Find consecutive None intervals
            j = i + 1
            while j < len(segments) and segments[j][1] is None:
                j += 1
            
            # Merge consecutive None intervals with the previous valid URL
            if i > 0:
                prev_interval, prev_url = merged[-1]
                if prev_url is not None and prev_interval[1] == interval[0]:
                    merged[-1] = [[prev_interval[0], segments[j-1][0][1]], prev_url]
                else:
                    merged.append([interval, prev_url])
            else:
                merged.append([interval, None])
            i = j
        else:
            merged.append([interval, url])
            i += 1
    
    return merged

# Example usage (uncomment and modify as needed)
# script = "Your video script here."
# captions_timed = [[0, 5, "Caption 1"], [5, 10, "Caption 2"]]  # Example format
# result = getVideoSearchQueriesTimed(script, captions_timed)
# print(result)
