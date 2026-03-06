import os

FORMATS = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".gif": "image/gif",
}

def is_valid_image(path):
    ext = os.path.splitext(path)[1].lower()
    return ext in FORMATS

def load_image(path):
    if not os.path.exists(path):
        return None, None, f"File not found: {path}"
    ext = os.path.splitext(path)[1].lower()
    mime = FORMATS.get(ext, "image/jpeg")
    try:
        with open(path, "rb") as f:
            return f.read(), mime, None
    except Exception as e:
        return None, None, str(e)