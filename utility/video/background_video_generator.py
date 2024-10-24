import os
import requests
from utility.utils import log_response, LOG_TYPE_BING

BING_API_KEY = os.environ.get('BING_KEY')

def search_videos(query_string):
    url = "https://api.bing.microsoft.com/v7.0/videos/search"
    headers = {
        "Ocp-Apim-Subscription-Key": BING_API_KEY,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    params = {
        "q": query_string,
        "count": 15,
        "mkt": "en-US"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return {}

    json_data = response.json()
    log_response(LOG_TYPE_BING, query_string, json_data)

    return json_data

def getBestVideo(query_string, orientation_landscape=True, used_vids=[]):
    vids = search_videos(query_string)
    videos = vids.get('value', [])
    
    print(f"Videos found for query '{query_string}': {videos}")  # Debugging

    if not videos:
        print("No videos found.")
        return None

    # Filter based on orientation with relaxed conditions
    filtered_videos = [
        video for video in videos
        if ((orientation_landscape and video.get('width', 0) >= 1280 and video.get('height', 0) >= 720) or
            (not orientation_landscape and video.get('width', 0) >= 720 and video.get('height', 0) >= 1280))
    ]

    if not filtered_videos:
        print("No videos meet the filtering criteria.")
        return None

    # Sort the filtered videos by duration if available
    sorted_videos = sorted(filtered_videos, key=lambda x: abs(15 - x.get('duration', 0)))

    # Extract the top video URL
    for video in sorted_videos:
        video_link = video.get('contentUrl')
        if video_link and not (video_link.split('.hd')[0] in used_vids):
            return video_link

    print("No valid video links found after sorting.")
    return None

def generate_video_url(timed_video_searches,video_server):
        timed_video_urls = []
        if video_server == "bing":
            used_links = []
            for (t1, t2), search_terms in timed_video_searches:
                url = ""
                for query in search_terms:
                  
                    url = getBestVideo(query, orientation_landscape=True, used_vids=used_links)
                    if url:
                        used_links.append(url.split('.hd')[0])
                        break
                timed_video_urls.append([[t1, t2], url])
        elif video_server == "stable_diffusion":
            timed_video_urls = get_images_for_video(timed_video_searches)

        return timed_video_urls
