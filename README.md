# AI Chatbot Demo

This is a Flask-based web application featuring an AI-powered chatbot with document upload, RAG (Retrieval-Augmented Generation), and summarization capabilities.

## Features
- User authentication (demo account included)
- Chatbot interface with RAG and summarization
- File upload for document-based Q&A
- Per-user vector database
- Light purple modern UI (customizable)

## Demo Login
- **Email:** demo@cypherguard.io
- **Password:** demo@123

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <repo-directory>
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Create a `.env` file in the project root:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```

5. **Run the app:**
   ```bash
   python app.py
   ```
   The app will be available at [http://127.0.0.1:7860](http://127.0.0.1:7860)

## File Upload & RAG
- Upload documents via the chat interface to enable RAG-based Q&A.
- Uploaded files are stored per user and processed into a vector database.

## Customization
- **Theme:**
  - The color theme is defined in the Tailwind config section of the HTML files.
  - To change the gradient, edit the `custom-gradient` in `chat.html`, `signin.html`, and `signup.html`.
- **Demo User:**
  - Change or add users in `app.py` under the `User` model section.

## Folder Structure
- `app.py` - Main Flask app
- `templates/` - HTML templates
- `static/` - Images and static assets
- `uploads/` - Uploaded files (gitignored)
- `.env` - Environment variables (gitignored)

## License
This project is for demo and educational purposes. 