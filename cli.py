import typer
import json
import uuid
from pathlib import Path
import yaml
from collections import Counter
from typing import Optional

app = typer.Typer()

@app.command()
def generate(json_path: str, output: str = "generated_api"):
    with open(json_path, "r") as f:
        data = json.load(f)

    collection_name = Path(json_path).stem
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)

    model_fields = ""
    for key, value in data[0].items():
        value_type = "str" if isinstance(value, str) else type(value).__name__
        model_fields += f"    {key}: {value_type}\n"

    main_code = f"""from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI()

class ItemModel(BaseModel):
{model_fields}

db = []

@app.get("/{collection_name}")
def list_items():
    return db

@app.get("/{collection_name}" + "/{{item_id}}")
def get_item(item_id: str):
    for item in db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/{collection_name}")
def create_item(item: ItemModel):
    obj = item.dict()
    obj["id"] = str(uuid.uuid4())
    db.append(obj)
    return obj

@app.put("/{collection_name}" + "/{{item_id}}")
def update_item(item_id: str, item: ItemModel):
    for i, obj in enumerate(db):
        if obj["id"] == item_id:
            db[i].update(item.dict())
            return db[i]
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/{collection_name}" + "/{{item_id}}")
def delete_item(item_id: str):
    for i, obj in enumerate(db):
        if obj["id"] == item_id:
            return db.pop(i)
    raise HTTPException(status_code=404, detail="Item not found")
"""

    with open(output_path / "main.py", "w") as f:
        f.write(main_code)

    typer.echo(f"API generada en: {output_path}/main.py")

@app.command()
def validate(json_path: str):
    try:
        with open(json_path, "r") as f:
            data = json.load(f)

        if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
            raise ValueError("Debe ser una lista de diccionarios")

        keys = set(data[0].keys())
        for item in data:
            if set(item.keys()) != keys:
                raise ValueError("Los objetos no tienen las mismas claves")

        typer.echo("JSON válido.")
    except Exception as e:
        typer.echo(f"JSON inválido: {e}")

@app.command()
def add_field(json_path: str, key: str, value: str):
    with open(json_path, "r") as f:
        data = json.load(f)

    for item in data:
        item[key] = value

    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)

    typer.echo(f"Campo '{key}' añadido a todos los objetos.")

@app.command()
def convert(json_path: str, output: str = "converted.yaml"):
    with open(json_path, "r") as f:
        data = json.load(f)

    with open(output, "w") as f:
        yaml.dump(data, f)

    typer.echo(f"Convertido a YAML en {output}")

@app.command()
def serve(json_path: str):
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    import uvicorn

    with open(json_path, "r") as f:
        data = json.load(f)

    app = FastAPI()
    db = data
    collection_name = Path(json_path).stem

    class ItemModel(BaseModel):
        __annotations__ = {k: str for k in data[0].keys()}

    @app.get(f"/{collection_name}")
    def list_items():
        return db

    @app.get(f"/{collection_name}" + "/{item_id}")
    def get_item(item_id: str):
        for item in db:
            if item.get("id") == item_id:
                return item
        raise HTTPException(status_code=404, detail="Item not found")

    @app.post(f"/{collection_name}")
    def create_item(item: ItemModel):
        obj = item.dict()
        obj["id"] = str(uuid.uuid4())
        db.append(obj)
        return obj

    uvicorn.run(app, host="127.0.0.1", port=8000)

@app.command()
def filter(json_path: str, field: str, value: str):
    with open(json_path, "r") as f:
        data = json.load(f)

    result = [item for item in data if str(item.get(field)) == value]
    typer.echo(json.dumps(result, indent=2))

@app.command()
def summary(json_path: str):
    with open(json_path, "r") as f:
        data = json.load(f)

    count = len(data)
    keys = list(data[0].keys())
    field_counts = {k: Counter([str(item[k]) for item in data if k in item]) for k in keys}

    typer.echo(f"Total registros: {count}")
    for k in keys:
        typer.echo(f"\n{str(k)}:")
        for val, cnt in field_counts[k].most_common(3):
            typer.echo(f"  {val}: {cnt} veces")

@app.command()
def schema(json_path: str):
    with open(json_path, "r") as f:
        data = json.load(f)

    schema = {}
    for key in data[0].keys():
        types = set(type(item.get(key)).__name__ for item in data)
        schema[key] = list(types)

    for k, t in schema.items():
        typer.echo(f"{k}: {', '.join(t)}")

@app.command()
def merge(file1: str, file2: str, output: str = "merged.json"):
    with open(file1, "r") as f1, open(file2, "r") as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    combined = data1 + data2
    with open(output, "w") as f:
        json.dump(combined, f, indent=2)

    typer.echo(f"Fusionados {len(data1)} + {len(data2)} registros en {output}")

@app.command()
def split(json_path: str, size: int = 100, output_dir: str = "splits"):
    with open(json_path, "r") as f:
        data = json.load(f)

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    for i in range(0, len(data), size):
        chunk = data[i:i+size]
        out_file = Path(output_dir) / f"part_{i//size}.json"
        with open(out_file, "w") as f_out:
            json.dump(chunk, f_out, indent=2)

    typer.echo(f"Archivo dividido en fragmentos de {size} registros en '{output_dir}'")
