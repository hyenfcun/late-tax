import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_511_KEY")

if not api_key:
    raise RuntimeError("API_511_KEY was not found in .env")

months = [
    "2025-06", "2025-07", "2025-08", "2025-09",
    "2025-10", "2025-11", "2025-12",
    "2026-01", "2026-02", "2026-03", "2026-04",
    "2026-05", "2026-06", "2026-07", "2026-08",
]

url = "https://api.511.org/transit/datafeeds"

output_dir = Path("data/raw/historical")
output_dir.mkdir(parents=True, exist_ok=True)

for month in months:
    output_file = output_dir / f"gtfs_{month}_so.zip"

    if output_file.exists():
        print(f"{month}: already exists — skipping")
        continue

    params = {
        "api_key": api_key,
        "operator_id": "RG",
        "historic": f"{month}-so",
    }

    print(f"{month}: downloading...")

    response = requests.get(
        url,
        params=params,
        stream=True,
        timeout=120,
    )

    response.raise_for_status()

    temp_file = output_file.with_suffix(".zip.part")

    with open(temp_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

    temp_file.rename(output_file)

    size_mb = output_file.stat().st_size / (1024 * 1024)

    print(f"{month}: complete ({size_mb:.1f} MB)")

