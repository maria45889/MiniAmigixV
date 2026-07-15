import re

file_path = r'C:\Users\majo1\Desktop\MiniAmigixV\templates\blog\blog.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_form_style = '''
  /* ── Formulario Modal ─────────────────────────────────── */
  .create-post-panel {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 20px;
    margin-bottom: 40px;
    backdrop-filter: blur(20px);
    overflow: hidden;
    animation: fadeSlideUp 0.4s ease;
  }
  .create-post-form-inner {
    padding: 30px;
  }
  .create-post-form-inner h3 {
    font-size: 1.5rem;
    color: #e2e8f0;
    margin-bottom: 24px;
    border-bottom: 1px solid rgba(99,102,241,0.15);
    padding-bottom: 15px;
  }
  .form-group label {
    display: block;
    font-size: 0.85rem;
    font-weight: 600;
    color: #a5b4fc;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .form-group input[type="text"],
  .form-group textarea,
  .form-group select {
    width: 100%;
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 12px;
    padding: 14px 16px;
    color: #f1f5f9;
    font-size: 1rem;
    margin-bottom: 20px;
    transition: all 0.3s;
    outline: none;
    font-family: 'Inter', sans-serif;
  }
  .form-group input[type="text"]:focus,
  .form-group textarea:focus,
  .form-group select:focus {
    border-color: rgba(99,102,241,0.6);
    background: rgba(99,102,241,0.05);
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15);
  }
  .form-group input[type="file"] {
    background: rgba(255,255,255,0.05);
    padding: 10px;
    border-radius: 12px;
    border: 1px dashed rgba(99,102,241,0.4);
    width: 100%;
    color: #a5b4fc;
    margin-bottom: 20px;
  }
  .form-group-check {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
  }
  .form-group-check input[type="checkbox"] {
    width: 18px;
    height: 18px;
    accent-color: #6366f1;
  }
  .form-group-check label {
    font-size: 0.95rem;
    color: #e2e8f0;
  }
  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 15px;
    margin-top: 30px;
  }
  .btn-cancel {
    background: rgba(255,255,255,0.1);
    color: #e2e8f0;
    border: none;
    padding: 12px 24px;
    border-radius: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }
  .btn-cancel:hover { background: rgba(255,255,255,0.15); }
  .btn-submit {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    color: #fff;
    border: none;
    padding: 12px 30px;
    border-radius: 12px;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(99,102,241,0.4);
    transition: all 0.2s;
  }
  .btn-submit:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(99,102,241,0.5); }
</style>
'''

if '/* ── Formulario Modal ─────────────────────────────────── */' not in content:
    content = content.replace('</style>', new_form_style)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Blog updated")
