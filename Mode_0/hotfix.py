import subprocess
import sys
import os

# Create simplified requirements first
with open("requirements-simple.txt", "w") as f:
    f.write("""# Core dependencies
twitchio>=2.6.0
aiohttp>=3.8.4
apscheduler>=3.10.1
websockets>=11.0.3
python-dotenv>=1.0.0
colorlog>=6.7.0
sqlalchemy>=2.0.0
""")

# Install pre-built packages only
python_path = os.path.join("venv", "Scripts", "python")
print("Installing core dependencies...")
subprocess.check_call([python_path, "-m", "pip", "install", "--upgrade", "pip"])
subprocess.check_call([python_path, "-m", "pip", "install", "-r", "requirements-simple.txt"])

print("\nSetup complete! You can add advanced packages like spacy later if needed.")