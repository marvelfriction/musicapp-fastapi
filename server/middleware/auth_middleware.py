from fastapi import Header, HTTPException
import jwt

def auth_middleware(x_auth_token=Header()):
    try:
        if not x_auth_token:
            raise HTTPException(401, "No Auth Token, access denied")
        verified_token = jwt.decode(x_auth_token, "password_key", ["HS256"])
        if not verified_token:
            raise HTTPException(401, "Token verification failed, access denied")
        # get id from the token
        uid = verified_token.get("id")
        return {"uid": uid, "x_auth_token": x_auth_token}
    except jwt.PyJWTError:
        raise HTTPException(401, "Token is not valid, access denied")