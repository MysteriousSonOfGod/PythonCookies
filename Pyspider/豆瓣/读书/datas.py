import csv
import logging

file = 'doubanbooks.csv'


def create_logging(logger_name, logger_file):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    handle_write = logging.FileHandler(logger_file)
    handle_print = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    handle_print.setFormatter(formatter)
    handle_write.setFormatter(formatter)
    logger.addHandler(handle_print)
    logger.addHandler(handle_write)
    return logger


def write_to_csv(house_dict):
    fieldnames = ['书名', '作者', '豆瓣评分', '简介']
    with open(file, 'a+', encoding='utf8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(house_dict)
