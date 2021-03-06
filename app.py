#!/usr/bin/env python3
"""Example bot that returns a synchronous response."""

from flask import Flask, request, json
import src.mongo.hangouts as hangouts
import src.service.buscarCredencialesSFSF as bc
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
  return 'Hello', 200

@app.route('/push', methods=['POST'])
def index_on_event():
  event = request.get_json()
  
  if os.environ['FLASK_ENV'] != 'development':
    hangouts.guardarMensaje(event)

  if event['type'] == 'ADDED_TO_SPACE' and event['space']['type'] == 'ROOM':
    return json.jsonify({'text': 'Hola! Por ahora, solo puedo ayudar con credenciales de SFSF... Preguntas como entel, abastible, arauco, etc...'})
  elif event['type'] == 'MESSAGE':
    text = event['message']['text']
  else:
    return 
  
  return json.jsonify( bc.BuscarCredenciales(text) )

def main():
  if os.environ['FLASK_ENV'] == 'development':
      app.run()
  else:
      app.run("0.0.0.0", port=80, debug=False)

if __name__ == '__main__':
  main()
