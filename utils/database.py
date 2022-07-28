from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import gspread
import pandas as pd


@dataclass(repr=False, eq=False)
class Serializable:

    id: int
    datetime: datetime

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> "Serializable":
        raise NotImplementedError

    def to_record(self):
        return asdict(self)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, type(self)):
            return self.id == __o.id
        return False


def init_database_for(record: dict[str, Any], dbpath: str) -> pd.DataFrame:
    """Veritabanının oluşturur."""
    db = Path(dbpath)
    if not db.exists():
        os.makedirs(db.parent, exist_ok=True)
        db.touch()
        db.write_text(",".join(record))
    return pd.read_csv(db)


def insert_to_csv(data: Serializable, dbpath: str):
    """Database'e hesap ekler, varsa üzerine yazar."""
    record = data.to_record()
    df = init_database_for(record, dbpath)
    df = pd.read_csv(dbpath)
    df.drop(df[df["id"] == record["id"]].index, inplace=True)  # type: ignore
    df = df.append(record, ignore_index=True)
    df.to_csv(dbpath, index=False)


def find_in_csv(search_value: int | str, dbpath: str, search_column: str = "id") -> dict[str, Any] | None:
    """Database'de hesap id'si ile arar."""
    db = Path(dbpath)
    if db.exists():
        df = pd.read_csv(db)
        df = df[df[search_column] == search_value]
        if not df.empty:
            return df.iloc[0].to_dict()
    return None


def push_to_sheet(spreadsheet: gspread.Spreadsheet, title: str, dbpath: str) -> None:
    df = pd.read_csv(dbpath)
    try:
        worksheet = spreadsheet.worksheet(title)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title, df.shape[0], df.shape[1])
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())


def pull_from_sheet(spreadsheet: gspread.Spreadsheet, title: str, dbpath: str) -> None:
    try:
        worksheet = spreadsheet.worksheet(title)
        df = pd.DataFrame(worksheet.get_all_records())
        df.to_csv(dbpath, index=False)
    except gspread.WorksheetNotFound:
        pass
