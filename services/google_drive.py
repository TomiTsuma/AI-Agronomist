from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
import io

SERVICE_ACCOUNT_FILE = './service-457211-261e41feb0b4.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

def upload_image_to_drive(image_bytes, image_name):
    # Authenticate using service account
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    # Prepare the image in memory
    image_stream = io.BytesIO(image_bytes)
    media = MediaIoBaseUpload(image_stream, mimetype='image/jpeg')

    file_metadata = {
        'name': image_name,
        'mimeType': 'image/jpeg'
    }
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = file.get('id')

    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    service.permissions().create(fileId=file_id, body=permission).execute()

    public_url = f"https://drive.google.com/uc?id={file_id}"
    print(public_url)
    return public_url
