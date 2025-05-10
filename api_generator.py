from fastapi import FastAPI, HTTPException
from typing import Dict, List
from pydantic import BaseModel
import uuid

def generate_api(app: FastAPI, store: Dict[str, List[Dict]]):
    for collection_name in store.keys():
        create_crud_endpoints(app, collection_name, store)

def create_crud_endpoints(app: FastAPI, name: str, store: Dict[str, List[Dict]]):
    class ItemModel(BaseModel):
        __annotations__ = {
            key: (str if isinstance(val, str) else type(val))
            for key, val in (store[name][0].items() if store[name] else {"id": str}.items())
        }

    @app.get(f"/{name}")
    def list_items():
        return store[name]

    @app.get(f"/{name}" + "/{item_id}")
    def get_item(item_id: str):
        for item in store[name]:
            if item["id"] == item_id:
                return item
        raise HTTPException(status_code=404, detail="Item not found")

    @app.post(f"/{name}")
    def create_item(item: ItemModel):
        item_dict = item.dict()
        item_dict["id"] = str(uuid.uuid4())
        store[name].append(item_dict)
        return item_dict

    @app.put(f"/{name}" + "/{item_id}")
    def update_item(item_id: str, item: ItemModel):
        for i, obj in enumerate(store[name]):
            if obj["id"] == item_id:
                store[name][i].update(item.dict())
                return store[name][i]
        raise HTTPException(status_code=404, detail="Item not found")

    @app.delete(f"/{name}" + "/{item_id}")
    def delete_item(item_id: str):
        for i, obj in enumerate(store[name]):
            if obj["id"] == item_id:
                return store[name].pop(i)
        raise HTTPException(status_code=404, detail="Item not found")
