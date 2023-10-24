import asyncio
import json
import random
import time

import pika
import psycopg2
from pika.channel import Channel
from retry import retry

from application.services.cnpj_service import CNPJService
from models.cnpj import Cnpj

service = None

# Substitua 'user' e 'password' pelos seus dados
user = "admin"
password = "123123"
exchange_name = "receita-result"


def publish(channel: Channel, data):
    mensagem = {
        "messageType": [
            "urn:message:Alice.Lote.Sodexo.Domain.Bus:ReceitaProcessResult"
        ],
        "message": {
            "batchItem": {
                "document": data[0],
                "batchId": data[1],
                "birthDate": None,
                "batchItemId": data[2],
                "typeDocument": "Cnpj",
            }
        },
        "responseAddress": None,
        "messageId": None,
        "requestId": None,
        "conversationId": None,
        "sourceAddress": None,
    }

    # Publica a mensagem na exchange
    channel.basic_publish(
        exchange=exchange_name, routing_key="", body=json.dumps(mensagem)
    )


def consume_callback(ch: Channel, method, properties: pika.BasicProperties, body):
    try:
        obj = json.loads(body.decode("utf-8"))
        cpf = obj["message"]["batchItem"]["document"]
        print(cpf)
        success = False
        try:
            max_attempts = 10
            attempts = 0
            while attempts <= max_attempts:
                (response, cache, status) = asyncio.run(
                    service.consultar_cnpj(
                        cpf, headless=False
                    )
                )
                success = True
                break

            if status == 200:
                publish(
                    ch,
                    [
                        cpf,
                        obj["message"]["batchItem"]["batchId"],
                        obj["message"]["batchItem"]["batchItemId"]
                    ],
                )
            if status == 409 or status == 404:
                publish(
                    ch,
                    [
                        cpf,
                        obj["message"]["batchItem"]["batchId"],
                        obj["message"]["batchItem"]["batchItemId"]
                    ],
                )

            # Simula uma consulta (substitua pelo seu código real)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            if not cache:
                time.sleep(5)

        except Exception as error:
            # Publica a mensagem na exchange
            properties.headers.update({"error": str(error)})
            ch.basic_publish(
                exchange="receitapj_error",
                routing_key="",
                properties=properties,
                body=body,
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        properties.headers.update({"error": str(e)})
        ch.basic_publish(
                exchange="receitapj_error",
                routing_key="",
                properties=properties,
                body=body,
            )
        ch.basic_ack(delivery_tag=method.delivery_tag)



def run():
    # if __name__ == "__main__":

    # Substitua pelos detalhes de conexão do seu banco de dados
    db_host = "172.19.61.7"
    db_port = "5440"
    db_name = "receita"
    db_user = "postgres"
    db_password = "alice3795"
    application_name = "RoboReceitaPfApiTesteDue"

    # Abra uma conexão com o banco de dados
    connection = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password,
        application_name=application_name,
    )

    global service
    service = CNPJService(connection)

    connect_to_rabbitmq()


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 10))
def connect_to_rabbitmq():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="172.19.61.15",
            port=5672,
            virtual_host="alice-lote",
            credentials=pika.PlainCredentials(user, password),
        )
    )
    channel = connection.channel()

    queue = "receitapj"
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_qos(prefetch_count=1)

    print(f" [*] Waiting for messages in {queue}. To exit press CTRL+C")

    channel.basic_consume(
        queue=queue,
        on_message_callback=consume_callback,
        auto_ack=False,
    )
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()


if __name__ == "__main__":
    run()
