import base64
import json
import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
from openai import OpenAI
import replicate

from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("./config.txt")

# print("this should be the key ", config_object["USERINFO"]['GPT_API_KEY'])

vertexai.init(project="trusty-ether-313614", location="us-central1")
client = OpenAI(api_key=config_object["USERINFO"]['GPT_API_KEY'])
os.environ["REPLICATE_API_TOKEN"] = config_object["USERINFO"]['LLAMA_API_KEY']

model = "llama" # "gpt" # "gemini"

content = "Alle EU-landen moeten een evenredig aandeel asielzoekers opnemen."

# load model settings from JSON file
with open('model_settings.json') as json_file:
    settings = json.load(json_file)

model_settings = settings[model]

# safety_settings = {
# generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
# generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
# generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
# generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
# }

# responses = GenerativeModel(model_settings['model'], system_instruction=model_settings['system_instruction']).generate_content(
#     [f"""The statement is: {content}"""],
#     generation_config=model_settings['generation_config'],
#     safety_settings=safety_settings,
#     stream=False,
# )

# print(responses.text)

# model_settings['messages'][1]['content'] = model_settings['messages'][1]['content'].format(content=content)
# response = client.chat.completions.create(**model_settings)
# completion = response.choices[0].message.content.strip()

# print(completion)

model_settings['input']['prompt'] = model_settings['input']['prompt'].format(content=content)
response = replicate.run(model_settings['model'], input=model_settings['input'])
completion = "".join(response)

print(completion)
