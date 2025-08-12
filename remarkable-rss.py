import os
import feedparser
from datetime import datetime
import textwrap
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fpdf import FPDF
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
import requests
import xml.etree.ElementTree as ET
from smolagents import VisitWebpageTool, LiteLLMModel

# Load environment variables
load_dotenv()

# Retrieve folder ID and service.json file
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
FOLDER_ID = os.getenv('FOLDER_ID')
model_id = os.getenv('MODEL_ID')

# Validate the presence of required environment variables
if not SERVICE_ACCOUNT_FILE or not FOLDER_ID:
    raise ValueError("Both SERVICE_ACCOUNT_FILE and FOLDER_ID environment variables must be set.")

# Define the scopes for Google Drive access
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def upload_to_google_drive(file_path, folder_id=None):
    """Upload a file to Google Drive."""
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    file_metadata = {
        'name': os.path.basename(file_path),
        'mimeType': 'application/pdf',  # Assuming you are uploading a PDF file
    }
    if folder_id:  # Include folder_id if provided
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(file_path, mimetype='application/pdf')
    try:
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Uploaded to Google Drive with file ID: {file.get('id')}")
    except Exception as e:
        print(f"Upload to Google Drive failed: {e}")


def fetch_rss_feed(url):
    """
    Fetch news items from the given RSS feed URL.
    Args:
        url (str): The URL of the RSS feed to fetch.

    Returns:
        list: A list of news links.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        root = ET.fromstring(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []

    data = []
    for item in root.findall('.//item'):
        title = item.find('title').text
        link = item.find('link').text
        data.append({"title":title, "link":link})
    return data[:5]

def process_rss_links(links):
    web_reader = VisitWebpageTool()
    model = LiteLLMModel(
    model_id=model_id)

    for item in links:
        model_response = model([
        {"system": "Identify the news description from the provided text, remove the title from it, then print the news description in human readable text",
        "role":"user",
        "content":web_reader(item['link'])
        }])
        item['model_response'] = model_response.content
    return links

def save_rss_data_as_txt(rss_data, txt_file_name):
    """Save RSS feed data as a text file."""
    with open(txt_file_name, 'w', encoding='utf-8') as f:
        for item in rss_data:
            f.write(textwrap.fill(item['title'], width=100) + '\n')
            f.write(textwrap.fill(item['model_response'], width=100) + '\n\n')
    print(f"Created: {txt_file_name}")


def txt_to_pdf(txt_file, pdf_file):
    """Convert text from a .txt file to a PDF file."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Set font for the PDF; make sure the font is available
    try:
        pdf.add_font('ArialUnicodeMS', '', 'ArialUnicodeMS.TTF', uni=True)
        pdf.set_font('ArialUnicodeMS', '', 10)
    except Exception as e:
        print(f"Could not load font: {e}. Default font will be used.")
        pdf.set_font('Arial', '', 10)  # Fallback to a default font if custom font fails

    # Read the content of the text file and add it to the PDF
    with open(txt_file, 'r', encoding='utf-8') as f:
        for line in f:
            pdf.multi_cell(0, 6, line)

    # Output the generated PDF to file
    pdf.output(pdf_file)


if __name__ == "__main__":
    # RSS feed URLs
    rss_urls = ["https://www.onmanorama.com/kerala.feeds.onmrss.xml","https://timesofindia.indiatimes.com/rssfeedstopstories.cms", "https://timesofindia.indiatimes.com/rssfeeds/30359486.cms", "https://timesofindia.indiatimes.com/rssfeeds/-2128672765.cms"]
    
    # Generate the file path for saving the RSS data
    date_str = datetime.now().strftime('%Y-%m-%d')
    file_path = f"RSS-Feed_{date_str}"
    
    # Fetch and save RSS feed data
    rss_links = [link for url in rss_urls for link in fetch_rss_feed(url)]
    rss_data = process_rss_links(rss_links)

    txt_file_name = f"{file_path}.txt"
    save_rss_data_as_txt(rss_data, txt_file_name)

    pdf_file_name = f"{file_path}.pdf"
    txt_to_pdf(txt_file_name, pdf_file_name)
    
    # Upload the PDF to Google Drive
    upload_to_google_drive(pdf_file_name, FOLDER_ID)
