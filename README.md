# 🎬 MovieLens - Movie Identifier Agent

**MovieLens** is an intelligent AI agent that identifies movies from screenshots and finds you the best places to watch them. Built with **Google Gemini 1.5 Flash** for vision analysis and **Tavily API** for real-time search.

![MovieLens Demo](https://placehold.co/600x400/101010/6366f1?text=MovieLens+Preview)

## ✨ Features

- **📸 Instant Identification**: Drag & drop any focused movie screenshot.
- **🧠 AI-Powered**: Uses Gemini's advanced vision capabilities to recognize scenes, actors, and context.
- **📺 Streaming Links**: Automatically searches for legal streaming options (Netflix, Hulu, Prime, etc.).
- **💎 Premium Design**: A sleek, dark-mode interface with glassmorphism effects and smooth animations.

## 🛠️ Tech Stack

- **Backend**: Python (FastAPI)
- **AI Model**: Google Gemini 1.5 Flash
- **Search**: Tavily Search API
- **Frontend**: Vanilla HTML/CSS/JS (No complex build steps!)

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A [Google Gemini API Key](https://aistudio.google.com/)
- A [Tavily API Key](https://tavily.com/)

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/JacobItopa/movie_lens.git
    cd movie_lens
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**
    Create a `.env` file in the root directory:
    ```bash
    cp .env.example .env
    ```
    Add your API keys:
    ```env
    GOOGLE_API_KEY=your_gemini_key
    TAVILY_API_KEY=your_tavily_key
    ```

4.  **Run the App**
    ```bash
    uvicorn app.main:app --reload
    ```
    Open `http://localhost:8000` in your browser.

## ☁️ Deployment (Render)

This project is configured for easy deployment on **Render.com**.

1.  Create a new **Web Service** on Render connected to this repo.
2.  Render will auto-detect `render.yaml`.
3.  Add your `GOOGLE_API_KEY` and `TAVILY_API_KEY` in the **Environment** settings.
4.  Deploy!

## 📄 License

MIT License. Free to use and modify.
