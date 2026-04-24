import os

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

KASSALAPP_API_KEY = os.getenv("vcZDiDR6iCz7LeutQ6YxQxZymbnYyGufF1pfjoOZ")


@app.get("/")
def home():
    return {"message": "Backend is working"}


@app.get("/search")
async def search(q: str):
    if not KASSALAPP_API_KEY:
        return {"error": "Missing KASSALAPP_API_KEY"}

    url = "https://kassal.app/api/v1/products"
    headers = {
        "Authorization": f"Bearer {KASSALAPP_API_KEY}",
        "Accept": "application/json",
    }
    params = {
        "search": q,
        "size": 10,
        "sort": "price_asc",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        data = response.json()

    products = []

    for item in data.get("data", []):
        products.append(
            {
                "store": item.get("store", {}).get("name", "Unknown"),
                "product": item.get("name", "Unknown product"),
                "price": item.get("current_price", 0),
                "unit_price": item.get("current_unit_price", 0),
                "unit_label": "kr/l",
                "is_discount": False,
                "before_price": None,
                "last_updated": item.get("updated_at", "Unknown"),
            }
        )

    return products
