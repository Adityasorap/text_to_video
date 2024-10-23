import os
import requests
from utility.utils import log_response, LOG_TYPE_PEXEL  # Assuming this import is for logging

# Placeholder for potential Bing API key retrieval (replace with actual implementation)
BING_VIDEO_SEARCH_KEY = os.environ.get('BING_VIDEO_SEARCH_KEY')

def search_videos(query_string, orientation_landscape=True):
    """Searches for videos using the Bing Video Search API (replace with actual API call).

    Args:
        query_string (str): The search query.
        orientation_landscape (bool, optional): Whether to search for landscape videos. Defaults to True.

    Returns:
        dict: The JSON response from the Bing Video Search API (structure may differ).
    """

    # Replace with Bing Video Search API endpoint and parameters (consider using query parameters)
    url = "https://<BING_VIDEO_SEARCH_API_ENDPOINT>"  # Replace with actual Bing Video Search API endpoint
    headers = {
        "Ocp-Apim-Subscription-Key": BING_VIDEO_SEARCH_KEY  # Replace with Bing API key header name
    }
    params = {
        "q": query_string,  # Replace with Bing API query parameter name
        "count": 15  # Consider using an appropriate parameter to limit results (if supported)
    }
    # Additional parameters for orientation, resolution, etc. may be available depending on Bing's API

    response = requests.get(url, headers=headers, params=params)
    json_data = response.json()
    log_response(LOG_TYPE_PEXEL, query_string, response.json())  # Assuming logging functionality

    return json_data


def getBestVideo(query_string, orientation_landscape=True, used_vids=[]):
    """Finds the best video from the search results (adapt based on Bing API response structure).

    Args:
        query_string (str): The search query.
        orientation_landscape (bool, optional): Whether to search for landscape videos. Defaults to True.
        used_vids (list, optional): A list of already used video links to avoid duplicates. Defaults to [].

    Returns:
        str: The URL of the best video, or None if no suitable video is found.
    """

    vids = search_videos(query_string, orientation_landscape)
    videos = vids.get('videos', [])  # Replace with Bing API response structure to extract video data

    # Adapt filtering based on Bing API response structure and video properties
    filtered_videos = []
    for video in videos:
        if orientation_landscape:
            # Check for properties like width, height, or aspect ratio (adapt based on Bing's API)
            if video.get('width', 0) >= 1920 and video.get('height', 0) >= 1080 and video.get('aspect_ratio', 0) == 16/9:
                filtered_videos.append(video)
        else:
            # Check for properties like width, height, or aspect ratio (adapt based on Bing's API)
            if video.get('width', 0) >= 1080 and video.get('height', 0) >= 1920 and video.get('aspect_ratio', 0) == 9/16:
                filtered_videos.append(video)

    # Adapt sorting based on Bing API response structure (if duration is available)
    sorted_videos = sorted(filtered_videos, key=lambda x: abs(15 - int(x.get('duration', 0))), reverse=True)  # Assuming duration is available

    # Adapt extracting video URLs and checking duplicates based on Bing API response structure
    for video in sorted_videos:
        for video_file in video.get('video_files', []):
            if orientation_landscape:
                if video_file.get('width', 0) == 1920 and video_file.get:

def generate_video_url(timed_video_searches, video_server):
    timed_video_urls = []
    if video_server == "bing":  # Replace "pexel" with "bing"
        used_links = []
        for (t1, t2), search_terms in timed_video_searches:
            url = ""
            for query in search_terms:
                url = getBestVideo(query, orientation_landscape=True, used_vids=used_links)  # Replace "getBestVideo" with appropriate Bing function
                if url:
                    used_links.append(url.split('.hd')[0])
                    break
            timed_video_urls.append([[t1, t2], url])
    elif video_server == "stable_diffusion":
        timed_video_urls = get_images_for_video(timed_video_searches)

    return timed_video_urls
