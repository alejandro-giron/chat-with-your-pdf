# Chat with your PDF

A simple console app that lets you ask questions about a local PDF document.

## Setup

1. Create and activate a virtual environment.
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your Gemini API key as an environment variable:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```
   The app uses this key to generate embeddings and answers.
4. Run the app:
   ```bash
   python app.py
   ```

A sample PDF is included in the repository for local testing, so you can use it immediately after setup.

## Usage

When the app starts, enter the path to a local PDF file. After the document is indexed, you can enter questions about its contents.

## Tests

Run the test suite with:
```bash
python -m pytest
```
