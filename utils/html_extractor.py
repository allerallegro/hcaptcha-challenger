import re
import string

from pyquery import PyQuery as pq

from models.comprovante_situacao_cadastral import ConsultaCpfModel


def from_html(html:string) -> ConsultaCpfModel:
    doc = pq(html)
    result = ConsultaCpfModel()
    for el in doc('.clConteudoDados'):
        if "N" == el.text.strip():
            result.cpf = re.sub(r'\D', '', doc('b',el).text().strip())
        elif "Nome:" == el.text.strip():
            result.nome = doc('b',el).text().strip()
        elif "Data de Nascimento:" == el.text.strip():
            result.data_nascimento = doc('b',el).text().strip()
        elif "Situação Cadastral:" == el.text.strip():
            result.situacao = doc('b',el).text().strip()
        elif "Data da Inscrição:" == el.text.strip():
            result.data_inscricao = doc('b',el).text().strip()
        elif "Digito Verificador:" == el.text.strip():
            result.digito_verificador = doc('b',el).text().strip()
    for el in doc('.clConteudoComp'):
        if "Comprovante emitido às:" == el.text.strip():
            result.data_comprovante = f"{doc('b',el)[1].text.strip()} {doc('b',el)[0].text.strip()}"
        elif "Código de controle do comprovante:" == el.text.strip():
            result.codigo_comprovante = doc('b',el).text().strip()
    result.obito = 'TITULAR FALECIDO' == result.situacao   
    return result