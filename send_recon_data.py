###
# Para enviar os dados ao servidor, executar ESTE script
###
import requests
import json
import time
import datetime
import crud_utils

def enviaDados():
    dataRecon = crud_utils.read_nao_enviados()

    if len(dataRecon) > 0:
        token = getToken()

        if token == '':
            print('Erro ao buscar o token. Não foi possível o envio dos dados')
            return

        list_dados = []

        for item in dataRecon:
            dado = {
                "codigo": item[0],
                "cdEmpresa": item[1],
                "cdLocal": item[2],
                "raspId": item[3],
                "idadeAprox": 20,
                "genero": "M",
                "horarioRecon": item[6]
            }
            list_dados.append(dado)

        request_body = {
            "singleReconDataList": list_dados,
            "totalCount": len(list_dados)
        }
        url = 'http://facesapi.trudata.com.br/api/v1/ReconData/Multiple'
        header = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}
        
        try:
            resp = requests.post(url = url, data = json.dumps(request_body), headers = header, timeout = 10)
        except Exception as e:
            print('Ocorreu um problema com a requisição. Verifique o acesso à web. Erro: ' + str(e))
            return

        if resp.status_code == 400 or resp.status_code == 401:
            print('Não foi possível enviar os registros. Acesso não autorizado')
            return

        if resp.status_code == 200:
            analisaRetornoDados(resp.json(), dataRecon)
            return

        print('Ocorreu algum problema com a execução.')

    print('Não existem dados para envio.')
            

def getToken():
    token = ''
    token_data = crud_utils.get_token_bd()

    if len(token_data) == 0:
        json_token = request_token()

        if json_token is not None and json_token.get('authenticated') == True:
            token = json_token.get('accessToken')
            crud_utils.upsert_token(token, json_token.get('expiration'), False)
    else:
        token = token_data[0][0]
        str_data_expirado = token_data[0][1]
        data_expirado = datetime.datetime.strptime(str_data_expirado, '%Y-%m-%d %H:%M:%S')

        ##verifica se o token já venceu, atualiza
        if (datetime.datetime.now() > data_expirado):
            json_token = request_token()

            if json_token is not None and json_token.get('authenticated') == True:
                token = json_token.get('accessToken')
                crud_utils.upsert_token(token, json_token.get('expiration'), True)

    return token

def request_token():
    url = 'http://facesapi.trudata.com.br/api/v1/Login'
    requestBody = {
            "userName": "jedi@hansenautomacao.com",
            "password": "@H4ns3n!."
        }
    headers = {'content-type': 'application/json'}

    try:
        resp = requests.post(url, data = json.dumps(requestBody), headers = headers, timeout = 10)
    except:
        print('Não foi possível conectar ao servidor para obter o token. Tente mais tarde.')
        return

    status = resp.status_code

    if (status == 200):
        json_token = resp.json()
        return json_token

    return

def analisaRetornoDados(retorno, dados_enviados):
    count_retorno = retorno.get('itensCount')
    count_enviados = len(dados_enviados)

    if count_retorno == len(dados_enviados):
        print('Não foi possível inserir nenhum registro no servidor.')
        return

    for item in dados_enviados:
        crud_utils.update_dado(item[0], 1)

    ##statusCode = 2 todos os dados ok, se não for tem itens com erro
    if retorno.get('statusCode') == '2':
        print('Todos os dados foram enviados com sucesso. Total: {}'.format(count_enviados))
        return

    itens_erro = retorno.get('itens')

    for item in itens_erro:
        crud_utils.update_dado(item.get('codigo'), 0)

    itens_sucesso = count_enviados - count_retorno
    print('Dados inseridos parcialmente no servidor. Com sucesso: {} / Erros: {}'.format(
        itens_sucesso, count_retorno))


enviaDados()