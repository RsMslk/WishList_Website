
# Класс Итема в ЦСВ файлике
class Item:
    # Дефолтный Конструктор
    def __init__(self):
        self.id = 0
        self.title = "no title"
        self.url = "#/index.html"
        self.status = False
        self.who = "Noone"

    def __init__(self, id, title, url, who, status):
        self.id = id
        self.title = title
        self.url = url
        self.who = who
        self.status = status

    def getId(self):
        return self.id

    def getTitle(self):
        return self.title

    def getURL(self):
        return self.url

    def getStatus(self):
        return self.status

    def getWho(self):
        return self.who

    def get(self):
        return self.id, self.title, self.status, self.who, self.status
