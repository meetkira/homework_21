from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def add(self, title: str, quantity: int):
        """увеличивает запас items"""
        pass

    @abstractmethod
    def remove(self, title: str, quantity: int):
        """уменьшает запас items"""
        pass

    @abstractmethod
    def get_free_space(self):
        """возвращает количество свободных мест"""
        pass

    @abstractmethod
    def get_items(self):
        """возвращает содержание склада в словаре {товар: количество}"""
        pass

    @abstractmethod
    def get_unique_items_count(self):
        """возвращает количество уникальных товаров"""
        pass


class Store(Storage):
    def __init__(self):
        self._items = {}
        self._capacity = 100

    def add(self, title: str, quantity: int):
        """увеличивает запас items с учетом лимита capacity"""
        if self.get_free_space() <= quantity:
            return False, f"Товар не может быть добавлен, так как есть место только для {self.get_free_space()} единиц товара"
        if title not in self._items.keys():
            self._items[title] = quantity
        else:
            self._items[title] += quantity
        return True, "Товар успешно добавлен"

    def remove(self, title: str, quantity: int):
        """уменьшает запас items но не ниже 0"""
        if title not in self._items.keys():
            return False, f"Товар {title} не обнаружен"
        if quantity > self._items[title]:
            return False, f"Товара не хватает, попробуйте заказать меньше"
        else:
            self._items[title] = self._items[title] - quantity
            if self._items[title] == 0:
                del self._items[title]
            return True, f"Есть нужное количество товара\nКурьер забрал {quantity} {title}"

    def get_free_space(self):
        """возвращает количество свободных мест"""
        return self._capacity - sum(self._items.values())

    def get_items(self):
        """возвращает содержание склада в словаре {товар: количество}"""
        return self._items

    def get_unique_items_count(self):
        """возвращает количество уникальных товаров"""
        return len(self._items.keys())


class Shop(Store):
    def __init__(self):
        super(Shop, self).__init__()
        self._capacity = 25

    def add(self, title: str, quantity: int):
        if title not in self.get_items().keys() and self.get_unique_items_count() == 5:
            return False, "Товар не может быть доставлен, так как в магазине уже есть 5 различных товаров"
        return super(Shop, self).add(title, quantity)


class Request:
    def __init__(self, amount, product, from_, to):
        self.amount = amount
        self.product = product
        self.from_ = from_
        self.to = to


def check_request(request):
    """проверка формата запроса"""
    if len(request) < 5:
        return False, "Запрос должен состоять минимум из пяти слов"

    try:
        request[1] = int(request[1])
    except Exception:
        return False, "На втором месте в запросе должно быть целое положительное число"

    if int(request[1]) <= 0:
        return False, "Количество товара должно быть целым положительным числом"

    if request[0].lower() not in ["доставить", "забрать"]:
        return False, "Запрос должен начинаться со слов доставить/забрать"

    if request[0].lower() == "доставить" and request[4].lower() != "склад":
        return False, "Запрос, начинающийся со слова 'доставить', должен содержать слово склад"

    if request[0].lower() == "доставить" and len(request) < 7:
        return False, "Запрос, начинающийся со слова 'доставить', должен содержать минимум 7 слов"

    if request[0].lower() == "доставить" and request[6].lower() != "магазин":
        return False, "Пунктом доставки товара может быть только 'магазин'"

    if request[0].lower() == "забрать" and request[4].lower() != "магазин":
        return False, "Запрос, начинающийся со слова 'забрать', должен содержать слово магазин"

    return True, ""


def main():
    # создадим объекты классов
    store = Store()
    shop = Shop()

    # добавим несколько товаров на склад
    store.add("печеньки", 3)
    store.add("собачки", 1)
    store.add("коробки", 10)
    store.add("елки", 30)
    store.add("кактусы", 13)
    store.add("вафельки", 24)
    ask = """
    Введите запрос.
    Возможные варианты запросов:
    1. Доставить [n] [печеньки/собачки/коробки/etc] из склад в магазин
    2. Забрать [n] [печеньки/собачки/коробки/etc] из магазин

    Если хотите выйти из программы - введите 'Выход'
    """
    while True:
        print(ask)
        input_request = input()
        if input_request.lower() == "выход":
            break

        user_request = input_request.split()

        is_request_good, message = check_request(user_request)
        if not is_request_good:
            print(message)
            continue
        else:
            if len(user_request) < 7:
                to = None
            else:
                to = user_request[6]
            request = Request(amount=user_request[1], product=user_request[2], from_=user_request[4], to=to)

            if request.from_ == "склад":  # 1 вариант запроса

                can_get, message = store.remove(request.product,
                                                request.amount)  # можно ли взять со склада требуемое количество
                print(message)
                if can_get:
                    can_add, message = shop.add(request.product,
                                                request.amount)  # можно ли добавить в магазин требуемое количество
                    print(message)
                    if not can_add:  # если нельзя, возвращаем товар на склад
                        store.add(request.product, request.amount)

            else:
                _, message = shop.remove(request.product, request.amount)  # забираем товар из магазина
                print(message)

            print("На складе хранится: ", store.get_items())
            print("В магазине хранится: ", shop.get_items())


if __name__ == '__main__':
    main()
