import sys
import io
import json
import os
import ollama

MODEL = "gemma3:1b"  # Same model as before, keep it consistent.
FILE_NAME = r"C:\Users\Adam\Desktop\Mes Projects\python\test\SelfCodeHelperAi\main.py"  # NEVER CHANGE THIS LINE

def load_code(filename):
    """Loads the code from a file.  Handles potential errors."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()
        return code
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def save_code(code, filename):
    """Saves the code to a file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)
    except Exception as e:
        print(f"Error saving file: {e}")


def analyze_code(code):
    """Analyzes the code to detect potential bugs and issues."""
    if "try...except" in code:
        print("Code contains try/except block. Consider logging or handling errors.")
    if "import" in code:
        print("Code contains 'import' statements.  Ensure these are correct and necessary.")

    # Add more sophisticated checks here as needed (e.g., variable types, function signatures)
    return True  # Placeholder -  Expand this

def chat_with_assistant(prompt):
    """Simulates a conversation with the AI assistant."""
    print("\n--- Chat with the Assistant ---")
    print(f"User: {prompt}")
    print("Assistant:  I am here to help you with your code.  How can I assist?")

    try:
        response = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
        if "message" in response and "content" in response["message"]:
            content = response["message"]["content"]
        else:
            content = str(response)

        # Basic bug detection (simplified)
        if "TypeError" in content:
            print("Potential TypeError detected.  Please review code for type mismatches.")
        if "NameError" in content:
            print("Potential NameError.  Ensure variables are defined.")

        print("Assistant:  I've analyzed your code.  It looks fine.  What would you like to do?")
        return content  # Return content for further processing
    except Exception as e:
        print(f"An error occurred during the chat: {e}")
        return None

"""
def main():
    "Main function to orchestrate the process."
    code = load_code(FILE_NAME)
    if code:
        if analyze_code(code):
            print("Code is OK!")
            if "Bug detected" in content:
                print("Bug detected!  Please review the error messages.")
            else:
                print("Code is fine.")

            # Example of saving the code
            save_code(code, FILE_NAME)
        else:
            print("Code is not valid.")
    else:
        print("Could not load code.  Exiting.")


if __name__ == "__main__":
    main()
"""
