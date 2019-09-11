import pika
import requests
from faker import Factory

URI = 'http://jandan.net/ooxx'
fake = Factory.create()


class Jiandan(object):
    def __init__(self, host='localhost'):
        self.host = host
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='jiandan_meizhi', durable=True)

    def close(self):
        self.connection.close()

    def publish(self, message):
        self.channel.basic_publish(exchange='', routing_key='jiandan_meizhi',
                                   body=message, properties=pika.BasicProperties(delivery_mode=2))

    def fetch(self):
        rs = requests.get('https://www.baidu.com', headers={'User-Agent': fake.user_agent()}).content
        # selector = etree.HTML(rs)
        # urls = selector.xpath('//a[@class="view_img_link"]/@href')
        print('charu')
        self.publish('http://gz.lianjia.com/zufang/GZ0002002779.html')
        self.publish('http://gz.lianjia.com/zufang/GZ0002042073.html')
        self.publish('http://gz.lianjia.com/zufang/GZ0002045392.html')
        self.publish('http://gz.lianjia.com/zufang/GZ0002159665.html')
        self.publish('http://gz.lianjia.com/zufang/GZ0002166394.html')
        self.publish('http://gz.lianjia.com/zufang/GZ0002167192.html')
        self.publish('http://gz.lianjia.com/zufang/GZ0002171748.html')
        self.publish('http://gz.lianjia.com/zufang/GZ0002171998.html')
        self.publish('http://gz.lianjia.com/zufang/GZ0002172114.html')
        # for url in urls:
        #     print(url)
        #     self.publish(urljoin('http://', url))

    def run(self):
        self.fetch()


if __name__ == '__main__':
    jiandan = Jiandan('localhost')
    jiandan.run()
    jiandan.close()
