#!/usr/bin/env python3
"""Example bot that returns a synchronous response."""

from flask import Flask, request, json
import src.mongo.hangouts as hangouts

cliente = 'd'
ambiente = 'prd'
link = 'https://google.com'
usuario = 'dsadas'
password = 'dsadsda'
companyId = 'C000000'

i = 0
a = []

while (i < 2):
	a.append(json.dumps({
				'header': {
			        'title': 'Arauco',
			        'subtitle': cliente
			      },
			      'sections': [
			        {
			          'widgets': [
			          		{
			          		'buttons': [
				                	{
					                  'textButton': {
					                    'text': 'Link '+ ambiente,
					                    'onClick': {
					                      'openLink': {
					                        'url': link
					                      }
					                    }
					                  }
					                }
				              	]
							},
							{
								'keyValue': {
								  'topLabel': 'Usuario',
								  'content': usuario
								}
							},
							{
								'keyValue': {
								  'topLabel': 'Contrasena',
								  'content': password
								}
							},
							{
								'keyValue': {
								  'topLabel': 'Company ID',
								  'content': companyId
								}
							}
			          ]
			        }
			      ]
			    }
			)
	)
	i = i + 1

app = Flask(__name__)

@app.route('/', methods=['POST'])

def on_event():
  event = request.get_json()
  
  #hangouts.guardarMensaje(event)

  if event['type'] == 'ADDED_TO_SPACE' and event['space']['type'] == 'ROOM':
    text = 'Thanks for adding me to "%s"!' % event['space']['displayName']
  elif event['type'] == 'MESSAGE':
    text = 'You said: `%s`' % event['message']['text']
  else:
    return
  return json.jsonify(
					{
					  'cards': a
					}
  				)

if __name__ == '__main__':
  app.run()
