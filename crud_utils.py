### 
# Este é o ÚNICO script necessário para import no horus.py para inserir
# os dados no sistema. A princípio, o único método a ser usado vai ser o
# inserir_dado()
###
import sqlite3
import db_utils
import logging
import time
import datetime

logger = logging.getLogger('crud_utils')
handler = logging.FileHandler('datalog.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

###
# Só enviar a quantidade da contagem e a config da rasp, o resto a função executa,
# inclusive gera o horário da contagem
# Diluição: se contagem > 1, por ex. 5, esse valor será quebrado em 5 inserts no sistema.
# ex. chamada:
# import crud_utils
#
# crud_utils.inserir_dado(2, 2, 'd3f2d810-1193-4cef-8a7a-971890a4157d', 5)
###
def inserir_dado(cd_empresa, cd_local, rasp_id, contagem):
    retok = False

    if db_utils.criar_tabelas():
        try:
            conn = sqlite3.connect('dados_recon.db')
            cur = conn.cursor()
            horario = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")

            ## valor de contagem gera um loop para diluir em uma única info de contagem
            for x in range(contagem):            
                cur.execute("""
                    insert into dados_recon(cd_empresa, cd_local, raspid, horario_recon, enviado)
                    values (?, ?, ?, ?, ?)
                """, (cd_empresa, cd_local, rasp_id, horario, 0))

            conn.commit()
            conn.close()
            retok = True
        except Exception as e:
            logger.info('erro gerado: ' + str(e))
            conn.close()

    return retok

## armazena o token no BD para não precisar buscar um novo a cada chamada ao server
def upsert_token(token, expiration_date, is_update):
    retok = False
    
    if db_utils.criar_tabelas():
        try:
            conn = sqlite3.connect('dados_recon.db')
            cur = conn.cursor()

            if not is_update:
                cur.execute("""
                    insert into token_data(codigo, access_token, expiration_date)
                    values (?, ?, ?)
                """, (1, token, expiration_date))
            else:
                cur.execute("""
                    update token_data set access_token = ? and expiration_date = ?
                    where codigo = 1
                """, (token, expiration_date))

            conn.commit()
            conn.close()
            retok = True
        except Exception as e:
            logger.info('erro gerado (upsert_token): ' + str(e))
            conn.close()

    return retok

## atualiza o dado contagem conforme valor - se 1 enviado / 0 - não enviado
def update_dado(codigo, valor):
    retok = True

    try:
        conn = sqlite3.connect('dados_recon.db')
        cur = conn.cursor()

        cur.execute("""
            update dados_recon
            set enviado = ?
            where codigo = ?
        """, (valor, codigo))

        conn.commit()
        conn.close()
    except Exception as e:
        logger.info('erro gerado (update_dado): ' + str(e))
        conn.close()
        retok = False

    return retok

def read_nao_enviados():
    if not db_utils.criar_tabelas():
        return []

    sql = 'select * from dados_recon where enviado = 0'
    conn = sqlite3.connect('dados_recon.db')
    cur = conn.cursor()
    query = cur.execute(sql)
    dados = query.fetchall()
    conn.close()

    return dados

def get_token_bd():
    if not db_utils.criar_tabelas():
        return []

    sql = 'select access_token, expiration_date from token_data where codigo = 1'
    conn = sqlite3.connect('dados_recon.db')
    cur = conn.cursor()
    query = cur.execute(sql)
    dados = query.fetchall()
    conn.close()

    return dados