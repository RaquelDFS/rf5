import sqlite3
import shutil
from pathlib import Path
from datetime import datetime


DATABASE_NAME = "sistema.db"


def conectar():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            nome         TEXT    NOT NULL,
            login        TEXT    NOT NULL UNIQUE,
            senha        TEXT    NOT NULL,
            funcao       TEXT    NOT NULL,
            email        TEXT,
            empresa      TEXT,
            tipo_cliente TEXT,
            documento    TEXT,
            ativo        INTEGER NOT NULL DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projeto (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            nome              TEXT    NOT NULL,
            descricao         TEXT    NOT NULL,
            status            TEXT    NOT NULL DEFAULT 'iniciado' CHECK (
                                  status IN (
                                      'iniciado',
                                      'em_aprovacao',
                                      'aprovado',
                                      'em_construcao',
                                      'em_atraso',
                                      'em_revisao',
                                      'concluido',
                                      'suspenso',
                                      'cancelado'
                                  )
                              ),
            data_inicio       TEXT    NOT NULL,
            data_fim_prevista TEXT    NOT NULL,
            data_formalizacao TEXT,
            id_responsavel    INTEGER NOT NULL,
            id_cliente        INTEGER NOT NULL,

            FOREIGN KEY (id_responsavel)
                REFERENCES usuarios(id)
                ON DELETE RESTRICT,

            FOREIGN KEY (id_cliente)
                REFERENCES usuarios(id)
                ON DELETE RESTRICT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requisitos (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id          INTEGER NOT NULL,
            nome                TEXT    NOT NULL,
            descricao           TEXT    NOT NULL,
            tipo                TEXT    NOT NULL CHECK (
                                    tipo IN ('funcional', 'nao_funcional')
                                ),
            status              TEXT    NOT NULL DEFAULT 'em_analise' CHECK (
                                    status IN (
                                        'em_analise',
                                        'aguardando_aprovacao',
                                        'aprovado',
                                        'reprovado'
                                    )
                                ),
            visivel_cliente     INTEGER NOT NULL DEFAULT 1,

            FOREIGN KEY (projeto_id)
                REFERENCES projeto(id)
                ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comentarios_requisitos (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            id_requisito    INTEGER NOT NULL,
            id_usuario      INTEGER NOT NULL,
            comentario      TEXT    NOT NULL,
            data_comentario TEXT    NOT NULL,

            FOREIGN KEY (id_requisito)
                REFERENCES requisitos(id)
                ON DELETE CASCADE,

            FOREIGN KEY (id_usuario)
                REFERENCES usuarios(id)
                ON DELETE RESTRICT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_sistema (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_entidade  TEXT    NOT NULL,
            id_entidade    INTEGER NOT NULL,
            id_usuario     INTEGER,
            acao           TEXT    NOT NULL,
            descricao      TEXT    NOT NULL,
            data_historico TEXT    NOT NULL,

            FOREIGN KEY (id_usuario)
                REFERENCES usuarios(id)
                ON DELETE SET NULL
        )
    """)

    conn.commit()
    conn.close()


def garantir_colunas_usuarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(usuarios)")
    colunas = [coluna[1] for coluna in cursor.fetchall()]

    novas_colunas = {
        "empresa": "TEXT",
        "tipo_cliente": "TEXT",
        "documento": "TEXT"
    }

    for coluna, tipo in novas_colunas.items():
        if coluna not in colunas:
            cursor.execute(f"ALTER TABLE usuarios ADD COLUMN {coluna} {tipo}")

    conn.commit()
    conn.close()


def criar_usuarios_padrao():
    conn = conectar()
    cursor = conn.cursor()

    usuarios = [
        ("Raquel da Fonseca", "raquel", "123", "analista", "raquel@email.com", "", "", "", 1),
        ("Wallace Oliveira", "Wallace", "123456", "cliente", "wallace@clinicavidamais.com.br", "Clínica Vida Mais", "Pessoa Jurídica", "00.000.000/0001-00", 1),
        ("Caio Martins", "Caio", "123456", "cliente", "caio@inovatech.com.br", "InovaTech Soluções", "Pessoa Jurídica", "", 1),
        ("Gerente do Projeto", "gerente", "123456", "gerente", "gerente@email.com", "", "", "", 1),
        ("Desenvolvedor Teste", "dev", "123456", "desenvolvedor", "dev@email.com", "", "", "", 1),
        ("Testador Teste", "testador", "123456", "testador", "testador@email.com", "", "", "", 1)
    ]

    for usuario in usuarios:
        cursor.execute("""
            INSERT OR IGNORE INTO usuarios
            (nome, login, senha, funcao, email, empresa, tipo_cliente, documento, ativo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, usuario)

    conn.commit()
    conn.close()


def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, login, funcao, email, empresa, tipo_cliente, documento, ativo
        FROM usuarios
        ORDER BY nome
    """)

    usuarios = cursor.fetchall()
    conn.close()

    return usuarios


def listar_usuarios_ativos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, login, funcao, email, empresa, tipo_cliente, documento, ativo
        FROM usuarios
        WHERE ativo = 1
        ORDER BY nome
    """)

    usuarios = cursor.fetchall()
    conn.close()

    return usuarios


def listar_responsaveis_projeto():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, login, funcao
        FROM usuarios
        WHERE ativo = 1
        AND funcao IN ('gerente', 'analista')
        ORDER BY nome
    """)

    responsaveis = cursor.fetchall()
    conn.close()

    return responsaveis


def buscar_usuario_por_id(id_usuario):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, login, funcao, email, empresa, tipo_cliente, documento, ativo
        FROM usuarios
        WHERE id = ?
    """, (id_usuario,))

    usuario = cursor.fetchone()
    conn.close()

    return usuario


def cadastrar_usuario(nome, login, senha, funcao, email, empresa="", tipo_cliente="", documento=""):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM usuarios
        WHERE login = ?
    """, (login,))

    usuario_existente = cursor.fetchone()

    if usuario_existente:
        conn.close()
        return False, "Já existe um usuário cadastrado com esse login."

    cursor.execute("""
        INSERT INTO usuarios
        (nome, login, senha, funcao, email, empresa, tipo_cliente, documento, ativo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
    """, (nome, login, senha, funcao, email, empresa, tipo_cliente, documento))

    conn.commit()
    conn.close()

    return True, "Usuário cadastrado com sucesso."


def atualizar_usuario(id_usuario, nome, login, funcao, email, ativo, empresa="", tipo_cliente="", documento=""):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM usuarios
        WHERE login = ?
        AND id <> ?
    """, (login, id_usuario))

    usuario_existente = cursor.fetchone()

    if usuario_existente:
        conn.close()
        return False, "Já existe outro usuário com esse login."

    cursor.execute("""
        UPDATE usuarios
        SET nome = ?,
            login = ?,
            funcao = ?,
            email = ?,
            empresa = ?,
            tipo_cliente = ?,
            documento = ?,
            ativo = ?
        WHERE id = ?
    """, (nome, login, funcao, email, empresa, tipo_cliente, documento, ativo, id_usuario))

    conn.commit()
    conn.close()

    return True, "Usuário atualizado com sucesso."


def desativar_usuario(id_usuario):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET ativo = 0
        WHERE id = ?
    """, (id_usuario,))

    conn.commit()
    conn.close()

    return True, "Usuário desativado com sucesso."


def autenticar_usuario(login, senha):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, login, funcao
        FROM usuarios
        WHERE login = ?
        AND senha = ?
        AND ativo = 1
    """, (login, senha))

    usuario = cursor.fetchone()
    conn.close()

    return usuario


def alterar_senha(id_usuario, nova_senha):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET senha = ?
        WHERE id = ?
    """, (nova_senha, id_usuario))

    conn.commit()
    conn.close()


def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, login, empresa, tipo_cliente, documento
        FROM usuarios
        WHERE funcao = 'cliente'
        AND ativo = 1
        ORDER BY COALESCE(NULLIF(empresa, ''), nome)
    """)

    clientes = cursor.fetchall()
    conn.close()

    return clientes


def listar_clientes_gestao():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, login, email, ativo, empresa, tipo_cliente, documento
        FROM usuarios
        WHERE funcao = 'cliente'
        ORDER BY COALESCE(NULLIF(empresa, ''), nome)
    """)

    clientes = cursor.fetchall()
    conn.close()

    return clientes


def buscar_cliente_por_id(id_cliente):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, login, funcao, email, empresa, tipo_cliente, documento, ativo
        FROM usuarios
        WHERE id = ?
        AND funcao = 'cliente'
    """, (id_cliente,))

    cliente = cursor.fetchone()
    conn.close()

    return cliente


def cadastrar_cliente(nome, login, senha, email, empresa="", tipo_cliente="", documento=""):
    if not nome or not nome.strip():
        return False, "Informe o nome do cliente."

    if not login or not login.strip():
        return False, "Informe o login do cliente."

    if not senha or not senha.strip():
        return False, "Informe a senha do cliente."

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM usuarios
        WHERE login = ?
    """, (login.strip(),))

    usuario_existente = cursor.fetchone()

    if usuario_existente:
        conn.close()
        return False, "Já existe um usuário cadastrado com esse login."

    cursor.execute("""
        INSERT INTO usuarios
        (nome, login, senha, funcao, email, empresa, tipo_cliente, documento, ativo)
        VALUES (?, ?, ?, 'cliente', ?, ?, ?, ?, 1)
    """, (
        nome.strip(),
        login.strip(),
        senha.strip(),
        email.strip() if email else "",
        empresa.strip() if empresa else "",
        tipo_cliente.strip() if tipo_cliente else "",
        documento.strip() if documento else ""
    ))

    conn.commit()
    conn.close()

    return True, "Cliente cadastrado com sucesso."


def atualizar_cliente(id_cliente, nome, login, email, ativo, empresa="", tipo_cliente="", documento=""):
    if not nome or not nome.strip():
        return False, "Informe o nome do cliente."

    if not login or not login.strip():
        return False, "Informe o login do cliente."

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM usuarios
        WHERE login = ?
        AND id <> ?
    """, (login.strip(), id_cliente))

    usuario_existente = cursor.fetchone()

    if usuario_existente:
        conn.close()
        return False, "Já existe outro usuário com esse login."

    cursor.execute("""
        UPDATE usuarios
        SET nome = ?,
            login = ?,
            email = ?,
            empresa = ?,
            tipo_cliente = ?,
            documento = ?,
            ativo = ?,
            funcao = 'cliente'
        WHERE id = ?
    """, (
        nome.strip(),
        login.strip(),
        email.strip() if email else "",
        empresa.strip() if empresa else "",
        tipo_cliente.strip() if tipo_cliente else "",
        documento.strip() if documento else "",
        ativo,
        id_cliente
    ))

    conn.commit()
    conn.close()

    return True, "Cliente atualizado com sucesso."


def desativar_cliente(id_cliente):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET ativo = 0
        WHERE id = ?
        AND funcao = 'cliente'
    """, (id_cliente,))

    conn.commit()
    conn.close()

    return True, "Cliente desativado com sucesso."


def criar_projeto(
    nome,
    descricao,
    data_inicio,
    data_fim_prevista,
    id_responsavel,
    id_cliente
):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO projeto (
            nome,
            descricao,
            status,
            data_inicio,
            data_fim_prevista,
            id_responsavel,
            id_cliente
        )
        VALUES (?, ?, 'iniciado', ?, ?, ?, ?)
    """, (
        nome,
        descricao,
        data_inicio,
        data_fim_prevista,
        id_responsavel,
        id_cliente
    ))

    id_projeto = cursor.lastrowid

    conn.commit()
    conn.close()

    return id_projeto


def listar_projetos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.nome,
            p.descricao,
            p.status,
            p.data_inicio,
            p.data_fim_prevista,
            p.data_formalizacao,
            resp.nome AS responsavel,
            COALESCE(NULLIF(cli.empresa, ''), cli.nome) AS cliente,
            cli.nome AS cliente_contato
        FROM projeto p
        INNER JOIN usuarios resp ON resp.id = p.id_responsavel
        INNER JOIN usuarios cli  ON cli.id  = p.id_cliente
        ORDER BY p.id DESC
    """)

    projetos = cursor.fetchall()
    conn.close()

    return projetos


def listar_projetos_por_usuario(id_usuario):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT funcao
        FROM usuarios
        WHERE id = ?
    """, (id_usuario,))

    usuario = cursor.fetchone()

    if usuario and usuario[0] == "gerente":
        cursor.execute("""
            SELECT
                p.id,
                p.nome,
                p.descricao,
                p.status,
                p.data_inicio,
                p.data_fim_prevista,
                p.data_formalizacao,
                resp.nome AS responsavel,
                COALESCE(NULLIF(cli.empresa, ''), cli.nome) AS cliente,
                cli.nome AS cliente_contato
            FROM projeto p
            INNER JOIN usuarios resp ON resp.id = p.id_responsavel
            INNER JOIN usuarios cli  ON cli.id  = p.id_cliente
            ORDER BY p.id DESC
        """)
    else:
        cursor.execute("""
            SELECT
                p.id,
                p.nome,
                p.descricao,
                p.status,
                p.data_inicio,
                p.data_fim_prevista,
                p.data_formalizacao,
                resp.nome AS responsavel,
                COALESCE(NULLIF(cli.empresa, ''), cli.nome) AS cliente,
                cli.nome AS cliente_contato
            FROM projeto p
            INNER JOIN usuarios resp ON resp.id = p.id_responsavel
            INNER JOIN usuarios cli  ON cli.id  = p.id_cliente
            WHERE p.id_responsavel = ?
               OR p.id_cliente = ?
            ORDER BY p.id DESC
        """, (id_usuario, id_usuario))

    projetos = cursor.fetchall()
    conn.close()

    return projetos


def buscar_projeto_por_id(id_projeto):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.nome,
            p.descricao,
            p.status,
            p.data_inicio,
            p.data_fim_prevista,
            p.data_formalizacao,
            p.id_responsavel,
            p.id_cliente,
            resp.nome AS responsavel,
            COALESCE(NULLIF(cli.empresa, ''), cli.nome) AS cliente,
            cli.nome AS cliente_contato
        FROM projeto p
        INNER JOIN usuarios resp ON resp.id = p.id_responsavel
        INNER JOIN usuarios cli  ON cli.id  = p.id_cliente
        WHERE p.id = ?
    """, (id_projeto,))

    projeto = cursor.fetchone()
    conn.close()

    return projeto


def atualizar_projeto(
    id_projeto,
    nome,
    descricao,
    status,
    data_inicio,
    data_fim_prevista,
    id_responsavel,
    id_cliente=None
):
    conn = conectar()
    cursor = conn.cursor()

    if id_cliente is None:
        cursor.execute("""
            UPDATE projeto
            SET
                nome              = ?,
                descricao         = ?,
                status            = ?,
                data_inicio       = ?,
                data_fim_prevista = ?,
                id_responsavel    = ?
            WHERE id = ?
        """, (
            nome,
            descricao,
            status,
            data_inicio,
            data_fim_prevista,
            id_responsavel,
            id_projeto
        ))
    else:
        cursor.execute("""
            UPDATE projeto
            SET
                nome              = ?,
                descricao         = ?,
                status            = ?,
                data_inicio       = ?,
                data_fim_prevista = ?,
                id_responsavel    = ?,
                id_cliente        = ?
            WHERE id = ?
        """, (
            nome,
            descricao,
            status,
            data_inicio,
            data_fim_prevista,
            id_responsavel,
            id_cliente,
            id_projeto
        ))

    conn.commit()
    conn.close()


def registrar_formalizacao(id_projeto, data_formalizacao):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE projeto
        SET
            data_formalizacao = ?,
            status            = 'aprovado'
        WHERE id = ?
    """, (data_formalizacao, id_projeto))

    conn.commit()
    conn.close()


def excluir_projeto(id_projeto):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM projeto
        WHERE id = ?
    """, (id_projeto,))

    conn.commit()
    conn.close()


def _buscar_id_cliente_do_projeto(cursor, projeto_id):
    cursor.execute("""
        SELECT id_cliente
        FROM projeto
        WHERE id = ?
    """, (projeto_id,))

    resultado = cursor.fetchone()

    if resultado is None:
        raise ValueError(f"Projeto com id {projeto_id} não encontrado.")

    return resultado[0]


def criar_requisito(
    projeto_id,
    nome,
    descricao,
    tipo,
    visivel_cliente=1,
    status="em_analise"
):
    conn = conectar()
    cursor = conn.cursor()

    _buscar_id_cliente_do_projeto(cursor, projeto_id)

    cursor.execute("""
        INSERT INTO requisitos (
            projeto_id,
            nome,
            descricao,
            tipo,
            status,
            visivel_cliente
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        projeto_id,
        nome,
        descricao,
        tipo,
        status,
        visivel_cliente
    ))

    id_requisito = cursor.lastrowid

    conn.commit()
    conn.close()

    return id_requisito


def listar_todos_requisitos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.id,
            r.nome,
            r.descricao,
            r.tipo,
            r.status,
            r.visivel_cliente,
            p.nome    AS projeto,
            COALESCE(NULLIF(cli.empresa, ''), cli.nome) AS cliente
        FROM requisitos r
        INNER JOIN projeto  p   ON p.id  = r.projeto_id
        INNER JOIN usuarios cli ON cli.id = p.id_cliente
        ORDER BY r.id DESC
    """)

    dados = cursor.fetchall()
    conn.close()

    return dados


def listar_requisitos_por_projeto(projeto_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.id,
            r.nome,
            r.descricao,
            r.tipo,
            r.status,
            r.visivel_cliente
        FROM requisitos r
        WHERE r.projeto_id = ?
        ORDER BY r.id DESC
    """, (projeto_id,))

    requisitos = cursor.fetchall()
    conn.close()

    return requisitos


def listar_requisitos_cliente(id_cliente):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.id,
            r.nome,
            r.descricao,
            r.tipo,
            r.status,
            p.nome AS projeto
        FROM requisitos r
        INNER JOIN projeto p ON p.id = r.projeto_id
        WHERE p.id_cliente = ?
        AND r.visivel_cliente = 1
        ORDER BY p.nome ASC, r.id DESC
    """, (id_cliente,))

    requisitos = cursor.fetchall()
    conn.close()

    return requisitos


def buscar_requisito_por_id(id_requisito):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.id,
            r.nome,
            r.descricao,
            r.tipo,
            r.status,
            r.visivel_cliente,
            r.projeto_id,
            p.id_cliente,
            COALESCE(NULLIF(cli.empresa, ''), cli.nome) AS cliente
        FROM requisitos r
        INNER JOIN projeto  p   ON p.id  = r.projeto_id
        INNER JOIN usuarios cli ON cli.id = p.id_cliente
        WHERE r.id = ?
    """, (id_requisito,))

    requisito = cursor.fetchone()
    conn.close()

    return requisito


def atualizar_requisito(
    id_requisito,
    nome,
    descricao,
    tipo,
    status,
    visivel_cliente
):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE requisitos
        SET
            nome            = ?,
            descricao       = ?,
            tipo            = ?,
            status          = ?,
            visivel_cliente = ?
        WHERE id = ?
    """, (
        nome,
        descricao,
        tipo,
        status,
        visivel_cliente,
        id_requisito
    ))

    conn.commit()
    conn.close()


def atualizar_status_requisito(id_requisito, status):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE requisitos
        SET status = ?
        WHERE id = ?
    """, (status, id_requisito))

    conn.commit()
    conn.close()


def excluir_requisito(id_requisito):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM requisitos
        WHERE id = ?
    """, (id_requisito,))

    conn.commit()
    conn.close()


def listar_requisitos_completos_por_projeto(id_projeto):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.id,
            r.nome,
            r.descricao,
            r.tipo,
            r.status,
            r.visivel_cliente,
            r.projeto_id,
            p.nome AS projeto,
            COALESCE(NULLIF(cli.empresa, ''), cli.nome) AS cliente,
            resp.nome AS responsavel
        FROM requisitos r
        INNER JOIN projeto p ON p.id = r.projeto_id
        INNER JOIN usuarios cli ON cli.id = p.id_cliente
        INNER JOIN usuarios resp ON resp.id = p.id_responsavel
        WHERE r.projeto_id = ?
        ORDER BY r.id ASC
    """, (id_projeto,))

    linhas = cursor.fetchall()
    conn.close()

    requisitos = []

    for linha in linhas:
        requisitos.append({
            "id": linha[0],
            "nome": linha[1],
            "descricao": linha[2],
            "tipo": linha[3],
            "status": linha[4],
            "visivel_cliente": linha[5],
            "projeto_id": linha[6],
            "projeto": linha[7],
            "cliente": linha[8],
            "responsavel": linha[9]
        })

    return requisitos


def listar_comentarios_por_projeto(id_projeto):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.id,
            c.id_requisito,
            r.nome AS requisito,
            c.comentario,
            c.data_comentario,
            u.nome AS usuario,
            u.funcao AS funcao
        FROM comentarios_requisitos c
        INNER JOIN requisitos r ON r.id = c.id_requisito
        INNER JOIN usuarios u ON u.id = c.id_usuario
        WHERE r.projeto_id = ?
        ORDER BY c.id ASC
    """, (id_projeto,))

    linhas = cursor.fetchall()
    conn.close()

    comentarios = []

    for linha in linhas:
        comentarios.append({
            "id": linha[0],
            "id_requisito": linha[1],
            "requisito": linha[2],
            "comentario": linha[3],
            "data_comentario": linha[4],
            "usuario": linha[5],
            "funcao": linha[6]
        })

    return comentarios


def listar_historico_por_projeto_e_requisitos(id_projeto):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            h.id AS historico_id,
            h.tipo_entidade AS tipo_entidade,
            h.id_entidade AS id_entidade,
            h.acao AS acao,
            h.descricao AS descricao,
            h.data_historico AS data_historico,
            u.nome AS usuario,
            u.funcao AS funcao,
            NULL AS requisito
        FROM historico_sistema h
        LEFT JOIN usuarios u ON u.id = h.id_usuario
        WHERE h.tipo_entidade = 'projeto'
        AND h.id_entidade = ?

        UNION ALL

        SELECT
            h.id AS historico_id,
            h.tipo_entidade AS tipo_entidade,
            h.id_entidade AS id_entidade,
            h.acao AS acao,
            h.descricao AS descricao,
            h.data_historico AS data_historico,
            u.nome AS usuario,
            u.funcao AS funcao,
            r.nome AS requisito
        FROM historico_sistema h
        LEFT JOIN usuarios u ON u.id = h.id_usuario
        INNER JOIN requisitos r ON r.id = h.id_entidade
        WHERE h.tipo_entidade = 'requisito'
        AND r.projeto_id = ?

        ORDER BY historico_id ASC
    """, (id_projeto, id_projeto))

    linhas = cursor.fetchall()
    conn.close()

    historicos = []

    for linha in linhas:
        historicos.append({
            "id": linha[0],
            "tipo_entidade": linha[1],
            "id_entidade": linha[2],
            "acao": linha[3],
            "descricao": linha[4],
            "data_historico": linha[5],
            "usuario": linha[6] if linha[6] else "Sistema",
            "funcao": linha[7] if linha[7] else "-",
            "requisito": linha[8]
        })

    return historicos


def listar_aprovacoes_reprovacoes_por_projeto(id_projeto):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            h.id,
            h.acao,
            h.descricao,
            h.data_historico,
            u.nome AS usuario,
            u.funcao AS funcao,
            r.nome AS requisito
        FROM historico_sistema h
        LEFT JOIN usuarios u ON u.id = h.id_usuario
        INNER JOIN requisitos r ON r.id = h.id_entidade
        WHERE h.tipo_entidade = 'requisito'
        AND r.projeto_id = ?
        AND (
            LOWER(h.acao) LIKE '%aprov%'
            OR LOWER(h.acao) LIKE '%reprov%'
            OR LOWER(h.descricao) LIKE '%aprov%'
            OR LOWER(h.descricao) LIKE '%reprov%'
        )
        ORDER BY h.id ASC
    """, (id_projeto,))

    linhas = cursor.fetchall()
    conn.close()

    registros = []

    for linha in linhas:
        registros.append({
            "id": linha[0],
            "acao": linha[1],
            "descricao": linha[2],
            "data_historico": linha[3],
            "usuario": linha[4] if linha[4] else "Sistema",
            "funcao": linha[5] if linha[5] else "-",
            "requisito": linha[6]
        })

    return registros


def criar_comentario_requisito(id_requisito, id_usuario, comentario):
    conn = conectar()
    cursor = conn.cursor()

    data_comentario = datetime.now().strftime("%d/%m/%Y %H:%M")

    cursor.execute("""
        INSERT INTO comentarios_requisitos (
            id_requisito,
            id_usuario,
            comentario,
            data_comentario
        )
        VALUES (?, ?, ?, ?)
    """, (
        id_requisito,
        id_usuario,
        comentario,
        data_comentario
    ))

    conn.commit()
    conn.close()


def listar_comentarios_requisito(id_requisito):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.id,
            c.comentario,
            c.data_comentario,
            u.nome,
            u.funcao
        FROM comentarios_requisitos c
        INNER JOIN usuarios u ON u.id = c.id_usuario
        WHERE c.id_requisito = ?
        ORDER BY c.id ASC
    """, (id_requisito,))

    comentarios = cursor.fetchall()
    conn.close()

    return comentarios


def registrar_historico(
    tipo_entidade,
    id_entidade,
    id_usuario,
    acao,
    descricao
):
    conn = conectar()
    cursor = conn.cursor()

    data_historico = datetime.now().strftime("%d/%m/%Y %H:%M")

    cursor.execute("""
        INSERT INTO historico_sistema (
            tipo_entidade,
            id_entidade,
            id_usuario,
            acao,
            descricao,
            data_historico
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        tipo_entidade,
        id_entidade,
        id_usuario,
        acao,
        descricao,
        data_historico
    ))

    conn.commit()
    conn.close()


def listar_historico_requisito(id_requisito):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            h.id,
            h.acao,
            h.descricao,
            h.data_historico,
            u.nome,
            u.funcao
        FROM historico_sistema h
        LEFT JOIN usuarios u ON u.id = h.id_usuario
        WHERE h.tipo_entidade = 'requisito'
        AND h.id_entidade = ?
        ORDER BY h.id DESC
    """, (id_requisito,))

    historico = cursor.fetchall()
    conn.close()

    return historico


def listar_historico_projeto(id_projeto):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            h.id,
            h.acao,
            h.descricao,
            h.data_historico,
            u.nome,
            u.funcao
        FROM historico_sistema h
        LEFT JOIN usuarios u ON u.id = h.id_usuario
        WHERE h.tipo_entidade = 'projeto'
        AND h.id_entidade = ?
        ORDER BY h.id DESC
    """, (id_projeto,))

    historico = cursor.fetchall()
    conn.close()

    return historico


def gerar_backup_banco():
    caminho_banco = Path(DATABASE_NAME)

    if not caminho_banco.exists():
        return False, None, "Banco de dados sistema.db não encontrado."

    pasta_backup = Path("backups")
    pasta_backup.mkdir(exist_ok=True)

    data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_backup = f"backup_sistema_{data_hora}.db"
    caminho_backup = pasta_backup / nome_backup

    try:
        shutil.copy2(caminho_banco, caminho_backup)
        return True, str(caminho_backup), "Backup gerado com sucesso."
    except Exception as erro:
        return False, None, f"Erro ao gerar backup: {erro}"


def listar_backups_banco():
    pasta_backup = Path("backups")

    if not pasta_backup.exists():
        return []

    backups = list(pasta_backup.glob("backup_sistema_*.db"))
    backups.sort(key=lambda arquivo: arquivo.stat().st_mtime, reverse=True)

    return backups


def inicializar_banco():
    criar_tabelas()
    garantir_colunas_usuarios()
    criar_usuarios_padrao()