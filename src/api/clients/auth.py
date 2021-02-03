from fastapi import HTTPException

from google.oauth2 import id_token
from google.auth.transport import requests


class AuthClient:

    def __init__(self):
        pass

    def google_verify_id_token(self, token):
        try:
            request = requests.Request()
            id_info = id_token.verify_oauth2_token(
                token, request, '49547330958-ngop94cdmpb4bhipqsfnughsjbp0qcam.apps.googleusercontent.com')
            user_id = id_info['sub']
            return user_id
        except Exception as e:
            print(str(e))
            raise HTTPException(status_code=401, detail=str(e))
