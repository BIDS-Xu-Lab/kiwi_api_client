import requests
import os

class KiwiApiClient:
    def __init__(self, api_key):
        self.api_key = "Bearer " + api_key
        self.base_url = "https://kiwi.chpk8s.ynhh.org/src"

    def get_api_key(self):
        return self.api_key

    def get_base_url(self):
        return self.base_url
    
    def key_info(self):
        url = self.base_url + "/api_key_info"
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        return response.json()
    
    def single_prediction(self, input_data):
        url = self.base_url + "/single_predict"
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
        url = self.base_url + "/batch_process"
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
        url = self.base_url + "/task_status"
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
        url = self.base_url + "/incomplete_tasks"
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        return response.json()
    
    def cancel_task(self, task_id):
        url = self.base_url + "/cancel_task"
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
        url = self.base_url + "/download"
        params = {
            "task_id": task_id,
            "type": type
        }
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        # check if output_file_path is valid if provided
        if output_file_path:
            if not os.path.exists(output_file_path):
                return {"status": "error", "message": "Invalid output file path"}
        # if file path not end of /, add /
        if not output_file_path.endswith('/'):
            output_file_path = output_file_path + '/'
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            # Get filename from Content-Disposition header if available
            if 'Content-Disposition' in response.headers:
                content_disposition = response.headers['Content-Disposition']
                filename = content_disposition.split('filename=')[-1].strip('"\'')
            else:
                filename = f"task_{task_id}.{type}"
            
            # default to save as working directory, if output_file_path provided, save to provided path
            file_path = os.path.join(output_file_path, filename) if output_file_path else filename

            with open(file_path, 'wb') as file:
                file.write(response.content)
            return {"status": "success", "message": f"File downloaded to {file_path}"}
        else:
            return {"status": "error", "message": "Failed to download file"}

