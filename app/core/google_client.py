# ...app/core/google_client.py

# Подключаем классы асинхронной бибилиотеки
from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

# Подключаем настройки
from app.core.config import settings

# Список разрешений
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
# Формируем словарь с учётными данными сервисного аккаунта
INFO = {
    'type': settings.type,
    'project_id': settings.project_id,
    'private_key_id': settings.private_key_id,
    'private_key': settings.private_key,
    'client_email': settings.client_email,
    'client_id': settings.client_id,
    'auth_uri': settings.auth_uri,
    'token_uri': settings.token_uri,
    'auth_provider_x509_cert_url': settings.auth_provider_x509_cert_url,
    'client_x509_cert_url': settings.client_x509_cert_url
}
# Получаем объект учётных данных
cred = ServiceAccountCreds(scopes=SCOPES, **INFO)


# Создаём экземпляр класса Aiogoogle
async def get_service():
    async with Aiogoogle(service_account_creds=cred) as aiogoogle:
        yield aiogoogle
