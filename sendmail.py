#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import os
import sys
import smtplib
import time

PROVIDERS = {
	'GMAIL': {
		'domain': 'smtp.gmail.com',
		'port': 587,
		'encryption': 'tls'},
	'OUTLOOK': {
		'domain': 'smtp-mail.outlook.com',
		'port': 587,
		'encryption': 'tls'},
	'YAHOO': {
		'domain': 'smtp.mail.yahoo.com',
		'port': 587,
		'encryption': 'tls'},
	'AT&T': {
		'domain': 'smtp.mail.att.net',
		'port': 465,
		'encryption': 'ssl'},
	'COMCAST': {
		'domain': 'smtp.comcast.net',
		'port': 587,
		'encryption': 'tls'},
	'VERIZON': {
		'domain': 'smtp.verizon.net',
		'port': 465,
		'encryption': 'ssl'}
}

def send_mail(domain, port, encryption, username, password, addresses, subject, message)
	try:
		print('Setting up connection to server for email provider...')
		smtpObj = smtplib.SMTP(domain, port)
	except:
		try:
			port = 465
			encryption = 'ssl'
			smtpObj = smtplib.SMTP_SSL(domain, port)
		except:
			raise Exception('Unable to connect to server for email provider. Check your internet connection.')
			sys.exit()
	finally:
		print('Connecting to server for email provider...')
		server = smtpObj.ehlo()
		if int(server(0)) != 250:
			raise Exception('Server for email provider denied greeting request. Check your security settings.')
			sys.exit()
		else:
			print('Initial server connection successful...')

	if encryption == 'tls':
		try:
			print('Encrypting server connection with TLS...')
			server.starttls()
		except:
			raise Exception('Unable to encrypt TLS connection. Not sure what went wrong.')
			sys.exit()

	try:
		print('Logging into email server...')
		server.login(username, password)
	except:
		raise Exception('Unable to login into to email server. Check your login credentials & try again.')
		sys.exit()

	try:
		print('Sending emails to recipient addresses...')
		content = 'Subject: ' + subject + '\n' + message
		errors = server.sendmail(username, addresses, content)
	except:
		raise Exception('Unable to send emails. Check for your internet connection & list of recipients.')
		sys.exit()

	if len(errors) == 0:
		print('Successfully sent emails to all recipients.')
	else:
		print('Finished sending emails. Errors occured for the following recipients:')
		for key, value in errors.items():
			print(key, ' - ', value)

	if len(errors) == 0:
		address_list = addresses
	else:
		address_list = []
		for address in addresses:
			if address not in errors.keys and address not in error.values:
				address_list.append(address)

	local = time.localtime()
	day = str(local.tm_mday)
	month = str(local.tm_mon)
	year = str(local.tm_year)
	hour = str(local.tm_hour)
	minute = str(local.tm_min)
	timestamp = '{}{}{}_{}{}'.format(month,day,year,hour,minute)

	try:
		with open(('./logs/'+timestamp+'.txt'), 'w') as f:
			f.write('TO: ')
			for address in address_list:
				f.write(address, ';')
			f.write('\nFROM: {}'.format(username))
			f.write('\n\n')
			f.write(content)
		print('Records of emails sent have been stored in a text file under the ./logs directory.')
	except:
		print('Unable to store email logs in text file. Not sure what went wrong.')

	print('All done. Nothing more to do.')


def main():
	if os.path.exists('./config/login.ini') is False:
		raise Exception('Missing login configuration file in ./config directory containing username & password.')
	if os.path.exists('./config/subject.txt') is False:
		raise Exception('Missing text file in ./config directory containing subject header.')
		sys.exit()
	if os.path.exists('./config/message.txt') is False:
		raise Exception('Missing text file in c./onfig directory containing message content.')
		sys.exit()
	if os.path.exists('./config/addresses.txt') is False:
		raise Exception('Missing text file in ./config directory containing email addresses.')
		sys.exit()

	config = configparser.ConfigParser()
	config.read('./config/login.ini')
	sections = list(config.sections)

	provider = sections[0].upper()
	try:
		username = config[provider]['username']
		password = config[provider]['password']
	except:
		raise Exception('Login configuration file misisng username and/or password for email server.')
		sys.exit()
	domain = PROVIDERS[provider]['domain']
	port = PROVIDERS[provider]['port']
	encryption = PROVIDERS[provider]['encryption']

	with open('./config/subject.txt', 'r') as f:
		subject = f.read.replace('\n', '').strip()
	with open('./config/message.txt', 'r') as f:
		message = f.read()
	with open('./config/addresses.txt', 'r') as f:
		addresses = []
		for line in f:
			addresses.append(line.replace('\n', '').strip())

	send_email(domain, port, encryption, username, password, addresses, subject, message)

if __name__ == '__main__':
	main()