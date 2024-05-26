import os
from openai import AzureOpenAI
from API_chatbot import ChatBot

# client = AzureOpenAI(
#   azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
#   api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
#   api_version="2024-02-01"
# )

# gpt_prompt=""
# with open("gpt-prompt.txt") as file:
#     prompt_lines = file.readlines()
#     for line in prompt_lines:
#         gpt_prompt += line + "\n"

# conversation=[{"role": "system", "content": gpt_prompt}]

# while True:
#     question = client.chat.completions.create(
#         model=os.getenv("AZURE_OPENAI_MODEL"),
#         messages=conversation,
#         temperature=1.5
#     )
#     print("\n" + question.choices[0].message.content + "\n")
#     conversation.append({"role": "assistant", "content": question.choices[0].message.content})

#     user_input = input("Ans:  >>  ")      
#     conversation.append({"role": "user", "content": f"{user_input}"})
    
#     if user_input == "done":
#         break

# conversation.append({"role": "user", "content": "done"})
    
# result = client.chat.completions.create(
#     model=os.getenv("AZURE_OPENAI_MODEL"),
#     messages=conversation,
#     temperature=0.2
# )

# print(result.choices[0].message.content)
    
    
bot = ChatBot()

initial = bot.startConversation()

print(initial)

while True:
    user_input = input(" >> ")
    if (user_input == "done"):
        break
    response = bot.generateResponse(user_input)
    print(response)

score = bot.finishConversation()

print("A!!!!!!!!!!!!!!!!1", score)




# # #print(response)
# # print(response.model_dump_json(indent=2))
# # print(response.choices[0].message.content)