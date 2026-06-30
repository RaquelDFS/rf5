from database import db


class HistoricoService:

    def registrar(self, tipo_entidade, id_entidade, id_usuario, acao, descricao):
        return db.registrar_historico(
            tipo_entidade=tipo_entidade,
            id_entidade=id_entidade,
            id_usuario=id_usuario,
            acao=acao,
            descricao=descricao
        )

    def listar_requisito(self, id_requisito):
        return db.listar_historico_requisito(id_requisito)

    def listar_projeto(self, id_projeto):
        return db.listar_historico_projeto(id_projeto)

    def listar_projeto_e_requisitos(self, id_projeto):
        return db.listar_historico_por_projeto_e_requisitos(id_projeto)
