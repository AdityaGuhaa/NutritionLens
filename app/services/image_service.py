import os
from datetime import datetime
import uuid

DATA_DIR = "data"


def save_image(image_bytes: bytes, extension: str = "jpg") -> str:
    """
    Saves uploaded image to data folder with unique name
    Returns file path
    """

    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:6]

    filename = f"food_{timestamp}_{unique_id}.{extension}"
    file_path = os.path.join(DATA_DIR, filename)

    # Save file
    with open(file_path, "wb") as f:
        f.write(image_bytes)

    return file_path