"""
Image generation tool using gemini-3.1-flash-lite-image for travel-concierge agent.
"""

import time
import subprocess
from google import genai
from google.genai import types
from google.cloud import storage
from google.oauth2.credentials import Credentials
from google.adk.tools import ToolContext

# Hardcode project ID and bucket name as strings per instructions
PROJECT_ID = "qwiklabs-gcp-01-502ef792f702"
BUCKET_NAME = "travel-concierge-assets-qwiklabs-gcp-01-502ef792f702"

def get_storage_client():
    """Returns storage client with project ID."""
    try:
        token = subprocess.check_output(
            ["gcloud", "auth", "application-default", "print-access-token"],
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
        if token:
            return storage.Client(project=PROJECT_ID, credentials=Credentials(token))
    except Exception:
        pass
    return storage.Client(project=PROJECT_ID)

def generate_destination_image(prompt: str, tool_context: ToolContext) -> dict:
    """Generates a travel landscape or destination image based on a prompt.

    Args:
        prompt: Description of the destination image to generate (e.g., 'A beautiful sunset over Mount Fuji in Japan').
        tool_context: ADK ToolContext injected automatically for artifact saving.

    Returns:
        Dictionary containing the public Cloud Storage HTTPS URL of the generated image.
    """
    try:
        # Initialize Vertex AI client in the global region per instructions
        client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-image",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
            ),
        )

        image_bytes = None
        mime_type = "image/jpeg"

        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    image_bytes = part.inline_data.data
                    if part.inline_data.mime_type:
                        mime_type = part.inline_data.mime_type
                    break

        if not image_bytes:
            return {"error": "Failed to generate image bytes from model response."}

        timestamp = int(time.time())
        filename = f"destination_{timestamp}.jpg"

        # (1) Save artifact in Playground's Artifacts panel
        artifact_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
        tool_context.save_artifact(filename=filename, artifact=artifact_part)

        # (2) Upload image bytes to public Cloud Storage bucket
        gcs_client = get_storage_client()
        bucket = gcs_client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(image_bytes, content_type=mime_type)

        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"

        return {
            "prompt": prompt,
            "filename": filename,
            "public_url": public_url,
        }
    except Exception as e:
        return {"error": f"Image generation failed: {str(e)}"}
