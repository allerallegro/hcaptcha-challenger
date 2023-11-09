import json
from datetime import datetime, timedelta
from typing import Optional

import psycopg2

from models.comprovante_situacao_cadastral import ConsultaCpfModel


class CPFRepository:
    def __init__(self, connection: psycopg2.extensions.connection):
        self.connection = connection

    def get_ultima_consulta(self, cpf: str, nascimento: str) -> Optional[dict]:
        query = """
            SELECT * FROM tb_cache
            WHERE documento = %s AND dh_consulta >= %s AND data#>>'{dataNascimento}' = %s
            ORDER BY 1 DESC LIMIT 1;
        """
        data_limite = datetime.now() - timedelta(days=180)

        cursor = self.connection.cursor()
        cursor.execute(query, (cpf, data_limite.isoformat(), nascimento))
        row = cursor.fetchone()
        cursor.close()

        if row:
            return row[3]

        return None

    def salvar(self, cpf: str, data: ConsultaCpfModel) -> None:
        query = """
            INSERT INTO tb_cache (documento, dh_consulta, data)
            VALUES (%s, NOW(), %s::jsonb)
            RETURNING *;
        """

        cursor = self.connection.cursor()
        cursor.execute(query, (cpf, json.dumps(data.to_dict(), ensure_ascii=False)))
        cursor.close()
        self.connection.commit()

    def update(self, id: int) -> None:
        query = """
            UPDATE tb_lote_item SET proc_receita = true
            WHERE id_lote_item = %s
            RETURNING *;
        """
        cursor = self.connection.cursor()
        cursor.execute(query, (id,))
        cursor.close()
        self.connection.commit()
