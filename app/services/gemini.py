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

    async def identify_movie(self, image_data: bytes, mime_type: str = "image/jpeg") -> dict:
        try:
            # Create a Part object consistent with what Gemini expects
            image_part = {
                "mime_type": mime_type,
                "data": image_data
            }

            prompt = """
            Analyze this image and determine if it is a screenshot from a movie or TV show.
            If it is:
            1. Identify the Movie/Show Title.
            2. Estimate the Release Year.
            3. Provide a brief 1-sentence plot summary relevant to the scene if possible, or the movie in general.
            4. Give a confidence score (0.0 to 1.0).

            If it is NOT a movie/show (e.g., a desktop screenshot, personal photo, random object), set 'is_movie' to false.

            Return the result as a raw JSON object with the following structure:
            {
                "title": "Movie Title",
                "year": "YYYY",
                "summary": "Plot summary...",
                "confidence": 0.95,
                "is_movie": true
            }
            """

            response = self.model.generate_content(
                [prompt, image_part],
                generation_config={"response_mime_type": "application/json"}
            )
            
            print(f"Gemini Raw Response: {response.text}") # Debug log

            result = json.loads(response.text)
            return result

        except Exception as e:
            print(f"Error in GeminiService: {e}")
            return {"error": str(e), "is_movie": False}

gemini_service = GeminiService()
