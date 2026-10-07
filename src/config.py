import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_DIR = Path(os.getenv("YELP_DATASET_DIR", str(PROJECT_ROOT / "dataset"))).resolve()

DATASET_FILES = {
    "business": DATASET_DIR / "yelp_academic_dataset_business.json",
    "review": DATASET_DIR / "yelp_academic_dataset_review.json",
    "tip": DATASET_DIR / "yelp_academic_dataset_tip.json",
    "checkin": DATASET_DIR / "yelp_academic_dataset_checkin.json",
    "user": DATASET_DIR / "yelp_academic_dataset_user.json",
}

STEPCASE = {
    1: PROJECT_ROOT / "step1",
    2: PROJECT_ROOT / "step2",
    3: PROJECT_ROOT / "step3",
    4: PROJECT_ROOT / "step4",
    5: PROJECT_ROOT / "step5",
}

SUPPORT_FILES = {
    "step4_dishes": STEPCASE[4] / "American Cuisine-Dishes.txt",
    "step3_phrases": STEPCASE[3] / "American_Cuisine_Phrases.csv",
    "step3_expanded": STEPCASE[3] / "expanded_dish_list.csv",
    "step3_labels_dir": STEPCASE[3] / "manualAnnotationTask",
}


def dataset_path(name: str) -> Path:
    return DATASET_FILES[name]


def step_dir(step_num: int) -> Path:
    return STEPCASE[step_num]


def check_dataset(files=("business", "review")):
    missing = []
    for f in files:
        p = dataset_path(f)
        if not p.exists():
            missing.append(str(p))
    if missing:
        print("[WARN] Missing dataset files:")
        for m in missing:
            print(f"  - {m}")
        print(f"\n[INFO] Set YELP_DATASET_DIR in .env or place files in:\n  {DATASET_DIR}")
        return False
    print(f"[OK] Dataset files found in: {DATASET_DIR}")
    return True
