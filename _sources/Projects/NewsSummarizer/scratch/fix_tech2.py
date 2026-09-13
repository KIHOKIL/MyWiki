import re

with open('agents/tech/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

# For the calls that look like:
# response = client.models.generate_content(
#     model='gemini-3.6-flash',
#     contents=prompt,
#     config=types.GenerateContentConfig(...)
# )
# We can replace just "client.models.generate_content("
# with "safe_generate_content(client, "

# Wait, the method signature of safe_generate_content:
# def safe_generate_content(client, model, contents, config=None, max_retries=6):

# It's better to just replace the whole client.models.generate_content block
# Let's do a simple string replacement for the exact blocks:

block1 = """        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=sys_instruction,
                temperature=0.7
            )
        )"""

rep1 = """        response = safe_generate_content(
            client,
            model='gemini-3.6-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=sys_instruction,
                temperature=0.7
            )
        )"""

text = text.replace(block1, rep1)

with open('agents/tech/main.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Replacement done.")
