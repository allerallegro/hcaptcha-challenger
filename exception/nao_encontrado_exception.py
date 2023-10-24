class NaoEncontradoException(Exception):
    def __init__(self):
        super().__init__('Não existe no Cadastro de Pessoas Jurdicas o número de CNPJ informado. Verifique se o mesmo foi digitado corretamente.')
