# Quiz-Generator-Using-Gemini
This is a simple AI projects where one can select a file from a path and pass it to google LLM. As of now, it can only take a word and pdf file. The output of the AI is save as pdf.

You need to this first in your terminal:
pip install google-genai python-docx fpdf2

In order to run the AI, you need to have an API Key from Google AI Studio. After that, you can do any of the following:
Option 1: Pass the api key in the created client.
          Ex: client = genai.Client(api_key = "YOUR GEMINI API KEY";
Option 2: Create a new environment variable.
          - Search in your windows "Edit the system environment variables."
          - Click the environment variable... button.
          - Create new.
          - Note: The variable name should only be: GEMINI_API_KEY
          - The value is your api key. There you go!
          - But first, restart you VS Code or any.
          
