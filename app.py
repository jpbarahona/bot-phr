#!/usr/bin/env python3
"""Example bot that returns a synchronous response."""

from flask import Flask, request, json
import src.mongo.hangouts as hangouts

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
					  'cards': [
					    {
					      'header': {
					        'title': 'Arauco',
					        'subtitle': 'Credenciales'
					      },
					      'sections': [
					        {
					          'widgets': [
					              {
					                'keyValue': {
					                  'topLabel': 'Ambiente',
					                  'content': 'PRD'
					                  }
					              },
					              {
					                'keyValue': {
					                  'topLabel': 'Usuario',
					                  'content': 'phr'
					                }
					              },
					              {
					                'keyValue': {
					                  'topLabel': 'Contraseña',
					                  'content': 'dsa'
					                }
					              },
					              {
					                'keyValue': {
					                  'topLabel': 'Company ID',
					                  'content': 'C000000000'
					                }
					              },
					             	'buttons': [
									{
					                  'textButton': {
					                      'text': 'Link',
					                      'onClick': {
						                      'openLink': {
						                        'url': 'https://google.com/'
						                      }
					                      }
					                  }
					                }
								]
					          ]
					        }
					      ]
					    }
					  ]
					}
  	)

if __name__ == '__main__':
  app.run()
