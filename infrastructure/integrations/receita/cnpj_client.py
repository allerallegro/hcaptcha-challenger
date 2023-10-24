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
from models.cnpj import Cnpj, from_html

# Init local-side of the ModelHub
solver.install(upgrade=True)

# Save dataset to current working directory
tmp_dir = Path(__file__).parent.joinpath("tmp_dir")
user_data_dir = Path(__file__).parent.joinpath("user_data_dir")
context_dir = user_data_dir.joinpath("context")
record_dir = user_data_dir.joinpath("record")
record_har_path = record_dir.joinpath(f"eg-{int(time.time())}.har")

sitekey = SiteKey.user_easy

CNPJ_NAO_ENCONTRADO = "Não existe no Cadastro de Pessoas Jurdicas o número de CNPJ informado. Verifique se o mesmo foi digitado corretamente."





class CNPJClient:
    def __init__(self):
        pass

    async def consultar_cnpj(
        self,
        cnpj: str,
        proxy: Optional[str] = None,
        proxy_username: Optional[str] = None,
        proxy_password: Optional[str] = None,
        headless: bool = True,
    ) -> Optional[Cnpj]:
            malenia = Malenia(
                user_data_dir=context_dir, record_dir=record_dir, record_har_path=record_har_path
            )
            result = await malenia.execute(sequence=[self.hit_challenge],parameters={
            "cnpj": cnpj
            }, headless=False)
            if isinstance(result[0], Exception):
                raise result[0]
            return result[0]
    
    @logger.catch
    async def hit_challenge(self,context: ASyncContext, times: int = 8, cnpj=''):
        page = context.pages[0]
        agent = AgentT.from_page(page=page, tmp_dir=tmp_dir)
        await page.goto(f'https://solucoes.receita.fazenda.gov.br/servicos/cnpjreva/cnpjreva_solicitacao.asp?cnpj={cnpj}',timeout=60000)

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

        await page.wait_for_selector('button[type="submit"]')

        # Aguarda 5 segundos
        await asyncio.sleep(2)

        await page.click('button[type="submit"]',timeout=60000)

        await page.wait_for_function(
            """() => {
                const h2Elements  = Array.from(document.querySelectorAll("h2"));
                const pElements  = Array.from(document.querySelectorAll("p"));  
                return h2Elements.some(h2 => h2.textContent.includes("Comprovante de Inscrição e de Situação Cadastral")) ||
                pElements.some(p => p.textContent.includes("O número do CNPJ não é válido") || 
                p.textContent.includes("Não existe no Cadastro de Pessoas Jurídicas o número de CNPJ informado.")) ;
            }""",
            
        )

        html1 = await page.content()
        html2 = ""
        
        if CNPJ_NAO_ENCONTRADO in html1 or 'O número do CNPJ não é válido' in html1:
            raise NaoEncontradoException(CNPJ_NAO_ENCONTRADO)

        try:
            
            tem_qsa = False
            try:
                await page.wait_for_selector("button[name=qsa]", timeout=3000)
                tem_qsa =  True
            except:
                pass

            if tem_qsa:
                await page.click("button[name=qsa]")

                await page.wait_for_function(
                    """() => {
                const h2Elements = Array.from(document.querySelectorAll("h2"));
                return h2Elements.some(h2 => h2.textContent.includes("Consulta Quadro de Sócios"));
                        }""",
                    
                )
                html2 = await page.evaluate('(element) => element.innerHTML', await page.query_selector('.conteudo'))

        except Exception as e:
            await page.screenshot({"path": "screenshot.png"})
            print(e)

        result = from_html(html1, html2)

        return result


    def format_date(self, date: date) -> str:
        return date.strftime("%d/%m/%Y")
