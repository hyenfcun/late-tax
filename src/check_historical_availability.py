import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_511_KEY")

months = [
    "2025-06", "2025-07", "2025-08", "2025-09",
    "2025-10", "2025-11", "2025-12",
    "2026-01", "2026-02", "2026-03", "2026-04",
    "2026-05", "2026-06", "2026-07", "2026-08"
]

url = "https://api.511.org/transit/datafeeds"

for month in months:
    params = {
        "api_key": api_key,
        "operator_id": "RG",
        "historic": f"{month}-so"
    }

    response = requests.get(
        url,
        params=params,
        stream=True,
        timeout=30
    )

    print(month, response.status_code)
    response.close()


