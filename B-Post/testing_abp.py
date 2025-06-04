import subprocess
import requests
from docx import Document
from requests.auth import HTTPBasicAuth

# === CONFIGURATION ===
WP_API_BASE = 'https://www.dailytechdrip.com/wp-json/wp/v2'
WP_USERNAME = 'pprasoon91'
WP_APP_PASSWORD = 'E4eH 2y2C 9gay m47e CFqR uUky'  # Use a secure way to store this!

# === CLIPBOARD READER ===

def get_clipboard_content():
    try:
        clipboard_content = subprocess.check_output(
            ["xclip", "-selection", "clipboard", "-o"],
            text=True
        )
        return clipboard_content
    except Exception as e:
        print(f"Error reading clipboard: {e}")
        return ""

# === EXTRACT SEO DATA ===

def parse_seo_data(clipboard_text):
    seo_data = {
        'keyphrase': '',
        'title': '',
        'slug': '',
        'meta_description': '',
        'tags': [],
        'categories': []
    }

    # Look for SEO ELEMENTS section in clipboard data
    in_seo_block = False
    seo_lines = []
    content_lines = []

    for line in clipboard_text.splitlines():
        stripped = line.strip()

        if "SEO ELEMENTS" in stripped:
            in_seo_block = True
            continue

        if in_seo_block:
            seo_lines.append(stripped)
        else:
            content_lines.append(stripped)

    # Parse SEO lines
    for line in seo_lines:
        if line.lower().startswith("focused keyphrase"):
            seo_data['keyphrase'] = line.split(":", 1)[-1].strip()
        elif line.lower().startswith("title:"):
            seo_data['title'] = line.split(":", 1)[-1].strip()
        elif line.lower().startswith("slug:"):
            seo_data['slug'] = line.split(":", 1)[-1].strip()
        elif line.lower().startswith("meta description"):
            seo_data['meta_description'] = line.split(":", 1)[-1].strip()
        elif line.lower().startswith("tags:"):
            seo_data['tags'] = [tag.strip() for tag in line.split(":", 1)[-1].split(',')]
        elif line.lower().startswith("categories:"):
            seo_data['categories'] = [cat.strip() for cat in line.split(":", 1)[-1].split(',')]

    # Use first non-empty line as title if SEO title is not given
    title = seo_data['title'] or (next((line for line in content_lines if line), "Untitled Post"))

    # Join all content as plain HTML paragraphs
    html_body = "".join([f"<p>{line}</p>" for line in content_lines if line])

    return title, html_body, seo_data

# === WORDPRESS API FUNCTIONS ===

def get_or_create_term(name, taxonomy):
    url = f"{WP_API_BASE}/{taxonomy}"
    params = {'search': name}
    response = requests.get(url, auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD), params=params)

    if response.status_code == 200 and response.json():
        return response.json()[0]['id']
    else:
        create_resp = requests.post(url,
            auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD),
            json={'name': name}
        )
        if create_resp.status_code in (200, 201):
            return create_resp.json()['id']
        else:
            print(f"❌ Failed to create {taxonomy[:-1]}: {name}")
            return None

def publish_to_wordpress(title, body, seo):
    tag_ids = [get_or_create_term(tag, 'tags') for tag in seo.get('tags', [])]
    cat_ids = [get_or_create_term(cat, 'categories') for cat in seo.get('categories', [])]

    payload = {
        'title': title,
        'content': body,
        'status': 'pending',  # Admin review
        'slug': seo.get('slug'),
        'excerpt': seo.get('meta_description'),
        'tags': [tid for tid in tag_ids if tid],
        'categories': [cid for cid in cat_ids if cid]
    }

    post_url = f"{WP_API_BASE}/posts"
    response = requests.post(post_url,
        auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD),
        json=payload
    )

    if response.status_code in (200, 201):
        print(f"✅ Blog submitted for review: {response.json().get('link')}")
    else:
        print(f"❌ Failed to post: {response.status_code}")
        print(response.text)

# === MAIN ===

if __name__ == "__main__":
    clipboard_text = get_clipboard_content()
    if clipboard_text:
        title, body, seo = parse_seo_data(clipboard_text)
        print(f"Preparing to post: {title}")
        publish_to_wordpress(title, body, seo)
    else:
        print("❌ Clipboard is empty or could not be read.")
