import pandas as pd
from rapidfuzz import fuzz, process
from concurrent.futures import ThreadPoolExecutor

# Загрузка данных
forum_data = pd.read_excel('1.xlsx')
with open('2.txt', 'r', encoding='utf-8') as file:
    exclude_titles = [line.strip() for line in file]

# Функция для проверки схожести названий
def is_similar(title, exclude_titles, threshold=50):
    match = process.extractOne(title, exclude_titles, scorer=fuzz.ratio)
    return match and match[1] >= threshold

# Параллельная фильтрация данных
def filter_data(row):
    return not is_similar(row['Название'], exclude_titles)

with ThreadPoolExecutor() as executor:
    results = list(executor.map(filter_data, forum_data.to_dict('records')))

filtered_forum_data = forum_data[results]

# Сохранение результата
filtered_forum_data.to_excel('filtered_1.xlsx', index=False)

print("Фильтрация завершена. Отфильтрованный файл сохранен как filtered_1.xlsx.")
