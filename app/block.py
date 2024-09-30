import json
import os
import hashlib
import logging

blockchain_dir = os.curdir + '/blockchain/'

# Настроим логирование с выводом в консоль
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info(f"Директория блокчейна: {blockchain_dir}")


def get_hash(filename):
    logging.info(f"Получаем хеш для файла: {filename}")
    try:
        file = open(blockchain_dir + filename, 'rb').read()
        return hashlib.md5(file).hexdigest()
    except FileNotFoundError:
        logging.error(f"Файл не найден: {filename}")
        return None


def get_files():
    logging.info("Получаем список файлов в блокчейне")
    try:
        files = os.listdir(blockchain_dir)
        return sorted([int(i) for i in files])
    except FileNotFoundError:
        logging.error(f"Директория {blockchain_dir} не найдена.")
        return []


def check_integrity():
    logging.info("Начинаем проверку целостности блоков")
    files = get_files()
    results = []

    for file in files[1:]:
        with open(blockchain_dir + str(file)) as f:
            h = json.load(f)['hash']

        pre_file = str(file - 1)
        current_hash = get_hash(pre_file)

        if h == current_hash:
            res = 'OK'
            logging.info(f"Блок {pre_file}: целостность подтверждена")
        else:
            res = 'Corrupted'
            logging.warning(f"Блок {pre_file}: поврежден")

        results.append({'block': pre_file, 'result': res})

    return results


def create_block(name, amount, to_whom):
    logging.info(f"Создаем блок: lender={name}, amount={amount}, to_whom={to_whom}")
    files = get_files()
    if not files:
        pre_file = 0
    else:
        pre_file = files[-1]

    filename = str(pre_file + 1)
    prev_hash = get_hash(str(pre_file))

    data = {
        'name': name,
        'amount': amount,
        'to_whom': to_whom,
        'hash': prev_hash
    }

    with open(blockchain_dir + filename, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    logging.info(f"Блок {filename} успешно создан")