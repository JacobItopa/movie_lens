from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.services.gemini import gemini_service
from app.services.tavily import tavily_service
import shutil
import os

app = FastAPI(title="Movie Identifier Agent")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
@app.post("/api/identify")
async def identify_movie(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Read file content
        contents = await file.read()
        
        # 1. Identify with Gemini
        movie_info = await gemini_service.identify_movie(contents, file.content_type)
        
        if not movie_info.get("is_movie"):
            return {
                "success": False,
                "message": "Could not identify a movie in this image.",
                "data": movie_info
            }

        # 2. Find links with Tavily
        links = await tavily_service.find_streaming_links(
            movie_info.get("title"), 
            movie_info.get("year", "")
        )

        return {
            "success": True,
            "data": {
                **movie_info,
                "links": links
            }
        }

    except Exception as e:
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Mount Static Files (Frontend)
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
