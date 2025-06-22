# grammar_def.py
"""
Tabla LL(1) completa SIN atajos: cada función de video usa
su propio token (VIDEO_RESIZE, VIDEO_FLIP, …).

TokenType esperados
-------------------
VIDEO_RESIZE, VIDEO_FLIP, VIDEO_VELOCIDAD, VIDEO_FADEIN,
VIDEO_FADEOUT, VIDEO_SILENCIO, VIDEO_EXTRAER_AUDIO,
VIDEO_QUITAR_AUDIO, VIDEO_AGREGAR_MUSICA, VIDEO_CONCATENAR,
VIDEO_CORTAR
​—además de todos los ya definidos en enums.py (keywords, tipos,
operadores, literales, IDENTIFIER, EOF, etc.).
"""

from enums import TokenType

EPSILON = "ε"
START_SYMBOL = "Program"

# ------------------------------------------------------------
#                 TABLA LL(1)
# ------------------------------------------------------------
PARSING_TABLE: dict[str, dict[TokenType | str, list]] = {

    # ────────── Programa ──────────
    "Program": {
        TokenType.MAIN: [TokenType.MAIN, "Block", TokenType.EOF],
    },

    # ────────── Bloque { … } ──────────
    "Block": {
        TokenType.LBRACE: [TokenType.LBRACE, "StmtList", TokenType.RBRACE],
    },

    "StmtList": {
        TokenType.INT_TYPE:   ["Stmt", "StmtList"],
        TokenType.FLOAT_TYPE: ["Stmt", "StmtList"],
        TokenType.STRING_TYPE:["Stmt", "StmtList"],
        TokenType.VIDEO_TYPE: ["Stmt", "StmtList"],
        TokenType.AUDIO_TYPE: ["Stmt", "StmtList"],
        TokenType.IDENTIFIER: ["Stmt", "StmtList"],
        TokenType.IF:         ["Stmt", "StmtList"],
        TokenType.WHILE:      ["Stmt", "StmtList"],
        TokenType.RBRACE:     [EPSILON],
    },

    "Stmt": {
        TokenType.INT_TYPE:   ["VarDecl", TokenType.SEMICOLON],
        TokenType.FLOAT_TYPE: ["VarDecl", TokenType.SEMICOLON],
        TokenType.STRING_TYPE:["VarDecl", TokenType.SEMICOLON],
        TokenType.VIDEO_TYPE: ["VarDecl", TokenType.SEMICOLON],
        TokenType.AUDIO_TYPE: ["VarDecl", TokenType.SEMICOLON],
        TokenType.IDENTIFIER: ["Assignment", TokenType.SEMICOLON],
        TokenType.IF:         ["IfStmt"],
        TokenType.WHILE:      ["WhileStmt"],
    },

    # ───────── Declaración de variables ─────────
    "VarDecl": {
        TokenType.INT_TYPE:   ["Type", TokenType.COLON, TokenType.IDENTIFIER, "VarInitOpt"],
        TokenType.FLOAT_TYPE: ["Type", TokenType.COLON, TokenType.IDENTIFIER, "VarInitOpt"],
        TokenType.STRING_TYPE:["Type", TokenType.COLON, TokenType.IDENTIFIER, "VarInitOpt"],
        TokenType.VIDEO_TYPE: ["Type", TokenType.COLON, TokenType.IDENTIFIER, "VarInitOpt"],
        TokenType.AUDIO_TYPE: ["Type", TokenType.COLON, TokenType.IDENTIFIER, "VarInitOpt"],
    },
    "VarInitOpt": {
        TokenType.ASSIGN:    [TokenType.ASSIGN, "Expr"],
        TokenType.SEMICOLON: [EPSILON],
    },

    "Type": {
        TokenType.INT_TYPE:   [TokenType.INT_TYPE],
        TokenType.FLOAT_TYPE: [TokenType.FLOAT_TYPE],
        TokenType.STRING_TYPE:[TokenType.STRING_TYPE],
        TokenType.VIDEO_TYPE: [TokenType.VIDEO_TYPE],
        TokenType.AUDIO_TYPE: [TokenType.AUDIO_TYPE],
    },

    # ───────── Asignación ─────────
    "Assignment": {
        TokenType.IDENTIFIER: [TokenType.IDENTIFIER, TokenType.ASSIGN, "Expr"],
    },

    # ───────── If / Else ─────────
    "IfStmt": {
        TokenType.IF: [TokenType.IF, TokenType.LPAREN, "Expr",TokenType.RPAREN, "Block", "ElseOpt"],
    },
    "ElseOpt": {
        TokenType.ELSE:      [TokenType.ELSE, "Block"],
        TokenType.INT_TYPE:   [EPSILON], 
        TokenType.FLOAT_TYPE: [EPSILON],
        TokenType.STRING_TYPE:[EPSILON], 
        TokenType.VIDEO_TYPE: [EPSILON],
        TokenType.AUDIO_TYPE: [EPSILON], 
        TokenType.IDENTIFIER: [EPSILON],
        TokenType.IF:         [EPSILON], 
        TokenType.WHILE:      [EPSILON],
        TokenType.RBRACE:     [EPSILON],
    },

    # ───────── While ─────────
    "WhileStmt": {
        TokenType.WHILE: [TokenType.WHILE, TokenType.LPAREN, "Expr",
                          TokenType.RPAREN, "Block"],
    },

    # =========================================================
    #                     EXPRESIONES
    # =========================================================
    # Expr
    "Expr": {
        TokenType.IDENTIFIER: ["OrExpr"],
        TokenType.INT_LITERAL: ["OrExpr"],
        TokenType.FLOAT_LITERAL: ["OrExpr"],
        TokenType.STRING_LITERAL: ["OrExpr"],
        TokenType.LPAREN: ["OrExpr"],
        TokenType.NOT: ["OrExpr"],
        TokenType.MINUS: ["OrExpr"],

        TokenType.VIDEO_RESIZE: ["OrExpr"],
        TokenType.VIDEO_FLIP: ["OrExpr"],
        TokenType.VIDEO_VELOCIDAD: ["OrExpr"],
        TokenType.VIDEO_FADEIN: ["OrExpr"],
        TokenType.VIDEO_FADEOUT: ["OrExpr"],
        TokenType.VIDEO_SILENCIO: ["OrExpr"],
        TokenType.VIDEO_EXTRAER_AUDIO: ["OrExpr"],
        TokenType.VIDEO_QUITAR_AUDIO: ["OrExpr"],
        TokenType.VIDEO_AGREGAR_MUSICA: ["OrExpr"],
        TokenType.VIDEO_CONCATENAR: ["OrExpr"],
        TokenType.VIDEO_CORTAR: ["OrExpr"],
    },

    # OrExpr
    "OrExpr": {
        TokenType.IDENTIFIER: ["AndExpr", "OrExpr'"],
        TokenType.INT_LITERAL: ["AndExpr", "OrExpr'"],
        TokenType.FLOAT_LITERAL: ["AndExpr", "OrExpr'"],
        TokenType.STRING_LITERAL: ["AndExpr", "OrExpr'"],
        TokenType.LPAREN: ["AndExpr", "OrExpr'"],
        TokenType.NOT: ["AndExpr", "OrExpr'"],
        TokenType.MINUS: ["AndExpr", "OrExpr'"],

        TokenType.VIDEO_RESIZE: ["AndExpr", "OrExpr'"],
        TokenType.VIDEO_FLIP: ["AndExpr", "OrExpr'"],
        TokenType.VIDEO_VELOCIDAD: ["AndExpr", "OrExpr'"],
        TokenType.VIDEO_FADEIN: ["AndExpr", "OrExpr'"],
        TokenType.VIDEO_FADEOUT: ["AndExpr", "OrExpr'"],
        TokenType.VIDEO_SILENCIO: ["AndExpr", "OrExpr'"],
        TokenType.VIDEO_EXTRAER_AUDIO: ["AndExpr", "OrExpr'"],
        TokenType.VIDEO_QUITAR_AUDIO: ["AndExpr", "OrExpr'"],
        TokenType.VIDEO_AGREGAR_MUSICA: ["AndExpr", "OrExpr'"],
        TokenType.VIDEO_CONCATENAR: ["AndExpr", "OrExpr'"],
        TokenType.VIDEO_CORTAR: ["AndExpr", "OrExpr'"],
    },
    "OrExpr'": {
        TokenType.OR: [TokenType.OR, "AndExpr", "OrExpr'"],
        TokenType.RPAREN: [EPSILON], TokenType.SEMICOLON: [EPSILON],
        TokenType.COMMA: [EPSILON], TokenType.RBRACKET: [EPSILON],
    },

    # AndExpr
    "AndExpr": {
        TokenType.IDENTIFIER: ["EqualityExpr", "AndExpr'"],
        TokenType.INT_LITERAL: ["EqualityExpr", "AndExpr'"],
        TokenType.FLOAT_LITERAL: ["EqualityExpr", "AndExpr'"],
        TokenType.STRING_LITERAL: ["EqualityExpr", "AndExpr'"],
        TokenType.LPAREN: ["EqualityExpr", "AndExpr'"],
        TokenType.NOT: ["EqualityExpr", "AndExpr'"],
        TokenType.MINUS: ["EqualityExpr", "AndExpr'"],

        TokenType.VIDEO_RESIZE: ["EqualityExpr", "AndExpr'"],
        TokenType.VIDEO_FLIP: ["EqualityExpr", "AndExpr'"],
        TokenType.VIDEO_VELOCIDAD: ["EqualityExpr", "AndExpr'"],
        TokenType.VIDEO_FADEIN: ["EqualityExpr", "AndExpr'"],
        TokenType.VIDEO_FADEOUT: ["EqualityExpr", "AndExpr'"],
        TokenType.VIDEO_SILENCIO: ["EqualityExpr", "AndExpr'"],
        TokenType.VIDEO_EXTRAER_AUDIO: ["EqualityExpr", "AndExpr'"],
        TokenType.VIDEO_QUITAR_AUDIO: ["EqualityExpr", "AndExpr'"],
        TokenType.VIDEO_AGREGAR_MUSICA: ["EqualityExpr", "AndExpr'"],
        TokenType.VIDEO_CONCATENAR: ["EqualityExpr", "AndExpr'"],
        TokenType.VIDEO_CORTAR: ["EqualityExpr", "AndExpr'"],
    },
    "AndExpr'": {
        TokenType.AND: [TokenType.AND, "EqualityExpr", "AndExpr'"],
        TokenType.OR: [EPSILON], TokenType.RPAREN: [EPSILON],
        TokenType.SEMICOLON: [EPSILON], TokenType.COMMA: [EPSILON],
        TokenType.RBRACKET: [EPSILON],
    },

    # EqualityExpr
    "EqualityExpr": {
        TokenType.IDENTIFIER: ["RelExpr", "EqualityExpr'"],
        TokenType.INT_LITERAL: ["RelExpr", "EqualityExpr'"],
        TokenType.FLOAT_LITERAL: ["RelExpr", "EqualityExpr'"],
        TokenType.STRING_LITERAL: ["RelExpr", "EqualityExpr'"],
        TokenType.LPAREN: ["RelExpr", "EqualityExpr'"],
        TokenType.NOT: ["RelExpr", "EqualityExpr'"],
        TokenType.MINUS: ["RelExpr", "EqualityExpr'"],

        TokenType.VIDEO_RESIZE: ["RelExpr", "EqualityExpr'"],
        TokenType.VIDEO_FLIP: ["RelExpr", "EqualityExpr'"],
        TokenType.VIDEO_VELOCIDAD: ["RelExpr", "EqualityExpr'"],
        TokenType.VIDEO_FADEIN: ["RelExpr", "EqualityExpr'"],
        TokenType.VIDEO_FADEOUT: ["RelExpr", "EqualityExpr'"],
        TokenType.VIDEO_SILENCIO: ["RelExpr", "EqualityExpr'"],
        TokenType.VIDEO_EXTRAER_AUDIO: ["RelExpr", "EqualityExpr'"],
        TokenType.VIDEO_QUITAR_AUDIO: ["RelExpr", "EqualityExpr'"],
        TokenType.VIDEO_AGREGAR_MUSICA: ["RelExpr", "EqualityExpr'"],
        TokenType.VIDEO_CONCATENAR: ["RelExpr", "EqualityExpr'"],
        TokenType.VIDEO_CORTAR: ["RelExpr", "EqualityExpr'"],
    },
    "EqualityExpr'": {
        TokenType.EQ: [TokenType.EQ, "RelExpr", "EqualityExpr'"],
        TokenType.NEQ: [TokenType.NEQ, "RelExpr", "EqualityExpr'"],
        TokenType.LT: [EPSILON], TokenType.LE: [EPSILON],
        TokenType.GT: [EPSILON], TokenType.GE: [EPSILON],
        TokenType.AND: [EPSILON], TokenType.OR: [EPSILON],
        TokenType.RPAREN: [EPSILON], TokenType.SEMICOLON: [EPSILON],
        TokenType.COMMA: [EPSILON], TokenType.RBRACKET: [EPSILON],
    },

    # RelExpr
    "RelExpr": {
        TokenType.IDENTIFIER: ["AddExpr", "RelExpr'"],
        TokenType.INT_LITERAL: ["AddExpr", "RelExpr'"],
        TokenType.FLOAT_LITERAL: ["AddExpr", "RelExpr'"],
        TokenType.STRING_LITERAL: ["AddExpr", "RelExpr'"],
        TokenType.LPAREN: ["AddExpr", "RelExpr'"],
        TokenType.NOT: ["AddExpr", "RelExpr'"],
        TokenType.MINUS: ["AddExpr", "RelExpr'"],

        TokenType.VIDEO_RESIZE: ["AddExpr", "RelExpr'"],
        TokenType.VIDEO_FLIP: ["AddExpr", "RelExpr'"],
        TokenType.VIDEO_VELOCIDAD: ["AddExpr", "RelExpr'"],
        TokenType.VIDEO_FADEIN: ["AddExpr", "RelExpr'"],
        TokenType.VIDEO_FADEOUT: ["AddExpr", "RelExpr'"],
        TokenType.VIDEO_SILENCIO: ["AddExpr", "RelExpr'"],
        TokenType.VIDEO_EXTRAER_AUDIO: ["AddExpr", "RelExpr'"],
        TokenType.VIDEO_QUITAR_AUDIO: ["AddExpr", "RelExpr'"],
        TokenType.VIDEO_AGREGAR_MUSICA: ["AddExpr", "RelExpr'"],
        TokenType.VIDEO_CONCATENAR: ["AddExpr", "RelExpr'"],
        TokenType.VIDEO_CORTAR: ["AddExpr", "RelExpr'"],
    },
    "RelExpr'": {
        TokenType.LT: [TokenType.LT, "AddExpr", "RelExpr'"],
        TokenType.LE: [TokenType.LE, "AddExpr", "RelExpr'"],
        TokenType.GT: [TokenType.GT, "AddExpr", "RelExpr'"],
        TokenType.GE: [TokenType.GE, "AddExpr", "RelExpr'"],
        TokenType.EQ: [EPSILON], TokenType.NEQ: [EPSILON],
        TokenType.AND: [EPSILON], TokenType.OR: [EPSILON],
        TokenType.RPAREN: [EPSILON], TokenType.SEMICOLON: [EPSILON],
        TokenType.COMMA: [EPSILON], TokenType.RBRACKET: [EPSILON],
    },

    # AddExpr
    "AddExpr": {
        TokenType.IDENTIFIER: ["Term", "AddExpr'"],
        TokenType.INT_LITERAL: ["Term", "AddExpr'"],
        TokenType.FLOAT_LITERAL: ["Term", "AddExpr'"],
        TokenType.STRING_LITERAL: ["Term", "AddExpr'"],
        TokenType.LPAREN: ["Term", "AddExpr'"],
        TokenType.NOT: ["Term", "AddExpr'"],
        TokenType.MINUS: ["Term", "AddExpr'"],

        TokenType.VIDEO_RESIZE: ["Term", "AddExpr'"],
        TokenType.VIDEO_FLIP: ["Term", "AddExpr'"],
        TokenType.VIDEO_VELOCIDAD: ["Term", "AddExpr'"],
        TokenType.VIDEO_FADEIN: ["Term", "AddExpr'"],
        TokenType.VIDEO_FADEOUT: ["Term", "AddExpr'"],
        TokenType.VIDEO_SILENCIO: ["Term", "AddExpr'"],
        TokenType.VIDEO_EXTRAER_AUDIO: ["Term", "AddExpr'"],
        TokenType.VIDEO_QUITAR_AUDIO: ["Term", "AddExpr'"],
        TokenType.VIDEO_AGREGAR_MUSICA: ["Term", "AddExpr'"],
        TokenType.VIDEO_CONCATENAR: ["Term", "AddExpr'"],
        TokenType.VIDEO_CORTAR: ["Term", "AddExpr'"],
    },
    "AddExpr'": {
        TokenType.PLUS: [TokenType.PLUS, "Term", "AddExpr'"],
        TokenType.MINUS: [TokenType.MINUS, "Term", "AddExpr'"],
        TokenType.LT: [EPSILON], TokenType.LE: [EPSILON],
        TokenType.GT: [EPSILON], TokenType.GE: [EPSILON],
        TokenType.EQ: [EPSILON], TokenType.NEQ: [EPSILON],
        TokenType.AND: [EPSILON], TokenType.OR: [EPSILON],
        TokenType.RPAREN: [EPSILON], TokenType.SEMICOLON: [EPSILON],
        TokenType.COMMA: [EPSILON], TokenType.RBRACKET: [EPSILON],
    },

    # Term
    "Term": {
        TokenType.IDENTIFIER: ["Factor", "Term'"],
        TokenType.INT_LITERAL: ["Factor", "Term'"],
        TokenType.FLOAT_LITERAL: ["Factor", "Term'"],
        TokenType.STRING_LITERAL: ["Factor", "Term'"],
        TokenType.LPAREN: ["Factor", "Term'"],
        TokenType.NOT: ["Factor", "Term'"],
        TokenType.MINUS: ["Factor", "Term'"],

        TokenType.VIDEO_RESIZE: ["Factor", "Term'"],
        TokenType.VIDEO_FLIP: ["Factor", "Term'"],
        TokenType.VIDEO_VELOCIDAD: ["Factor", "Term'"],
        TokenType.VIDEO_FADEIN: ["Factor", "Term'"],
        TokenType.VIDEO_FADEOUT: ["Factor", "Term'"],
        TokenType.VIDEO_SILENCIO: ["Factor", "Term'"],
        TokenType.VIDEO_EXTRAER_AUDIO: ["Factor", "Term'"],
        TokenType.VIDEO_QUITAR_AUDIO: ["Factor", "Term'"],
        TokenType.VIDEO_AGREGAR_MUSICA: ["Factor", "Term'"],
        TokenType.VIDEO_CONCATENAR: ["Factor", "Term'"],
        TokenType.VIDEO_CORTAR: ["Factor", "Term'"],
    },
    "Term'": {
        TokenType.MULT: [TokenType.MULT, "Factor", "Term'"],
        TokenType.DIV:  [TokenType.DIV,  "Factor", "Term'"],
        TokenType.PLUS: [EPSILON], TokenType.MINUS: [EPSILON],
        TokenType.LT: [EPSILON], TokenType.LE: [EPSILON],
        TokenType.GT: [EPSILON], TokenType.GE: [EPSILON],
        TokenType.EQ: [EPSILON], TokenType.NEQ: [EPSILON],
        TokenType.AND: [EPSILON], TokenType.OR: [EPSILON],
        TokenType.RPAREN: [EPSILON], TokenType.SEMICOLON: [EPSILON],
        TokenType.COMMA: [EPSILON], TokenType.RBRACKET: [EPSILON],
    },

    # Factor
    "Factor": {
        TokenType.IDENTIFIER: [TokenType.IDENTIFIER],
        TokenType.INT_LITERAL: [TokenType.INT_LITERAL],
        TokenType.FLOAT_LITERAL: [TokenType.FLOAT_LITERAL],
        TokenType.STRING_LITERAL: [TokenType.STRING_LITERAL],
        TokenType.LPAREN: [TokenType.LPAREN, "Expr", TokenType.RPAREN],
        TokenType.NOT: [TokenType.NOT, "Factor"],
        TokenType.MINUS: [TokenType.MINUS, "Factor"],

        TokenType.VIDEO_RESIZE: ["FunctionCall"],
        TokenType.VIDEO_FLIP: ["FunctionCall"],
        TokenType.VIDEO_VELOCIDAD: ["FunctionCall"],
        TokenType.VIDEO_FADEIN: ["FunctionCall"],
        TokenType.VIDEO_FADEOUT: ["FunctionCall"],
        TokenType.VIDEO_SILENCIO: ["FunctionCall"],
        TokenType.VIDEO_EXTRAER_AUDIO: ["FunctionCall"],
        TokenType.VIDEO_QUITAR_AUDIO: ["FunctionCall"],
        TokenType.VIDEO_AGREGAR_MUSICA: ["FunctionCall"],
        TokenType.VIDEO_CONCATENAR: ["FunctionCall"],
        TokenType.VIDEO_CORTAR: ["FunctionCall"],
    },

    # FunctionCall
    "FunctionCall": {
        TokenType.VIDEO_RESIZE: [TokenType.VIDEO_RESIZE, TokenType.LBRACKET, "ArgListOpt", TokenType.RBRACKET],
        TokenType.VIDEO_FLIP: [TokenType.VIDEO_FLIP, TokenType.LBRACKET, "ArgListOpt", TokenType.RBRACKET],
        TokenType.VIDEO_VELOCIDAD: [TokenType.VIDEO_VELOCIDAD, TokenType.LBRACKET, "ArgListOpt", TokenType.RBRACKET],
        TokenType.VIDEO_FADEIN: [TokenType.VIDEO_FADEIN, TokenType.LBRACKET, "ArgListOpt", TokenType.RBRACKET],
        TokenType.VIDEO_FADEOUT: [TokenType.VIDEO_FADEOUT, TokenType.LBRACKET, "ArgListOpt", TokenType.RBRACKET],
        TokenType.VIDEO_SILENCIO: [TokenType.VIDEO_SILENCIO, TokenType.LBRACKET, "ArgListOpt", TokenType.RBRACKET],
        TokenType.VIDEO_EXTRAER_AUDIO: [TokenType.VIDEO_EXTRAER_AUDIO, TokenType.LBRACKET, "ArgListOpt", TokenType.RBRACKET],
        TokenType.VIDEO_QUITAR_AUDIO: [TokenType.VIDEO_QUITAR_AUDIO, TokenType.LBRACKET, "ArgListOpt", TokenType.RBRACKET],
        TokenType.VIDEO_AGREGAR_MUSICA: [TokenType.VIDEO_AGREGAR_MUSICA, TokenType.LBRACKET, "ArgListOpt", TokenType.RBRACKET],
        TokenType.VIDEO_CONCATENAR: [TokenType.VIDEO_CONCATENAR, TokenType.LBRACKET, "ArgListOpt", TokenType.RBRACKET],
        TokenType.VIDEO_CORTAR: [TokenType.VIDEO_CORTAR, TokenType.LBRACKET, "ArgListOpt", TokenType.RBRACKET],
    },
    "ArgListOpt": {
        TokenType.IDENTIFIER: ["ArgList"],
        TokenType.INT_LITERAL: ["ArgList"],
        TokenType.FLOAT_LITERAL: ["ArgList"],
        TokenType.STRING_LITERAL: ["ArgList"],
        TokenType.LPAREN: ["ArgList"],
        TokenType.NOT: ["ArgList"],
        TokenType.MINUS: ["ArgList"],

        TokenType.VIDEO_RESIZE: ["ArgList"],
        TokenType.VIDEO_FLIP: ["ArgList"],
        TokenType.VIDEO_VELOCIDAD: ["ArgList"],
        TokenType.VIDEO_FADEIN: ["ArgList"],
        TokenType.VIDEO_FADEOUT: ["ArgList"],
        TokenType.VIDEO_SILENCIO: ["ArgList"],
        TokenType.VIDEO_EXTRAER_AUDIO: ["ArgList"],
        TokenType.VIDEO_QUITAR_AUDIO: ["ArgList"],
        TokenType.VIDEO_AGREGAR_MUSICA: ["ArgList"],
        TokenType.VIDEO_CONCATENAR: ["ArgList"],
        TokenType.VIDEO_CORTAR: ["ArgList"],

        TokenType.RBRACKET: [EPSILON],
    },
    "ArgList": {
        TokenType.IDENTIFIER: ["Expr", "ArgList'"],
        TokenType.INT_LITERAL: ["Expr", "ArgList'"],
        TokenType.FLOAT_LITERAL: ["Expr", "ArgList'"],
        TokenType.STRING_LITERAL: ["Expr", "ArgList'"],
        TokenType.LPAREN: ["Expr", "ArgList'"],
        TokenType.NOT: ["Expr", "ArgList'"],
        TokenType.MINUS: ["Expr", "ArgList'"],

        TokenType.VIDEO_RESIZE: ["Expr", "ArgList'"],
        TokenType.VIDEO_FLIP: ["Expr", "ArgList'"],
        TokenType.VIDEO_VELOCIDAD: ["Expr", "ArgList'"],
        TokenType.VIDEO_FADEIN: ["Expr", "ArgList'"],
        TokenType.VIDEO_FADEOUT: ["Expr", "ArgList'"],
        TokenType.VIDEO_SILENCIO: ["Expr", "ArgList'"],
        TokenType.VIDEO_EXTRAER_AUDIO: ["Expr", "ArgList'"],
        TokenType.VIDEO_QUITAR_AUDIO: ["Expr", "ArgList'"],
        TokenType.VIDEO_AGREGAR_MUSICA: ["Expr", "ArgList'"],
        TokenType.VIDEO_CONCATENAR: ["Expr", "ArgList'"],
        TokenType.VIDEO_CORTAR: ["Expr", "ArgList'"],
    },
    "ArgList'": {
        TokenType.COMMA: [TokenType.COMMA, "Expr", "ArgList'"],
        TokenType.RBRACKET: [EPSILON],
    },
}
