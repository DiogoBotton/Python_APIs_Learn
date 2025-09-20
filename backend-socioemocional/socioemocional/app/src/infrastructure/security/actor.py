from fastapi import Depends
from src.infrastructure.security.routes import JWTBearer

class Actor:
    def __init__(
        self,
        payload: dict = Depends(JWTBearer())
    ):
        self._payload = payload

    @property
    def user_id(self) -> str:
        return self._payload.get("sub")

    @property
    def user_email(self) -> str:
        return self._payload.get("email")

    @property
    def user_cpf(self) -> str:
        return self._payload.get("cpf")

    @property
    def role(self) -> str | None:
        return self._payload.get("role")