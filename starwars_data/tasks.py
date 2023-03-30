import uuid
from celery import shared_task
from starwars_data.collection_generator import CollectionGenerator
from starwars_data.models import Collection

from starwars_explorer.swapi_client import RequestsSWAPIClient, SWAPIClient
swapi_client: SWAPIClient = RequestsSWAPIClient()

fields_to_exclude = [
    "films",
    "species",
    "vehicles",
    "starships",
    "created",
    "url",
]

@shared_task
def generate_collection_task():
    file_name = f'{str(uuid.uuid1()).replace("-", "")}.csv'
    # fetch data
    people = swapi_client.get_resource("people")
    planets = swapi_client.get_resource("planets")

    # transformations
    collection_generator = CollectionGenerator(data=people)
    
    collection_generator.drop_columns(columns=fields_to_exclude)
    collection_generator.change_date_format()
    collection_generator.rename(fields = {"edited": "date"})

    planet_url_to_name = {planet["url"]: planet["name"] for planet in planets}
    collection_generator.resolve_fields(column="homeworld", mapping=planet_url_to_name)

    collection_generator.save_to_csv(file_name)
    Collection.objects.create(file_name=file_name)
        
