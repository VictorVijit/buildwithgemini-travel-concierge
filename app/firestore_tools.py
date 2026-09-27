"""
Firestore backend function tools for travel-concierge agent.
"""

import subprocess
from google.cloud import firestore
from google.oauth2.credentials import Credentials

# Hardcode project ID as a string per lab instructions
PROJECT_ID = "qwiklabs-gcp-01-502ef792f702"

def get_firestore_client():
    """Returns a Firestore client initialized with hardcoded project ID."""
    try:
        # Check for local user access token when running locally
        token = subprocess.check_output(
            ["gcloud", "auth", "application-default", "print-access-token"],
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
        if token:
            return firestore.Client(project=PROJECT_ID, credentials=Credentials(token))
    except Exception:
        pass
    return firestore.Client(project=PROJECT_ID)

def get_destination_details(destination_id: str) -> dict:
    """Retrieves details of a travel destination from Firestore by ID.

    Args:
        destination_id: The unique identifier of the destination (e.g., 'tokyo', 'paris', 'kyoto', 'cairo').

    Returns:
        Dictionary containing destination details or an error message if not found.
    """
    try:
        db = get_firestore_client()
        doc = db.collection("destinations").document(destination_id.lower()).get()
        if doc.exists:
            return doc.to_dict()
        return {"error": f"Destination '{destination_id}' not found in Firestore."}
    except Exception as e:
        return {"error": f"Failed to retrieve destination: {str(e)}"}

def search_destinations(category: str = None, country: str = None) -> list[dict]:
    """Searches for travel destinations in Firestore filtered by category or country.

    Args:
        category: Optional category filter (e.g., 'Culture & Food', 'Art & Romance', 'History & Nature', 'History & Monuments').
        country: Optional country filter (e.g., 'Japan', 'France', 'Egypt').

    Returns:
        List of matching destination dictionaries.
    """
    try:
        db = get_firestore_client()
        query = db.collection("destinations")
        if category:
            query = query.where("category", "==", category)
        if country:
            query = query.where("country", "==", country)
        
        results = [doc.to_dict() for doc in query.stream()]
        return results
    except Exception as e:
        return [{"error": f"Failed to search destinations: {str(e)}"}]

def add_destination(
    destination_id: str,
    name: str,
    country: str,
    category: str,
    budget_level: str,
    highlights: list[str],
    best_season: str,
    rating: float = 4.5
) -> str:
    """Adds or updates a travel destination in the Firestore database.

    Args:
        destination_id: Unique slug identifier for the destination (e.g., 'barcelona').
        name: Name of the destination (e.g., 'Barcelona').
        country: Country where the destination is located (e.g., 'Spain').
        category: Travel category (e.g., 'Architecture & Culture').
        budget_level: Budget indicator (e.g., '$', '$$', '$$$', '$$$$').
        highlights: Key attractions or highlights (e.g., ['Sagrada Familia', 'Park Guell']).
        best_season: Recommended season to visit (e.g., 'Spring / Autumn').
        rating: Rating score out of 5.0 (default: 4.5).

    Returns:
        Status string confirming document creation.
    """
    try:
        db = get_firestore_client()
        doc_data = {
            "id": destination_id.lower(),
            "name": name,
            "country": country,
            "category": category,
            "budget_level": budget_level,
            "highlights": highlights,
            "best_season": best_season,
            "rating": rating,
        }
        db.collection("destinations").document(destination_id.lower()).set(doc_data)
        return f"Successfully added destination '{name}' ({destination_id}) to Firestore."
    except Exception as e:
        return f"Error adding destination to Firestore: {str(e)}"


def calculate_trip_budget(
    duration_days: int,
    daily_budget: float,
    travelers: int = 1,
    currency: str = "USD"
) -> dict:
    """Calculates an estimated travel budget breakdown based on duration, daily spend allowance, and travelers.

    Args:
        duration_days: Number of days for the trip.
        daily_budget: Estimated daily spend budget per traveler (e.g. 150.0).
        travelers: Number of travelers (default: 1).
        currency: Currency symbol or code (default: 'USD').

    Returns:
        Dictionary containing grand total cost and detailed cost breakdown for accommodation, food, and activities.
    """
    total_per_person = duration_days * daily_budget
    grand_total = total_per_person * travelers

    accommodation = round(grand_total * 0.45, 2)
    food_and_dining = round(grand_total * 0.35, 2)
    activities_and_transport = round(grand_total * 0.20, 2)

    return {
        "duration_days": duration_days,
        "travelers": travelers,
        "daily_budget_per_person": daily_budget,
        "currency": currency,
        "grand_total": round(grand_total, 2),
        "breakdown": {
            "accommodation": accommodation,
            "food_and_dining": food_and_dining,
            "activities_and_transport": activities_and_transport,
        },
    }


def get_currency_exchange_rates(base_currency: str = "USD", target_currencies: list[str] = None) -> dict:
    """Fetches real-time foreign currency exchange rates for travel planning and budgeting.

    Args:
        base_currency: Three-letter base currency code (e.g. 'USD', 'EUR', 'GBP'). Default: 'USD'.
        target_currencies: Optional list of target currency codes to filter (e.g. ['JPY', 'EUR', 'GBP']).

    Returns:
        Dictionary containing base currency code, rate date, and exchange rate mappings.
    """
    import os
    import requests

    # Read optional API key from env variable if provided
    api_key = os.environ.get("EXCHANGE_RATE_API_KEY")

    try:
        base = base_currency.upper()
        url = f"https://api.frankfurter.dev/v1/latest?base={base}"
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        rates = data.get("rates", {})
        if target_currencies:
            targets = [t.upper() for t in target_currencies]
            rates = {k: v for k, v in rates.items() if k in targets}

        return {
            "base": data.get("base", base),
            "date": data.get("date"),
            "rates": rates,
        }
    except Exception as e:
        return {"error": f"Failed to fetch exchange rates: {str(e)}"}


