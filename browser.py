from bs4 import BeautifulSoup
from collections import deque
import argparse
import os
import requests

parser = argparse.ArgumentParser()
parser.add_argument('dir')
args = parser.parse_args()

if args.dir:
    dir_name = args.dir
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        print('Diretory ' + dir_name + ' already exists')


#with open(args.dir + '/nytimes.txt', 'w', encoding='utf-8') as file_nytimes, \
#        open(args.dir + '/bloomberg.txt', 'w', encoding='utf-8') as file_bloomberg:
#    file_nytimes.write(nytimes_com)
#    file_bloomberg.write(bloomberg_com)

stack = deque()
path = ''
while True:
    url = input()
    if url == "exit":
        break
    elif url == 'back':
        try:
            with open(stack.pop(), 'r', encoding='utf-8') as file:
                print(file.read())
        except FileNotFoundError:
            print('error')

    elif url.endswith('.com') or url.endswith('.org'):
        stack.append(path)
        if not url.startswith('https://'):
            url = 'https://' + url
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        tags = soup.find_all(['p', 'a', 'ul', 'ol', 'li'])
        url = url[8:]
        path = args.dir + '/' + url.split('.')[0] + '.txt'
        try:
            with open(path, 'w', encoding='utf-8') as file:
                for tag in tags:
                    if tag.name == 'a':
                        print('\033[34m' + tag.get_text())
                        print('\033[39m')  # and reset to default color
                    else:
                        print(tag.get_text())
                    file.write(tag.get_text())

        except FileNotFoundError:
            print('error')
    else:
        print('error')
