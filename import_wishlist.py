import pandas as pd
from app import app, db, WishlistItem  # Убедитесь, что импортируете нужные модули

# Чтение данных из CSV
df = pd.read_csv('wishlist_utf8.csv')
print(df.columns)

# Удаление дубликатов из базы данных
with app.app_context():
    all_items = WishlistItem.query.all()
    seen = set()
    for item in all_items:
        if item.url in seen:  # Если элемент уже встречался
            db.session.delete(item)  # Удаляем дубликат
        else:
            seen.add(item.url)  # Добавляем уникальный элемент в набор
    db.session.commit()

# Импорт данных в базу данных
with app.app_context():
    for index, row in df.iterrows():
        # Проверка на существование элемента по уникальному полю (например, url)
        existing_item = WishlistItem.query.filter_by(url=row['url']).first()
        if existing_item is None:  # Если элемент не найден, добавляем его
            item = WishlistItem(title=row['title'], url=row['url'], purchased=bool(row['purchased']))
            db.session.add(item)

    db.session.commit()

print("Данные успешно импортированы в базу данных!")


