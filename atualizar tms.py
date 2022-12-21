from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from google_api_functions import *
from selenium import webdriver
from counter_restart import *
from exceptions import *
import pandas as pd
import logging
import time
import json
import os
import numpy as np
import traceback

def verificarPausa():
    while True:
        try:
            os.chdir(diretorio_robo)
            with open("pause.json", "r") as infile:
                parametros = json.load(infile)
            if parametros["statuspausa"]:
                time.sleep(2)
                print("Robô em pausa")
            else:
                break
        except:
            time.sleep(2)
            print('verificar')
            pass

def retornarEncerramentoFalse():
    while True:
        try:
            with open("exit.json", "r") as infile:
                parametros = json.load(infile)
            break
        except FileNotFoundError:
            parametros = {
            "statusencerramento": False,
        }
            with open("exit.json", "w") as outfile:
                json.dump(parametros, outfile)

    if parametros["statusencerramento"] == True:
        parametros["statusencerramento"] = False
    else:
        parametros["statusencerramento"] = True
    parametros = {
        "statusencerramento": parametros["statusencerramento"],
    }
    with open("exit.json", "w") as outfile:
        json.dump(parametros, outfile)

def verificarEncerramento():
    while True:
        try:
            os.chdir(diretorio_robo)
            with open("exit.json", "r") as infile:
                parametros = json.load(infile)
            if parametros["statusencerramento"]:
                print("Encerrando robô...")
                retornarEncerramentoFalse()
                time.sleep(2)
                exit()
            else:
                break
        except:
            time.sleep(2)
            print('verificar')
            pass

def carregarParametros():
    with open(f"{diretorio_robo}\\parametros.json", "r") as infile:
        parametros = json.load(infile)
    return parametros

def gerarLinkTMS():
    data_15 = time.strftime('%Y-%m-%d',time.gmtime(time.time()-(60*60*15)))
    h_15 = time.strftime('%H',time.gmtime(time.time()-(60*60*15)))
    data_hoje = time.strftime('%Y-%m-%d',time.gmtime(time.time()))
    hora_hoje = time.strftime('%H',time.gmtime(time.time()))
    minuto, segundo = time.strftime('%M',time.gmtime(time.time())),time.strftime('%S',time.gmtime(time.time()))
    IncludedAtDateStart = data_15 + 'T' + h_15 + '%3A' + minuto + '%3A' + segundo + 'Z'
    IncludedAtDateEnd = data_hoje + 'T' + hora_hoje + '%3A' + minuto + '%3A' + segundo + 'Z'
    getLink = 'https://tms.mercadolivre.com.br/packages/list?inboundIncludedAtDateStart=' + IncludedAtDateStart + '&inboundIncludedAtDateEnd=' + IncludedAtDateEnd + '&columnSort=shipment_id&orderSort=asc&page=1&limit=10'
    return getLink

def apagarCSVs():
    os.chdir(r'C:\\Users\\'+ user_name +'\\Downloads')
    try:
        nomesDosArquivos = [nomesDosArquivos for nomesDosArquivos in os.listdir() if ('.csv' in nomesDosArquivos) and ('.part' not in nomesDosArquivos)]
        print('Pasta de download limpa.')
        for arquivo in nomesDosArquivos:
            os.remove(arquivo)
        os.chdir(diretorio_robo)
    except IndexError:
        pass
    except Exception as e:
        logging.debug('Erro na funcao apagarCSVs - ' + str(e))
def atualizarBase(SAMPLE_RANGE_NAME,PROCESS_NAME):
    start_try = time.time() 
    while True:
        try:
            time.sleep(int(carregarParametros()["delayprecarregamento"]))
            time.sleep(contador.delay)
            contador.contador_func(funcao_principal)
            os.chdir(r'C:\\Users\\'+ user_name +'\\Downloads')
            nomeDoArquivo = [nomeDoArquivo for nomeDoArquivo in os.listdir() if '.csv' in nomeDoArquivo][0]
            if 'Journey' in nomeDoArquivo and PROCESS_NAME=='TMS':
                apagarCSVs()
                break
            tmsOrYMSFile = pd.read_csv(nomeDoArquivo, low_memory=False)
            tmsOrYMSFile = tmsOrYMSFile.fillna('')
            tmsOrYMSFile = tmsOrYMSFile[tmsOrYMSFile.columns].values.tolist()
            os.remove(nomeDoArquivo)
            os.chdir(diretorio_robo)
            limpar_celulas(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME)
            update_values(value_input_option = 'USER_ENTERED', spreadsheet_id=SAMPLE_SPREADSHEET_ID, range_name = SAMPLE_RANGE_NAME,  _values = tmsOrYMSFile)
            end_try = time.time()
            logging.debug('Execution time of atualizarBase: ' + str(end_try - start_try))
            contador.zerar_contagem()
            del tmsOrYMSFile

            break
        except Exception as e:
            logging.debug('Erro na função atualizarBase - ' + str(e))
            print('Não foi possível atualizar a base')

def atualizarBase2(SAMPLE_RANGE_NAME,PROCESS_NAME):
    start_try = time.time() 
    while True:
        try:
            for i in range(int(carregarParametros()["delayprecarregamento"])):
                time.sleep(1)
                try:
                    os.chdir(r'C:\\Users\\'+ user_name +'\\Downloads')

                    nomeDoArquivo = [nomeDoArquivo for nomeDoArquivo in os.listdir() if '.csv' in nomeDoArquivo and ('.part' not in nomeDoArquivo)][0]
                    break
                except:
                    if debug_mode: print(traceback.format_exc())

                    pass
            # time.sleep(int(carregarParametros()["delayprecarregamento"]))
            # time.sleep(contador.delay)
            contador.contador_func(funcao_principal)
            os.chdir(r'C:\\Users\\'+ user_name +'\\Downloads')
            if 'Journey' in nomeDoArquivo and PROCESS_NAME=='TMS':
                apagarCSVs()
                break
            try:
                tmsOrYMSFile = pd.read_csv(nomeDoArquivo, delimiter=',',encoding='utf8',engine='python',on_bad_lines='skip')
            except:
                if debug_mode: print(traceback.format_exc())

                tmsOrYMSFile = pd.read_csv(nomeDoArquivo,on_bad_lines='skip')
            colunas_indisponiveis = ['Inbound ID', 'Dispatch ID', 'Date Created', 'NFE', 'Reject Reason',
       'Inbound Date Opened', 'Inbound Date Closed', 'Inbound Carrier Name',
       'Inbound Dock ID', 'Labeling Date Printed',
       'Labeling Authorization Date', 'Labeling Last Print User',
       'Labeling Workstation ID', 'Weight', 'Labeling Carrier Name',
       'Labeling Service Id', 'Labeling Service Name', 'Tracking Number',
       'Outbound Date Opened', 'Outbound Date Closed', 'Outbound User IDs',
       'Dispatch Included Date', 'Dispatch Truck ID', 'Dispatch User ID',
       'Dispatch Dock ID', 'Priority', 'Process Type', 'Seller ID', 'Buyer ID',
       'Divergence', 'LastMile', 'LastMile Reimpressão', 'InBuffer',
       'InBuffer Name', 'InBuffer Promise EDT', 'InBuffer Promise Shipping',
       'Arrived LastMile', 'Arrived Npym', 'Was Reauthorized', 'Cutoff',
       'Start Priorization', 'End Priorization', 'Arrival Logistic Type',
       'Arrival Tracking Number']
            
            for i in tmsOrYMSFile.columns:
                if i in colunas_indisponiveis:
                    tmsOrYMSFile[i] = ''
            tmsOrYMSFile = tmsOrYMSFile.fillna('')
            tmsOrYMSFile = tmsOrYMSFile[tmsOrYMSFile.columns].values.tolist()
            os.remove(nomeDoArquivo)
            os.chdir(diretorio_robo)
            if len(tmsOrYMSFile) > 50000:
                limpar_celulas(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME)
                if (len(tmsOrYMSFile) >=50000) and (len(tmsOrYMSFile)<75000):
                    numero_de_fracoes = 2
                elif (len(tmsOrYMSFile) >=75000) and (len(tmsOrYMSFile)<100000):
                    numero_de_fracoes = 3
                elif (len(tmsOrYMSFile) >=100000):
                    numero_de_fracoes = 4
                dfs = np.array_split(tmsOrYMSFile,numero_de_fracoes)
                for df in dfs:
                    last_row = str(int(ultima_linha(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME))+1)
                    SAMPLE_RANGE_NAME_ALTERNATIVE = f'TMS!A{last_row}'
                    df = pd.DataFrame(df)
                    df = df.fillna('')
                    df = df[df.columns].values.tolist()
                    update_values(value_input_option = 'USER_ENTERED', spreadsheet_id=SAMPLE_SPREADSHEET_ID, range_name = SAMPLE_RANGE_NAME_ALTERNATIVE,  _values = df)
                end_try = time.time()
                logging.debug('Execution time of atualizarBase: ' + str(end_try - start_try))
                contador.zerar_contagem()
                del tmsOrYMSFile
                break
            else:        
                limpar_celulas(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME)
                update_values(value_input_option = 'USER_ENTERED', spreadsheet_id=SAMPLE_SPREADSHEET_ID, range_name = SAMPLE_RANGE_NAME,  _values = tmsOrYMSFile)
                end_try = time.time()
                logging.debug('Execution time of atualizarBase: ' + str(end_try - start_try))
                contador.zerar_contagem()
                del tmsOrYMSFile
                break
        except Exception as e:
            if debug_mode: print(traceback.format_exc())
            
            time.sleep(1)
            logging.debug('Erro na função atualizarBase - ' + str(traceback.format_exc()))
            print('Não foi possível atualizar a base')


def funcao_principal():
    apagarCSVs()
    logging.debug('Robô iniciado')
    while True:
        try:
            verificarPausa()
            # verificarEncerramento()
            driver.get(gerarLinkTMS())
            time.sleep(int(carregarParametros()["delayclicweb"]))
            driver.find_element(By.XPATH,'/html/body/main/div/div/div[2]/div/div/div/div/div[3]/div/div[2]/ul[2]/li[2]/a').click()
            atualizarBase2(SAMPLE_RANGE_NAME_TMS,'TMS')
            driver2.get(carregarParametros()["linkdolooker"])
            driver2.refresh()
            time.sleep(int(carregarParametros()["delayclicweb"]))
            driver2.find_element(By.ID,'dashboard-layout-wrapper').click()
            time.sleep(int(carregarParametros()["delayclicweb"]))
            driver2.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div/section/div/div[2]/div[1]/div/div[2]/div/section/div/div[1]/div/button[1]/div[2]').click()
            time.sleep(int(carregarParametros()["delayclicweb"]))
            driver2.find_element(By.XPATH,'/html/body/div[3]/div/div/div/div/div/ul/li[2]/button').click()
            time.sleep(int(carregarParametros()["delayclicweb"]))
            driver2.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/footer/div[1]/button[1]').click()
            atualizarBase2(SAMPLE_RANGE_NAME_YMS,'YMS')
            print('Pausa para acompanhamento. (',carregarParametros()["delayacompanhamento"],'min)')
            time.sleep(60*int(carregarParametros()["delayacompanhamento"]))
        except Exception as e:
            logging.debug('Erro na função funcao_principal - ' + str(e))
            print('Não foi possível completar processo de download.')
            if debug_mode: print(traceback.format_exc())
            pass

# parametros = carregarParametros()

user_name = os.getlogin()
diretorio_robo = os.getcwd()
debug_mode = False
log_filename_start = os.getcwd() + '\\Logs\\' + time.strftime('%d_%m_%Y %H_%M_%S') + '.log'
logging.basicConfig(filename=log_filename_start, level=logging.DEBUG, format='%(asctime)s, %(message)s',datefmt='%m/%d/%Y %H:%M:%S')

contador = Counter()
controlerobo = ControlRobot()

# The ID and range of a sample spreadsheet.

SAMPLE_SPREADSHEET_ID = carregarParametros()["idplanilha"]
# SAMPLE_SPREADSHEET_ID = '1pn4STF7yzx14FjZ1kJaQ5swsc5xiRA56PAiXrpvAkaU'
SAMPLE_RANGE_NAME_TMS = 'TMS!A2:BG'
SAMPLE_RANGE_NAME_YMS = 'YMS!A2:BG'

options = Options()
options.set_preference('network.proxy.type',0)
options.binary_location = carregarParametros()["caminhonavegador"]
# options.binary_location = r'C:\\Users\\'+ user_name +'\\AppData\\Local\\Mozilla Firefox\\firefox.exe'

driver = webdriver.Firefox(options=options)
driver.get('https://tms.mercadolivre.com.br/')
driver2 = webdriver.Firefox(options=options)

driver2.get(carregarParametros()["linkdolooker"])
# driver2.get('https://meli.looker.com/dashboards/shipping::yms_journey_driver?Facility=%22BRXRJ1%2CSRJ1%22%2CXRJ1%2C%22XRJ1%2CSRJ1%22%2CXDRJ1%2CSRJ1&Arrival+Facility=SRJ1%2CXRJ1%2C%22XRJ1%2CSRJ1%22&Mile=%22first_mile%22&Licence+Plate=&Operation=&Date=today&Shipment+Type=')
os.system('pause')
time.sleep(3)
funcao_principal()
