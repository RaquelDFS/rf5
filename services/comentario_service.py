from database import db


class ComentarioService:

    def criar(self, id_requisito, id_usuario, comentario):
        return db.criar_comentario_requisito(id_requisito, id_usuario, comentario)

    def listar_por_requisito(self, id_requisito):
        return db.listar_comentarios_requisito(id_requisito)

    def listar_por_projeto(self, id_projeto):
        return db.listar_comentarios_por_projeto(id_projeto)
