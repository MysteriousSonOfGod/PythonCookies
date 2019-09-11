from scrapy import cmdline

cmdline.execute('scrapy crawl cars -s LOG_FILE=logo.log'.split())
