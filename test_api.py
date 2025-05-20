import requests

# Flask server URL
url = 'http://127.0.0.1:8086/compare'

# Full absolute path to sample.txt
file_path = r'F:\vr-text-similarity-app\vr-text-similarity-app\sample.txt'

# Data payload
data = {
    'audio_text': 'This text is about similarity checking using AI models',
    'language': 'en'
}

# Files to upload
files = {
    'file': open(file_path, 'rb')
}

# Send the request
response = requests.post(url, data=data, files=files)

# Output the results
print("Status Code:", response.status_code)
try:
    print("Response JSON:", response.json())
except Exception as e:
    print("Error decoding JSON:", e)
    print("Raw Response:", response.text)
