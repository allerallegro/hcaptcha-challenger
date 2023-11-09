class NaoEncontradoException(Exception):
    def __init__(self):
        super().__init__('CPF não encontrado na base de dados da Receita Federal')
