import openai
import os
import re
import json

# Configure the OpenAI API key environment variable
os.environ["OPENAI_API_KEY"] = "Your OpenAI API key"
openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_chatgpt_response(prompt, model='gpt-4', temperature=0):
    """
    Fetches a response from ChatGPT given a prompt and a model.
    Compatible with models: GPT-3.5-turbo, GPT-4, and GPT-4O.
    """
    chat_response = openai.ChatCompletion.create(
        model=model,
        messages=prompt,
        temperature=temperature,
    )
    return chat_response

def extract_code_blocks(response_text, programming_language):
    """
    Retrieves code blocks from the provided text for a specific programming language.
    """
    if "```" not in response_text:
        return response_text.strip()

    code_pattern = rf'```{programming_language}(.*?)```' if f"```{programming_language}" in response_text else r'```(.*?)```'
    found_code_blocks = re.findall(code_pattern, response_text, re.DOTALL)
    return ''.join(found_code_blocks).strip()

def create_code_from_feedback(output_directory, language="python"):
    """
    Automatically generates code by processing feedback and descriptions from ChatGPT.
    Now supports multiple versions of GPT models including GPT-4 and GPT-4O.
    """
    leetcode_tasks_path = r"path/to/leetcode_tasks/leetcode.json"
    generated_code_path = r"path/to/data/chatgpt_generated_code/{}.json".format(language)

    with open(leetcode_tasks_path, 'r') as task_file:
        tasks_list = json.load(task_file)

    with open(generated_code_path, 'r') as code_file:
        code_list = json.load(code_file)

    for task in tasks_list:
        task_id = task['id']
        task_name = task['name']
        description = task['task_description']

        matching_code = next((code for code in code_list if code['id'] == task_id), None)
        code_error = matching_code['error'] if matching_code else None
        quality_issue = matching_code['is_quality_issue'] if matching_code else None

        if code_error or (quality_issue == 1):
            prompt_text = f"Please generate a code solution based on the description below:\n{description}"
            template_key = f"{language}_template"
            if template_key in task:
                prompt_text += f"\nUse the following {language} template:\n{task[template_key]}"

            conversation = [
                {"role": "system", "content": f"Task: Write a {language} program."},
                {"role": "user", "content": prompt_text},
                {"role": "assistant", "content": f"Initial code:\n{matching_code['generated_code']}"},
                {"role": "user", "content": "Identified issues with the code. Please provide an improved version."}
            ]

            result = fetch_chatgpt_response(conversation, model='gpt-4')  # Specify the model as needed
            refined_code = extract_code_blocks(result['choices'][0]['message']['content'], language)

            file_path = os.path.join(output_directory, f"{task_id}-{task_name}.{language}")
            with open(file_path, 'w') as file_writer:
                file_writer.write(refined_code)

if __name__ == "__main__":
    results_path = "path/to/data/results/"
    create_code_from_feedback(results_path, language="python")
