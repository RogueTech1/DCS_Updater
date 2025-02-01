using System;
using System.IO;
using System.Net;
using System.IO.Compression;
using System.Timers;
using System.Diagnostics;
using System.Windows.Forms;

class DcsLiveryUpdater
{
    private static readonly string repoOwner = "pschilly";
    private static readonly string repoName = "gtfo-liveries";
    private static readonly string installDir = AppDomain.CurrentDomain.BaseDirectory;
    private static readonly string logFile = Path.Combine(installDir, "livery_updater.log");
    private static NotifyIcon trayIcon;
    private static Timer updateTimer;

    [STAThread]
    static void Main()
    {
        Application.EnableVisualStyles();
        Application.SetCompatibleTextRenderingDefault(false);
        
        trayIcon = new NotifyIcon()
        {
            Icon = SystemIcons.Application,
            Visible = true,
            Text = "DCS Livery Updater"
        };
        
        ContextMenuStrip menu = new ContextMenuStrip();
        menu.Items.Add("Update Now", null, (s, e) => UpdateLiveries());
        menu.Items.Add("Exit", null, (s, e) => ExitApplication());
        trayIcon.ContextMenuStrip = menu;
        
        updateTimer = new Timer(900000); // 15 minutes
        updateTimer.Elapsed += (s, e) => UpdateLiveries();
        updateTimer.Start();
        
        Application.Run();
    }

    static void UpdateLiveries()
    {
        try
        {
            LogMessage("Starting livery update...");
            string defaultBranch = GetDefaultBranch();
            string zipUrl = $"https://github.com/{repoOwner}/{repoName}/archive/refs/heads/{defaultBranch}.zip";
            string tempDir = Path.Combine(Path.GetTempPath(), "DCS_Livery_Updater");
            string zipPath = Path.Combine(tempDir, "DCS_Liveries.zip");
            string extractPath = Path.Combine(tempDir, "extracted");
            string dcsLiveriesPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), "Saved Games", "DCS", "Liveries");
            
            if (Directory.Exists(tempDir))
                Directory.Delete(tempDir, true);
            Directory.CreateDirectory(tempDir);
            
            using (WebClient client = new WebClient())
                client.DownloadFile(zipUrl, zipPath);
            
            LogMessage("Download completed.");
            ZipFile.ExtractToDirectory(zipPath, extractPath);
            LogMessage("Extraction completed.");
            
            string extractedFolder = Path.Combine(extractPath, $"{repoName}-{defaultBranch}");
            string liveriesSource = Path.Combine(extractedFolder, "Liveries");
            
            if (Directory.Exists(liveriesSource))
            {
                if (!Directory.Exists(dcsLiveriesPath))
                    Directory.CreateDirectory(dcsLiveriesPath);
                
                foreach (var dir in Directory.GetDirectories(liveriesSource))
                {
                    string targetDir = Path.Combine(dcsLiveriesPath, Path.GetFileName(dir));
                    if (Directory.Exists(targetDir))
                        Directory.Delete(targetDir, true);
                    Directory.Move(dir, targetDir);
                }
            }
            
            LogMessage("Liveries copied to destination.");
            Directory.Delete(tempDir, true);
            LogMessage("Cleanup completed.");
            trayIcon.ShowBalloonTip(3000, "DCS Livery Updater", "Liveries updated successfully!", ToolTipIcon.Info);
        }
        catch (Exception ex)
        {
            LogMessage($"Error: {ex.Message}");
            trayIcon.ShowBalloonTip(3000, "DCS Livery Updater", "Update failed. Check logs.", ToolTipIcon.Error);
        }
    }

    static string GetDefaultBranch()
    {
        string apiUrl = $"https://api.github.com/repos/{repoOwner}/{repoName}";
        HttpWebRequest request = (HttpWebRequest)WebRequest.Create(apiUrl);
        request.UserAgent = "DCS-Livery-Updater";
        using (HttpWebResponse response = (HttpWebResponse)request.GetResponse())
        using (StreamReader reader = new StreamReader(response.GetResponseStream()))
        {
            string json = reader.ReadToEnd();
            int index = json.IndexOf("default_branch");
            if (index != -1)
            {
                int start = json.IndexOf(':', index) + 2;
                int end = json.IndexOf('"', start);
                return json.Substring(start, end - start);
            }
        }
        return "main";
    }

    static void LogMessage(string message)
    {
        File.AppendAllText(logFile, $"{DateTime.Now:yyyy-MM-dd HH:mm:ss} - {message}\n");
    }
    
    static void ExitApplication()
    {
        trayIcon.Visible = false;
        Application.Exit();
    }
}
