import yaml
from dotenv import load_dotenv
load_dotenv()
from langchain import hub
from langchain_core.load import dumpd

prompt = hub.pull("leonanluppi/bug_to_user_story_v1")

print("--- dumpd(prompt) ---")
print(yaml.dump(dumpd(prompt), sort_keys=False)[:500])

print("\n--- prompt.dict() ---")
# prompt.dict() might be too large
