import os

d = 'tests/tech'
for f in os.listdir(d):
    if f.endswith('.py'):
        path = os.path.join(d, f)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        content = content.replace('"main.', '"agents.tech.main.')
        content = content.replace("'main.", "'agents.tech.main.")
        content = content.replace('"update_topic.', '"agents.tech.update_topic.')
        
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
