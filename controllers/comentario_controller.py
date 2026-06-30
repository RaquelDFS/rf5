from services.comentario_service import ComentarioService


class ComentarioController:

    def __init__(self):
        self.service = ComentarioService()

    def criar(self, id_requisito, id_usuario, comentario):
        if not id_requisito:
            return False, "Requisito não informado."
        if not id_usuario:
            return False, "Usuário não informado."
        if not comentario or not comentario.strip():
            return False, "Informe um comentário."

        self.service.criar(id_requisito, id_usuario, comentario.strip())
        return True, "Comentário registrado com sucesso."

    def listar_por_requisito(self, id_requisito):
        return self.service.listar_por_requisito(id_requisito)

    def listar_por_projeto(self, id_projeto):
        return self.service.listar_por_projeto(id_projeto)
