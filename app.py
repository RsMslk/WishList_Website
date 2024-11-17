from flask import Flask, render_template, redirect, request, jsonify
import pandas as pd
import chardet
import os

from item import Item
app = Flask(__name__)

# Маршрут для главной страницы
@app.route('/')
def index():  # Читаем CSV
    df = pd.read_csv("wishlist_utf8.csv")
    df = df.reset_index()
    # Запихиваем всю дату в список итемов
    all_items = []
    for _, row in df.iterrows():
        all_items.append(Item(row['id'], row['title'],
                         row['url'], row['who'], row['purchased']))

    return render_template('index.html', wishlist=all_items)


@app.route('/mark_as_gifted/<int:item_id>', methods=['POST'])
def mark_as_gifted(item_id):
    # Здесь логика для отметки предмета как подаренного
    df = (pd.read_csv("wishlist_utf8.csv"))
    df.loc[df['id'] == item_id, 'purchased'] = 1
    df.to_csv("wishlist_utf8.csv", index=False)
    # Пример ответа (обновите логику по мере необходимости)

    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
