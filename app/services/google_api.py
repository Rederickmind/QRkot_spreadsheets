# app/services/google_api.py

import copy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.services.constants import FORMAT_DATE, SPREADSHEET_BODY, TABLE_VALUES


# Функция создания таблицы
async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    # Получаем текущую дату для заголовка документа
    now_date_time = datetime.now().strftime(FORMAT_DATE)
    service = await wrapper_services.discover('sheets', 'v4')

    spreadsheet_body = copy.deepcopy(SPREADSHEET_BODY)
    spreadsheet_body['properties']['title'] = f'Отчет от {now_date_time}'

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


# Функция для предоставления прав доступа личному аккаунту
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
    table_values = copy.deepcopy(TABLE_VALUES)
    table_values[0] = ['Отчет от', now_date_time]
    # # Здесь в таблицу добавляются строки
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
    rows = len(table_values)
    columns = max(map(len, table_values))
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'R1C1:R{rows}C{columns}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
