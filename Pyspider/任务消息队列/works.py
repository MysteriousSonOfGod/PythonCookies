import pika
import requests
from faker import Factory

fake = Factory.create()


class JiandanImg(object):
    def __init__(self, host='localhost'):
        self.host = host
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='jiandan_meizhi', durable=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.download, queue='jiandan_meizhi')
        print(' [*] Waiting for messages. To exit press CTRL+C')

    def download(self, ch, method, properties, body):
        rs = requests.get(body, headers={'User-Agent': fake.user_agent()}).content
        with open(body.decode().split(r'/')[-1], 'wb') as f:
            f.write(rs)
        self.pri()
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print('已经消费了body')

    def pri(self):
        print('可以跳转？？')

    def consume(self):
        self.channel.start_consuming()


if __name__ == '__main__':
    jiandanimg = JiandanImg('localhost')
    jiandanimg.consume()
