import hashlib
import json
import os
import re

import requests

from embedchain.loaders.base_loader import BaseLoader
from embedchain.utils import clean_string, is_valid_json_string

VALID_URL_PATTERN = "^https:\/\/[0-9A-z.]+.[0-9A-z.]+.[a-z]+\/.*\.json$"


class JSONLoader(BaseLoader):
    @staticmethod
    def _get_llama_hub_loader():
        try:
            from llama_hub.jsondata.base import \
                JSONDataReader as LLHUBJSONLoader
        except ImportError as e:
            raise Exception(
                f"Failed to install required packages: {e}, \
                install them using `pip install --upgrade 'embedchain[json]`"
            )

        return LLHUBJSONLoader()

    @staticmethod
    def load_data(content):
        """Load a json file. Each data point is a key value pair."""

        loader = JSONLoader._get_llama_hub_loader()

        if not isinstance(content, str) and not isinstance(content, list):
            print("Invaid content input. Provide the correct path to the json file.")

        content_url_str = content
        data = []
        data_content = []

        # Load json data from various sources.
        if isinstance(content, list) and (all(isinstance(doc, dict)) for doc in content):
            docs = []
            for doc in content:
                docs.extend(loader.load_data(doc))
            content_url_str = hashlib.sha256((str(content)).encode()).hexdigest()
        elif isinstance(content, dict):
            docs = loader.load_data(content)
            content_url_str = hashlib.sha256((str(content)).encode()).hexdigest()
        else:
            if os.path.isfile(content):
                with open(content, "r", encoding="utf-8") as json_file:
                    json_data = json.load(json_file)
            elif re.match(VALID_URL_PATTERN, content):
                response = requests.get(content)
                if response.status_code == 200:
                    json_data = response.json()
                else:
                    raise ValueError(
                        f"Loading data from the given url: {content} failed. \
                        Make sure the url is working."
                    )
            elif is_valid_json_string(content):
                print("VALID STRING: ", content)
                json_data = content
                content_url_str = hashlib.sha256((content).encode()).hexdigest()
            else:
                raise ValueError(f"Invalid content to load json data from: {content}")

            docs = loader.load_data(json_data)

        for doc in docs:
            doc_content = clean_string(doc.text)
            data.append({"content": doc_content, "meta_data": {"url": content_url_str}})
            data_content.append(doc_content)

        doc_id = hashlib.sha256((content_url_str + ", ".join(data_content)).encode()).hexdigest()
        return {"doc_id": doc_id, "data": data}
