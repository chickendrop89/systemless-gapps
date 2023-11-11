import os
import sys
import requests

from bs4 import BeautifulSoup
from termcolor import cprint

# I/O Parameters
if len(sys.argv) != 3:
    cprint("USAGE: sf_download.py <URL> <output directory>", "black", "on_red", attrs=["bold"])
    sys.exit(1)
else:
    inputAddress = sys.argv[1]
    outputDirectory = sys.argv[2]

    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory, exist_ok=True)


def download_files_from_sourceforge(sf_url, download_dir):
    """Downloads multiple files from SourceForge directory"""
    request = requests.get(sf_url, timeout=120)
    soup = BeautifulSoup(request.content, 'html.parser')

    files = [file.a['href']for file in soup.find_all('th', headers='files_name_h')]

    for file_download_url in files:
        filename = file_download_url.split('/')[-2]

        # Skip files that already exist
        if filename not in os.listdir(download_dir):
            request = requests.get(file_download_url, timeout=120)

            with open(os.path.join(download_dir, filename), 'wb') as f:
                f.write(request.content)
                cprint(f"Downloaded {os.path.join(download_dir, filename)}", "black", "on_green", attrs=["bold"])


download_files_from_sourceforge(inputAddress, outputDirectory)
