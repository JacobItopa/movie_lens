import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import typing_extensions

load_dotenv()

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("Warning: GOOGLE_API_KEY not found in environment variables.")
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')

    class MovieInfo(typing_extensions.TypedDict):
        title: str
        year: str
        summary: str
        confidence: float
        is_movie: bool

    async def identify_movie(self, images: list[dict]) -> dict:
        try:
            # Create a list of Part objects
            parts = []
            
            prompt = """
            Analyze these images and determine if they are screenshots from the same movie or TV show.
            They are likely different scenes or frames from a single title.
            
            1. Identify the Movie/Show Title.
            2. Estimate the Release Year.
            3. Provide a brief 1-sentence plot summary.
            4. Give a confidence score (0.0 to 1.0).

            If they are NOT from a movie/show (e.g., desktop screenshots, personal photos), set 'is_movie' to false.

            Return the result as a raw JSON object with the following structure:
            {
                "title": "Movie Title",
                "year": "YYYY",
                "summary": "Plot summary...",
                "confidence": 0.95,
                "is_movie": true
            }
            """
            parts.append(prompt)

            for img in images:
                parts.append({
                    "mime_type": img["mime_type"],
                    "data": img["data"]
                })

            response = self.model.generate_content(
                parts,
                generation_config={"response_mime_type": "application/json"}
            )
            
            print(f"Gemini Raw Response: {response.text}") # Debug log

            result = json.loads(response.text)
            return result

        except Exception as e:
            print(f"Error in GeminiService: {e}")
            return {"error": str(e), "is_movie": False}

gemini_service = GeminiService()
