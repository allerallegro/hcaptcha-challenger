from datetime import datetime, timedelta
from threading import Thread

from flask import Flask, jsonify

from application.consumers.cnpj_consumer import get_datetime, run, set_datetime

app = Flask(__name__)

last_update = datetime.now()


@app.route("/")
def home():
    return "Bem-vindo à sua aplicação!"


@app.route("/healthcheck")
def healthcheck():
    if not last_update is None:
        dif = datetime.now() - get_datetime()
        if dif > timedelta(minutes=3):
            return jsonify(status="error")
    return jsonify(status="ok", last_update=last_update)


def run_flask():
    app.run(host="0.0.0.0", port=6000)


if __name__ == "__main__":
    # Inicie o Flask em uma thread separada
    thread_flask = Thread(target=run_flask)
    thread_flask.start()
    run()
