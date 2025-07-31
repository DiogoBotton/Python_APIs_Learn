from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.infrastructure.security.token import decode_jwt
from src.domains.enums.role_type import RoleType

class JWTBearer(HTTPBearer):
    def __init__(self, allowed_roles: list[RoleType] = None, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.allowed_roles = allowed_roles or []

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=403, detail="Schema de autorização inválido.")
            
            payload = decode_jwt(credentials.credentials)
            if not payload:
                raise HTTPException(status_code=403, detail="Token inválido ou expirado.")
            
            if self.allowed_roles and payload.get("role") not in self.allowed_roles:
                raise HTTPException(status_code=403, detail="Usuário não tem a permissão necessária para acessar este recurso.")
            
            return payload
        else:
            raise HTTPException(status_code=403, detail="Código de autorização inválido.")
