from enum import Enum

class AuthOpenApiRequest(Enum):
    Token = {
        "username": {"type": "string", "required": True, "default":"sid"},
        "password": {"type": "string", "required": True, "default":"1234"}
    }