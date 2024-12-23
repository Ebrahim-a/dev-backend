from fastapi import FastAPI, HTTPException
import requests
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins - adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")


headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': API_HOST,
}

# Function to handle external API requests, now supporting parameters
def get_external_data(url: str, params: dict = None):
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data")
    return response.json()

# Route for getting anime details
@app.get("/anime/{anime_id}")
def get_anime_details(anime_id: int):
    url = f"https://{API_HOST}/anime/{anime_id}"
    return get_external_data(url)

# Route for getting top animes
@app.get("/top-animes")
def get_top_animes(limit: int = 50):
    url = f"https://{API_HOST}/anime/top/all"
    params = {"limit": limit}
    return get_external_data(url, params=params)

# Route for getting anime recommendations by anime ID
@app.get("/anime/recommendations/{anime_id}")
def get_anime_recommendations_by_anime(anime_id: int):
    url = f"https://{API_HOST}/v2/anime/recommendations/{anime_id}"
    return get_external_data(url)

# Route for getting general anime recommendations
@app.get("/v2/anime/recommendations")
def get_anime_recommendations():
    url = f"https://{API_HOST}/v2/anime/recommendations"
    return get_external_data(url)

# Route for getting seasonal animes
@app.get("/v2/anime/seasonal")
def get_seasonal_animes(year: int, season: str):
    url = f"https://{API_HOST}/v2/anime/seasonal"
    params = {"year": year, "season": season}
    return get_external_data(url, params=params)

# Route for searching anime by query
@app.get("/v2/anime/search")
def search_anime(query: str, limit: int = 50):
    url = f"https://{API_HOST}/v2/anime/search"
    params = {"q": query, "n": limit}
    return get_external_data(url, params=params)
