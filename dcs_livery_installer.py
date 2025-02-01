import sys
import os
import requests
import zipfile
import shutil
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon

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

def download_and_extract():
    """Downloads and installs the latest liveries"""
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
    
    # Extract ZIP
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
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
    
    # Cleanup temp files
    shutil.rmtree(temp_dir, ignore_errors=True)
    
    return "Liveries installed successfully!"

class LiveryUpdaterApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.tray_icon = QSystemTrayIcon(QIcon("icon.ico"), self.app)
        self.menu = QMenu()

        self.update_action = QAction("Update Liveries", self.app)
        self.update_action.triggered.connect(self.update_liveries)
        self.menu.addAction(self.update_action)
        
        self.exit_action = QAction("Exit", self.app)
        self.exit_action.triggered.connect(self.exit_app)
        self.menu.addAction(self.exit_action)
        
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.show()
        self.tray_icon.setToolTip("DCS Livery Updater")
    
    def update_liveries(self):
        """Handle livery update event"""
        try:
            message = download_and_extract()
            self.tray_icon.showMessage("DCS Livery Updater", message, QSystemTrayIcon.Information)
        except Exception as e:
            self.tray_icon.showMessage("DCS Livery Updater", f"Error: {str(e)}", QSystemTrayIcon.Critical)
    
    def exit_app(self):
        """Exit application"""
        self.tray_icon.hide()
        sys.exit()

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app = LiveryUpdaterApp()
    app.run()
