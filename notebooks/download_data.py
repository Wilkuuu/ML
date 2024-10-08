import requests
import zipfile

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def unzip_file(source, destination_path):
    with zipfile.ZipFile(source, 'r') as zip_ref:
        zip_ref.extractall(destination_path)
                
def download_data():
    file_id = '1yW9p_Go1USHWTpuM92r3IicTPzt7cSZe'
    destination = 'data/athlete_events/athlete_events.zip'
    download_file_from_google_drive(file_id, destination)
    destination_path = 'data/athlete_events'
    unzip_file(destination, destination_path)
    print('Done.')

                
if __name__ == "__main__":
    download_data()