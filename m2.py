import pandas as pd
from rapidfuzz import fuzz, process
from concurrent.futures import ThreadPoolExecutor
import re

# Загрузка данных
forum_data = pd.read_excel('1.xlsx')
with open('2.txt', 'r', encoding='utf-8') as file:
    exclude_titles = [line.strip() for line in file]

# Ключевые слова для удаления
keywords_to_exclude = ["Skillbox", "OTUS", "geekbrains", "Яндекс практикум"]

# Функция для проверки схожести названий
def is_similar(title, exclude_titles, threshold=70):
    match = process.extractOne(title, exclude_titles, scorer=fuzz.ratio)
    return match and match[1] >= threshold

# Функция для проверки наличия ключевых слов
def contains_keywords(title, keywords):
    return any(keyword.lower() in title.lower() for keyword in keywords)

# Параллельная фильтрация данных
def filter_data(row):
    title = row[forum_data.columns[0]]  # Используем первую колонку по индексу
    return not (is_similar(title, exclude_titles) or contains_keywords(title, keywords_to_exclude))

with ThreadPoolExecutor() as executor:
    results = list(executor.map(filter_data, forum_data.to_dict('records')))

filtered_forum_data = forum_data[results]

# Регулярное выражение для поиска года в формате (YYYY)
year_pattern = re.compile(r'\((\d{4})\)')

# Разделение данных по годам
data_2024 = []
data_2023 = []
data_2022 = []
data_others = []

for index, row in filtered_forum_data.iterrows():
    title = row[filtered_forum_data.columns[0]]  # Используем первую колонку по индексу
    match = year_pattern.search(title)
    if match:
        year = int(match.group(1))
        if year == 2024:
            data_2024.append(row)
        elif year == 2023:
            data_2023.append(row)
        elif year == 2022:
            data_2022.append(row)
        else:
            data_others.append(row)
    else:
        data_others.append(row)

# Создание DataFrame из списков
df_2024 = pd.DataFrame(data_2024, columns=filtered_forum_data.columns)
df_2023 = pd.DataFrame(data_2023, columns=filtered_forum_data.columns)
df_2022 = pd.DataFrame(data_2022, columns=filtered_forum_data.columns)
df_others = pd.DataFrame(data_others, columns=filtered_forum_data.columns)

# Сохранение результатов
df_2024.to_excel('courses_2024.xlsx', index=False)
df_2023.to_excel('courses_2023.xlsx', index=False)
df_2022.to_excel('courses_2022.xlsx', index=False)
df_others.to_excel('courses_others.xlsx', index=False)

print("Фильтрация завершена. Файлы сохранены как courses_2024.xlsx, courses_2023.xlsx, courses_2022.xlsx и courses_others.xlsx.")
