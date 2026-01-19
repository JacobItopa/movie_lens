import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

class TavilyService:
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            print("Warning: TAVILY_API_KEY not found in environment variables.")
            self.client = None
        else:
            self.client = TavilyClient(api_key=api_key)

    async def find_streaming_links(self, moodie_title: str, year: str) -> list:
        if not self.client:
            return []

        query = f"watch {moodie_title} {year} movie streaming online legal"
        
        try:
            response = self.client.search(
                query=query,
                search_depth="basic",
                include_domains=["netflix.com", "hulu.com", "amazon.com", "disneyplus.com", "hbo.com", "apple.com", "primevideo.com", "peacocktv.com"],
                max_results=5
            )
            
            results = []
            if 'results' in response:
                for res in response['results']:
                    results.append({
                        "title": res.get('title'),
                        "url": res.get('url'),
                        "content": res.get('content')
                    })
            return results

        except Exception as e:
            print(f"Error in TavilyService: {e}")
            return []

tavily_service = TavilyService()
