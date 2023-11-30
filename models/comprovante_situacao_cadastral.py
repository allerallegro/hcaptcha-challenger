from datetime import datetime
import re

class ConsultaCpfModel:
    def __init__(self, cpf="", nome="", data_nascimento=None, situacao="", data_inscricao=None,
                 data_comprovante=None, codigo_comprovante="", erro="", nome_social="", obito=False, html=""):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.situacao = situacao
        self.data_inscricao = data_inscricao
        self.data_comprovante = data_comprovante
        self.codigo_comprovante = codigo_comprovante
        self.erro = erro
        self.nome_social = nome_social
        self.obito = obito
        self.html = html

    def set_data_nascimento(self, data_nascimento_str):
        # Método para definir a data de nascimento a partir de uma string no formato "yyyy-MM-dd"
        if data_nascimento_str:
            self.data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()

    def set_data_inscricao(self, data_inscricao_str):
        # Método para definir a data de inscrição a partir de uma string no formato "yyyy-MM-dd"
        if data_inscricao_str:
            self.data_inscricao = datetime.strptime(data_inscricao_str, '%Y-%m-%d').date()

    def set_data_comprovante(self, data_comprovante_str):
        # Método para definir a data do comprovante a partir de uma string (formato específico)
        if data_comprovante_str:
            self.data_comprovante = datetime.strptime(data_comprovante_str, '%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return f"CPF: {self.cpf}, Nome: {self.nome}, Data de Nascimento: {self.data_nascimento}, Situação: {self.situacao}, Data de Inscrição: {self.data_inscricao}, Nome Social: {self.nome_social}, Óbito: {self.obito}, HTML: {self.html}"

    def to_dict(self)->dict:
        return {
            "cpf": self.cpf,
            "nome": self.nome,
            "dataNascimento": self.data_nascimento,
            "situacao": self.situacao,
            "dataInscricao": (self.data_inscricao if self.data_inscricao!=None and re.match(r'/^\d{0,2}/\d{0,2}/\d{4}$/',self.data_inscricao) else None),
            "dataInscricaoText": (self.data_inscricao if self.data_inscricao!=None and not re.match(r'/^\d{0,2}/\d{0,2}/\d{4}$/',self.data_inscricao) else None),
            "nomeSocial": self.nome_social,
            "obito": self.obito,
            "html": self.html,
            "dataComprovante": self.data_comprovante ,
            "codigoComprovante": self.codigo_comprovante,
            "erro": self.erro,
            "html": self.html
        }

