import requests
import json
import pprint

accuwheaterApiKey = 'gbdGCHk5hXTYCMeIPzQbkbCFGHmrwXeI'

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
                climaDia = []
                climaDia['max'] = day['Temperature']['Maximum']['Value']
                climaDia['min'] = day['Temperature']['Minimum']['Value']
                climaDia['clima'] = day['Day']['IconPhrase']
                climaDia['dia'] = day['EpochDate']
                infoClima5Dias.append(climaDia)
            return infoClima5Dias
        except:
            print('Não foi possivel obter o clima atual')


try:
    coordenadas = pegarCoordenadas()
    local = pegarCodigoLocal(coordenadas['lat'], coordenadas['long'])
    climaAtual = pegarTempoAgora(local['codigoLocal'], local['nomeLocal'])
    print('Clima atual em ' + climaAtual['nomeLocal'])
    print(climaAtual['textoClima'])
    print('Temperatura ' + str(climaAtual['temperatura']) + '\xb0' + 'C')

    print('\nClima para hoje e os próximos dias: \n')
    previsao5Dias = pegarPrevisaoProximosDias(local['codigoLocal'])
    print(previsao5Dias)
except:
    print('Erro ao processar Solicitação. Entre em contato com o suporte')






