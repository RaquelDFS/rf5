from database import db
from models.requisito import Requisito


class RequisitoService:
    """Camada de serviço responsável pelas operações de requisitos."""

    def listar_todos(self):
        return db.listar_todos_requisitos()

    def listar_por_projeto(self, projeto_id):
        return db.listar_requisitos_por_projeto(projeto_id)

    def listar_cliente(self, id_cliente):
        return db.listar_requisitos_cliente(id_cliente)

    def buscar_por_id(self, id_requisito):
        registro = db.buscar_requisito_por_id(id_requisito)
        if not registro:
            return None

        return Requisito(
            id=registro[0],
            nome=registro[1],
            descricao=registro[2],
            tipo=registro[3],
            status=registro[4],
            visivel_cliente=registro[5],
            projeto_id=registro[6]
        )

    def buscar_registro_por_id(self, id_requisito):
        """Retorna a tupla original do banco para telas que ainda usam índice."""
        return db.buscar_requisito_por_id(id_requisito)

    def criar(self, projeto_id, nome, descricao, tipo, visivel_cliente=1, status="em_analise"):
        return db.criar_requisito(
            projeto_id=projeto_id,
            nome=nome,
            descricao=descricao,
            tipo=tipo,
            visivel_cliente=visivel_cliente,
            status=status
        )

    def atualizar(self, id_requisito, nome, descricao, tipo, status, visivel_cliente):
        return db.atualizar_requisito(
            id_requisito=id_requisito,
            nome=nome,
            descricao=descricao,
            tipo=tipo,
            status=status,
            visivel_cliente=visivel_cliente
        )

    def atualizar_status(self, id_requisito, status):
        return db.atualizar_status_requisito(id_requisito, status)

    def excluir(self, id_requisito):
        return db.excluir_requisito(id_requisito)
