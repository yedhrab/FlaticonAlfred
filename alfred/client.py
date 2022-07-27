from __future__ import annotations

import json
import sys
from collections.abc import Callable

from .models import Result


class Client:

    query: str
    page_count: int

    results: list[Result]

    def __init__(self) -> None:
        self.page_count = sys.argv[1].count("+") + 1
        self.query = sys.argv[1].replace("+", "")
        self.results = []

    def add_result(
        self,
        title: str,
        subtitle: str,
        icon_path: str | None = None,
        arg: str | None = None,
        http_downloader: Callable[[str], str] | None = None,
    ):
        """Create and add alfred result."""
        icon = None
        if icon_path:
            if http_downloader and "http" in icon_path:
                icon_path = http_downloader(icon_path)
            icon = Result.Icon(icon_path)
        self.results.append(Result(title=title, subtitle=subtitle, icon=icon, arg=arg))

    def response(self):
        """Print alfred results and exit."""
        print(json.dumps({"items": [result.to_dict() for result in self.results]}))
        exit(0)
