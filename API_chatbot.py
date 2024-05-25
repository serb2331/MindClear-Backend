import os
from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2024-02-01"
)

gpt_prompt=""
with open("gpt-prompt.txt") as file:
    prompt_lines = file.readlines()
    for line in prompt_lines:
        gpt_prompt += line + "\n"

conversation=[{"role": "system", "content": gpt_prompt}]

def generateResponse(user_input: str) -> str:
    conversation.append({"role": "system", "content": user_input})
    
    question = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_MODEL"),
        messages=conversation,
        temperature=1.5
    )
    conversation.append({"role": "assistant", "content": question.choices[0].message.content})
    return question.choices[0].message.content

def finishConversation() -> int:
    conversation.append({"role": "system", "content": "done"})
    
    question = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_MODEL"),
        messages=conversation,
        temperature=0.2
    )
    
    return int(question.choices[0].message.content)