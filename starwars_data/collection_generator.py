from typing import List
import os
import datetime
import petl as etl

class CollectionGenerator(): 

    def __init__(self, data: List[dict]) -> None:
        self.table = etl.fromdicts(data)

    def rename(self, fields):
        self.table = self.table.rename(fields)

    def save_to_csv(self, file_name):
        if not os.path.exists("collections"):
            os.makedirs("collections")

        etl.tocsv(self.table, f"collections/{file_name}")

    def drop_columns(self, columns):
        self.table =  etl.cutout(self.table, *columns)

    def change_date_format(self):
        self.table = self.table.convert(
            "edited",
            lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
                "%Y-%m-%d"
            ),
        )

    def resolve_fields(self, column: str, mapping: dict):
        self.table = self.table.convert(column, lambda x: mapping[x])
        return self.table
