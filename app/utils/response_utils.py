from typing import Any, Optional
from pydantic import BaseModel

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

def create_response(data: Any = None, message: str = "Success", success: bool = True) -> dict:
    """
    Helper to create a consistent JSON response.
    """
    return {
        "success": success,
        "message": message,
        "data": data
    }
