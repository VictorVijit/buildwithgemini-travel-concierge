"""
Seed script to populate Firestore with sample destination data for travel-concierge.
"""

import subprocess
from google.cloud import firestore
from google.oauth2.credentials import Credentials

# Hardcode project ID as a string per lab requirements
PROJECT_ID = "qwiklabs-gcp-01-502ef792f702"

def get_firestore_client():
    try:
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

def seed_firestore():
    print(f"Connecting to Firestore for project: {PROJECT_ID}")
    db = get_firestore_client()

    destinations = [
        {
            "id": "tokyo",
            "name": "Tokyo",
            "country": "Japan",
            "category": "Culture & Food",
            "budget_level": "$$$",
            "highlights": ["Shibuya Crossing", "Tsukiji Outer Market", "Akihabara"],
            "best_season": "Spring / Autumn",
            "rating": 4.9,
        },
        {
            "id": "paris",
            "name": "Paris",
            "country": "France",
            "category": "Art & Romance",
            "budget_level": "$$$$",
            "highlights": ["Eiffel Tower", "Louvre Museum", "Montmartre"],
            "best_season": "Spring / Summer",
            "rating": 4.8,
        },
        {
            "id": "kyoto",
            "name": "Kyoto",
            "country": "Japan",
            "category": "History & Nature",
            "budget_level": "$$",
            "highlights": ["Fushimi Inari Shrine", "Arashiyama Bamboo Grove", "Kinkaku-ji"],
            "best_season": "Spring / Autumn",
            "rating": 4.9,
        },
        {
            "id": "cairo",
            "name": "Cairo",
            "country": "Egypt",
            "category": "History & Monuments",
            "budget_level": "$$",
            "highlights": ["Pyramids of Giza", "The Egyptian Museum", "Khan el-Khalili"],
            "best_season": "Winter",
            "rating": 4.7,
        },
    ]

    for item in destinations:
        doc_ref = db.collection("destinations").document(item["id"])
        doc_ref.set(item)
        print(f"✅ Seeded destination: {item['name']} ({item['id']})")

    print("🎉 Firestore seeding complete!")

if __name__ == "__main__":
    seed_firestore()
