import sys
import os
import requests
import zipfile
import shutil
import time
import ctypes
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QIcon
from threading import Thread

def get_default_branch():
    """Fetch the default branch of the GitHub repo"""
    repo_owner = "pschilly"
    repo_name = "gtfo-liveries"
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    headers = {"User-Agent": "DCS-Livery-Updater"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("default_branch", "main")
    return "main"

def log_message(message):
    """Logs messages to a file in the install directory"""
    install_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    log_file = os.path.join(install_dir, "livery_updater.log")
    with open(log_file, "a") as log:
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def download_and_extract():
    """Downloads and installs the latest liveries"""
    log_message("Starting livery update...")
    repo_owner = "pschilly"
    repo_name = "gtfo-liveries"
    default_branch = get_default_branch()
    zip_url = f"https://github.com/{repo_owner}/{repo_name}/archive/refs/heads/{default_branch}.zip"
    
    temp_dir = os.path.join(os.environ['TEMP'], "DCS_Livery_Updater")
    zip_path = os.path.join(temp_dir, "DCS_Liveries.zip")
    extract_path = os.path.join(temp_dir, "extracted")
    dcs_liveries_path = os.path.join(os.path.expanduser("~"), "Saved Games", "DCS", "Liveries")
    
    # Ensure temp directory exists
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # Download ZIP file
    response = requests.get(zip_url, stream=True)
    with open(zip_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
    log_message("Download completed.")
    
    # Extract ZIP
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    log_message("Extraction completed.")
    
    # Find extracted folder
    extracted_folder = os.path.join(extract_path, f"{repo_name}-{default_branch}")
    
    # Copy liveries to DCS folder
    liveries_source = os.path.join(extracted_folder, "Liveries")
    if os.path.exists(liveries_source):
        if not os.path.exists(dcs_liveries_path):
            os.makedirs(dcs_liveries_path)
        for item in os.listdir(liveries_source):
            src_path = os.path.join(liveries_source, item)
            dst_path = os.path.join(dcs_liveries_path, item)
            if os.path.exists(dst_path):
                shutil.rmtree(dst_path, ignore_errors=True)
            shutil.copytree(src_path, dst_path)
    log_message("Liveries copied to destination.")
    
    # Cleanup temp files
    shutil.rmtree(temp_dir, ignore_errors=True)
    log_message("Cleanup completed.")
    
    global last_update_time
    last_update_time = time.strftime("%Y-%m-%d %H:%M:%S")
    
    return "Liveries installed successfully!"

def check_for_updates():
    """Runs in the background to check for updates every 15 minutes"""
    while True:
        try:
            download_and_extract()
        except Exception as e:
            log_message(f"Update check failed: {e}")
        time.sleep(900)  # Wait 15 minutes before checking again
