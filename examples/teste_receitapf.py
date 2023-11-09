# -*- coding: utf-8 -*-
# Time       : 2023/8/20 23:12
# Author     : QIN2DIM
# GitHub     : https://github.com/QIN2DIM
# Description:
from __future__ import annotations

import asyncio
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

from loguru import logger
from playwright.async_api import BrowserContext as ASyncContext

import hcaptcha_challenger as solver
from hcaptcha_challenger.agents import AgentT, Malenia
from hcaptcha_challenger.utils import SiteKey
from utils.html_extractor import from_html

# Init local-side of the ModelHub
solver.install(upgrade=True, flush_yolo=[solver.DEFAULT_KEYPOINT_MODEL])

# Save dataset to current working directory
tmp_dir = Path(__file__).parent.joinpath("tmp_dir")
user_data_dir = Path(__file__).parent.joinpath("user_data_dir")
context_dir = user_data_dir.joinpath("context")
record_dir = user_data_dir.joinpath("record")
record_har_path = record_dir.joinpath(f"eg-{int(time.time())}.har")

sitekey = SiteKey.user_easy


@logger.catch
async def hit_challenge(context: ASyncContext, times: int = 8, cpf='', nascimento=''):
    page = context.pages[0]
    agent = AgentT.from_page(page=page, tmp_dir=tmp_dir)
    await page.goto(f'https://servicos.receita.fazenda.gov.br/Servicos/CPF/ConsultaSituacao/ConsultaPublica.asp?cpf={cpf}&nascimento={nascimento}')

    await agent.handle_checkbox()

    for pth in range(1, times):
        result = await agent()
        print(f">> {pth} - Challenge Result: {result}")
        match result:
            case agent.status.CHALLENGE_BACKCALL:
                await page.wait_for_timeout(500)
                fl = page.frame_locator(agent.HOOK_CHALLENGE)
                await fl.locator("//div[@class='refresh button']").click()
            case agent.status.CHALLENGE_SUCCESS:
                rqdata_path = agent.export_rq()
                print(f"View RQdata path={rqdata_path}")
                break
    
    await page.bring_to_front()

    await page.wait_for_selector('#id_submit')

    # Aguarda 5 segundos
    await asyncio.sleep(2)

    await page.click('#id_submit')

    await page.wait_for_function(
        """() => {
            const spanElements  = Array.from(document.querySelectorAll("span"));
            return spanElements.some(span => span.textContent.includes("Comprovante de Situação Cadastral no CPF"));
        }""",
        
    )

    html1 = await page.content()
    
    result = from_html(html1)
    
    return result




async def bytedance():
    malenia = Malenia(
        user_data_dir=context_dir, record_dir=record_dir, record_har_path=record_har_path
    )

    
    
    # Abra o arquivo lista.txt para leitura
    with open('examples/lista.txt', 'r') as arquivo:
        # Leia as linhas do arquivo
        linhas = arquivo.readlines()

    # Crie uma lista para armazenar os dados lidos
    dados = []

    # Itere pelas linhas do arquivo
    for linha in linhas:
        # Divida a linha em colunas usando o caractere de separação (por exemplo, tabulação '\t' ou vírgula ',')
        colunas = linha.strip().split('\t')  # Use '\t' se as colunas estiverem separadas por tabulação

        # Verifique se há pelo menos duas colunas (CPF e data de nascimento)
        if len(colunas) >= 2:
            cpf = colunas[0]  # A primeira coluna é o CPF
            data_nascimento = colunas[1]  # A segunda coluna é a data de nascimento
            # Formate a data de nascimento
            data_nascimento_formatada = formatar_data(data_nascimento)

            # Aplique o URL encoding à data de nascimento formatada
            data_nascimento_encoded = urllib.parse.quote(data_nascimento_formatada)

            dados.append((cpf, data_nascimento_encoded))


    # Agora, a lista 'dados' contém pares de CPF e data de nascimento
    # Você pode iterar sobre 'dados' para processar esses valores conforme necessário
    for cpf, data_nascimento in dados:
        print(f"CPF: {cpf}, Data de Nascimento: {data_nascimento}")
        result = await malenia.execute(sequence=[hit_challenge],parameters={
            "cpf": cpf, "nascimento": data_nascimento
            }, headless=False)
        print(result)

# Função para formatar a data de nascimento no formato "dd/MM/yyyy"
def formatar_data(data_nascimento):
    # Converter a data de nascimento para um objeto datetime
    data_obj = datetime.strptime(data_nascimento, '%Y-%m-%d')
    # Formatar a data no novo formato
    return data_obj.strftime('%d/%m/%Y')

if __name__ == "__main__":
    asyncio.run(bytedance())
