import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, Content
import google.auth # Import google.auth for loading service account credentials

# --- Configuration ---
# Replace with your Google Cloud Project ID and desired location
PROJECT_ID = "your-google-cloud-project-id" # e.g., "my-gemini-project-12345"
LOCATION = "us-central1" # Or another supported Vertex AI region for Gemini

# --- Service Account Configuration ---
# IMPORTANT: Replace "path/to/your/service-account-key.json" with the actual path
# to your service account JSON key file.
# Make sure this file is kept secure and not committed to public repositories.
SERVICE_ACCOUNT_KEY_FILE = "path/to/your/service-account-key.json"

# Initialize Vertex AI
# This assumes you've authenticated using a service account JSON key file
try:
    # Load credentials from the service account key file
    credentials, project_id = google.auth.load_credentials_from_file(SERVICE_ACCOUNT_KEY_FILE)
    vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)
    print(f"Vertex AI initialized for project: {PROJECT_ID} in region: {LOCATION} using service account.")
except Exception as e:
    print(f"Error initializing Vertex AI: {e}")
    print("Please ensure your Google Cloud project ID and location are correct,")
    print("and the 'SERVICE_ACCOUNT_KEY_FILE' path points to a valid service account JSON key.")
    print("\n--- Troubleshooting Service Account Setup ---")
    print("1. Create a Service Account: Go to Google Cloud Console > IAM & Admin > Service Accounts.")
    print("2. Grant Permissions: Ensure the service account has the 'Vertex AI User' role (roles/aiplatform.user)")
    print("   or equivalent permissions on your Google Cloud project.")
    print("3. Create Key: For the created service account, go to 'Keys' tab > 'Add Key' > 'Create new key' > 'JSON'.")
    print("   Download this JSON file and update 'SERVICE_ACCOUNT_KEY_FILE' with its path.")
    print("-------------------------------------------\n")
    exit()

# Load the Gemini 1.5 Pro model
MODEL_NAME = "gemini-2.5-pro" # Using a stable version for wider availability
model = GenerativeModel(MODEL_NAME)
print(f"Successfully loaded model: {MODEL_NAME}")

# --- Helper Function to Interact with Gemini ---
def generate_text_with_gemini(prompt_text: str, is_conversation: bool = False):
    """
    Sends a text prompt to Gemini and prints the response.
    If is_conversation is True, it uses the chat history.
    """
    print("\n--- Gemini's Response ---")
    try:
        if is_conversation:
            # For conversations, we use the `start_chat` method to maintain context
            # In this simple example, `start_chat` would re-initialize the conversation
            # For a persistent chat, you'd keep the `chat` object active across calls.
            # Here, we'll simulate a single turn within a 'conversation' context.
            chat = model.start_chat()
            response = chat.send_message(prompt_text)
        else:
            response = model.generate_content(prompt_text)

        print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your prompt or try a different task.")
        print("Ensure the service account has the necessary IAM permissions (e.g., 'Vertex AI User') for your project.")
    print("-------------------------\n")

# --- Main Application Logic ---
def main():
    while True:
        print("\n--- Gemini LLM App (Unimodal Text) ---")
        print("Select a task for Gemini Pro:")
        print("1. Generate a Story/Poem/Article")
        print("2. Answer a Question")
        print("3. Summarize Content")
        print("4. Translate Languages")
        print("5. Generate Code")
        print("6. Engage in Conversation")
        print("7. Exit")
        print("-------------------------------------")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            print("\n--- Generate Text (Story/Poem/Article) ---")
            topic = input("Enter a topic for the story/poem/article: ")
            prompt = (
                f"Write a creative and engaging piece (story, poem, or article) "
                f"about the following topic: '{topic}'. "
                f"Make it at least 200 words long. Focus on imaginative details."
            )
            generate_text_with_gemini(prompt)

        elif choice == '2':
            print("\n--- Answer a Question ---")
            question = input("Ask Gemini a question: ")
            prompt = f"Answer the following question clearly and concisely: '{question}'."
            generate_text_with_gemini(prompt)

        elif choice == '3':
            print("\n--- Summarize Content ---")
            content_to_summarize = input("Paste the content you want to summarize: ")
            length_preference = input("Desired summary length (e.g., 'short', 'detailed', '3 bullet points'): ")
            prompt = (
                f"Summarize the following content. "
                f"Desired length/format: {length_preference}.\n\n"
                f"Content: {content_to_summarize}"
            )
            generate_text_with_gemini(prompt)

        elif choice == '4':
            print("\n--- Translate Languages ---")
            text_to_translate = input("Enter the text to translate: ")
            target_language = input("Enter the target language (e.g., 'French', 'Spanish', 'Japanese'): ")
            prompt = (
                f"Translate the following text into {target_language}. "
                f"Provide only the translated text.\n\n"
                f"Text: '{text_to_translate}'"
            )
            generate_text_with_gemini(prompt)

        elif choice == '5':
            print("\n--- Generate Code ---")
            code_request = input("Describe the code you want Gemini to generate (e.g., 'Python function to calculate factorial'): ")
            language = input("In which programming language? (e.g., 'Python', 'JavaScript', 'Java'): ")
            prompt = (
                f"Generate a {language} code snippet for the following request: "
                f"'{code_request}'. Include comments and make it functional."
            )
            generate_text_with_gemini(prompt)

        elif choice == '6':
            print("\n--- Engage in Conversation ---")
            print("Type 'quit' to end the conversation session.")
            conversation_history = []
            while True:
                user_message = input("You: ")
                if user_message.lower() == 'quit':
                    print("Ending conversation.")
                    break

                # Build the prompt with history
                full_prompt = "You are engaging in a conversation. Respond naturally.\n\n"
                for role, text in conversation_history:
                    full_prompt += f"{role}: {text}\n"
                full_prompt += f"User: {user_message}"

                # Send message and get response
                try:
                    chat = model.start_chat(history=[
                        Content(role="user", parts=[Part.from_text(m[1])]) if m[0] == "User" else Content(role="model", parts=[Part.from_text(m[1])])
                        for m in conversation_history
                    ])
                    response = chat.send_message(user_message)
                    gemini_response = response.text
                except Exception as e:
                    gemini_response = f"An error occurred during conversation: {e}"

                print(f"Gemini: {gemini_response}")

                # Update conversation history
                conversation_history.append(("User", user_message))
                conversation_history.append(("Gemini", gemini_response))

        elif choice == '7':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()