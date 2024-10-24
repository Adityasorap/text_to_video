def getVideoSearchQueriesTimed(script, captions_timed):
    end = captions_timed[-1][0][1]
    out = [[[0, 0], ""]]
    
    try:
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
    user_content = f"Script: {script}\nTimed Captions: {''.join(map(str, captions_timed))}"
    
    print("User Content:", user_content)
    
    try:
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
        print("Response Text:", text)
        log_response(LOG_TYPE_GPT, script, text)
        return text
    except Exception as e:
        print("Error calling OpenAI:", e)
        return ""
        
def merge_empty_intervals(segments):
    if segments is None:
        return []  # Handle None case
    
    merged = []
    i = 0
    while i < len(segments):
        interval, url = segments[i]
        if url is None:
            # Find consecutive None intervals
            j = i + 1
            while j < len(segments) and segments[j][1] is None:
                j += 1
            
            if i > 0:
                prev_interval, prev_url = merged[-1]
                if prev_url is not None and prev_interval[1] == interval[0]:
                    merged[-1] = [[prev_interval[0], segments[j - 1][0][1]], prev_url]
                else:
                    merged.append([interval, prev_url])
            else:
                merged.append([interval, None])
            i = j
        else:
            merged.append([interval, url])
            i += 1
    
    return merged
