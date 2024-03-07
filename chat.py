import os
from openai import OpenAI
from halo import Halo
from dotenv import load_dotenv
from time import time, sleep

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_KEY"))

###     file operations

def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()

###  OpenAI chat completions call
def chatbot(conversation):
        while True:
            try:
                spinner = Halo(text='Thinking...', spinner='dots')
                spinner.start()

                response = client.chat.completions.create(
                    model="gpt-4-1106-preview",
                    messages=conversation,
                    stream=False,
                    max_tokens=2000,
                    temperature=0,
                )
                text = response.choices[0].message.content
                tokens = response.usage.total_tokens

                spinner.stop()

                return text, tokens
            except Exception as yikes:
                print(f'\n\nError communicating with OpenAI: "{yikes}"')
                exit(0)

if __name__ == '__main__':
    ## load case
    case = open_file('./data/NYT_Complaint_Dec2023.txt').replace('\n\n', '\n')

    # Create Defendant notes
    conversation = list()
    conversation.append({'role': 'system', 'content': open_file('./defendant/system_01_notes.md')})
    conversation.append({'role': 'user', 'content': case})
    notes, tokens = chatbot(conversation)

    save_file('./defendant/log_%s_notes.txt' % time(), notes)

    print('\n\nNotes:\n\n%s' % notes)

    # Create Defendant opening statement
    conversation = list()
    conversation.append({'role': 'system', 'content': open_file('./defendant/system_02_opening.md')})
    conversation.append({'role': 'user', 'content': notes})
    opening, tokens = chatbot(conversation)

    save_file('./defendant/log_%s_opening.txt' % time(), opening)

    print('\n\nOpening:\n\n%s' % opening)