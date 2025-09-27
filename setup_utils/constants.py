from pathlib import Path


IMAGES_FOLDER = Path(__file__).parent.parent / "static" / "images"
IMAGE_SUFFIXES = {".jpg", ".png", ".jpeg", ".gif"}
GUEST_BOOK = Path(__file__).parent.parent / "data" / "guestbook.txt"
UPLOAD_FOLDER = Path(__file__).parent.parent / "static" / "uploads"

GROWTH_THRESHOLDS = {
    0: 0,
    1: 3,
    2: 6,
    3: 12,
    4: 20
}

STAGE_LABELS = {
    0: "🌱",
    1: "🌿",
    2: "🌳"
}