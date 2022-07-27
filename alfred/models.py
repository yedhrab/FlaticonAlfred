from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class Result:
    """Alfred result.
    
    {
        "uid": "desktop",
        "type": "file",
        "title": "Desktop",
        "subtitle": "~/Desktop",
        "arg": "~/Desktop",
        "autocomplete": "Desktop",
        "icon": {
            "type": "fileicon",
            "path": "~/Desktop"
        }
    }
    """

    @dataclass
    class Icon:

        path: str
        type: str | None = None

    title: str
    subtitle: str

    uid: str | None = None
    arg: str | None = None
    autocomplete: str | None = None
    icon: Icon | None = None

    def to_dict(self) -> dict[str, str | None]:
        return asdict(self)
