import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup


@dataclass
class Image:

    url: str
    name: str

    pack: str
    downloads: int

    @classmethod
    def from_url(cls, url: str):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("li", class_="icon--item linear-colored")

        image_urls: List[Image] = []
        for result in results:
            image_url = cls(
                url=result["data-png"],
                name=result["data-name"],
                downloads=result.get("data-downloads", 0),
                pack=result.get("data-pack_name", "Unknown"),
            )
            image_urls.append(image_url)
        return image_urls

    @staticmethod
    def download_image(image_url, foldername="", filename="") -> Path:
        datapath = Path.home() / "flaticon" / foldername
        os.makedirs(datapath, exist_ok=True)

        if not filename:
            filename = image_url.split("?")[0].split("/")[-1]

        imagepath = datapath / filename
        if not imagepath.exists():
            content = requests.get(image_url).content
            with imagepath.open("wb+") as file:
                file.write(content)
        return imagepath

    def download(self, foldername="", filename=""):
        return Image.download_image(self.url, foldername=foldername, filename=filename)


class FlatIconAPI:

    @staticmethod
    def create_search_url(query: str, shape: str, order_by=4) -> str:
        url = f"https://www.flaticon.com/search?word={query}"
        if shape:
            url += f"&shape={shape}"
        url += f"&order_by={order_by}"
        return url

    @staticmethod
    def search_for_images(query: str, shape: str = "", order_by=4) -> List[Image]:
        """Search query for flat icon

        Args:
            query (str): Image name
            shape (str, optional): Flat icon shapes. Defaults to "".
            order_by (int, optional): Order type. Defaults to 4.

        Returns:
            List[str]: Url of images
        
        Examples:
            >>> image_names, image_urls = FlatIconAPI.search_for_images("color", shape="lineal-color")
        """
        url = FlatIconAPI.create_search_url(query, shape, order_by)
        return Image.from_url(url)

    @staticmethod
    def download_image(image_url: str, foldername="", filename="") -> Path:
        return Image.download_image(image_url, foldername=foldername, filename=filename)


if __name__ == "__main__":
    results = FlatIconAPI.search_for_images("color", shape="lineal-color")
    imagepath = results[0].download()
    print(imagepath)
