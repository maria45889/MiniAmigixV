import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(os.path.join(Path('config/settings.py').resolve().parent.parent, '.env'), override=True)
debug_val = os.getenv('DEBUG', 'True')
print(f'DEBUG env = {repr(debug_val)}')
print(f'DEBUG result = {debug_val.lower() == "true"}')
