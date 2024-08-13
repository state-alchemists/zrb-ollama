import json
from typing import Literal

import requests


def get_current_weather(
    latitude: float,
    longitude: float,
    temperature_unit: Literal["celsius", "fahrenheit"],
) -> str:
    """Get the current weather in a given location."""
    resp = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "temperature_unit": temperature_unit,
            "current_weather": True,
        },
    )
    return json.dumps(resp.json())
