import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas
import os

config_file = open('./src/service/config.json','r')
config = json.load(config_file)

scope = config['scope']
creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(os.environ['CLIENT_SECRET_TEST']),scope)
client = gspread.authorize(creds)

sheet = client.open(config['archivo']['credencialesSFSF']['sheet'])
worksheet = sheet.worksheet(config['archivo']['credencialesSFSF']['workSheet'])

wsheet = worksheet.get_all_values()

# out json
def outCardsCredencialesSFSF(payload):
    cards = []

    for index, row in payload.iterrows():
        cards.append(
            {
              'header': {
                  'title': row.Cliente,
                  'subtitle': 'Company ID: '+row['Company ID']
                },
                'sections': [
                  {
                    'widgets': [
                          {
                          'buttons': [
                                  {
                                    'textButton': {
                                      'text': 'Link '+ row['Tipo Acceso'],
                                      'onClick': {
                                        'openLink': {
                                          'url': row.Link
                                        }
                                      }
                                    }
                                  }
                              ]
                          },
                          {
                              'keyValue': {
                                'topLabel': 'Usuario',
                                'content': row.Usuario
                              }
                          },
                          {
                              'keyValue': {
                                'topLabel': 'Contraseña',
                                'content': row.Contraseña
                              }
                          }
                    ]
                  }
                ]
              }
        )

    return cards

def BuscarCredenciales (cliente, ambiente = ''): 
  # header -> primera fila es un comentario
  df = pandas.DataFrame.from_records(wsheet[1:])

  # .values -> array o matriz
  header = (df.loc[df[0] == 'Cliente']).values[0]
  dataSet = (df.loc[df[0] != 'Cliente']).values

  dff = pandas.DataFrame.from_records(dataSet, columns = header)
  cliente = dff.Cliente.str.upper() == cliente.upper()

  if (ambiente != ''):
    ambiente = dff['Tipo Acceso'].str.upper() == ambiente.upper()

    return outCardsCredencialesSFSF(dff.loc[cliente & ambiente])
  else:        
    return outCardsCredencialesSFSF(dff.loc[cliente])
