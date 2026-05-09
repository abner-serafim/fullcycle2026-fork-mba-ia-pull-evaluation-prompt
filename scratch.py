from dotenv import load_dotenv
load_dotenv()
from langchain import hub
prompt = hub.pull("leonanluppi/bug_to_user_story_v1")
print(type(prompt))
if hasattr(prompt, 'dict'):
    print("Has dict")
if hasattr(prompt, 'to_json'):
    print("Has to_json")
# try to see its structure
# Let's save it to a file
from langchain_core.load import dumpd
data = dumpd(prompt)
print(type(data))
print(data.keys())
