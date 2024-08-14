import os
import glob
from openai import OpenAI
from dotenv import load_dotenv
import questionary
import tiktoken

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("PROJECT_OPENAI_KEY"))

def read_markdown_files(docs_folder):
    markdown_content = ""
    for filename in glob.glob(os.path.join(docs_folder, "**/*.md"), recursive=True):
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
            doc_name = os.path.basename(filename)
            markdown_content += f"<<{doc_name}>>\n{content}\n\n<<END {doc_name}>>\n"

    if not markdown_content:
        raise FileNotFoundError("No markdown files found in the docs folder.")

    enc = tiktoken.encoding_for_model("gpt-4")
    response = enc.encode(markdown_content)
    print(f"Num tokens: {len(response)}")
    return markdown_content

def get_chat_completion_stream(prompt, context):
    try:
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Your name is @bountybotfaq, the official assistant bot for Bountycaster. You are here to answer your questions about Bountycaster. If you are unsure, you can tag @Linda for help. All your replies will fit within a single tweet (320 characters max) and every tweet should be complete and self descriptive. Do not add hashtags",
                },
                {
                    "role": "system",
                    "content": f"Here's the context from the documentation:\n\n{context}",
                },
                {"role": "user", "content": prompt},
            ],
            stream=True,
        )
        return stream
    except Exception as e:
        return f"An error occurred: {str(e)}"

def print_streaming_response(stream):
    full_response = ""
    print("\n@bountybotfaq: ", end="", flush=True)
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_response += content
    print("\n")
    return full_response

def reinforce_answer(question, answer):
    reinforced_answer = questionary.text(
        "Please provide the reinforced answer:",
        default=answer
    ).ask()
    
    reinforced_content = f"Q: {question}\nA: {reinforced_answer}\n\n"
    
    os.makedirs("docs", exist_ok=True)
    with open("docs/reinforced.md", "a", encoding="utf-8") as file:
        file.write(reinforced_content)
    
    print("Answer reinforced and saved successfully.")

def main():
    print("Welcome to the Bountycaster FAQ CLI tool!")
    print("Loading documentation...")

    try:
        context = read_markdown_files("./docs")
        print("Documentation loaded successfully.")
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        return

    while True:
        action = questionary.select(
            "What would you like to do?", choices=["Ask a question", "Exit"]
        ).ask()

        if action == "Exit":
            print("Thank you for using the Bountycaster FAQ CLI tool. Goodbye!")
            break

        if action == "Ask a question":
            user_input = questionary.text(
                "What is your question about Bountycaster?"
            ).ask()
            if user_input:
                stream = get_chat_completion_stream(user_input, context)
                answer = print_streaming_response(stream)
                
                reinforce = questionary.confirm("Would you like to reinforce this answer?").ask()
                if reinforce:
                    reinforce_answer(user_input, answer)
                    context = read_markdown_files("./docs")
            else:
                print("Please enter a valid input.")

if __name__ == "__main__":
    main()