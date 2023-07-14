import requests
from bs4 import BeautifulSoup

from embedchain.utils import clean_string


class WebPageLoader:
    def load_data(self, url):
        """Load data from a web page."""
        response = requests.get(url)
        data = response.content
        soup = BeautifulSoup(data, "html.parser")
        for tag in soup(
            [
                "nav",
                "aside",
                "form",
                "header",
                "noscript",
                "svg",
                "canvas",
                "footer",
                "script",
                "style",
            ]
        ):
            tag.decompose()

        ids_to_exclude = ["sidebar"]
        for id in ids_to_exclude:
            tag = soup.find(id=id)
            if tag:
                tag.decompose()

        content = soup.get_text()
        content = clean_string(content)

        meta_data = {
            "url": url,
        }

        return [
            {
                "content": content,
                "meta_data": meta_data,
            }
        ]
