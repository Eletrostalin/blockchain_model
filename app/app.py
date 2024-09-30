import logging
from flask import Flask, render_template, redirect, url_for, request
from block import create_block, check_integrity

app = Flask(__name__)

# Настроим логирование
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/', methods=['POST', 'GET'])
def index():
    logging.info("Запрос на главную страницу")

    if request.method == 'POST':
        lender = request.form['lender']
        amount = request.form['amount']
        borrower = request.form['borrower']

        logging.info(f"POST-запрос: lender={lender}, amount={amount}, borrower={borrower}")
        create_block(name=lender, amount=amount, to_whom=borrower)

        logging.info("Блок успешно создан")
        return redirect(url_for('index'))

    return render_template('index.html')


@app.route('/cheking', methods=["GET"])
def check():
    logging.info("Запрос на проверку целостности блоков")
    results = check_integrity()
    logging.info(f"Результаты проверки: {results}")
    return render_template('index.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)