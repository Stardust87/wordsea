import typesense
from tqdm import tqdm
from typesense import exceptions

from wordsea.db import Meaning


def create_typesense_index() -> None:
    client = typesense.Client(
        {
            "nodes": [
                {
                    "host": "localhost",
                    "port": "8108",
                    "protocol": "http",
                }
            ],
            "api_key": "xyz",
            "connection_timeout_seconds": 2,
        }
    )

    try:
        client.collections["words"].delete()
    except exceptions.ObjectNotFound:
        print("Collection not found")

    schema = {
        "name": "words",
        "fields": [
            {"name": "word", "type": "string", "facet": True, "sort": True},
            {"name": "forms", "type": "string[]", "facet": True},
        ],
    }

    client.collections.create(schema)

    pipeline = [{"$group": {"_id": "$word", "forms": {"$mergeObjects": "$forms"}}}]
    for meaning in tqdm(Meaning.objects().aggregate(pipeline), desc="Indexing"):
        forms = list(set(meaning["forms"].values()))
        client.collections["words"].documents.create(
            {
                "word": meaning["_id"],
                "forms": forms,
            }
        )
