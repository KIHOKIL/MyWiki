import re

with open('agents/tech/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace client.models.generate_content( with safe_generate_content(client, 
# But be careful not to replace the ones inside safe_generate_content itself!

text = text.replace("    response = client.models.generate_content(", "    response = safe_generate_content(client,")

with open('agents/tech/main.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Replacement done.")
