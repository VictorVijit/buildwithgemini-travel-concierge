# Travel Concierge ✈️

Travel Concierge is an AI-powered travel assistant built with the **Agent Development Kit (ADK)**, **Gemini 2.5 Flash**, and **Google Cloud**. It delivers personalized travel recommendations, calculates trip budgets, discovers nearby attractions, generates destination imagery, and remembers traveler preferences across sessions.

![Travel Concierge Demo](./demo.gif)

---

## ✨ Features & Cloud Integration

Based on the actual codebase implementation (`app/`), Travel Concierge integrates the following Google Cloud services and ADK tools:

* **Vertex AI Memory Bank**: Persists traveler preferences, dietary restrictions, allergies, and historical facts across sessions using `VertexAiMemoryBankService` and `PreloadMemoryTool`.
* **Firestore Travel Database**: Searches destinations (`search_destinations`), retrieves details (`get_destination_details`), adds new travel locations (`add_destination`), calculates trip budgets (`calculate_trip_budget`), and checks foreign exchange rates (`get_currency_exchange_rates`).
* **Google Maps Platform**: Geocodes destination addresses (`geocode_address`) and discovers nearby points of interest (`find_nearby_places`).
* **Vertex AI Imagen 3 & Cloud Storage**: Generates custom landscape images (`generate_destination_image`), uploads them to Google Cloud Storage (`gs://`), and serves public HTTPS links.
* **Agent Engine Sandbox Code Executor**: Safely executes Python code snippets in a cloud sandbox (`AgentEngineSandboxCodeExecutor`).
* **A2UI Rich Visual Rendering**: Emits A2UI schema-compliant UI cards, columns, rows, and images for rich visual display.
* **FastAPI A2A Proxy & Dialogue UI**: Communicates over the Agent-to-Agent (A2A) protocol with a clean, responsive chat interface.

---

## 🛠️ Project Structure

```
.
├── app/
│   ├── agent.py            # ADK Root Agent, Memory Bank, and tool declarations
│   ├── firestore_tools.py  # Firestore destination & budget lookup functions
│   ├── maps_tools.py       # Google Maps geocoding and places tools
│   ├── image_tools.py      # Vertex AI Imagen generation & GCS upload tool
│   └── a2ui_utils.py       # A2UI callback transformer
├── frontend/
│   ├── main.py             # FastAPI proxy communicating over A2A protocol
│   ├── static/index.html   # Dialogue chat interface with A2UI renderer & lightbox
│   └── Dockerfile          # Container specification for Cloud Run deployment
└── agents-cli-manifest.yaml # Agent Platform deployment configuration
```

---

## 🚀 Local Setup & Execution

### Prerequisites

Ensure Python 3.10+ and Google Cloud SDK (`gcloud`) are installed and authenticated.

```bash
# Authenticate with Google Cloud
gcloud auth login
gcloud auth application-default login
```

### Running Locally

1. **Install Dependencies**:

   ```bash
   pip install -r frontend/requirements.txt
   ```

2. **Set Environment Variables**:

   Set your deployed Agent Engine resource name and agent directory:

   ```bash
   export AGENT_ENGINE_RESOURCE_NAME="projects/<project-id>/locations/<region>/reasoningEngines/<resource-id>"
   export AGENT_DIRECTORY="app"
   export PORT=8080
   ```

3. **Start the Frontend Proxy Server**:

   ```bash
   python frontend/main.py
   ```

4. Open your browser and navigate to the configured port (default: port 8080) to interact with Travel Concierge.
