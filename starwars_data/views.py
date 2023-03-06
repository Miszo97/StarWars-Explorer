import asyncio
import datetime
import itertools
import json

import aiohttp
import petl as etl
from django.http import HttpResponse

people_urls = [f"https://swapi.dev/api/people/?page={page}" for page in range(1, 10)]
planets_urls = [f"https://swapi.dev/api/planets/?page={page}" for page in range(1, 7)]


async def fetch_url(session, url):
    async with session.get(url) as response:
        data = await response.json()
        return data


async def get_planets(session):
    planets_tasks = [
        asyncio.create_task(fetch_url(session, url)) for url in planets_urls
    ]
    planets_pages = await asyncio.gather(*planets_tasks)
    planets = (planets_page["results"] for planets_page in planets_pages)
    planets = list(itertools.chain.from_iterable(planets))

    return planets


async def get_people(session):
    people_tasks = [asyncio.create_task(fetch_url(session, url)) for url in people_urls]
    people_pages = await asyncio.gather(*people_tasks)
    people = (people_page["results"] for people_page in people_pages)
    people = list(itertools.chain.from_iterable(people))

    return people


# Create your views here.


async def craete_dataset(request):
    async with aiohttp.ClientSession() as session:
        print("waiting for people and planets")
        people_task = asyncio.create_task(get_people(session))
        planets_task = asyncio.create_task(get_planets(session))

        people = await people_task
        planets = await planets_task

        print("people:", len(people))
        print("planets:", len(planets))

        fields_to_exclude = [
            "films",
            "species",
            "vehicles",
            "starships",
            "created",
            "url",
        ]

        table = etl.fromdicts(people)
        table = etl.cutout(table, *fields_to_exclude)
        table = table.convert(
            "edited",
            lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
                "%Y-%m-%d"
            ),
        )
        table = table.rename({"edited": "date"})

        planet_url_to_name = {planet["url"]: planet["name"] for planet in planets}
        table = table.convert("homeworld", lambda x: planet_url_to_name[x])

        file_name = "output.csv"
        etl.tocsv(table, file_name)
        return HttpResponse(f"Collection was saved to {file_name}")
