import asyncio
import csv
import datetime
import os
import uuid
from typing import List

import aiohttp
import petl as etl
from asgiref.sync import sync_to_async
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView

from starwars_data.models import Collection
from starwars_explorer.swapi_client import SWAPIClient

# Hardcoded number of pages for simplicity.
# We could also determine the number of pages buy taking the count field and number of fetched resources from the first api call.
PEOPLE_PAGES_NUMBER = 9
PLANETS_PAGES_NUMBER = 6

swapi_client = SWAPIClient()


class GenerateCollectionView(View):
    def _save_to_csv(self, table, file_name):
        if not os.path.exists("collections"):
            os.makedirs("collections")

        etl.tocsv(table, f"collections/{file_name}")

    def _drop_columns(self, table, columns):
        return etl.cutout(table, *columns)

    def _change_date_format(self, table):
        return table.convert(
            "edited",
            lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
                "%Y-%m-%d"
            ),
        )

    def _resolve_homeworld_urls(self, table, planets):
        planet_url_to_name = {planet["url"]: planet["name"] for planet in planets}
        return table.convert("homeworld", lambda x: planet_url_to_name[x])

    async def get(self, request):
        fields_to_exclude = [
            "films",
            "species",
            "vehicles",
            "starships",
            "created",
            "url",
        ]

        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.create_task(
                    swapi_client.get_resource(
                        resource="people",
                        pages_number=PEOPLE_PAGES_NUMBER,
                        session=session,
                    )
                ),
                asyncio.create_task(
                    swapi_client.get_resource(
                        resource="planets",
                        pages_number=PLANETS_PAGES_NUMBER,
                        session=session,
                    )
                ),
            ]
            people, planets = await asyncio.gather(*tasks)

            # transformations
            table = etl.fromdicts(people)
            table = self._drop_columns(table, columns=fields_to_exclude)
            table = self._change_date_format(table)
            table = table.rename({"edited": "date"})
            table = self._resolve_homeworld_urls(table, planets)

            # TODO saving files on a disk and creating a database object could be atomic

            # save collection to a csv file
            file_name = f'{str(uuid.uuid1()).replace("-", "")}.csv'
            self._save_to_csv(table, file_name)

            # save collection to a database
            create_collection = sync_to_async(Collection.objects.create)
            await create_collection(file_name=file_name)

            return redirect("home")


class HomePageView(ListView):
    model = Collection
    ordering = ["-created_at"]


class ColectionView(View):
    START_QUERY_DEFAULT = 0
    LIMIT_QUERY_DEFAULT = 10

    def get(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)

        with open(f"collections/{collection.file_name}", "r") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            data = list(reader)

        start = int(request.GET.get("start", self.START_QUERY_DEFAULT))
        limit = int(request.GET.get("limit", self.LIMIT_QUERY_DEFAULT))
        data = data[start : start + limit]

        return render(
            request,
            "starwars_data/collection.html",
            context={
                "headers": headers,
                "data": data,
                "limit": limit,
                "pk": pk,
            },
        )


class AggregateData(View):
    START_QUERY_DEFAULT = 0
    LIMIT_QUERY_DEFAULT = 10

    def get(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        table = etl.fromcsv(f"collections/{collection.file_name}")

        limit = int(request.GET.get("limit", self.LIMIT_QUERY_DEFAULT))
        table = etl.head(table, limit)

        aggregate_fields: List = request.GET.getlist("aggregate_field")

        table = (
            etl.aggregate(table, aggregate_fields, len) if aggregate_fields else table
        )
        context = {
            "fieldnames": table.fieldnames(),
            "table": table,
            "pk": pk,
            "limit": limit,
        }

        return render(request, "starwars_data/collection_aggregate.html", context)
