from screens.requisitos import pagina_requisitos
from screens.clientes import pagina_clientes
from screens.usuarios import pagina_usuarios
from screens.inicio import pagina_inicio
from screens.perfis.perfil_usuario import pagina_meu_perfil
from screens.perfis.perfil_cliente import pagina_perfil_cliente
from screens.perfis.perfil_requisito import pagina_perfil_requisito
from screens.projetos import pagina_projetos
from screens.perfis.perfil_projeto import pagina_perfil_projeto


MENUS = {
    "gerente": [
        "Início",
        "Projetos",
        "Requisitos",
        "Clientes",
        "Usuários",
        "Meu Perfil"
    ],
    "analista": [
        "Início",
        "Projetos",
        "Requisitos",
        "Clientes",
        "Meu Perfil"
    ],
    "desenvolvedor": [
        "Início",
        "Projetos",
        "Requisitos",
        "Meu Perfil"
    ],
    "testador": [
        "Início",
        "Projetos",
        "Requisitos",
        "Meu Perfil"
    ],
    "cliente": [
        "Início",
        "Projetos",
        "Meu Perfil"
    ]
}


PAGINAS = {
    "Início":           pagina_inicio,
    "Projetos":         pagina_projetos,
    "Requisitos":       pagina_requisitos,
    "Clientes":         pagina_clientes,
    "Usuários":         pagina_usuarios,
    "Meu Perfil":       pagina_meu_perfil,
    "Perfil Cliente":   pagina_perfil_cliente,
    "Perfil Requisito": pagina_perfil_requisito,
    "Perfil Projeto":   pagina_perfil_projeto,
}

