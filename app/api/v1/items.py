from fastapi import APIRouter, HTTPException, status

from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])

# In-memory store (replace with a real DB in production)
_db: dict[int, dict] = {}
_next_id = 1


@router.get("/", response_model=list[ItemResponse])
def list_items():
    return [ItemResponse(id=k, **v) for k, v in _db.items()]


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    global _next_id
    item_id = _next_id
    _db[item_id] = item.model_dump()
    _next_id += 1
    return ItemResponse(id=item_id, **_db[item_id])


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    if item_id not in _db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return ItemResponse(id=item_id, **_db[item_id])


@router.patch("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, update: ItemUpdate):
    if item_id not in _db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    patch = update.model_dump(exclude_unset=True)
    _db[item_id].update(patch)
    return ItemResponse(id=item_id, **_db[item_id])


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    if item_id not in _db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    del _db[item_id]
