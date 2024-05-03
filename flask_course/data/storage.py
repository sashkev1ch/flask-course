from pathlib import Path
from typing import Dict, List, Union, Any
from json import load, dump


class DataStorage:
    def __init__(self, data_path: Path) -> None:
        self._data_path = data_path

    @property
    def _raw(self) -> Dict[str, Any]:
        with open(self._data_path, "r") as data:
            return load(data)

    def get(self) -> List[Dict[str, Union[int, str]]]:
        with open(self._data_path, "r") as data:
            if data:
                return list(load(data)["users"].values())

    def find(self, id: int) -> Dict[str, Union[int, str]]:
        data = self.get()
        for user in data:
            if user["id"] == int(id):
                return user

    def find_by_email(self, email: str) -> Dict[str, Union[int, str]]:
        data = self.get()
        for user in data:
            if user["email"].lower() == email.lower():
                return user


    def delete(self, id):
        data = self._raw
        try:
            data["users"].pop(id)
        except KeyError:
            print(f"No user with id: {id}")

        with open(self._data_path, "w") as file:
            dump(data, file)

    def save(self, new_data: Dict[str, Union[int, str]]):
        data = self._raw
        new_data_id = new_data.get("id", len(data["users"].keys()) + 1)
        new_data["id"] = new_data_id
        data["users"][str(new_data_id)] = new_data
        with open(self._data_path, "w") as file:
            dump(data, file)
