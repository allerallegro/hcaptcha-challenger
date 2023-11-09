class DataNascimentoDivergenteException(Exception):
    def __init__(self):
        super().__init__('Data de nascimento informada está divergente da constante na base de dados da Secretaria da Receita Federal do Brasil')
    