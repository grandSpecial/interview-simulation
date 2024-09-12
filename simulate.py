from openai import OpenAI
from termcolor import colored
import datetime
from pinecone import Pinecone, ServerlessSpec
import signal
import os  
from dotenv import load_dotenv
load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ORGANIZATION_ID = os.getenv("ORGANIZATION_ID")
PINECONE_KEY = os.getenv("PINECONE_KEY")

pinecone_client = Pinecone(api_key=PINECONE_KEY)

client = OpenAI(api_key=OPENAI_API_KEY, organization=ORGANIZATION_ID)

def retrieve(id: str, index: str):
    with pinecone_client.Index(index) as pinecone_index:
      results = pinecone_index.fetch(ids=[id])
      metadata = results['vectors'][id]['metadata']
    return metadata['text']

def create_response(last_message):
    completion = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[
            {"role": "system", "content": os.getenv("SYSTEM_PROMPT")},
            {"role": "user", "content": last_message}
        ],
        stream=True
    )
    chunks = []
    print(colored("\nFounder:", 'green', attrs=['bold']))
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            m = chunk.choices[0].delta.content
            print(colored(m, 'green'), end='', flush=True)
            chunks.append(m)
    print("\n" + "-"*50)
    return "".join(chunks)

def save_conversation(conversation):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"./logs/conversation_{timestamp}.txt"
    with open(filename, 'w') as f:
        for entry in conversation:
            f.write(f"{entry['role']}: {entry['content']}\n\n")
    print(colored(f"\nConversation saved to {filename}", 'yellow', attrs=['bold']))

def start_chat(assistant_id):
    """Start a command-line chat between an assistant and a chat completion."""
    
    thread = client.beta.threads.create()
    thread_id = thread.id
    print(colored("Starting conversation with assistant. Type 'exit' to end.\n", 'yellow', attrs=['bold']))
    last_response = None
    conversation = []

    try:
    
        while True:
            # Simulated founder's response
            if last_response:
                user_message = create_response(last_response)
            else:
                doc_id = os.getenv("DOC_ID")
                index = os.getenv("INDEX")

                source_doc = retrieve(doc_id,index)
                user_message = source_doc
                print(colored("\nFounder:", 'green', attrs=['bold']))
                #print the file contents
                #print(colored(user_message, 'green'))
                print(colored("REPORT CONTEXT APPENDED", "green"))
                print("-"*50)
            
            conversation.append({"role": "Founder", "content": user_message})
            
            # Post the user's message to the thread
            client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=user_message,
            )
            
            # Stream the analyst/assistant response
            stream = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
                stream=True
            )
            chunks = []
            print(colored("\nAnalyst:", 'blue', attrs=['bold']))
            for event in stream:
                if event.event == 'thread.message.delta':
                    response_text = event.data.delta.content[0].text.value
                    chunks.append(response_text)
                    print(colored(response_text, 'blue'), end='', flush=True)
            
            last_response = "".join(chunks)
            conversation.append({"role": "Analyst", "content": last_response})
            print("\n" + "-"*50)
            
            if "[HIDDEN]" in last_response:
                print(colored("\n[HIDDEN] found in Analyst's response. Ending conversation.", 'red', attrs=['bold']))
                save_conversation(conversation)
                break

    except KeyboardInterrupt:
        print(colored("\nCtrl+C detected. Saving conversation before exit...", 'red', attrs=['bold']))
        save_conversation(conversation)
        print(colored("Conversation saved. Exiting now.", 'yellow', attrs=['bold']))

if __name__ == "__main__":
    assistant_id = os.getenv("ASSISTANT_ID")
    start_chat(assistant_id)