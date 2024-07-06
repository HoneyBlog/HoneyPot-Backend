import re
from fastapi import HTTPException
from uuid import UUID
from typing import Any

# User Regex
USERNAME_REGEX = r'^[a-zA-Z0-9._-]{5,20}$'
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,25}$'
EMAIL_REGEX = r'^[\w._%+-]+@[\w.-]+\.[a-zA-Z]{2,}$'

# User validation
validation_err = "Invalid username or password"

def user_validaton(user):
    if not re.match(USERNAME_REGEX, user.username):
        raise HTTPException(status_code=400, detail=validation_err)
    if not re.match(PASSWORD_REGEX, user.password):
        raise HTTPException(status_code=400, detail=validation_err)
    if not re.match(EMAIL_REGEX, user.email):
        raise HTTPException(status_code=400, detail=validation_err)
    
    
    
def is_valid_uuid(uuid_str: Any) -> bool:
    if isinstance(uuid_str, UUID):
        return True
    if isinstance(uuid_str, str):
        try:
            uuid_obj = UUID(uuid_str, version=4)
            return True
        except ValueError:
            return False
    return False