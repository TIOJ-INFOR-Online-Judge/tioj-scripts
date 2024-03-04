#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import random
import string
from bs4 import BeautifulSoup
from getpass import *
from os import listdir
from os.path import join, isfile

judge_site = 'https://tioj.ck.tp.edu.tw'

session = requests.Session()
def login():
	TIOJusername = input('Username: ')
	TIOJpassword = getpass('Password: ')
	print('logging in...')
	global session
	rel = session.get(judge_site + '/users/sign_in')
	soup = BeautifulSoup(rel.text, "html.parser")
	inputs = soup.find('form').find_all('input')
	rel = session.post(judge_site + '/users/sign_in', data = {
		'authenticity_token': inputs[0].attrs['value'],
		'user[username]': TIOJusername,
		'user[password]': TIOJpassword,
		'user[remember_me]': '1',
		'commit': 'Sign in'
	})

login()
print('Successful log in')

problem_id = input('Problem ID: ')
tdpath = input('Testdata folder path: ')
files = [join(tdpath, f[:-3]) for f in listdir(tdpath) if isfile(join(tdpath, f)) and f[-3:] == '.in']

time_limit = input('Time limit: ')
memory_limit = input('Memory limit: ')

sign_up_get_url = judge_site + '/problems/%s/testdata/new' % problem_id
sign_up_post_url = judge_site + '/problems/%s/testdata' % problem_id
for f in files:
	print(f'processing {f}...')
	rel = session.get(sign_up_get_url)
	soup = BeautifulSoup(rel.text, "html.parser")
	inputs = soup.find('form').find_all('input')
	rel = session.post(sign_up_post_url, data = {
		'authenticity_token': inputs[0].attrs['value'],
		'testdatum[limit_attributes][time]': time_limit,
		'testdatum[limit_attributes][memory]': memory_limit,
		'testdatum[limit_attributes][output]': '65536',
		'testdatum[problem_id]': problem_id,
		'commit': 'Create Testdatum'
	}, files = {
		'testdatum[test_input]': open(f'{f}.in', 'rb'),
		'testdatum[test_output]': open(f'{f}.ans', 'rb')
	})
	print(f'Create {f}.')
