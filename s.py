import pandas as pd
from rapidfuzz import fuzz, process
from concurrent.futures import ThreadPoolExecutor

# Загрузка данных
forum_data = pd.read_excel('1.xlsx')
with open('2.txt', 'r', encoding='utf-8') as file:
    exclude_titles = [line.strip() for line in file]

# Ключевые слова для удаления
keywords_to_exclude = ["Skillbox", "OTUS", "geekbrains", "Яндекс практикум"]

# Функция для проверки схожести названий
def is_similar(title, exclude_titles, threshold=55):
    match = process.extractOne(title, exclude_titles, scorer=fuzz.ratio)
    return match and match[1] >= threshold

# Функция для проверки наличия ключевых слов
def contains_keywords(title, keywords):
    return any(keyword.lower() in title.lower() for keyword in keywords)

# Параллельная фильтрация данных
def filter_data(row):
    title = row['Название']
    return not (is_similar(title, exclude_titles) or contains_keywords(title, keywords_to_exclude))

with ThreadPoolExecutor() as executor:
    results = list(executor.map(filter_data, forum_data.to_dict('records')))

filtered_forum_data = forum_data[results]

# Сохранение результата
filtered_forum_data.to_excel('filtered_1.xlsx', index=False)

print("Фильтрация завершена. Отфильтрованный файл сохранен как filtered_1.xlsx.")
