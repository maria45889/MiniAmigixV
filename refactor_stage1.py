import os

views_path = r'C:\Users\majo1\Desktop\MiniAmigixV\apps\app\views.py'
constants_path = r'C:\Users\majo1\Desktop\MiniAmigixV\apps\app\constants.py'

# 1. Read views.py
with open(views_path, 'r', encoding='utf-8') as f:
    views_content = f.read()
    lines = views_content.split('\n')

# Extract 'recomendaciones' dictionary
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if 'def entretenimiento(request):' in line:
        start_idx = i
        break

if start_idx != -1:
    for i in range(start_idx, len(lines)):
        if 'return render(request, \'entretenimiento.html\'' in lines[i]:
            end_idx = i
            break

# The block to extract
if start_idx != -1 and end_idx != -1:
    recomendaciones_lines = lines[start_idx+1:end_idx]
    recomendaciones_str = '\n'.join(recomendaciones_lines).strip()
    
    # Write to constants.py
    with open(constants_path, 'w', encoding='utf-8') as f:
        f.write("# Constantes y datos estáticos de la aplicación\n\n")
        f.write("RECOMENDACIONES_ENTRETENIMIENTO = {\n")
        # Removing the 'recomendaciones = {' part since we declare it above
        first_bracket_idx = recomendaciones_str.find('{')
        if first_bracket_idx != -1:
            f.write(recomendaciones_str[first_bracket_idx+1:])
            
    print("Created constants.py with RECOMENDACIONES_ENTRETENIMIENTO.")
    
    # Replace in views.py
    new_views_content = views_content.replace(
        '\n'.join(recomendaciones_lines),
        "    recomendaciones = RECOMENDACIONES_ENTRETENIMIENTO"
    )
    
    # We also need to add the import at the top of views.py
    import_statement = "from .constants import RECOMENDACIONES_ENTRETENIMIENTO\n"
    if import_statement not in new_views_content:
        # Find the first 'from ' or 'import '
        for i, line in enumerate(new_views_content.split('\n')):
            if line.startswith('from ') or line.startswith('import '):
                new_views_lines = new_views_content.split('\n')
                new_views_lines.insert(i, import_statement)
                new_views_content = '\n'.join(new_views_lines)
                break
                
    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(new_views_content)
    
    print("Updated views.py to use RECOMENDACIONES_ENTRETENIMIENTO.")
