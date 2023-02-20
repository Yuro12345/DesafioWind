from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time as t
from selenium.webdriver.common.by import By
import shutil
from zipfile import ZipFile as zip
import os as o
import pandas as pd


def download():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    nav = webdriver.Chrome(executable_path="C:\Program Files (x86)\chromedriver.exe", options=chrome_options)

    nav.get("http://dados.tce.rs.gov.br/organization/tribunal-de-contas-do-estado-do-rio-grande-do-sul")
    t.sleep(0.5)
    nav.find_element(By.XPATH, '//*[@id="content"]/div[3]/div/article/div/ul/li[2]/div/h3/a').click()
    t.sleep(1)
    nav.find_element(By.XPATH, '//*[@id="dataset-resources"]/ul/li/div/button').click()
    t.sleep(0.5)
    nav.find_element(By.XPATH, '//*[@id="dataset-resources"]/ul/li/div/ul/li[2]/a').click()
    t.sleep(10)
    nav.quit()


def move():
    oldAdress = 'C:/Users/yurim/Downloads/2023.csv.zip' #alterar para sua pasta de Downloads
    newAdress = 'C:/DesafioWind/Files/' #alterar para pasta onde você salvou
    shutil.move(oldAdress, newAdress)


def moveCsv():
    shutil.move('item.csv', 'C:/DesafioWind/Files/') #alterar para pasta onde você salvou
    shutil.move('licitacao.csv', 'C:/DesafioWind/Files/') #alterar para pasta onde você salvou


def extract():
    caminho = zip('Files/2023.csv.zip', 'r')

    caminho.extract("item.csv")
    caminho.extract("licitacao.csv")


def filtros():
    dfItem = pd.read_csv('Files/item.csv')
    dfLicitacao = pd.read_csv('Files/licitacao.csv')

    dfMaskLicitacao = dfLicitacao['DT_ABERTURA'] > '01/05/2022'
    filteredDf = dfLicitacao[dfMaskLicitacao]

    count = 0

    for index, row in filteredDf.iterrows():
        dfMaskItem = dfItem["CD_ORGAO"] == row["CD_ORGAO"]
        filteredDfItem = dfItem[dfMaskItem]
        dfMaskItem = dfItem["CD_TIPO_MODALIDADE"] == row["CD_TIPO_MODALIDADE"]
        filteredDfItem = filteredDfItem[dfMaskItem]
        dfMaskItem = dfItem["NR_LICITACAO"] == row["NR_LICITACAO"]
        filteredDfItem = filteredDfItem[dfMaskItem]
        dfMaskItem = dfItem["ANO_LICITACAO"] == row["ANO_LICITACAO"]
        filteredDfItem = filteredDfItem[dfMaskItem]
        o.mkdir(
            f'./licitacoes/{row["CD_ORGAO"]} - {row["CD_TIPO_MODALIDADE"]} - {row["NR_LICITACAO"]} - {row["ANO_LICITACAO"]}')
        open(
            f'./licitacoes/{row["CD_ORGAO"]} - {row["CD_TIPO_MODALIDADE"]} - {row["NR_LICITACAO"]} - {row["ANO_LICITACAO"]}/link.txt',
            "x")
        link = open(
            f'./licitacoes/{row["CD_ORGAO"]} - {row["CD_TIPO_MODALIDADE"]} - {row["NR_LICITACAO"]} - {row["ANO_LICITACAO"]}/link.txt',
            "a")
        link.write(f'{row["LINK_LICITACON_CIDADAO"]}')
        link.close()
        open(
            f'./licitacoes/{row["CD_ORGAO"]} - {row["CD_TIPO_MODALIDADE"]} - {row["NR_LICITACAO"]} - {row["ANO_LICITACAO"]}/itens-licitacao.csv',
            "x")
        item = open(
            f'./licitacoes/{row["CD_ORGAO"]} - {row["CD_TIPO_MODALIDADE"]} - {row["NR_LICITACAO"]} - {row["ANO_LICITACAO"]}/itens-licitacao.csv',
            "a")
        item.write(f'{filteredDfItem["DS_ITEM"]}')
        item.close()

        count += 1
        if count == 30:
            break


def limpeza():
    o.remove('C:/DesafioWind/Files/2023.csv.zip')
    o.remove('C:/DesafioWind/Files/item.csv')
    o.remove('C:/DesafioWind/Files/licitacao.csv')


download()

move()

t.sleep(2)
extract()

t.sleep(2)
moveCsv()

t.sleep(2)
filtros()

t.sleep(2)
limpeza()
