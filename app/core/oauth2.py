"""Authentication using oauth2."""
from fastapi.security import OAuth2PasswordBearer

# Generate an auth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
