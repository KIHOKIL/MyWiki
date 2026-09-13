import re

with open('agents/tech/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r"client\.models\.generate_content\(\s*model='gemini-3\.6-flash',\s*contents=prompt\s*\)"
replacement = "safe_generate_content(client, 'gemini-3.6-flash', prompt)"

new_text = re.sub(pattern, replacement, text)

with open('agents/tech/main.py', 'w', encoding='utf-8') as f:
    f.write(new_text)

print('Replaced occurrences in tech/main.py:', len(re.findall(r"safe_generate_content", new_text)))
