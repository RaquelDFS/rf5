class Comentario:
    def __init__(
        self,
        id=None,
        id_requisito=None,
        id_usuario=None,
        comentario="",
        data_comentario=None
    ):
        self.id = id
        self.id_requisito = id_requisito
        self.id_usuario = id_usuario
        self.comentario = comentario
        self.data_comentario = data_comentario

    def possui_texto(self):
        return self.comentario.strip() != ""

    def to_dict(self):
        return {
            "id": self.id,
            "id_requisito": self.id_requisito,
            "id_usuario": self.id_usuario,
            "comentario": self.comentario,
            "data_comentario": self.data_comentario
        }

    def __str__(self):
        return self.comentario
