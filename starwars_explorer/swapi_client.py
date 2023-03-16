from abc import ABC

import requests

from starwars_explorer.settings import SWAPI_BASE_URL


class SWAPIClient(ABC):
    def get_resource(self, resource: str) -> list:
        pass


class RequestsSWAPIClient(SWAPIClient):
    def get_resource(self, resource: str) -> list:
        page = 1
        all_data = []
        while True:
            response = requests.get(f"{SWAPI_BASE_URL}/{resource}/?page={page}")
            data = response.json()
            all_data.extend(data["results"])
            if data["next"] is None:
                break
            print(page)
            page += 1

        return all_data
