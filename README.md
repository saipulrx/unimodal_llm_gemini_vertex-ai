# Build Unimodal LLM apps using Google Gemini Pro 2.5 and Vertex AI

In this tutorial, we'll create simple LLM Unimodal apps using Google Gemini Pro and Vertex AI

## Setup Instructions :
1. Google Cloud Setup
    - Create a GCP project and enable:
        - Vertex AI API
    - Create service account with:
        - Vertex AI Service Agent
        - Vertex AI User
    - Generate and download JSON key
    - 
2. Installation
   - git clone this repo
    - Create python virtual env
    ```
    python -v venv .env
    ```
    - Activate new virtual env
    ```
    source .env/bin/activate
    ```
    - Install all python libraries in requirements.txt 
    ```
    pip install -r requirements.txt
    ```
    - Change value project_id, location and gcp_service_account in apps.py to your gcp account
4. Run locally
   
   Type command bellow to run apps
    ```
    python apps.py
    ```
