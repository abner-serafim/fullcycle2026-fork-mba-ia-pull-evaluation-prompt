from dotenv import load_dotenv
load_dotenv()
from langchain import hub

prompt = hub.pull("leonanluppi/bug_to_user_story_v1")

print(prompt.messages)
print("\n--- Prompt variables ---")
print(prompt.input_variables)
