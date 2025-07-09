import dropbox
from dropbox.files import WriteMode
from utils.config import get_dropbox_access_token
import io

def upload_image_to_dropbox(image_stream, image_name, dropbox_path="/"):
    access_token = get_dropbox_access_token()
    print(">>>>>>>>>>>>>>>>>>>>>>>>:", access_token)
    """
    Uploads an image from a BytesIO stream to Dropbox.

    Args:
        image_stream (io.BytesIO): The image byte stream.
        image_name (str): The name to use for the uploaded image (e.g. 'photo.jpg').
        access_token (str): Your Dropbox API access token.
        dropbox_path (str): Folder path in Dropbox (default: root '/').
    
    Returns:
        str: Shared link to the uploaded image (if sharing enabled).
    """
    # Ensure dropbox_path ends with '/'
    if not dropbox_path.endswith("/"):
        dropbox_path += "/"

    full_path = f"{dropbox_path}{image_name}"
    dbx = dropbox.Dropbox(access_token)

    # Upload image
    image_stream = io.BytesIO(image_stream)
    dbx.files_upload(image_stream.read(), full_path, mode=WriteMode('overwrite'))

    # Try to create a shared link
    try:
        shared_link = dbx.sharing_create_shared_link_with_settings(full_path).url
        # Modify link to allow direct access
        if shared_link.endswith('?dl=0'):
            shared_link = shared_link.replace('?dl=0', '?raw=1')
        return shared_link
    except dropbox.exceptions.ApiError:
        return f"Uploaded to {full_path} (no shared link available)"
