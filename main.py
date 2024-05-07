from datetime import datetime

TEXT_FILE = 'data.txt'


class ClientWallet:
    def __init__(self) -> None:
        """Чтение файла при инициализаии."""
        try:
            with open(TEXT_FILE, 'r', encoding='utf-8') as file:
                self.file_records = file.read()
        except Exception as error:
            raise error

    def get_balance(self) -> int:
        """Возвращает текущий баланс."""
        lines = self.file_records.split('\n')
        sign = 1
        balance = 0

        for line in lines:
            if line.endswith('Расход'):
                sign = -1
            elif line.endswith('Доход'):
                sign = 1
            elif line.startswith('Сумма'):
                balance += sign * int(line.split()[1])

        return balance

    def add_record(self, **kwargs: str) -> None:
        """Добавляет новую запись."""
        record = ('\nДата: {date}\nКатегория: {category}\nСумма: {amount}'
                  '\nОписание: {description}\n***'.format(**kwargs))

        try:
            with open(TEXT_FILE, 'a', encoding='utf-8') as file:
                file.write(record)
        except Exception as error:
            print(f'Произошла ошибка при записи в файл: {error}')

        self.file_records += record

    def edit_record(self, old_record: str, **kwargs: str) -> None:
        """Изменяет существующую запись."""
        new_file_records = self.file_records.replace(
            old_record,
            '\nДата: {date}\nКатегория: {category}\nСумма: {amount}'
            '\nОписание: {description}\n'.format(**kwargs)
        )

        self.file_records = new_file_records

        try:
            with open(TEXT_FILE, 'w', encoding='utf-8') as file:
                file.write(new_file_records)
        except Exception as error:
            print(f'Произошла ошибка при записи в файл: {error}')

    def find_records(self, request: str) -> list[str]:
        """Возвращает список записей оп слову или предложению."""
        records_list: list[str] = []

        records: list[str] = self.file_records.split('***')[:-1]

        for record in records:
            if record.lower().find(request.lower()) != -1:
                records_list.append(record)

        return records_list


def write_record() -> dict[str, str]:
    """Возвращает словарь с данными о записи, которую создаёт пользователь. """
    while True:
        date = input('Дата: ')
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            print('Введите дату корректно. Пример: 2023-10-29')
            continue

        category = input('Категория: ')
        if category not in ('Расход', 'Доход'):
            print('Введите категорию <Доход> или <Расход>')
            continue

        amount = input('Сумма: ')
        try:
            int(amount)
        except ValueError:
            print('Введите целое число.')
            continue
        if int(amount) < 0:
            print('Введите положительное число.')
            continue

        description = input('Описание: ')
        break

    return {
        'date': date,
        'category': category,
        'amount': amount,
        'description': description
    }


def main():
    """Основная функция с интерфейсом в командной строке."""
    my_wallet = ClientWallet()
    while True:
        key = input('\n Выберите один из вариантов:\n1 - Проверить баланс'
                    '.\n2 - Добавить запись.\n3 - Изменить запись.'
                    '\n4 - Найти запись.\n5 - Выйти.\n\n')
        match key:
            case '1':
                print(f'Ваш баланс: {my_wallet.get_balance()} руб.')
            case '2':
                record: dict[str, str] = write_record()
                my_wallet.add_record(**record)
            case '3':
                if not my_wallet.file_records:
                    print('У Вас пока нет записей.')
                    continue

                i = 1
                records: dict[str, str] = {}
                for record in my_wallet.find_records(''):
                    print(f'{i}: {record}')
                    records[str(i)] = record
                    i += 1

                while True:
                    key = input('\nВыберите запись, '
                                'которую хотите изменить: ')
                    if not records.get(key):
                        print('Записи под таким номером нет.')
                    else:
                        break

                old_record: str = my_wallet.find_records(records[key])[0]
                new_record: dict[str, str] = write_record()

                my_wallet.edit_record(old_record, **new_record)
            case '4':
                request = input('Поиск по словам: ')
                for record in my_wallet.find_records(request):
                    print(record)
            case '5':
                break
            case _:
                pass


if __name__ == '__main__':
    main()
