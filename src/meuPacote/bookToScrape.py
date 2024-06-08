from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
import pandas as pd
import re

def getPrice(nome):
    """
    Funcao para pegar o preco no site https://books.toscrape.com/

    Essa função pega no nome do livro e retorna o seu preço atual

    Parameters:
    nome (str): Nome do livro a ser consultado.

    Returns:
    int or float: Preço atual do livro.
    """
    driver = webdriver.Chrome(options=chrome_options)
    site = 'https://books.toscrape.com/catalogue/category/books/classics_6/index.html'
    driver.get(site)
    sleep(5)
    try:
        xpath = '//*[@id="default"]/div/div/div/div/section/div[2]/ol'
        elements = driver.find_elements(By.XPATH, xpath)
        for elem in elements:
            texto = re.split('\n', elem.text)
            indices = [i for i, item in enumerate(texto) if re.search('^£', item)]
            titulos = []
            precos = []
            for i in indices:
                titulo = texto[i-1]
                preco = texto[i]
                titulos += [titulo]
                precos += [preco]
            df = pd.DataFrame({'titulo':titulos, 'preco':precos}) 
            preco = df.loc[df.titulo.str.contains(nome, regex=True, case=False), ['preco']].values[0][0][1:]
            preco = float(preco)
        driver.close()
        return preco
    except Exception as e:
        print(f'Erro: {e}')