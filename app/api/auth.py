from fastapi import HTTPException, status, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

router = APIRouter()
VALID_USERNAME = "admin"
VALID_PASSWORD = "quiz123"

security = HTTPBasic()

def authenticate_user(credentials: HTTPBasicCredentials):
    correct_username = secrets.compare_digest(credentials.username, VALID_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, VALID_PASSWORD)
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username