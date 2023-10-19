NAME_DUPLICATE = 'Проект с таким именем уже существует!'
PROJECT_CLOSE = 'Закрытый проект нельзя редактировать!'
PROJECT_RAISING_MONEY = 'В проект были внесены средства, не подлежит удалению!'
SUMM_LOWER = 'Нельзя установить сумму меньше уже вложенной: '
PROJECT_NOT_FOUND = 'Не найден благотворительный проект с id: '

FORMAT_DATE = "%Y/%m/%d %H:%M:%S"
SPREADSHEET_BODY = {
    'properties': {'title': 'Отчет от определенной даты',
                   'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Лист1',
                               'gridProperties': {'rowCount': 100,
                                                  'columnCount': 11}}}]
}

TABLE_VALUES = [
    ['Отчет от', 'дата'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]