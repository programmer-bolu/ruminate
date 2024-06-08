import requests

def upload_to_imgbb(image):
    response = requests.post(
        'https://api.imgbb.com/1/upload',
        params={'key': 'f41f1c9e23fa49e6d2d53f2938a18920'},
        files={'image': image}
    )

    if response.status_code == 200:
        return response.json()
    else:
        return response.raise_for_status()
