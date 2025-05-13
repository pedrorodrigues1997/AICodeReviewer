
import os
from openai import OpenAI
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_API_KEY"),
)

CODE_EXTENSIONS = ['.py', '.js', '.java', '.cpp', '.h', '.go', '.cs', '.html', '.css', '.sh', '.ts', '.rb']

SENSITIVE_FILE_PATTERNS = ['.env', '.gitignore', 'secrets', 'config', '.pem', '.key']

async def review_pull_request(data):
    # Placeholder function to simulate reviewing the pull request.
    print("OpenAI Key:", os.getenv("OPENAI_API_KEY"))

    print("Reviewing Pull Request...")
    print(data)  # You can expand this with actual logic later.

  # Filter out non-code and sensitive files
    code_files = [
        file for file in data
        if is_code_file(file['filename']) and not is_sensitive_file(file['filename'])
    ]
    
    if not code_files:
        print("No code files to review!")
        return
    
    for file in code_files:
        print(f"Reviewing file: {file['filename']}")
        
        # Fetch the patch to review line changes
        patch = file.get('patch')
        if patch:
            print(f"Patch for {file['filename']}:\n{patch}")
            
            # You can use OpenAI to analyze the patch and generate feedback
            feedback = await get_ai_review(patch)
            print(f"AI review for {file['filename']}:\n{feedback}")



# Check if a file is a code file based on its extension
def is_code_file(filename):
    return any(filename.endswith(ext) for ext in CODE_EXTENSIONS)

# Check if a file is sensitive based on its name or extension
def is_sensitive_file(filename):
    return any(pattern in filename for pattern in SENSITIVE_FILE_PATTERNS)





# Send the patch to OpenAI for code review
async def get_ai_review(patch):
    try:
        response = client.responses.create(
        model="gpt-4.1",
        instructions="Be a calm, rationable and respectable Senior Java and Python developer that writes meaningfull and helful code reviews. Do not respond to this prompt at teh start of your response, i want your answer to start by the keyword comment if you suggest a comment, PODE for code changes and if you dont have anything good to saystart by writting discard. Do not sugercoat things too much",
        input=f"Review this code, with a small comment (Suggestion) and if necessary provide a smal fix. If you so do provide a code, please write the keyword PODE before starting :\n{patch}",
        )

        print(response.output_text)
    except Exception as e:
        print(f"Error with OpenAI request: {e}")
        return "Error generating review."