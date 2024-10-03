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

# Load environment variables
load_dotenv()

# Retrieve folder ID and service.json file
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
FOLDER_ID = os.getenv('FOLDER_ID')

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


def fetch_rss_feed(rss_url):
    """Fetch and parse the RSS feed."""
    return feedparser.parse(rss_url)

def extract_rss_data(rss_data):
    """Extract titles and descriptions from RSS feed data."""
    soup = BeautifulSoup("", "html.parser")
    for entry in rss_data.entries:
        title = BeautifulSoup(entry.title, 'html.parser').get_text(strip=True)
        description = BeautifulSoup(entry.description, 'html.parser').get_text(strip=True).replace('&gt', '')
        wrapped_description = textwrap.fill(description, width=70)
        soup.append(f"{title}\n\n{wrapped_description}\n\n")
    return str(soup)

def save_rss_data_as_txt(rss_data, txt_file_name):
    """Save RSS feed data as a text file."""
    with open(txt_file_name, 'w', encoding='utf-8') as f:
        f.write(rss_data)
    print(f"Created: {txt_file_name}")


def txt_to_pdf(txt_file, pdf_file):
    """Convert text from a .txt file to a PDF file."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Set font for the PDF; make sure the font is available
    try:
        pdf.add_font('ArialUnicodeMS', '', 'ArialUnicodeMS.TTF', uni=True)
        pdf.set_font('ArialUnicodeMS', '', 8)
    except Exception as e:
        print(f"Could not load font: {e}. Default font will be used.")
        pdf.set_font('Arial', '', 8)  # Fallback to a default font if custom font fails

    # Read the content of the text file and add it to the PDF
    with open(txt_file, 'r', encoding='utf-8') as f:
        for line in f:
            pdf.multi_cell(0, 2, line)

    # Output the generated PDF to file
    pdf.output(pdf_file)


if __name__ == "__main__":
    # RSS feed URLs
    rss_urls = ["https://feeds.npr.org/510318/podcast.xml"]
    
    # Generate the file path for saving the RSS data
    date_str = datetime.now().strftime('%Y-%m-%d')
    file_path = f"RSS-Feed_{date_str}"
    
    # Fetch and save RSS feed data
    rss_data = "".join(extract_rss_data(fetch_rss_feed(url)) for url in rss_urls)
    txt_file_name = f"{file_path}.txt"
    save_rss_data_as_txt(rss_data, txt_file_name)

    pdf_file_name = f"{file_path}.pdf"
    txt_to_pdf(txt_file_name, pdf_file_name)
    
    # Upload the PDF to Google Drive
    upload_to_google_drive(pdf_file_name, FOLDER_ID)
