import io
import re

try:
    with io.open('requirements.txt', 'r', encoding='utf-16le') as f:
        content = f.read()

    # Replace strict Django version with a compatible one
    content = re.sub(r'Django==6\.0\.1', 'Django>=4.2,<6.0', content)

    # Save it back as utf-8 (which is standard and works fine usually)
    with io.open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Fixed requirements.txt")
except Exception as e:
    print(f"Error fixing: {e}")
