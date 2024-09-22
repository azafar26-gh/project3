from flask import Flask, render_template, request
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

# Replace with your actual connection string
connection_string = 'BlobEndpoint=https://storageaccountp3.blob.core.windows.net/;QueueEndpoint=https://storageaccountp3.queue.core.windows.net/;FileEndpoint=https://storageaccountp3.file.core.windows.net/;TableEndpoint=https://storageaccountp3.table.core.windows.net/;SharedAccessSignature=sv=2022-11-02&ss=bfqt&srt=sco&sp=rwtfx&se=2024-09-22T20:49:52Z&st=2024-09-22T12:49:52Z&spr=https,http&sig=URsQnqYGvwm6ufWZncsLmvFAzjscyrsBt1AohS%2Fa%2F%2FQ%3D'
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = 'uploads'

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Single upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    # Upload the file to Azure Blob Storage
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)
    blob_client.upload_blob(file)

    return 'File uploaded to Azure Blob Storage', 200

if __name__ == "__main__":
    app.run(debug=True)
