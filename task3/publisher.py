import pika
import os
import json
import time


def create_messages():
    files = {}
    all_files = os.listdir("data/")
    for file in all_files:
        with open(f'data/{file}') as f:
            value = f.read()
            key = f'{file[:-4]}'
            files.update([(key, value)])
        os.remove(f"data/{file}")
    return files


def main():
    queue = 'rmq_test_qu'
    exchange = 'rmq_test_ex'

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, exchange_type='direct')

    channel.queue_declare(queue=queue, durable=True)

    channel.queue_bind(exchange=exchange, queue=queue)

    index = 0
    while True:
        index = index + 1
        if index > 50:
            break

        message = json.dumps({
            "id": index,
            "list_file": create_messages(),
        })

        channel.basic_publish(
            exchange=exchange,
            routing_key=queue,
            properties=pika.BasicProperties(
                delivery_mode=2,
            ),
            body=message,
        )
        print(f" [x] Sent {index}")
        time.sleep(10)

    connection.close()


if __name__ == '__main__':
    main()
