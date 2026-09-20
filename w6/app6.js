from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Schemas
class ItemCreate(BaseModel):
    name: str
    price: float

class ItemPublic(BaseModel):
    id: int
    name: str
    price: float

# Database giả lập
_items: list[ItemPublic] = []
_next_id: int = 1

def _find(item_id: int) -> ItemPublic | None:
    for it in _items:
        if it.id == item_id:
            return it
    return None

app = FastAPI()
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/items/me")
def read_me():
    return "Welcome!"

# GET AN ITEM
@app.get("/items/{item_id}", response_model=ItemPublic)
def read_item(item_id: int):
    item = _find(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# GET ITEMS
@app.get("/items")
def read_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    q: str | None = Query(None, min_length=2)
):
    return _items[skip : skip + limit]

# CREATE AN ITEM
@app.post("/items", response_model=ItemPublic, status_code=201)
def create_item(data: ItemCreate):
    global _next_id
    newItem = ItemPublic(name=data.name, price=data.price, id=_next_id)
    _next_id += 1
    _items.append(newItem)
    return newItem

# UPDATE AN ITEM
@app.put("/items/{item_id}", response_model=ItemPublic)
def update_item(item_id: int, data: ItemCreate):
    item = _find(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    updateValue = ItemPublic(name=data.name, price=data.price, id=item.id)
    index = _items.index(item)
    _items[index] = updateValue
    return updateValue

# DELETE AN ITEM
@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    item = _find(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    _items.remove(item)
    return None