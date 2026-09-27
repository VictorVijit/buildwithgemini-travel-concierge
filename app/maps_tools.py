"""
Google Maps function tools (Geocoding & Places New API) for travel-concierge agent.
"""

import os
import requests
from dotenv import load_dotenv

# Load local .env file
load_dotenv()

def geocode_address(address: str) -> dict:
    """Converts a location name or address into geographic coordinates (latitude and longitude).

    Args:
        address: The address or place name to geocode (e.g., 'Tokyo Tower', 'Eiffel Tower, Paris').

    Returns:
        Dictionary containing key fields: name, address, and location (latitude/longitude coordinates).
    """
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return {"error": "GOOGLE_MAPS_API_KEY environment variable is not set."}

    try:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": address, "key": api_key}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        if not results:
            return {"error": f"No geocoding results found for address '{address}'."}

        first = results[0]
        loc = first.get("geometry", {}).get("location", {})
        return {
            "name": address,
            "address": first.get("formatted_address"),
            "location": {
                "latitude": loc.get("lat"),
                "longitude": loc.get("lng"),
            },
        }
    except Exception as e:
        return {"error": f"Geocoding request failed: {str(e)}"}

def find_nearby_places(
    latitude: float,
    longitude: float,
    place_type: str = "restaurant",
    radius_meters: float = 1000.0
) -> list[dict]:
    """Finds nearby places of a specified type near coordinates using Google Places API (New).

    Args:
        latitude: Latitude coordinate.
        longitude: Longitude coordinate.
        place_type: Type of place to search for (e.g. 'restaurant', 'tourist_attraction', 'museum', 'hotel', 'cafe').
        radius_meters: Search radius in meters (default: 1000.0).

    Returns:
        List of nearby place dictionaries containing key fields (name, address, location).
    """
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return [{"error": "GOOGLE_MAPS_API_KEY environment variable is not set."}]

    try:
        url = "https://places.googleapis.com/v1/places:searchNearby"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location",
        }
        payload = {
            "includedTypes": [place_type.lower()],
            "maxResultCount": 5,
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": latitude,
                        "longitude": longitude,
                    },
                    "radius": radius_meters,
                }
            },
        }
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        places = data.get("places", [])
        formatted_places = []
        for p in places:
            display_name = p.get("displayName", {}).get("text", "")
            formatted_places.append({
                "name": display_name,
                "address": p.get("formattedAddress", ""),
                "location": p.get("location", {}),
            })

        return formatted_places
    except Exception as e:
        return [{"error": f"Places search failed: {str(e)}"}]
