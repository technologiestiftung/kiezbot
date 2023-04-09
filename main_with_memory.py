import os
import subprocess
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from utils.gtts_synthing import synthing


def getCharacter(code):
    characterRFID = {
    "1":0,
    "2":1,
    "3":2,
    "4": 3,
    "5": 4,
    "0004632310": 0, 
    "0001427161": 1,
    "0004663272": 2,
    "0001384652": 3,
    "0001416771": 4
    }

    if code in characterRFID:
        return characterRFID[code]
    else:
        return "Invalid character code " + code


def getPrompt(key):
    with open("tests/memory/characters.txt", "r", encoding="utf-8") as file:
        prompt_templates = [line.strip() for line in file.readlines()]
    prompts = [PromptTemplate(input_variables=['history', 'input'], output_parser=None, partial_variables={}, template=template) for template in prompt_templates]
    return prompts[key]


def makeConversation(chain):
     # Sending an empty user input first to let the AI start the conversation
    user_input = ""
    
    # greeting audio is in a subprocess in order not to block the main thread
    subprocess.Popen(["afplay", "audio/bee_greetings.mp3"])
    
    reply = chain.predict(input=user_input)
    print(reply)

    while user_input.lower() != "q":
        user_input = input("Enter input (or 'q' to quit): ")

        if user_input.lower() != "q":
            subprocess.Popen(["afplay", "audio/bee_wait.mp3"])
            reply = chain.predict(input=user_input)
            print(reply)
            synthing(reply)
            play_audio("reply")

def play_audio(audio):
    os.system("afplay " + "output_gtts.mp3")

def main():
    os.system("clear")
    load_dotenv()
    
    ## VOICE OUTPUT CURRENTLY ONLY WORKS WITH CHARACTER 1 (BEE)
    characterCode = input("Charakter auswählen (1-5) oder RFID Chip auflegen: ")
    prompt = getPrompt(getCharacter(characterCode))
    
    chatgpt = ChatOpenAI(model_name='gpt-3.5-turbo', openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0)
    chain = ConversationChain(llm=chatgpt, verbose=False, memory=ConversationBufferMemory(), prompt=prompt)
    makeConversation(chain)

if __name__ == '__main__':
    main()