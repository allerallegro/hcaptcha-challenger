from dataclasses import dataclass


@dataclass
class Socio:
    def __init__(self):
        self.nome = ""
        self.qualificacao = ""
        self.qualificacao_rep_legal = ""
        self.nome_representante_legal = ""

    def to_dict(self):
        # Crie um dicionário com atributos formatados
        return {
            "nome": self.nome,
            "qualificacao": self.qualificacao,
            "nomeRepresentanteLegal": self.nome_representante_legal,
            "qualificacaoRepLegal": self.qualificacao_rep_legal,
        }

    def set_nome(self, value):
        self.nome = value

    def set_qualificacao(self, value):
        self.qualificacao = value

    def set_qualificacao_replegal(self, value):
        self.qualificacao_rep_legal = value

    def set_nome_representante_legal(self, value):
        self.nome_representante_legal = value
