# AI_game_web\battles_ai\game\openai_util.py

import requests

def query_openai(prompt):
    """
    Function to query the OpenAI API with a given prompt.
    """
    api_key = 'Your-OpenAI-API-Key'  # Replace with your actual API key
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        'model': 'text-davinci-003',  # or any other suitable model
        'prompt': prompt,
        'max_tokens': 150  # Adjust as needed
    }

    response = requests.post('https://api.openai.com/v1/engines/davinci/completions', json=data, headers=headers)
    return response.json()
