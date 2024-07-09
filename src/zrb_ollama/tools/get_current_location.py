import json
import requests
from typing import Annotated


def get_current_location() -> Annotated[str, "JSON string representing latitude and longitude"]:  # noqa
    """Get the user's current location."""
    return json.dumps(
        requests.get("http://ip-api.com/json?fields=lat,lon").json()
    )
