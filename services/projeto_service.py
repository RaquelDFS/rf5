from database import db
from models.projeto import Projeto


class ProjetoService:

    def listar(self):
        return db.listar_projetos()

    def listar_por_usuario(self, id_usuario):
        return db.listar_projetos_por_usuario(id_usuario)

    def buscar_por_id(self, id_projeto):
        registro = db.buscar_projeto_por_id(id_projeto)
        if not registro:
            return None

        return Projeto(
            id=registro[0],
            nome=registro[1],
            descricao=registro[2],
            status=registro[3],
            data_inicio=registro[4],
            data_fim_prevista=registro[5],
            data_formalizacao=registro[6],
            id_responsavel=registro[7],
            id_cliente=registro[8]
        )

    def buscar_registro_por_id(self, id_projeto):
        return db.buscar_projeto_por_id(id_projeto)

    def criar(self, nome, descricao, data_inicio, data_fim_prevista, id_responsavel, id_cliente):
        return db.criar_projeto(
            nome=nome,
            descricao=descricao,
            data_inicio=data_inicio,
            data_fim_prevista=data_fim_prevista,
            id_responsavel=id_responsavel,
            id_cliente=id_cliente
        )

    def atualizar(self, id_projeto, nome, descricao, status, data_inicio, data_fim_prevista, id_responsavel, id_cliente=None):
        return db.atualizar_projeto(
            id_projeto=id_projeto,
            nome=nome,
            descricao=descricao,
            status=status,
            data_inicio=data_inicio,
            data_fim_prevista=data_fim_prevista,
            id_responsavel=id_responsavel,
            id_cliente=id_cliente
        )

    def registrar_formalizacao(self, id_projeto, data_formalizacao):
        return db.registrar_formalizacao(id_projeto, data_formalizacao)

    def excluir(self, id_projeto):
        return db.excluir_projeto(id_projeto)

    def listar_requisitos_completos(self, id_projeto):
        return db.listar_requisitos_completos_por_projeto(id_projeto)

    def listar_comentarios(self, id_projeto):
        return db.listar_comentarios_por_projeto(id_projeto)

    def listar_historico_completo(self, id_projeto):
        return db.listar_historico_por_projeto_e_requisitos(id_projeto)

    def listar_aprovacoes_reprovacoes(self, id_projeto):
        return db.listar_aprovacoes_reprovacoes_por_projeto(id_projeto)
