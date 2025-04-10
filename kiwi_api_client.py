import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

ROOT_PATH = os.getenv("ROOT_PATH")
API_KEY = os.getenv("API_KEY")


class KiwiApiClient:
    def __init__(self):
        self.api_key = "Bearer " + API_KEY
        self.base_url = ROOT_PATH

    def get_api_key(self):
        return self.api_key

    def get_base_url(self):
        return self.base_url
    
    def key_info(self):
        url = self.base_url + "/api_key_info/"
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        return response.json()
    
    def single_prediction(self, input_data):
        url = self.base_url + "/single_predict/"
        params = {
            "text": input_data
        }
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    
    def batch_prediction(self, file_path):
        url = self.base_url + "/batch_process/"
        headers = {
            "Authorization": self.api_key,
            "accept": "application/json"
        }
        
        with open(file_path, 'rb') as file:
            files = {
                'file': (os.path.basename(file_path), file, 'text/plain')
            }
            response = requests.post(url, headers=headers, files=files)
        
        return response.json()
    
    def task_status(self, task_id):
        url = self.base_url + "/task_status/"
        params = {
            "task_id": task_id
        }
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    
    def incomplete_tasks(self):
        url = self.base_url + "/incomplete_tasks/"
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        return response.json()
    
    def cancel_task(self, task_id):
        url = self.base_url + "/cancel_task/"
        params = {
            "task_id": task_id
        }
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    
    def download_task(self, task_id, output_file_path=None, type="zip"):
        url = self.base_url + "/download/"
        params = {
            "task_id": task_id,
            "type": type
        }
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            # Get filename from Content-Disposition header if available
            if 'Content-Disposition' in response.headers:
                content_disposition = response.headers['Content-Disposition']
                filename = content_disposition.split('filename=')[-1].strip('"\'')
            else:
                filename = f"task_{task_id}.{type}"
            
            # Use provided output path or default filename
            file_path = output_file_path or filename
            
            with open(file_path, 'wb') as file:
                file.write(response.content)
            return {"status": "success", "message": f"File downloaded to {file_path}"}
        else:
            return {"status": "error", "message": "Failed to download file"}

class KiwiApiPrediction:
    def __init__(self):
        self.KiwiApiClient = KiwiApiClient()
        
    def batch_prediction(self, input_data, output_file_path=None, type="json"):
        # first make a task
        task = self.KiwiApiClient.batch_prediction(input_data)
        print(f"Task created successfully, status: {task['message']}, task_id: {task['task_id']}, token remaining: {task['token_remaining']}, estimated time: {task['estimate_time']}")
        task_id = task["task_id"]
        # wait for the task to complete
        while True:
            task_status = self.KiwiApiClient.task_status(task_id)
            if task_status["status"] == "completed":
                break
            else:
                print(f"Task is not completed yet, status: {task_status['status']}, files remaining: {task_status.get('files_remaining', 'N/A')}, processed files: {task_status.get('processed_files', 'N/A')}, remaining time: {task_status.get('remaining_time', 'N/A')}")
                time.sleep(5)
        # download the task
        self.KiwiApiClient.download_task(task_id, output_file_path, type)
        return {"status": "success", "message": f"Task completed successfully, file downloaded to {output_file_path}"}
