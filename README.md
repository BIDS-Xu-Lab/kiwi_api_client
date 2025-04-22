# kiwi_api_client
## Overview

`kiwi_api_client` is a lightweight Python wrapper for the Kiwi API. It provides methods to authenticate, query your API key usage, submit single or batch text for processing, monitor and cancel jobs, and download results.

## Installation

```bash
pip install requests
# Then place `kiwi_api_client.py` in your project folder
```

## Usage

```python
from kiwi_api_client import KiwiApiClient

# Initialize the client with your API key
client = KiwiApiClient("YOUR_API_KEY")
```

### 1. get_api_key()

Returns the full Bearer token string.

```python
token = client.get_api_key()
print(token)  # e.g. "Bearer YOUR_API_KEY"
```

### 2. get_base_url()

Returns the base URL of the Kiwi API.

```python
url = client.get_base_url()
print(url)  # e.g. "https://kiwi-test.chpk8s.ynhh.org/src"
```

### 3. key_info()

Fetches usage statistics and expiration info for your API key.

```python
info = client.key_info()
print(info)
# Example:
# {
#   'usage_count': 46845,
#   'token_remain': 9953155,
#   'Expires_at': '2025-04-28 18:25:34'
# }
```

### 4. single_prediction(text)

Sends a single text string for analysis and returns the JSON result.

```python
result = client.single_prediction("Patient admitted with pneumonia and respiratory failure.")
print(result)
```

### 5. batch_prediction(file_path)

Uploads a text file for batch processing. Returns a task ID and estimates.

```python
response = client.batch_prediction("path/to/your_input.txt")
print(response)
# Example:
# {
#   'task_id': 'edb824e5-728d-4764-a17e-e1ad99c45349',
#   'message': 'Task in queue',
#   'token_usage': 6664,
#   'token_remaining': 9933148,
#   'estimate_time': '00:08:52'
# }
```

### 6. task_status(task_id)

Checks the current status of a batch task.

```python
status = client.task_status("edb824e5-728d-4764-a17e-e1ad99c45349")
print(status)
# Example:
# {
#   'task_id': 'edb824e5-728d-4764-a17e-e1ad99c45349',
#   'status': 'queued',
#   'queue_position': 2,
#   'remaining_time': '00:08:52'
# }
```

### 7. incomplete_tasks()

Lists all tasks that are still queued or processing.

```python
tasks = client.incomplete_tasks()
print(tasks)
# Example:
# {
#   'tasks': [
#     {'task_id': '69065885-16bb-4304-82de-993497a05977', 'status': 'completed'},
#     {'task_id': '26f62f73-5767-4239-94b6-186142074736', 'status': 'processing'},
#     ...
#   ]
# }
```

### 8. cancel_task(task_id)

Cancels a queued or processing batch task.

```python
cancel_resp = client.cancel_task("17500005-cb91-45a4-b173-f54c6c804f48")
print(cancel_resp)
# Example:
# {
#   'task_id': '17500005-cb91-45a4-b173-f54c6c804f48',
#   'message': 'Task canceled'
# }
```

### 9. download_task(task_id, output_file_path=None, type="zip")

Downloads the result of a completed task. Supports `"zip"` or `"json"`.

```python
download_resp = client.download_task(
    "edb824e5-728d-4764-a17e-e1ad99c45349", 
    "results_folder", 
    "json"
)
print(download_resp)
# Example:
# {
#   'status': 'success',
#   'message': 'File downloaded to results_folder/task_edb824e5-728d-4764-a17e-e1ad99c45349.json'
# }
```

## Example Notebook

A fully worked example is provided in `use_case.ipynb`:

```python
from kiwi_api_client import KiwiApiClient

# 1. Initialize
client = KiwiApiClient("replace the text to your API key")

# 2. Test key connection
client.key_info()

# 3. Single prediction
client.single_prediction("Replace the text to your text")

# 4. Batch processing
client.batch_prediction("replace the text to your file path")

# 5. Poll status
client.task_status("replace the text to task_id get from above function")

# 6. List incomplete tasks
client.incomplete_tasks()

# 7. Cancel a task
client.cancel_task("replace the text to task id")

# 8. Download results
client.download_task(
    "replace the text to task_id", 
    "output path", 
    "file type"
)
```

