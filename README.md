# Bountycaster FAQ CLI Tool

**Note: This is a test project and is not finished. It is intended for demonstration purposes only.**

This CLI tool allows users to interact with a Bountycaster FAQ bot, ask questions, and reinforce answers. It uses the OpenAI API to generate responses based on provided documentation.

## Installation Instructions

1. Ensure you have Python 3.11 or later installed on your system.

2. Install Poetry if you haven't already. You can find installation instructions [here](https://python-poetry.org/docs/#installation).

3. Clone this repository:
   ```
   git clone https://github.com/pirosb3/bountycaster-faq-ai.git
   cd bountycaster-faq-ai
   ```

4. Install the project dependencies using Poetry:
   ```
   poetry install
   ```

## Environment Variable Setup

1. Create a `.env` file in the root directory of the project.

2. Add your OpenAI API key to the `.env` file:
   ```
   PROJECT_OPENAI_KEY=your_openai_api_key_here
   ```

   Replace `your_openai_api_key_here` with your actual OpenAI API key.

## How to Run

1. Ensure you're in the project directory.

2. Run the CLI tool using Poetry:
   ```
   poetry run python openai_cli_tool/main.py
   ```

3. Follow the on-screen prompts to interact with the Bountycaster FAQ bot:
   - Choose to ask a question or exit the program.
   - If asking a question, type your question when prompted.
   - After receiving an answer, you can choose to reinforce it if desired.

4. To exit the program, select the "Exit" option from the menu.

Note: The tool reads Markdown files from a `docs` directory in the project root. Ensure this directory exists and contains the necessary documentation files before running the tool.

## Features

- Interactive CLI interface using questionary
- Streaming responses from the OpenAI API
- Option to reinforce and save improved answers
- Reads documentation from Markdown files

For any issues or questions, please open an issue in the GitHub repository.