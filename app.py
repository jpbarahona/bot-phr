#!/usr/bin/env python3
"""Example bot that returns a synchronous response."""

from flask import Flask, request, json
import src.mongo.hangouts as hangouts
import src.service.buscarCredencialesSFSF as bc

app = Flask(__name__)

@app.route('/', methods=['POST'])

def on_event():
  event = request.get_json()
  
  #hangouts.guardarMensaje(event)

  if event['type'] == 'ADDED_TO_SPACE' and event['space']['type'] == 'ROOM':
    return json.jsonify({'text': 'Hola! Por ahora, solo puedo ayudar con credenciales de SFSF... algunas... debido a la densidad de usuarios en algunos clientes, iré mejorando durante los días'})
  elif event['type'] == 'MESSAGE':
    text = event['message']['text']
  else:
    return 
  
  return json.jsonify( bc.BuscarCredenciales(text) )

if __name__ == '__main__':
  app.run()
