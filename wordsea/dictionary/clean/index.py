import typesense
from tqdm import tqdm
from typesense import exceptions

from wordsea.db import Meaning, Redirect


def create_typesense_index():
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
            {"name": "redirects", "type": "string[]", "facet": True},
        ],
    }

    client.collections.create(schema)

    for word in tqdm(Meaning.objects.distinct("word"), desc="Indexing"):
        redirects = [redirect.from_word for redirect in Redirect.objects(to_word=word)]
        client.collections["words"].documents.create(
            {
                "word": word,
                "redirects": redirects,
            }
        )
