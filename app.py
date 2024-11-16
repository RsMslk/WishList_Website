from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import chardet
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wishlist.db'
db = SQLAlchemy(app)

# Модель для базы данных 
# Тестовое изменение
class WishlistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    purchased = db.Column(db.Boolean, default=False)

# Функция для конвертации кодировки CSV файла
def convert_csv_encoding(input_file, output_file):
    # Определяем кодировку исходного файла
    with open(input_file, 'rb') as f:
        result = chardet.detect(f.read())
        file_encoding = result['encoding']
        print(f"Определённая кодировка: {file_encoding}")
    
    try:
        # Используем определённую кодировку для чтения
        df = pd.read_csv(input_file, encoding=file_encoding)
        df.to_csv(output_file, encoding='utf-8', index=False)
        print(f"Файл {input_file} успешно перекодирован и сохранён как {output_file}")
    except Exception as e:
        print(f"Ошибка при конвертации файла: {e}")

# Маршрут для главной страницы
@app.route('/')
def index():
    wishlist = WishlistItem.query.all()
    return render_template('index.html', wishlist=wishlist)

# Маршрут для отметки подарка как купленного
@app.route('/mark_purchased/<int:item_id>')
def mark_purchased(item_id):
    item = WishlistItem.query.get_or_404(item_id)
    item.purchased = True
    db.session.commit()
    return redirect('/')

# Маршрут для конвертации CSV файла
@app.route('/convert_csv')
def convert_csv():
    input_file = 'wishlist_utf8.csv'  # Укажи путь к исходному файлу
    output_file = 'wishlist_utf8.csv'  # Укажи путь к выходному файлу

    # Вызываем функцию для конвертации
    convert_csv_encoding(input_file, output_file)
    
    return "Конвертация завершена!"

if __name__ == '__main__':
    input_file = 'wishlist_utf8.csv'  # Укажи путь к исходному файлу
    output_file = 'wishlist_utf8.csv'  # Укажи путь к выходному файлу

    # Конвертируем CSV перед запуском сервера, если это нужно
    convert_csv_encoding(input_file, output_file)
    
    app.run(debug=True)
