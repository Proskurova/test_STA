import time, datetime
import json
import pika
import sys
import os


def processes_message(message):
    print(f"Start time of the function{datetime.datetime.now()}")
    msg = json.loads(message)
    for content_file in msg['list_file'].values():
        with open(f"result/{str(msg['id'])}.txt", "a+", encoding="utf-32") as f:
            f.write(content_file + '\n')
    time.sleep(20)
    print(f" [x] The message is processed and saved to a file {msg['id']}.txt\n"
          f"The end time of the function{datetime.datetime.now()}")


def main():
    queue = 'rmq_test_qu'
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        processes_message(body)
        print(f" [x] Received {body}")

    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)