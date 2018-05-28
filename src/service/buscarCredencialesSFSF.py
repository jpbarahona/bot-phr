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

# header -> primera fila es un comentario
df = pandas.DataFrame.from_records(wsheet[1:])

# .values -> array o matriz
header = (df.loc[df[0] == 'Cliente']).values[0]
dataSet = (df.loc[df[0] != 'Cliente']).values

dff = pandas.DataFrame.from_records(dataSet, columns = header)

# out json
def _outCardsCredencialesSFSF(payload):
    cards = []
    result = payload

    for index, row in result.iterrows():
        cards.append(
            {
                    'header': {
                        'title': 'Arauco',
                        'subtitle': row.Cliente
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
                                },
                                {
                                    'keyValue': {
                                      'topLabel': 'Company ID',
                                      'content': row['Company ID']
                                    }
                                }
                          ]
                        }
                      ]
                    }
        )
        
    return cards

def BuscarCredenciales (cliente, ambiente = ''):
	cliente = dff.Cliente == cliente

	config.close()

	if (ambiente != ''):
		ambiente = dff['Tipo Acceso'] == ambiente

		return _outCardsCredencialesSFSF(dff.loc[cliente & ambiente])
	else:
		return _outCardsCredencialesSFSF(dff.loc[cliente])
