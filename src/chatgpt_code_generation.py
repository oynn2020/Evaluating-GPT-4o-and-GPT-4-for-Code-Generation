import openai
import os
import re
import json

# Configure the OpenAI API key
os.environ["OPENAI_API_KEY"] = "Your OpenAI API key"
openai.api_key = os.getenv("OPENAI_API_KEY")

def retrieve_chatgpt_response(prompt, model='gpt-4', temperature=0):
    """
    Retrieves a response from ChatGPT based on the provided prompt
    """
    result = openai.ChatCompletion.create(
        model=model,
        messages=prompt,
        temperature=temperature,
    )
    return result

def extract_code_from_text(response_text, programming_lang):
    """
    Extracts and returns code segments from the response text if present
    """
    if "```" not in response_text:
        return response_text.strip()

    regex_pattern = rf'```{programming_lang}(.*?)```' if f"```{programming_lang}" in response_text else r'```(.*?)```'
    extracted_code = re.findall(regex_pattern, response_text, re.DOTALL)
    return ''.join(extracted_code).strip()

def produce_code_from_prompt(output_directory, lang="python"):
    """
    Produces code by processing tasks and prompts via ChatGPT
    """
    leetcode_tasks_file = r"path/to/leetcode_tasks/leetcode.json"
    with open(leetcode_tasks_file, 'r') as file:
        task_list = json.load(file)

    for task in task_list:
        task_id = task['id']
        task_name = task['name']
        task_description = task['task_description']

        task_prompt = f"Please provide a code implementation for the description:\n{task_description}"
        code_template_key = f"{lang}_template"
        if code_template_key in task:
            task_prompt += f"\nUse this {lang} code template:\n{task[code_template_key]}"

        interaction_messages = [{"role": "system", "content": f"Task: Write a {lang} program."}]
        interaction_messages.append({"role": "user", "content": task_prompt})
        chat_response = retrieve_chatgpt_response(interaction_messages)

        retrieved_code = extract_code_from_text(chat_response.choices[0].message.content, lang)
        file_name = f"{task_id}-{task_name}.{lang}"
        output_path = os.path.join(output_directory, file_name)

        with open(output_path, 'w') as output_file:
            output_file.write(retrieved_code)

if __name__ == "__main__":
    results_path = "path/to/data/results/code/java/"
    produce_code_from_prompt(results_path, lang="java")
