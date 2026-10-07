import json
from pathlib import Path
from typing import Iterable, List, Dict, Any, Iterator
import pandas as pd

from .config import dataset_path, check_dataset


def json_reader(file_path) -> Iterator[Dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def load_businesses(category=None) -> pd.DataFrame:
    check_dataset(("business",))
    records = []
    for biz in json_reader(dataset_path("business")):
        if category and (category not in biz.get("categories", "")):
            continue
        records.append({
            "business_id": biz.get("business_id"),
            "name": biz.get("name"),
            "state": biz.get("state"),
            "city": biz.get("city"),
            "address": biz.get("full_address", biz.get("address", "")),
            "review_count": biz.get("review_count", 0),
            "stars": biz.get("stars"),
            "categories": biz.get("categories", ""),
        })
    return pd.DataFrame(records)


def filter_business_ids_by_category(category: str) -> List[str]:
    ids = []
    for biz in json_reader(dataset_path("business")):
        if category in biz.get("categories", ""):
            ids.append(biz["business_id"])
    return ids


def load_reviews_for_businesses(business_ids: Iterable[str]) -> pd.DataFrame:
    check_dataset(("review",))
    id_set = set(business_ids)
    records = []
    for rev in json_reader(dataset_path("review")):
        if rev["business_id"] in id_set:
            records.append({
                "business_id": rev["business_id"],
                "text": rev.get("text", ""),
                "stars": rev.get("stars"),
                "date": rev.get("date"),
            })
    return pd.DataFrame(records)


def load_tips_for_businesses(business_ids: Iterable[str]) -> pd.DataFrame:
    check_dataset(("tip",))
    id_set = set(business_ids)
    records = []
    for tip in json_reader(dataset_path("tip")):
        if tip["business_id"] in id_set:
            records.append({
                "business_id": tip["business_id"],
                "text": tip.get("text", ""),
                "date": tip.get("date"),
            })
    return pd.DataFrame(records)


def ensure_dir(p: Path):
    Path(p).mkdir(parents=True, exist_ok=True)
    return p
