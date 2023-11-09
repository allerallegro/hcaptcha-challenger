from __future__ import annotations

import asyncio
import base64
import io
import random
import sys
import time
import urllib.parse
from datetime import date, datetime
from pathlib import Path
from typing import Optional

from loguru import logger
from playwright.async_api import BrowserContext as ASyncContext

import hcaptcha_challenger as solver
from exception.data_nascimento_exception import \
    DataNascimentoDivergenteException
from exception.nao_encontrado_exception import NaoEncontradoException
from hcaptcha_challenger.agents import AgentT, Malenia
from hcaptcha_challenger.utils import SiteKey
from models.comprovante_situacao_cadastral import ConsultaCpfModel
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

CNPJ_NAO_ENCONTRADO = "Não existe no Cadastro de Pessoas Jurdicas o número de CNPJ informado. Verifique se o mesmo foi digitado corretamente."





class CPFClient:
    def __init__(self):
        pass

    async def consultar_cpf(
        self,
        cpf: str,
        data_nascimento: str,
        proxy: Optional[str] = None,
        proxy_username: Optional[str] = None,
        proxy_password: Optional[str] = None,
        headless: bool = True,
    ) -> Optional[ConsultaCpfModel]:
            malenia = Malenia(
                user_data_dir=context_dir, record_dir=record_dir, record_har_path=record_har_path
            )
            result = await malenia.execute(sequence=[self.hit_challenge],parameters={
            "cpf": cpf, "nascimento": data_nascimento
            }, headless=headless)
            if isinstance(result[0], Exception):
                raise result[0]
            return result[0]
    
    @logger.catch
    async def hit_challenge(self,context: ASyncContext, times: int = 8, cpf='', nascimento=''):
        page = context.pages[0]
        agent = AgentT.from_page(page=page, tmp_dir=tmp_dir)
        data_nascimento_encoded = urllib.parse.quote(nascimento)
        await page.goto(f'https://servicos.receita.fazenda.gov.br/Servicos/CPF/ConsultaSituacao/ConsultaPublica.asp?cpf={cpf}&nascimento={data_nascimento_encoded}',timeout=60000)

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

        await page.click('#id_submit',timeout=60000)

        await page.wait_for_function(
            """() => {
                const spanElements  = Array.from(document.querySelectorAll("span"));
                const bElements  = Array.from(document.querySelectorAll("b"));  
                return spanElements.some(span => span.textContent.includes("Comprovante de Situação Cadastral no CPF")) ||
                bElements.some(b => b.textContent.includes("divergente da constante na base de dados") || 
                b.textContent.includes("encontrado na base de dados da Receita Federal") ||
                b.textContent.includes("CPF incorreto")) ;
            }""",
            
        )

        html1 = await page.content()
        
        if "divergente" in html1 :
            return DataNascimentoDivergenteException()
        elif "encontrado na base de dados da Receita Federal" in html1 or "CPF incorreto" in html1:
            return NaoEncontradoException()
        
        result = from_html(html1)
        
        return result

    def format_date(self, date: date) -> str:
        return date.strftime("%d/%m/%Y")
