from pathlib import Path
from bs4 import BeautifulSoup

path = Path(r'c:\Users\majo1\Desktop\MiniAmigixV\templates\configuracion\configuracion.html')
html = path.read_text(encoding='utf-8')
soup = BeautifulSoup(html, 'html.parser')
tabs = soup.select('.config-tab-content')
print('tabs', len(tabs))
for t in tabs:
    print('TAB', t.get('id'), 'ACTIVE' if 'active' in (t.get('class') or []) else '')