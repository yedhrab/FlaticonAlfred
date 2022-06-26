import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Union

import requests

AlfredResult = Dict[str, Union[str, Dict[str, str]]]


class AlfredAPI:

    @staticmethod
    def download_image(image_url: str) -> Path:
        datapath = Path.cwd() / "images"
        os.makedirs(datapath, exist_ok=True)
        filename = image_url.split("/")[-1].split("?")[0]
        imagepath = datapath / filename
        if not imagepath.exists():
            content = requests.get(image_url).content
            with imagepath.open("wb+") as file:
                file.write(content)
        return imagepath

    @staticmethod
    def to_result(title: str, subtitle: str, icon_path=None, arg=None) -> AlfredResult:
        result_dict: AlfredResult
        result_dict = {"title": title, "subtitle": subtitle}
        if icon_path:
            if "http" in icon_path:
                icon_path = AlfredAPI.download_image(icon_path)
            result_dict["icon"] = {"path": str(icon_path)}
        if arg:
            result_dict["arg"] = arg
        return result_dict

    @staticmethod
    def to_response(results: List[AlfredResult]):
        return json.dumps({"items": results})

    @staticmethod
    def get_query() -> str:
        return sys.argv[1]
