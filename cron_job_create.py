import subprocess
import sys

try:
    from crontab import CronTab
    import_crontab_ok = True
except:
    import_crontab_ok = False

    try:
        subprocess.call([sys.executable, "-m", "pip", "install", "python_crontab"])
        print('** Python crontab instalado com sucesso **')
        from crontab import CronTab
        import_crontab_ok = True
    except:
        print('Não foi possível instalar e importar o python_crontab! Impossível criar job.')

job_comment = 'job_send_data'

def add_job(file_path, hora, minuto):
    cron = CronTab(user='root')
    job = cron.new(command = 'cd {} && $(which python3) send_recon_data.py'.format(file_path), 
        comment = job_comment)
    job.minute.on(minuto)
    job.hour.also.on(hora)
    cron.write()
    print('Job criado com sucesso! Lista existentes: ')

    for item in cron:
        print(item)

def remove_job():
    cron = CronTab(user='root')
    cron.remove_all(comment = job_comment)
    cron.write()
    print('Job excluído com sucesso! Remanescentes: ')

    for item in cron:
        print(item)

def check_hora_min(hora, minuto):
    if hora < 0 or hora > 23:
        print('Hora informada deve ser entre 0 e 23')
        return False

    if minuto < 0 or minuto > 59:
        print ('Minuto informado deve ser entre 0 e 59')
        return False

    return True

if __name__ == '__main__':
    if import_crontab_ok:
        if len(sys.argv) == 4:
            try:
                file_path = str(sys.argv[1])
                hora = int(sys.argv[2])
                minuto = int(sys.argv[3])

                if check_hora_min(hora, minuto):
                    add_job(file_path, hora, minuto)
            except:
                print('Algum dos parâmetros não foi informado corretamente. Não foi possível criar o job')
        else:
            print('Erro ao criar job: informe todos os parâmetros (caminho - hora - minuto)')
else:
    if import_crontab_ok:
        remove_job()