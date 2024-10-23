import os
import requests
from utility.utils import log_response, LOG_TYPE_BING_VIDEO  # Use the new log type

# Consider using environment variables for Bing Search API key
BING_SEARCH_API_KEY = os.environ.get('BING_SEARCH_API_KEY')

def search_bing_videos(query_string, orientation_landscape=True):
  """
  Searches Bing Videos for the given query string and orientation.

  Args:
      query_string: The text query to search for videos.
      orientation_landscape: Whether to prioritize landscape videos (True) or portrait (False).

  Returns:
      A dictionary containing Bing Video search results or None on error.
  """
  
  # Bing Search API endpoint (replace with your specific endpoint for video search)
  url = "https://api.bing.microsoft.com/v7.0/Videos/Search"
  headers = {
      "Authorization": f"Bearer {BING_SEARCH_API_KEY}",  # Use your Bing Search API key
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
  }
  params = {
      "q": query_string,
      "count": 15,  # Adjust the number of results to retrieve
      "mkt": "en-US",  # Specify search region (optional)
      "offset": 0,  # Offset for pagination (optional)
      "sort": "Relevance"  # Sort by relevance (optional)
  }
  
  if orientation_landscape:
      params["aspect"] = "Wide"  # Request landscape videos (optional)
  else:
      params["aspect"] = "Tall"  # Request portrait videos (optional)

  try:
      response = requests.get(url, headers=headers, params=params)
      response.raise_for_status()  # Raise exception for non-200 status codes
      json_data = response.json()
      log_response(LOG_TYPE_BING_VIDEO, query_string, json_data)  # Log response
      return json_data
  except requests.exceptions.RequestException as e:
      print(f"Error searching Bing Videos: {e}")
      return None  # Indicate error

def get_best_video(query_string, orientation_landscape=True, used_vids=[]):
  """
  Extracts the best video URL from Bing search results.

  This function prioritizes videos with desired resolution (1920x1080 for landscape, 1080x1920 for portrait)
  and avoids returning the same video multiple times.

  Args:
      query_string: The text query to search for videos.
      orientation_landscape: Whether to prioritize landscape videos (True) or portrait (False).
      used_vids: A list of previously used video URLs to avoid duplicates.

  Returns:
      The best video URL based on criteria, or None if not found.
  """
  
  videos_data = search_bing_videos(query_string, orientation_landscape)
  if not videos_data:
      return None  # No results found

  videos = videos_data.get("webPages", {}).get("value", [])
  
  # Filter and sort logic can be adapted based on desired criteria
  filtered_videos = [video for video in videos if video.get("thumbnailUrl")]  # Ensure thumbnail exists
  sorted_videos = sorted(filtered_videos, key=lambda x: abs(15 - int(x.get("duration", 0))), reverse=True)  # Sort by closest duration to 15 seconds (optional)

  for video in sorted_videos:
    thumbnail_url = video.get("thumbnailUrl")
    if not thumbnail_url:
      continue
    video_url = video.get("url")
    if not video_url:
      continue
    
    # Extract resolution information from thumbnail URL (modify if Bing provides resolution data)
    # This part might require further investigation into Bing Video Search API details
    # resolution_str = thumbnail_url.split("/")[-1].split(".")[0]  # Example parsing (replace if needed)
    # width, height = resolution