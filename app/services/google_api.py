# app/services/google_api.py

from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.services.constants import FORMAT_DATE


# Функция создания таблицы
async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    # Получаем текущую дату для заголовка документа
    now_date_time = datetime.now().strftime(FORMAT_DATE)
    # Создаём экземпляр класса Resourse
    service = await wrapper_services.discover('sheets', 'v4')
    # Формируем тело запроса
    spreadsheet_body = {
        'properties': {'title': f'Отчет от {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 11}}}]
    }
    # Выполняем запрос
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


# Функция для предоставления прав доступа вашему личному аккаунту
async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


# Функция для записи полученной из базы данных информации
# в документ с таблицами
async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT_DATE)
    service = await wrapper_services.discover('sheets', 'v4')
    # Здесь формируется тело таблицы
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    # # Здесь в таблицу добавляются строчки
    for project in projects:
        project_row = [
            str(project['name']),
            str(project['funding_time']),
            str(project['description'])
        ]
        table_values.append(project_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
