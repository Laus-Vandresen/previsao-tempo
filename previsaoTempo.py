import requests
import json
from datetime import date
import urllib.parse

accuwheaterApiKey = 'gbdGCHk5hXTYCMeIPzQbkbCFGHmrwXeI'
mapBoxToken = 'pk.eyJ1IjoibGF1c3ZhbiIsImEiOiJja2xqeTk5NHgzMzlvMm90a2xhaDAzYzIwIn0.JuD8eonQkwAirBacw8Zarg'
diasSemana = ['Domingo', 'Segunda-Feira', 'Terça-Feira', 'Quarta-Feira', 'Quinta-Feira', 'Sexta-Feira','Sábado']

def pegarCoordenadas():
    r = requests.get('http://www.geoplugin.net/json.gp')
    if r.status_code != 200:
        print('Não foi possivel obter a localização')
        return None
    else:
        try:
            localizacao = json.loads(r.text)
            coordenadas = {}
            coordenadas['lat'] = localizacao['geoplugin_latitude']
            coordenadas['long'] = localizacao['geoplugin_longitude']
            return coordenadas
        except:
            return None

def pegarCodigoLocal(lat, long):
    locationApiUrl = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=' + accuwheaterApiKey + '&q=' + lat +'%2C' + long +'&language=pt-br'

    r = requests.get(locationApiUrl)
    if r.status_code != 200:
        print('Não foi possivel obter o código do local')
        return None
    else:
        try:
            locationResponse = json.loads(r.text)
            infoLocal = {}
            infoLocal['nomeLocal'] = locationResponse['LocalizedName'] + ',' + locationResponse['AdministrativeArea']['LocalizedName'] + '. ' + locationResponse['Country']['LocalizedName']
            infoLocal['codigoLocal'] = locationResponse['Key']
            return infoLocal
        except:
            return None
        
def pegarTempoAgora(codigoLocal, nomeLocal):
    currentConditionsUrl = 'http://dataservice.accuweather.com/currentconditions/v1/' + codigoLocal + '?apikey=' + accuwheaterApiKey +'&language=pt-br'

    r = requests.get(currentConditionsUrl)
    if r.status_code != 200:
        print('Não foi possivel obter o clima atual')
        return None
    else:
        try:
            currentConditionResponse = json.loads(r.text)
            infoClima = {}
            infoClima['textoClima'] = currentConditionResponse[0]['WeatherText']
            infoClima['temperatura'] = currentConditionResponse[0]['Temperature']['Metric']['Value']
            infoClima['nomeLocal'] = nomeLocal
            return infoClima
        except:
            return None

def pegarPrevisaoProximosDias(codigoLocal):
    weatherFiveUrl = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/' + codigoLocal + '?apikey=' + accuwheaterApiKey + '&language=pt-br&metric=true'
    r = requests.get(weatherFiveUrl)
    if r.status_code != 200:
        print('Não foi possivel obter o clima atual') 
    else:
        try:
            weatherResponse = json.loads(r.text)
            infoClima5Dias = []
            for day in weatherResponse['DailyForecasts']:
                climaDia = {}
                climaDia['max'] = day['Temperature']['Maximum']['Value']
                climaDia['min'] = day['Temperature']['Minimum']['Value']
                climaDia['clima'] = day['Day']['IconPhrase']
                climaDia['dia'] = diasSemana[int(date.fromtimestamp(day['EpochDate']).strftime('%w'))]
                infoClima5Dias.append(climaDia)
            return infoClima5Dias
        except:
            print('Não foi possivel obter o clima atual')

def mostrarPrevisao(lat, long):
    try:
        local = pegarCodigoLocal(lat, long)
        climaAtual = pegarTempoAgora(local['codigoLocal'], local['nomeLocal'])
        print('Clima atual em ' + climaAtual['nomeLocal'])
        print(climaAtual['textoClima'])
        print('Temperatura ' + str(climaAtual['temperatura']) + '\xb0' + 'C')
    except:
        print('Erro ao obter o clima atual')
        return None

    respostaUsuario = input('Deseja ver o clima dos próximos dias? (s ou n): ').lower()
    if respostaUsuario == 's':
        print('\nClima para hoje e os próximos dias: \n')
        try:
            previsao5Dias = pegarPrevisaoProximosDias(local['codigoLocal'])
            for day in previsao5Dias:
                print(day['dia'])
                print('Mínima: ' + str(day['min']) + '\xb0' + 'C')
                print('Máxima: ' + str(day['max']) + '\xb0' + 'C')
                print('Clima: ' + day['clima'])
                print('\n')
        except:
            print('Erro ao obter a previsão para os próximos dias')
            return None

def pesquisarLocal(local):
    _local = urllib.parse.quote(local)
    mapBoxUrl = 'https://api.mapbox.com/geocoding/v5/mapbox.places/' + _local +'.json?access_token=' + mapBoxToken
    r = requests.get(mapBoxUrl)
    if r.status_code != 200:
        print('Não foi possivel obter a localização') 
    else:
        try:
            localizationResponse = json.loads(r.text)
            coordenadas = {}
            coordenadas['long'] = str(localizationResponse['features'][0]['geometry']['coordinates'][0])
            coordenadas['lat'] = str(localizationResponse['features'][0]['geometry']['coordinates'][1])
            return coordenadas
        except:
            print('Não foi possivel obter o clima atual')
            return None




try:
    coordenadas = pegarCoordenadas()
    mostrarPrevisao(coordenadas['lat'], coordenadas['long'])
    
    continuar = 's'
    while continuar == 's':
        continuar = input('Deseja consultar a previsão de outro local? (s ou n): ').lower()
        print('\n')
        if continuar != 's':
            break
        local = input('Digite a cidade e o estado: ')
        print('\n')
        try:
            responseLocal = pesquisarLocal(local)
            mostrarPrevisao(responseLocal['lat'], responseLocal['long'])
        except:
            print('Não foi possível obter a previsão do tempo do local')


except:
    print('Erro ao processar Solicitação. Entre em contato com o suporte')