import re
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List, Union

from pyquery import PyQuery as pq

from models.socio import Socio


@dataclass
class Cnpj:
    def __init__(self):
        self.cnpj: str = ""
        self.tipo: str = ""
        self.data_abertura: Union[None, datetime] = None
        self.razao_social: str = ""
        self.nome_fantasia: str = ""
        self.porte: str = ""
        self.cnae: str = ""
        self.cnaes_secundarias: List[str] = []
        self.natureza_juridica: str = ""
        self.logradouro: str = ""
        self.numero: str = ""
        self.complemento: str = ""
        self.cep: str = ""
        self.bairro: str = ""
        self.cidade: str = ""
        self.uf: str = ""
        self.email: str = ""
        self.telefone: str = ""
        self.efr: str = ""
        self.situacao_cadastral: str = ""
        self.data_situacao_cadastral: Union[None, datetime] = None
        self.motivo_situacao_cadastral: str = ""
        self.situacao_especial: str = ""
        self.data_situacao_especial: Union[None, datetime] = None
        self.socios: List[Socio] = []
        self.capital_social: str = ""
        self.erro: str = ""
        self.status_code: int = 0
        self.data_consulta: datetime = datetime.now()

    def to_dict(self) -> dict:
        def format_datetime(date):
            return date.strftime("%d/%m/%Y") if date else None
            # Crie um dicionário com atributos formatados

        return {
            "cnpj": self.cnpj,
            "tipo": self.tipo,
            "dataAbertura": format_datetime(self.data_abertura),
            "razaoSocial": self.razao_social,
            "nomeFantasia": self.nome_fantasia,
            "porte": self.porte,
            "cnae": self.cnae,
            "cnaesSecundarias": self.cnaes_secundarias,
            "naturezaJuridica": self.natureza_juridica,
            "logradouro": self.logradouro,
            "numero": self.numero,
            "complemento": self.complemento,
            "cep": self.cep,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "uf": self.uf,
            "email": self.email,
            "telefone": self.telefone,
            "efr": self.efr,
            "situacaoCadastral": self.situacao_cadastral,
            "dataSituacaoCadastral": format_datetime(self.data_situacao_cadastral),
            "motivoSituacaoCadastral": self.motivo_situacao_cadastral,
            "situacaoEspecial": self.situacao_especial,
            "dataSituacaoEspecial": format_datetime(self.data_situacao_especial),
            "socios": [socio.to_dict() for socio in self.socios],
            "capitalSocial": self.capital_social,
            "erro": self.erro,
            "statusCode": self.status_code,
            "dataConsulta": format_datetime(self.data_consulta),
        }

    def get_cnpj(self) -> str:
        return self.cnpj

    def get_tipo(self) -> str:
        return self.tipo

    def get_data_abertura(self) -> Union[None, datetime]:
        return self.data_abertura

    def get_razao_social(self) -> str:
        return self.razao_social

    def get_nome_fantasia(self) -> str:
        return self.nome_fantasia

    def get_porte(self) -> str:
        return self.porte

    def get_cnae(self) -> str:
        return self.cnae

    def get_cnaes_secundarias(self) -> List[str]:
        return self.cnaes_secundarias

    def get_natureza_juridica(self) -> str:
        return self.natureza_juridica

    def get_logradouro(self) -> str:
        return self.logradouro

    def get_numero(self) -> str:
        return self.numero

    def get_complemento(self) -> str:
        return self.complemento

    def get_cep(self) -> str:
        return self.cep

    def get_bairro(self) -> str:
        return self.bairro

    def get_cidade(self) -> str:
        return self.cidade

    def get_uf(self) -> str:
        return self.uf

    def get_email(self) -> str:
        return self.email

    def get_telefone(self) -> str:
        return self.telefone

    def get_efr(self) -> str:
        return self.efr

    def get_situacao_cadastral(self) -> str:
        return self.situacao_cadastral

    def get_data_situacao_cadastral(self) -> Union[None, datetime]:
        return self.data_situacao_cadastral

    def get_motivo_situacao_cadastral(self) -> str:
        return self.motivo_situacao_cadastral

    def get_situacao_especial(self) -> str:
        return self.situacao_especial

    def get_data_situacao_especial(self) -> Union[None, datetime]:
        return self.data_situacao_especial

    def get_socios(self) -> List[Socio]:
        return self.socios

    def get_capital_social(self) -> str:
        return self.capital_social

    def get_erro(self) -> str:
        return self.erro

    def get_data_consulta(self) -> datetime:
        return self.data_consulta

    def get_status_code(self) -> int:
        return self.status_code

    def set_cnpj(self, cnpj: str) -> None:
        self.cnpj = cnpj

    def set_tipo(self, tipo: str) -> None:
        self.tipo = tipo

    def set_data_abertura(self, data_abertura: Union[None, datetime]) -> None:
        self.data_abertura = data_abertura

    def set_razao_social(self, razao_social: str) -> None:
        self.razao_social = razao_social

    def set_nome_fantasia(self, nome_fantasia: str) -> None:
        self.nome_fantasia = nome_fantasia

    def set_porte(self, porte: str) -> None:
        self.porte = porte

    def set_cnae(self, cnae: str) -> None:
        self.cnae = cnae

    def set_cnaes_secundarias(self, cnaes_secundarias: List[str]) -> None:
        self.cnaes_secundarias = cnaes_secundarias

    def set_natureza_juridica(self, natureza_juridica: str) -> None:
        self.natureza_juridica = natureza_juridica

    def set_logradouro(self, logradouro: str) -> None:
        self.logradouro = logradouro

    def set_numero(self, numero: str) -> None:
        self.numero = numero

    def set_complemento(self, complemento: str) -> None:
        self.complemento = complemento

    def set_cep(self, cep: str) -> None:
        self.cep = cep

    def set_bairro(self, bairro: str) -> None:
        self.bairro = bairro

    def set_cidade(self, cidade: str) -> None:
        self.cidade = cidade

    def set_uf(self, uf: str) -> None:
        self.uf = uf

    def set_email(self, email: str) -> None:
        self.email = email

    def set_telefone(self, telefone: str) -> None:
        self.telefone = telefone

    def set_efr(self, efr: str) -> None:
        self.efr = efr

    def set_situacao_cadastral(self, situacao_cadastral: str) -> None:
        self.situacao_cadastral = situacao_cadastral

    def set_data_situacao_cadastral(
        self, data_situacao_cadastral: Union[None, datetime]
    ) -> None:
        self.data_situacao_cadastral = data_situacao_cadastral

    def set_motivo_situacao_cadastral(self, motivo_situacao_cadastral: str) -> None:
        self.motivo_situacao_cadastral = motivo_situacao_cadastral

    def set_situacao_especial(self, situacao_especial: str) -> None:
        self.situacao_especial = situacao_especial

    def set_data_situacao_especial(
        self, data_situacao_especial: Union[None, datetime]
    ) -> None:
        self.data_situacao_especial = data_situacao_especial

    def set_socios(self, socios: List[Socio]) -> None:
        self.socios = socios

    def set_capital_social(self, capital_social: str) -> None:
        self.capital_social = capital_social

    def set_erro(self, erro: str) -> None:
        self.erro = erro

    def set_data_consulta(self, data_consulta: datetime) -> None:
        self.data_consulta = data_consulta

    def set_status_code(self, status_code: int) -> None:
        self.status_code = status_code

    def asdict(self):
        return asdict(self)


def remover_espacos_em_branco(input_string: str) -> str:
    return re.sub(r"[\t\n]", "", input_string)


def to_date(data_string: str) -> Union[datetime, None]:
    try:
        if re.findall(r"^\d{1,2}/\d{1,2}/\d{4}$", data_string):
            dia, mes, ano = map(int, data_string.split("/"))
            data = datetime(ano, mes, dia)
            return data
        else:
            return None
    except ValueError:
        return None


def from_html(html1: str, html2: str) -> Cnpj:
    cnpj = Cnpj()
    doc1 = pq(html1)

    cnpj.set_cnpj(
        re.sub(
            r"\D",
            "",
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(3) > tbody > tr > td:nth-child(1) > font:nth-child(3) > b:nth-child(1)"
            ).text(),
        )
    )
    cnpj.set_tipo(
        remover_espacos_em_branco(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(3) > tbody > tr > td:nth-child(1) > font:nth-child(3) > b:nth-child(3)"
            )
            .text()
            .strip()
        )
    )
    cnpj.set_data_abertura(
        to_date(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(3) > tbody > tr > td:nth-child(3) > font:nth-child(3) > b"
            )
            .text()
            .strip()
        )
    )
    cnpj.set_razao_social(
        remover_espacos_em_branco(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(5) > tbody > tr > td > font:nth-child(3) > b"
            )
            .text()
            .strip()
        )
    )
    cnpj.set_nome_fantasia(
        remover_espacos_em_branco(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(7) > tbody > tr > td:nth-child(1) > font:nth-child(3) > b"
            )
            .text()
            .strip()
        )
    )
    cnpj.set_porte(
        remover_espacos_em_branco(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(7) > tbody > tr > td:nth-child(3) > font:nth-child(3) > b"
            )
            .text()
            .strip()
        )
    )
    cnpj.set_cnae(
        remover_espacos_em_branco(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(9) > tbody > tr > td > font:nth-child(3) > b"
            )
            .text()
            .strip()
        )
    )

    for el in doc1(
        "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(11) > tbody > tr > td > font:nth-child(3) > b"
    ):
        cnpj.get_cnaes_secundarias().append(remover_espacos_em_branco(el.text.strip()))

    cnpj.set_natureza_juridica(
        remover_espacos_em_branco(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(13) > tbody > tr > td > font:nth-child(3) > b"
            )
            .text()
            .strip()
        )
    )
    cnpj.set_logradouro(
        remover_espacos_em_branco(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(15) > tbody > tr > td:nth-child(1) > font:nth-child(3) > b"
            )
            .text()
            .strip()
        )
    )
    cnpj.set_numero(
        remover_espacos_em_branco(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(15) > tbody > tr > td:nth-child(3) > font:nth-child(3) > b"
            ).text()
        )
    )
    cnpj.set_complemento(
        remover_espacos_em_branco(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(15) > tbody > tr > td:nth-child(5) > font:nth-child(3) > b"
            )
            .text()
            .strip()
        )
    )
    cnpj.set_cep(
        re.sub(
            r"\D",
            "",
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(17) > tbody > tr > td:nth-child(1) > font:nth-child(3) > b"
            )
            .text()
            .strip(),
        )
    )
    cnpj.set_bairro(
        remover_espacos_em_branco(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(17) > tbody > tr > td:nth-child(3) > font:nth-child(3) > b"
            )
            .text()
            .strip()
        )
    )
    cnpj.set_cidade(
        remover_espacos_em_branco(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(17) > tbody > tr > td:nth-child(5) > font:nth-child(3) > b"
            )
            .text()
            .strip()
        )
    )
    cnpj.set_uf(
        remover_espacos_em_branco(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(17) > tbody > tr > td:nth-child(7) > font:nth-child(3) > b"
            )
            .text()
            .strip()
        )
    )
    cnpj.set_email(
        remover_espacos_em_branco(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(17) > tbody > tr > td:nth-child(7) > font:nth-child(3) > b"
            )
            .text()
            .strip()
        )
    )
    cnpj.set_telefone(
        remover_espacos_em_branco(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(19) > tbody > tr > td:nth-child(3) > font:nth-child(3) > b"
            )
            .text()
            .strip()
        )
    )
    cnpj.set_efr(
        remover_espacos_em_branco(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(21) > tbody > tr > td > font:nth-child(3) > b"
            )
            .text()
            .strip()
        )
    )
    cnpj.set_situacao_cadastral(
        remover_espacos_em_branco(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(23) > tbody > tr > td:nth-child(1) > font:nth-child(3) > b"
            )
            .text()
            .strip()
        )
    )
    cnpj.set_data_situacao_cadastral(
        to_date(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(23) > tbody > tr > td:nth-child(3) > font:nth-child(3) > b"
            )
            .text()
            .strip()
        )
    )
    cnpj.set_motivo_situacao_cadastral(
        remover_espacos_em_branco(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(25) > tbody > tr > td > font:nth-child(3) > b"
            )
            .text()
            .strip()
        )
    )
    cnpj.set_situacao_especial(
        remover_espacos_em_branco(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(27) > tbody > tr > td:nth-child(1) > font:nth-child(3) > b"
            )
            .text()
            .strip()
        )
    )
    cnpj.set_data_situacao_especial(
        to_date(
            doc1(
                "#principal > table:nth-child(1) > tbody > tr > td > table:nth-child(27) > tbody > tr > td:nth-child(3) > font:nth-child(3) > b"
            )
            .text()
            .strip()
        )
    )
    cnpj.set_data_consulta(datetime.now())

    if html2 != "":
        doc2 = pq(html2)
        cnpj.set_capital_social(
            remover_espacos_em_branco(
                doc2("#capital > div:nth-child(3) > div.col-md-9").text()
            )
        )

        for el in [pq(x) for x in doc2("#principal > div > div > div:nth-child(n+6)")]:
            socio = Socio()
            socio.set_nome(
                remover_espacos_em_branco(
                    el.find("div.col-md-12 > div.alert > div.row > div.col-md-9")
                    .eq(0)
                    .text()
                    .strip()
                )
            )
            socio.set_qualificacao(
                remover_espacos_em_branco(
                    el.find("div.col-md-12 > div.alert > div.row > div.col-md-5")
                    .eq(0)
                    .text()
                    .strip()
                )
            )
            socio.set_qualificacao_replegal(
                remover_espacos_em_branco(
                    el.find("td:eq(1) > table > tbody > tr:eq(0) > td:eq(1)")
                    .eq(0)
                    .text()
                    .strip()
                )
            )
            socio.set_nome_representante_legal(
                remover_espacos_em_branco(
                    el.find("td:eq(1) > table > tbody > tr:eq(1) > td:eq(1)")
                    .eq(0)
                    .text()
                    .strip()
                )
            )
            if socio.nome != "":
                cnpj.get_socios().append(socio)

    return cnpj
