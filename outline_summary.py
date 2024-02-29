import os
import openai

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

openai.api_key = open_file('openaiapikey.txt')

def summarize_text(text):
    """
    使用 OpenAI Assistants API 对给定文本进行总结。
    """
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Help me summarise the content of this text in detail as OUTLINE: {text}"}
        ]
    )
    return response.choices[0].message['content']

def summarize_files_in_directory(directory_path, output_file_path):
    summaries = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                text = file.read()
                summary = summarize_text(text)
                summaries.append(summary)

    # 将所有总结保存到一个指定的文本文件中
    with open(output_file_path, 'w') as file:
        for summary in summaries:
            file.write(summary + '\n\n')

if __name__ == "__main__":
    directory_path = 'spilt_text_for_outline'
    output_file_path = 'outline.txt'
    summarize_files_in_directory(directory_path, output_file_path)
