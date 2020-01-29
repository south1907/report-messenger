import os.path
import json
import os
import time
import datetime

# Create by namph

root_path = os.path.dirname(os.path.abspath(__file__)) + '/data'

if os.path.isdir(root_path):
	folders = os.listdir(root_path)

	result = []
	for folder in folders:

		# check not folder media
		if os.path.isfile(root_path + '/' + folder + '/message_1.json'):
			# print(folder)

			# for message json in folder. If many many chat, fb split to many files
			files = os.listdir(root_path + '/' + folder)

			tmp = {}

			count_partner = 0
			count_me = 0
			last_time = 0
			last_message = 0

			try:
				for file in files:
					with open(root_path + '/' + folder + '/' + file, encoding='raw_unicode_escape') as f:
						json_string = f.read()
						data = json.loads(json_string.encode('raw_unicode_escape').decode())

					# not group
					if len(data['participants']) == 2:
						messages = data['messages']
						for message in sorted(messages, key = lambda i: i['timestamp_ms']):

							# contain hello message
							# if 'content' in message and 'Say hi to your new Facebook friend' in message['content']:
							# 	continue

							participants = data['participants']
							partner = participants[0]['name']
							me = participants[1]['name']

							timestamp_ms = message['timestamp_ms']
							timestamp_2019 = 1546300800000
							timestamp_2020 = 1577836800000
							
							# message in 2019
							if timestamp_ms < timestamp_2019 or timestamp_ms >= timestamp_2020:
								continue

							sender = message['sender_name']
							last_time = timestamp_ms
							if 'content' in message:
								last_message = message['content']

							if sender == partner:
								count_partner += 1

							if sender == me:
								count_me += 1

			except Exception as e:
				print('error load file ' + folder)

			tmp = {
				'name': partner,
				'count_partner': count_partner,
				'count_me': count_me,
				'total': count_me + count_partner,
				'last_time': time.strftime("%d/%m/%Y: %H:%M:%S", time.localtime(last_time / 1000)),
				'last_message': last_message
			}

			if (tmp['total'] > 0):
				result.append(tmp)

			# break
	
	count = 0
	for item in sorted(result, key = lambda i: i['total'], reverse=True):
  		
  		count += 1
  		if count > 100:
  			break
  		print(str(count) + ' | '  + item['name'] + ' | '  + str(item['total']) + ' | '  + str(item['count_partner']) + ' | '  + str(item['count_me'])  + ' | '  + str(item['last_time']) + ' | '  + str(item['last_message']))

  		# break