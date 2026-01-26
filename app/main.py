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

from typing import List

# API Routes
@app.post("/api/identify")
async def identify_movie(images: List[UploadFile] = File(...)):
    if not images:
         raise HTTPException(status_code=400, detail="No images uploaded")

    try:
        # Prepare images for Gemini
        images_payload = []
        for file in images:
            if not file.content_type.startswith("image/"):
                continue # Skip non-images
            
            content = await file.read()
            images_payload.append({
                "data": content,
                "mime_type": file.content_type
            })

        if not images_payload:
            raise HTTPException(status_code=400, detail="No valid images found")
        
        # 1. Identify with Gemini
        movie_info = await gemini_service.identify_movie(images_payload)
        
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
