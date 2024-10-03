# Remarkable RSS

## Overview
`remarkable-rss.py` is a Python script designed to fetch and display RSS feeds in a format suitable for the Remarkable e-reader. It enables users to stay updated on various content by converting RSS feeds into a compatible document format and sending it strait into the google drive, so that users can read it on remarkable.

## Requirements
- Python 3.x
- Feedparser library
- Any additional libraries required for rendering or converting formats

## Installation
1. Clone the repository:
2. Run `pip install -r requirements.txt`
3. Provide the RSS-Feed link inside the code.
4. Save the .json location and folder ID in a `.env` file as 
```
 SERVICE_ACCOUNT_FILE = ''
 FOLDER_ID = '' 
 ```
4. Execute and check the code if it is generating a .txt file and .pdf file.

## Setting Up Google Services Account and Enabling Google Drive API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project by clicking on the "Select a project" dropdown at the top and then "New Project."
3. Enter a name for your project and click "Create."
4. In the left sidebar, navigate to "APIs & Services" > "Library."
5. Search for "Google Drive API" and select it from the results.
6. Click on the "Enable" button to enable the Google Drive API for your project.
7. After enabling the API, navigate to "APIs & Services" > "Credentials."
8. Click on "Create Credentials" and select "Service account."
9. Fill in the details for your service account and click "Create."
10. Assign a role to your service account, such as "Editor," and click "Continue."
11. On the next screen, you can skip granting users access and click "Done."
12. In the "Service accounts" list, find your newly created service account and click on it.
13. Click on the "Add Key" dropdown and select "JSON" to create a key. This will download a JSON file containing your service account credentials.
14. Share the Google Drive folder you want to access by right-clicking the folder in Google Drive, selecting "Share," and entering the service account email address (found in the JSON file) to grant access.
15. Set the desired permissions (e.g., Viewer or Editor) and click "Send."

## Automating the Script Execution

### On Linux using Cron

1. Open the terminal.
2. Type `crontab -e` to edit the cron jobs.
3. Add the following line to execute the script every morning at 8 AM:

   ```bash
   0 8 * * * /path/to/python /path/to/remarkable-rss.py
   ```

### On Windows using Task Scheduler

1. Open the Start menu and search for "Task Scheduler."
2. Click on "Create Basic Task" in the right-hand sidebar.
3. Give your task a name (e.g., "Remarkable RSS Update") and click "Next."
4. Choose "Daily" and click "Next."
5. Set the start time and recurrence (e.g., every day) and click "Next."
6. Select "Start a Program" and click "Next."
7. In the "Program/script" box, enter the path to your Python executable (e.g., `C:\Python39\python.exe`).
8. In the "Add arguments (optional)" box, enter the path to your script (e.g., `C:\path\to\remarkable-rss.py`).
9. Click "Next," review your settings, and then click "Finish" to create the task.


### Thanks
Thanks to Remarkable for building such and amazing device.

[![rm2](https://img.shields.io/badge/rM2-supported-green)](https://remarkable.com/store/remarkable-2)
[![rmpp](https://img.shields.io/badge/rMPP-supported-green)](https://remarkable.com/store/overview/remarkable-paper-pro)
