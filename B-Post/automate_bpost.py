import requests
from docx import Document
from requests.auth import HTTPBasicAuth
from docx.shared import WD_PARAGRAPH_ALIGNMENT

# === CONFIGURATION ===

# Path to your Word document file
WORD_FILE_PATH = '/home/piyushprasoon/project/Python Learning/Python-Learning/B-Post/Apr_16.docx'

# Your WordPress site API endpoint
WP_API_BASE = 'https://www.dailytechdrip.com/wp-json/wp/v2'

# Your WordPress login credentials
WP_USERNAME = 'pprasoon91'
WP_APP_PASSWORD = 'E4eH 2y2C 9gay m47e CFqR uUky'  # Generated from WP user profile


# === SEO + CONTENT EXTRACTOR ===

def get_docx_with_seo(path):
    doc = Document(path)

    content_lines = []
    seo_data = {
        'keyphrase': '',
        'title': '',
        'slug': '',
        'meta_description': '',
        'tags': [],
        'categories': []
    }

    in_seo_block = False
    seo_lines = []
    
    # We will create a list to hold the HTML content
    html_content = []

    for para in doc.paragraphs:
        line = para.text.strip()

        # Detect the SEO section
        if "SEO ELEMENTS" in line:
            in_seo_block = True
            continue

        # Process SEO block separately
        if in_seo_block:
            seo_lines.append(line)
        else:
            # Handle content
            if para.style.name.startswith('Heading'):
                # Use the appropriate HTML tag based on the heading level
                heading_level = int(para.style.name.split()[-1][0])  # Extracts the number (e.g., 'Heading 1' -> 1)
                html_content.append(f"<h{heading_level}>{line}</h{heading_level}>")
            elif para.style.name == 'List Bullet' or para.style.name == 'List Number':
                # Handle bullet or numbered lists
                if len(html_content) == 0 or not html_content[-1].startswith('<ul>'):
                    html_content.append("<ul>")
                html_content.append(f"<li>{line}</li>")
                continue  # Skip the default content handling for lists
            else:
                # Regular content paragraphs
                html_content.append(f"<p>{line}</p>")

    # Close any open list tags
    if html_content and html_content[-1].startswith('<ul>'):
        html_content.append("</ul>")

    # Join the HTML content into a single string
    body = ''.join(html_content).strip()

    # Extract SEO data from the document
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

    # Ensure the title is taken from SEO or the first paragraph if not available
    title = seo_data['title'] or content_lines[0]
    if content_lines and content_lines[0] == title:
        content_lines = content_lines[1:]

    return title, body, seo_data


# === WORDPRESS HELPER FUNCTIONS ===

def get_or_create_term(name, taxonomy):
    """Look up a tag/category, or create it if it doesn't exist."""
    url = f"{WP_API_BASE}/{taxonomy}"
    params = {'search': name}
    response = requests.get(url, auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD), params=params)

    if response.status_code == 200 and response.json():
        return response.json()[0]['id']
    else:
        # Create the tag or category
        create_resp = requests.post(url,
            auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD),
            json={'name': name}
        )
        if create_resp.status_code in (200, 201):
            return create_resp.json()['id']
        else:
            print(f"❌ Failed to create {taxonomy[:-1]}: {name}")
            return None


# === FUNCTION TO PUBLISH TO WORDPRESS ===

def publish_to_wordpress(title, body, seo):
    # Convert tag/category names to WP IDs
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


# === MAIN EXECUTION ===

if __name__ == "__main__":
    title, body, seo = get_docx_with_seo(WORD_FILE_PATH)
    print(f"Preparing to post: {title}")
    publish_to_wordpress(title, body, seo)
