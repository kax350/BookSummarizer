import openai
import os
from time import time,sleep
import textwrap
import re


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = open_file('openaiapikey.txt')


def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def abstract_summary_extraction(transcription):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points."
                },
                {
                    "role": "user",
                    "content": transcription
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error during summary extraction: {e}")
        return None

def gpt3_completion(prompt, stop=['<<END>>']):
    max_retry = 5
    retry = 0
    while retry < max_retry:
        try:
            text = abstract_summary_extraction(prompt)
            if text is None:
                raise ValueError("Failed to generate a summary.")

            # Save the output
            filename = f'{time()}_gpt.txt'
            with open(f'gpt3_logs/{filename}', 'w') as outfile:
                outfile.write('PROMPT:\n\n' + prompt + '\n\n==========\n\nRESPONSE:\n\n' + text)

            return text
        except Exception as oops:
            retry += 1
            print(f'Error communicating with OpenAI: {oops}')
            sleep(1)
    
    return "GPT3 error: exceeded maximum retries"




if __name__ == '__main__':
    alltext = open_file('cleaned_text/input.txt')
    chunks = textwrap.wrap(alltext, 2000)
    result = list()
    count = 0
    for chunk in chunks:
        count = count + 1
        prompt = open_file('prompt.txt').replace('<<SUMMARY>>', chunk)
        prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
        summary = gpt3_completion(prompt)
        print('\n\n\n', count, 'of', len(chunks), ' - ', summary)
        result.append(summary)
    save_file('\n\n'.join(result), 'output_%s.txt' % time())
