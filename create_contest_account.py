#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""TIOJ AUTO ADD Acount Script"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import requests
import random
import string
from bs4 import BeautifulSoup

# config

contest_name = 'prefix_' # Less than 8 char
num = 1 # How many account you want to create
image_file_path = '' # Leave blank if you don't want to upload a image

# end config

judge_url = 'https://tioj.ck.tp.edu.tw'
sign_up_get_url = judge_url + '/users/sign_up'
sign_up_post_url = judge_url + '/users'
output_file = 'account_list.csv'


def random_string(length):
   return u''.join(random.choice('abcdefghijkmnprstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789') for i in range(length))


try:
    if image_file_path:
        img = open(image_file_path,'rb')
except IOError as e:
    print('JIZZ!! Image not found!!')
	print(e)
    exit(0)


with open(output_file, 'a') as f:
    for _i in range(num):
        i = _i + 1
        session = requests.Session()
        rel = session.get(sign_up_get_url)
        soup = BeautifulSoup(rel.text, "html.parser")
        inputs = soup.find('form').find_all('input')

        name = u'%s%02d' % (contest_name, i)
        password = random_string(6)


        f.write(u'%d,%s,%s\n' % (i, name, password))

        data = {
            inputs[0].attrs['name']: inputs[0].attrs['value'],
            inputs[1].attrs['name']: inputs[1].attrs['value'],
            'user[email]': u'%s@auto.upload' % name,
            'user[username]': name,
            'user[nickname]': name,
            'user[password]': password,
            'user[password_confirmation]': password,
            'user[name]': name,
            'user[school]': 'meow',
            'user[gradyear]': '111',
            'commit': 'Sign up'
        }
        rel = session.post(sign_up_post_url, data=data)
        print(rel.status_code)

        data['user[current_password]'] = password
        del data['user[password]']
        del data['user[password_confirmation]']
        del data['user[username]']
        data['_method'] = 'put'
        data['commit'] = 'Update'
        try:
            rel = session.post(sign_up_post_url, data=data, files={'user[avatar]':open(image_file_path, 'rb')})
        except FileNotFoundError as e:
            print(e)

        print(rel.status_code)
        print('Create %d!!' % i)
