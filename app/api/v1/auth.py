from fastapi import APIRouter, HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

# Demo user store (replace with a real DB in production)
_users: dict[str, str] = {
    "admin": hash_password("secret"),
}


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest):
    hashed = _users.get(credentials.username)
    if not hashed or not verify_password(credentials.password, hashed):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    token = create_access_token(subject=credentials.username)
    return TokenResponse(access_token=token)
