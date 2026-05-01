import base64
import os

def embed_logo():
    logo_path = 'assets/logo.png'
    html_path = 'dashboard/index.html'
    
    if not os.path.exists(logo_path):
        print("Logo not found")
        return

    with open(logo_path, 'rb') as f:
        b64_string = base64.b64encode(f.read()).decode()
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Substituir no favicon e na logo do nav
    new_html = html_content.replace('href="assets/logo.png"', f'href="data:image/png;base64,{b64_string}"')
    new_html = new_html.replace('src="assets/logo.png"', f'src="data:image/png;base64,{b64_string}"')
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Logo embedded successfully in HTML")

if __name__ == "__main__":
    embed_logo()
