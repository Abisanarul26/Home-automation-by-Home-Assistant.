# File: appdaemon/apps/azure_test.py
import hassapi as hass
import os
import time
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient

class AzureUploader(hass.Hass):

    def initialize(self):
        # 1. Listen for the instantaneous upload trigger from HA
        self.listen_event(self.upload_to_azure, "UPLOAD_CCTV")
        
        # 2. Schedule a daily maintenance task to clean local storage (Runs at 2:00 AM)
        self.run_daily(self.daily_local_cleanup, "02:00:00")
        
        self.log("Azure Sync Engine Ready: 7-Day Local Retention Active.")

    def upload_to_azure(self, event_name, data, kwargs):
        file_path = data.get("file_path")
        
        # Connection details (Use secrets.yaml in a real production environment)
        # Note: You should move this string to your appdaemon.yaml secrets section
        connect_str = self.args["azure_connection_string"]
        container_name = "ezviz-recordings"

        if not os.path.exists(file_path):
            self.log(f"Upload aborted: {file_path} not found on disk.", level="WARNING")
            return

        try:
            self.log(f"Initiating Azure Sync: {file_path}")
            
            blob_service_client = BlobServiceClient.from_connection_string(connect_str)
            filename = os.path.basename(file_path)
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

            with open(file_path, "rb") as video_data:
                blob_client.upload_blob(video_data, overwrite=True)
            
            self.log(f"Cloud Backup Successful: {filename}")

        except Exception as e:
            self.log(f"Cloud Backup Failed: {e}", level="ERROR")

    def daily_local_cleanup(self, kwargs):
        """
        Scans the local directory and removes files older than 7 days.
        """
        self.log("Running scheduled 7-day local storage maintenance...")
        directory = "/media/Azure_Cloud_Backup/"
        retention_days = 7
        now = time.time()

        try:
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                
                # Check if it's a file and if it's older than 7 days
                if os.path.isfile(file_path):
                    file_age_days = (now - os.path.getmtime(file_path)) / (24 * 3600)
                    
                    if file_age_days > retention_days:
                        os.remove(file_path)
                        self.log(f"Retention Policy Match: Deleted local copy of {filename} (Age: {int(file_age_days)} days)")
                        
        except Exception as e:
            self.log(f"Local Maintenance Error: {e}", level="ERROR")
