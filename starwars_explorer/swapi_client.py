import asyncio
import itertools

from starwars_explorer.settings import SWAPI_BASE_URL


class SWAPIClient:
    async def _fetch_url(self, session, url):
        async with session.get(url) as response:
            # We are assuming that we get the response, but we should check if the status is 200 and the returning data is json
            # We should handle the case when API doesn't respond or status codes are other than 200
            data = await response.json()
            return data

    async def get_resource(self, resource: str, session, pages_number: int = 1):
        # Usually, when we work with paginated data like this, we should work with the next field
        # But in this case, when we call it asynchronously, we can call for each page in advance
        urls = [
            f"{SWAPI_BASE_URL}/{resource}/?page={page}"
            for page in range(1, pages_number + 1)
        ]

        tasks = [asyncio.create_task(self._fetch_url(session, url)) for url in urls]
        resource_pages = await asyncio.gather(*tasks)
        resource = (resource_page["results"] for resource_page in resource_pages)
        resource = list(itertools.chain.from_iterable(resource))

        return resource
