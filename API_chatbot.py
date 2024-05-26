import os
from openai import AzureOpenAI

class ChatBot:
    def __init__(self):
        self._client = AzureOpenAI(
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
        api_version="2024-02-01"
        )

        self._gpt_prompt=""
        with open("gpt-prompt.txt") as file:
            prompt_lines = file.readlines()
            for line in prompt_lines:
                self._gpt_prompt += line + "\n"
        self._conversation=[{"role": "system", "content": self._gpt_prompt}]

    def startConversation(self) -> str:
        initial = self._client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_MODEL"),
            messages=self._conversation,
            temperature=1.5
        )
        self._conversation.append({"role": "assistant", "content": initial.choices[0].message.content})
        return initial.choices[0].message.content
    
    def generateResponse(self, user_input: str) -> str:
        self._conversation.append({"role": "user", "content": user_input})
        
        question = self._client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_MODEL"),
            messages=self._conversation,
            temperature=1.5
        )
        self._conversation.append({"role": "assistant", "content": question.choices[0].message.content})
        return question.choices[0].message.content

    def finishConversation(self) -> int:
        self._conversation.append({"role": "user", "content": "done"})
        
        question = self._client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_MODEL"),
            messages=self._conversation,
            temperature=0.2
        )
        
        return int(question.choices[0].message.content)