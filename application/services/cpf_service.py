from datetime import date
from typing import Optional

from exception.data_nascimento_exception import \
    DataNascimentoDivergenteException
from exception.nao_encontrado_exception import NaoEncontradoException
from infrastructure.database.db import Database
from infrastructure.integrations.receita.cpf_client import CPFClient
from infrastructure.repositories.cpf_repository import CPFRepository
from models.comprovante_situacao_cadastral import ConsultaCpfModel


class CPFService:
    def __init__(self, db: Database):
        self.cpf_repository = CPFRepository(db)

    async def consultar_cpf(
        self,
        cpf: str,
        nascimento: str,
        proxy: Optional[str] = None,
        proxy_username: Optional[str] = None,
        proxy_password: Optional[str] = None,
        headless: bool = True,
    ) -> (Optional[ConsultaCpfModel], bool):
        ultima_consulta = self.cpf_repository.get_ultima_consulta(cpf,nascimento)

        if ultima_consulta != None:
            return (ultima_consulta, True,200)

        client = CPFClient()

        try:
            result = await client.consultar_cpf(
                cpf=cpf,
                data_nascimento=nascimento,
                proxy=proxy,
                proxy_username=proxy_username,
                proxy_password=proxy_password,
                headless=headless,
            )
            if result is not None:
                self.salvar(cpf=cpf, data=result)
        except NaoEncontradoException as e:
            r = ConsultaCpfModel(erro=str(e), cpf=cpf)
            self.salvar(cpf=cpf, data=r)
            return (r,False,404)
        except DataNascimentoDivergenteException as e:
            r = ConsultaCpfModel(erro=str(e),cpf=cpf)
            self.salvar(cpf=cpf, data=r)
            return (r,False,409)

        return (result, False,200)
        

    def format_date(self, date: date) -> str:
        return date.strftime("%d/%m/%Y")

    def salvar(self, cpf: str, data: any) -> None:
        self.cpf_repository.salvar(cpf, data)
