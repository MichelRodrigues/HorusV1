import sqlite3

def criar_tabelas():
    try:
        conn = sqlite3.connect('dados_recon.db')
        cur = conn.cursor()

        sql = """
        create table if not exists dados_recon (
            codigo integer not null primary key autoincrement,
            cd_empresa integer not null,
            cd_local integer not null,
            raspid text not null,
            idade_aprox integer,
            genero text,
            horario_recon text not null,
            enviado integer not null
        );
        """
        #enviado: se = 0, não foi enviado. se = 1, enviado

        cur.execute(sql)

        sql = """
        create table if not exists token_data (
            codigo integer not null primary key,
            access_token text not null,
            expiration_date text not null
        );
        """

        cur.execute(sql)
        conn.close()
    except sqlite3.Error:
        print('Erro ao verificar criação do BD/tabelas')
        return False

    return True