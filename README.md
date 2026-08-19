# Quiz-Generator-Using-Gemini
This is a simple AI project wherein one can select a file from their file path and pass it to google LLM. As of now, it can only take a .docx and a .pdf file as an input. The output of the AI will be save as pdf— or not, it is totally fine as the output will also be printed in your Command Line Interface (CLI). 

You can also add some tweak in the prompt that were initially given. It is up to you on how you make the most of it.

For best experience, use VS Code if possible.

You need to install this first in your terminal:
pip install google-genai python-docx fpdf2

In order to request on GEMINI AI Model, you need to have an API Key from Google AI Studio. After that, you can do any of the following:
Option 1: Pass the api key in the created client.
          Ex: client = genai.Client(api_key = "YOUR GEMINI API KEY")
Option 2: Create a new environment variable.
          - Search in your windows "Edit the system environment variables."
          - Click the environment variable... button.
          - Create new.
          - Note: The variable name should only be: GEMINI_API_KEY
          - The value is your api key. There you go!
          - But first, restart you VS Code or any.
          
