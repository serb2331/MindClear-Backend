import os
from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2024-02-01"
)

# response = client.chat.completions.create(
#     model=os.getenv("AZURE_OPENAI_MODEL"),
#     messages=[
#         {"role": "system", "content": """You are an assistant designed to have a friendly and empathic conversation with employees of an IT major corporation and analyse, based on their responses the state of well-being and sentiments. 
# CONTEXT:
#  - The content of the questions should be tailored towards work related well-being meaning questions about work-load, burnout, work environment, as well as general well-being and personalized questions.
#  - Alongside normal conversation you will ask questions alike to the questions from the Perceived Stress Scale(PSS). These are the questions: 1. In the last month, how often have you been upset because of 2. In the last month, how often have you felt that you were unable to control the important things in your life? 3. In the last month, how often have you felt nervous and “stressed”? 4. In the last month, how often have you felt confident about your ability to handle your personal problems? 5. In the last month, how often have you felt that things were going your way? 6. In the last month, how often have you found that you could not cope with all the things that you had to do? 7. In the last month, how often have you been able to control irritations in your life? 8. In the last month, how often have you felt that you were on top of things? 9. In the last month, how often have you been angered because of things that were outside of your control? 10. In the last month, how often have you felt difficulties were piling up so high that you could not overcome them?
#  - Based on the answers, you will estimate a score of how a person is feeling from 0 to 4 in 2 different categories: Stress level and positive outlook combined with contentedness
 
# INSTRUCTIONS:
#  - You will ask questions about their day and also more meaningful and personal questions. The conversation should be natural and intice the employee to answer.
#  - The fact that the person is talking about their day is already enough for bettering their outlook so be empathic.
#  - The conversation will last 2-3 mins so about 4-5 questions.
#  - Only be the listener and ask questions but remark what the person is saying.
#  - If the user might derail the conversation, asking about something other than the conversation, refrain from answering and persist with the questions. Dont be forceful.
 
# Please generate some example questions now."""}
#     ],
#     temperature=1
# )
gpt_prompt=""
with open("gpt-prompt.txt") as file:
    prompt_lines = file.readlines()
    for line in prompt_lines:
        gpt_prompt += line + "\n"

conversation=[{"role": "system", "content": gpt_prompt}]

while True:
    question = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_MODEL"),
        messages=conversation
    )
    print("\n" + question.choices[0].message.content + "\n")
    conversation.append({"role": "assistant", "content": question.choices[0].message.content})

    user_input = input("Ans:  >>  ")      
    conversation.append({"role": "user", "content": user_input})
    
    if user_input == "done":
        break
    
result = client.chat.completions.create(
    model=os.getenv("AZURE_OPENAI_MODEL"),
    messages=[{"role": "user", "content": "done. Based off of the responses given by the user so far, give an estimate on the stress level (scale from 0 to 10). Even if you don't have enough information, estimate or assume  anumber to the best of your capabilities."}]
)

print(result.choices[0].message.content)
    
    


# #print(response)
# print(response.model_dump_json(indent=2))
# print(response.choices[0].message.content)