import json
from pathlib import Path
from typing import Any, List

class JSONRepository:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            self.file_path.write_text("[]")

    def _read(self) -> List[dict]:
        return json.loads(self.file_path.read_text())

    def _write(self, data: List[dict]):
        self.file_path.write_text(json.dumps(data, indent=2))

    def list_all(self) -> List[dict]:
        return self._read()

    def get_by_field(self, field: str, value: Any) -> dict:
        return next((item for item in self._read() if str(item.get(field)) == str(value)), None)

    def add(self, record: dict) -> dict:
        data = self._read()
        data.append(record)
        self._write(data)
        return record

    def update_by_field(self, field: str, value: Any, new_data: dict) -> dict:
        data = self._read()
        for idx, item in enumerate(data):
            if str(item.get(field)) == str(value):
                data[idx].update(new_data)
                self._write(data)
                return data[idx]
        return None

    def delete_by_field(self, field: str, value: Any) -> dict:
        data = self._read()
        for idx, item in enumerate(data):
            if str(item.get(field)) == str(value):
                removed = data.pop(idx)
                self._write(data)
                return removed
        return None
