import pandas as pd
from docx import Document
import emoji
import re

# Функция для удаления смайликов из текста
def remove_emojis(text):
    # Используем регулярное выражение для удаления смайликов
    clean_text = emoji.replace_emoji(text, replace='')
    return clean_text

def clear_text(text):
    # Удаление сносков (например, текст в квадратных скобках [1], [2], ...)
    text = re.sub(r'\[\d+\]', '', text)
    
    # Удаление лишних пробелов (замена нескольких пробелов на один)
    text = re.sub(r'\s+', ' ', text)
    
    # Удаление пробелов в начале и в конце строки
    text = text.strip()
    
    return text

# Чтение документа Word
def read_word_table(file_path):
    # Открываем документ
    doc = Document(file_path)
    # Список для хранения данных таблицы
    table_data = []

    # Проходим по всем таблицам в документе
    for table in doc.tables:
        # Для каждой таблицы добавляем строки в table_data
        i = 0
        for row in table.rows:
            if i == 0:
                i = 1
                continue
            for cell in row.cells:
                clean_text = remove_emojis(cell.text)  # Очищаем текст от смайликов
                table_data.append(clear_text(clean_text))

    # Создаем DataFrame
    df = pd.DataFrame(table_data)
    df = df.dropna()
    return df
