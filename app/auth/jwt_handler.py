import time
from typing import Dict

import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


def token_response(token: str):
    return {"access_token": token}


def sign_jwt(user_id: str) -> dict[str, str]:
    payload = {"user_id": user_id, "expires": time.time() + 180}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except jwt.ExpiredSignatureError:
        return {"error": "Expired token"}
    except jwt.DecodeError:
        return {"error": "Invalid token"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}