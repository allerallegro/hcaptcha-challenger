from datetime import date
from typing import Optional

from exception.data_nascimento_exception import \
    DataNascimentoDivergenteException
from exception.nao_encontrado_exception import NaoEncontradoException
from infrastructure.database.db import Database
from infrastructure.integrations.receita.cnpj_client import CNPJClient
from infrastructure.repositories.cnpj_repository import CNPJRepository
from models.cnpj import Cnpj


class CNPJService:
    def __init__(self, db: Database):
        self.cnpj_repository = CNPJRepository(db)

    async def consultar_cnpj(
        self,
        cnpj: str,
        proxy: Optional[str] = None,
        proxy_username: Optional[str] = None,
        proxy_password: Optional[str] = None,
        headless: bool = True,
    ) -> (Optional[Cnpj], bool):
        ultima_consulta = self.cnpj_repository.get_ultima_consulta(cnpj)

        if ultima_consulta != None:
            return (ultima_consulta, True,200)

        client = CNPJClient()

        try:
            result = await client.consultar_cnpj(
                cnpj=cnpj,
                proxy=proxy,
                proxy_username=proxy_username,
                proxy_password=proxy_password,
                headless=headless,
            )
            if result is not None:
                self.salvar(cpf=cnpj, data=result)
        except NaoEncontradoException as e:
            r = Cnpj(erro=str(e), cpf=cnpj)
            self.salvar(cpf=cnpj, data=r)
            return (r,False,404)


        return (result, False,200)
        

    def format_date(self, date: date) -> str:
        return date.strftime("%d/%m/%Y")

    def salvar(self, cpf: str, data: any) -> None:
        self.cnpj_repository.salvar(cpf, data)
