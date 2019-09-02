import os
import sys

my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../yggtorrentscraper/')
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
