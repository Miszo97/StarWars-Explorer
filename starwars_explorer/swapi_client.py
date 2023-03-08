import asyncio
import itertools

from starwars_explorer.settings import SWAPI_BASE_URL


class SWAPIClient:
    async def _fetch_url(self, session, url):
        async with session.get(url) as response:
            data = await response.json()
            return data

    async def get_resource(self, resource: str, session, pages_number: int = 1):
        urls = [
            f"{SWAPI_BASE_URL}/{resource}/?page={page}"
            for page in range(1, pages_number + 1)
        ]

        tasks = [asyncio.create_task(self._fetch_url(session, url)) for url in urls]
        resource_pages = await asyncio.gather(*tasks)
        resource = (resource_page["results"] for resource_page in resource_pages)
        resource = list(itertools.chain.from_iterable(resource))

        return resource
