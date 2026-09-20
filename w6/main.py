from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Schemas
class ItemCreate(BaseModel):
    name: str
    price: float


class ItemPublic(BaseModel):
    id: int
    name: str
    price: float

class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None


class ItemListResponse(BaseModel):
    items: list[ItemPublic]
    total: int
    skip: int
    limit: int


class HousePriceRequest(BaseModel):
    area_sqm: float = Field(gt=0)
    bedrooms: int = Field(ge=0)
    distance_to_center_km: float


class HousePricePrediction(BaseModel):
    predicted_price: float
    currency: str = "VND"


# Fake database
_items: list[ItemPublic] = []
_next_id: int = 1


def _find(item_id: int) -> ItemPublic | None:
    for item in _items:
        if item.id == item_id:
            return item
    return None


# FastAPI application
app = FastAPI()
app.mount("/static", StaticFiles(directory="../frontend"), name="static")


# GET /items/me
@app.get("/items/me")
def read_me():
    return "Welcome!"


# GET /items/{item_id}
@app.get("/items/{item_id}", response_model=ItemPublic)
def read_item(item_id: int):
    item = _find(item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return item


# GET /items
@app.get("/items", response_model=ItemListResponse)
def read_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    min_price: float | None = None,
    max_price: float | None = None,
    q: str | None = Query(None, min_length=2),
    sort_by: str = Query(
        "id",
        pattern="^(id|name|price)$"
    ),
    order: str = Query(
        "asc",
        pattern="^(asc|desc)$"
    )
):
    result = _items.copy()

    if min_price is not None:
        result = [
            item
            for item in result
            if item.price >= min_price
        ]

    if max_price is not None:
        result = [
            item
            for item in result
            if item.price <= max_price
        ]

    if q is not None:
        result = [
            item
            for item in result
            if q.lower() in item.name.lower()
        ]

    if sort_by == "id":
        result.sort(
            key=lambda item: item.id,
            reverse=(order == "desc")
        )

    elif sort_by == "name":
        result.sort(
            key=lambda item: item.name.lower(),
            reverse=(order == "desc")
        )

    elif sort_by == "price":
        result.sort(
            key=lambda item: item.price,
            reverse=(order == "desc")
        )


    total = len(result)
    result = result[skip: skip + limit]

    return ItemListResponse(
        items=result,
        total=total,
        skip=skip,
        limit=limit
    )


# POST /items

@app.post(
    "/items",
    response_model=ItemPublic,
    status_code=201
)
def create_item(data: ItemCreate):
    global _next_id

    for item in _items:
        if item.name.lower() == data.name.lower():
            raise HTTPException(
                status_code=409,
                detail="Item with this name already exists"
            )

    new_item = ItemPublic(
        name=data.name,
        price=data.price,
        id=_next_id
    )

    _next_id += 1
    _items.append(new_item)

    return new_item


# PUT /items/{item_id}
@app.put(
    "/items/{item_id}",
    response_model=ItemPublic
)
def update_item(item_id: int, data: ItemCreate):
    item = _find(item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    if data.name.lower() != item.name.lower():

        for other_item in _items:
            if (
                other_item.id != item_id
                and other_item.name.lower() == data.name.lower()
            ):
                raise HTTPException(
                    status_code=409,
                    detail="Item with this name already exists"
                )

    updated_item = ItemPublic(
        name=data.name,
        price=data.price,
        id=item.id
    )

    index = _items.index(item)
    _items[index] = updated_item

    return updated_item


# PATCH /items/{item_id}
@app.patch(
    "/items/{item_id}",
    response_model=ItemPublic
)
def patch_item(item_id: int, data: ItemUpdate):
    item = _find(item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    update_data = data.model_dump(exclude_unset=True)


    if "name" in update_data:
        new_name = update_data["name"]

        if new_name.lower() != item.name.lower():

            for other_item in _items:
                if (
                    other_item.id != item_id
                    and other_item.name.lower() == new_name.lower()
                ):
                    raise HTTPException(
                        status_code=409,
                        detail="Item with this name already exists"
                    )

    if "name" in update_data:
        item.name = update_data["name"]

    if "price" in update_data:
        item.price = update_data["price"]

    return item



# DELETE /items/{item_id}
@app.delete(
    "/items/{item_id}",
    status_code=204
)
def delete_item(item_id: int):
    item = _find(item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    _items.remove(item)

    return None


# POST /predict/house-price
@app.post(
    "/predict/house-price",
    response_model=HousePricePrediction
)
def predict_house_price(data: HousePriceRequest):
    price = (
        data.area_sqm * 15_000_000
        - data.distance_to_center_km * 5_000_000
        + data.bedrooms * 20_000_000
    )

    return HousePricePrediction(
        predicted_price=price
    )

