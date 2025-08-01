from fastapi import HTTPException
from httpx import AsyncClient, HTTPStatusError
from .models import EmailTemplate, SenderSend, MessageVersion, ToSend
from settings import Settings
from typing import List, Dict, Optional
import logging

class EmailService:
    def __init__(self):
        self.client = AsyncClient(base_url=Settings().EMAIL_BREVO_SEND_URL)
        self.headers = {
            "api-key": Settings().EMAIL_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    # Templates
    async def send_user_invite(self, users: List[Dict[str, str]]):
        """
        users: [{"email": "xxx@email.com", "name": "user name"}]
        """

        await self._send_template_email(
            tos=users,
            subject="Você foi convidado para a Plataforma Socioemocional!",
            template_id=Settings().EMAIL_TEMPLATE_USER_INVITE_ID,
            params= {"platformUrl": Settings().CONSUMER_URL}
        )

    # Internals
    async def _send_template_email(
        self,
        tos: List[Dict[str, str]],
        subject: str,
        template_id: int,
        params: Optional[Dict[str, str]] = {}
    ):
        email_template = self._set_email(
            to_emails=tos,
            subject=subject,
            template_id=template_id,
            params=params
        )
        print(email_template.model_dump(exclude_none=True))
        try:
            response = await self.client.post("",
                headers=self.headers,
                json=email_template.model_dump(exclude_none=True)
            )
            response.raise_for_status()
            return response.json()
        except HTTPStatusError as e:
            logging.error(f"Erro ao enviar e-mail: {e.response.text}")
            raise HTTPException(status_code=500, detail=f"Ocorreu um erro no envio de e-mail: {e.response.text}")

    def _build_message_versions(
            self,
            users: List[Dict[str, str]]) -> List[MessageVersion]:
        message_versions = []

        for user in users:
            to_entry = ToSend(email=user["email"], name=user["name"])

            mv = MessageVersion(
                to=[to_entry],
                params={"username": user["name"]}
            )

            message_versions.append(mv)

        return message_versions

    def _set_email(
        self,
        to_emails: List[Dict[str, str]],
        subject: str,
        template_id: int,
        params: Optional[Dict[str, str]] = None
    ) -> EmailTemplate:
        message_versions = self._build_message_versions(to_emails)

        return EmailTemplate(
            sender=SenderSend(name=Settings().EMAIL_SENDER_NAME, email=Settings().EMAIL_SENDER),
            subject=subject,
            templateId=template_id,
            params=params,
            messageVersions=message_versions
        )