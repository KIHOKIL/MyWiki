import os
import sys
import json
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def update_config(issue_title, issue_body):
    """Uses Gemini to generate an updated config.json based on a GitHub Issue."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set.")
        sys.exit(1)

    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            current_config = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find config file at {config_path}")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    
    prompt = f"""
You are an expert configuration manager for an AI News Summarizer.
The current configuration defines news categories, search queries, and AI focus prompts.

Current `config.json`:
```json
{current_config}
```

The user wants to update the topics. They submitted a GitHub Issue with the following details:
Issue Title: {issue_title}
Issue Body: {issue_body}

Your task:
1. Understand the user's intent. If they want to add a topic, create a new category object. If they want to modify or remove, adjust the existing JSON.
2. If adding a new topic, generate a relevant `name`, 3-5 specific English Google News search `queries`, and a detailed Korean `focus` prompt that tells the AI what to extract from the news.
3. Return ONLY valid JSON representing the entire updated `config.json`. Do NOT include markdown code blocks (like ```json), just the raw JSON text.

Output the final JSON string:
"""

    print("Calling Gemini to process the update...")
    # NOTE: user mentioned gemini-2.5-* models returned 404 earlier and they replaced with 3.5-flash.
    # Let's use gemini-3.5-flash here.
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                response_mime_type="application/json"
            )
        )
        new_config_str = response.text.strip()
    except Exception as e:
        print(f"Gemini API failed: {e}")
        print("Falling back to OpenAI (gpt-4o-mini)...")
        from openai import OpenAI
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            print("Error: OPENAI_API_KEY environment variable is not set for fallback.")
            sys.exit(1)
            
        openai_client = OpenAI(api_key=openai_api_key)
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a JSON generator. Output only valid JSON without markdown formatting. The output must be pure JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            new_config_str = response.choices[0].message.content.strip()
        except Exception as oe:
            print(f"Error calling OpenAI fallback: {oe}")
            sys.exit(1)
    
    # Strip out any potential markdown blocks or SDK warnings appended by the model
    if new_config_str.startswith("```json"):
        new_config_str = new_config_str[7:]
    if new_config_str.startswith("```"):
        new_config_str = new_config_str[3:]
    if new_config_str.endswith("```"):
        new_config_str = new_config_str[:-3]
        
    new_config_str = new_config_str.strip()
    
    # Find the first { and the last }
    start_idx = new_config_str.find('{')
    end_idx = new_config_str.rfind('}')
    
    if start_idx != -1 and end_idx != -1:
        new_config_str = new_config_str[start_idx:end_idx+1]
    
    # Verify it's valid JSON
    try:
        new_config = json.loads(new_config_str)
        if "categories" not in new_config:
            raise ValueError("The generated JSON is missing the 'categories' key.")
    except Exception as e:
        print("Error: Gemini returned invalid JSON.")
        print(f"Exception: {e}")
        print("Raw output:")
        print(new_config_str)
        sys.exit(1)

    # Save it back
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(new_config, f, indent=2, ensure_ascii=False)
        
    print("Successfully updated config.json!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update config.json via IssueOps")
    parser.add_argument("--title", type=str, required=True, help="GitHub Issue Title")
    parser.add_argument("--body", type=str, default="", help="GitHub Issue Body")
    args = parser.parse_args()
    
    update_config(args.title, args.body)
