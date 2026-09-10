from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

def predict_price(area: float, bedrooms: int, location: str) -> float:
    price = 500_000_000
    price += area * 15_000_000
    price += bedrooms * 50_000_000

    loc = location.lower()
    if loc == "hanoi":
        price *= 1.3
    elif loc == "hcmc":
        price *= 1.25

    return round(price / 1_000_000) * 1_000_000

@app.get("/predict")
def get_predict(area: float, bedrooms: int, location: str = "other"):
    predicted_price = predict_price(area, bedrooms, location)
    return {
        "area": area,
        "bedrooms": bedrooms,
        "location": location,
        "predicted_price": predicted_price,
    }

app.mount("/static", StaticFiles(directory="../frontend"), name="static")