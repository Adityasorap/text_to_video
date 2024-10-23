from serpapi import GoogleSearch
def generate_video_url(search_terms, VIDEO_SERVER="serpapi"):
  """
  Fetches background video URLs using SerpApi for each search term.

  Args:
      search_terms (list): List of timed search queries with (start_time, end_time, query) tuples.
      VIDEO_SERVER (str, optional): Video search engine (default: "serpapi").

  Returns:
      list: List of timed video URLs (or None if no video found).
  """

  if VIDEO_SERVER != "serpapi":
      raise NotImplementedError(f"Unsupported video server: {VIDEO_SERVER}")

  background_video_urls = []
  for start_time, end_time, query in search_terms:
    # Use SerpApi to search for videos related to the query
    search = GoogleSearch({
      "q": query,
      "tbm": "vid",  # Specify video search
      "api_key": "<5c6d98019f9e9fc8dc61b7a122c643e8952910a85011faec02c8326b8f891f66>"  # Replace with your SerpApi key
    })

    results = search.get_dict()

    # Extract the first video URL from search results
    if results.get("video_results"):
      video_url = results["video_results"][0]["link"]
      background_video_urls.append((start_time, end_time, video_url))
    else:
      background_video_urls.append((start_time, end_time, None))  # No video found

  return background_video_urls
