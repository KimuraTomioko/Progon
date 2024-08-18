import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# Загрузка данных
forum_data = pd.read_excel('1.xlsx')

# Чтение исключённых названий
with open('2.txt', 'r', encoding='utf-8') as file:
    exclude_titles = set(line.strip().lower() for line in file)  # Преобразуем в нижний регистр для проверки

# Отладка: Печать первых нескольких строк исключённых названий
print("Примеры исключённых названий:")
for title in list(exclude_titles)[:10]:  # Печатаем только первые 10
    print(title)

# Ключевые слова для удаления
keywords_to_exclude = {"Skillbox", "OTUS", "geekbrains", "Яндекс практикум"}

# Функция для проверки наличия ключевых слов
def contains_keywords(title, keywords):
    return any(keyword.lower() in title.lower() for keyword in keywords)

def filter_data(row):
    title = row[forum_data.columns[0]]  # Используем первую колонку по индексу
    title_lower = title.lower()
    # Проверяем наличие полного совпадения в exclude_titles и ключевых слов
    return not (title_lower in exclude_titles or contains_keywords(title, keywords_to_exclude))

# Параллельная фильтрация данных
with ThreadPoolExecutor() as executor:
    results = list(executor.map(filter_data, forum_data.to_dict('records')))

# Отладка: Выводим количество оставшихся строк
print(f"Оставлено строк: {results.count(True)}")
print(f"Удалено строк: {results.count(False)}")

filtered_forum_data = forum_data[results]

# Регулярное выражение для поиска года в формате (YYYY)
import re
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


