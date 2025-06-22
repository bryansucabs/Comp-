"""Definición de tokens del lenguaje de edición de video.

Este módulo centraliza todas las enumeraciones y tablas de mapeo
utilizadas por el lexer para convertir los lexemas de la entrada en
tipos de token.
"""

import enum
from dataclasses import dataclass


class TokenSpec:
    """Agrupa el enum de todos los tipos de token soportados."""

    class Type(enum.Enum):
        # --- Palabras clave del lenguaje ---
        MAIN = enum.auto()
        IF = enum.auto()
        ELSE = enum.auto()
        WHILE = enum.auto()
        EXPORT = enum.auto()
        AS = enum.auto()

        # — Tipos de datos —
        INT_TYPE = enum.auto()
        FLOAT_TYPE = enum.auto()
        STRING_TYPE = enum.auto()
        VIDEO_TYPE = enum.auto()
        AUDIO_TYPE = enum.auto()

        # — Literales e identificadores —
        INT_LITERAL = enum.auto()
        FLOAT_LITERAL = enum.auto()
        STRING_LITERAL = enum.auto()
        IDENTIFIER = enum.auto()

        # — Operadores lógicos —
        NOT = enum.auto()
        AND = enum.auto()
        OR = enum.auto()

        # — Operadores aritméticos —
        ASSIGN = enum.auto()  # '='
        PLUS = enum.auto()    # '+'
        MINUS = enum.auto()   # '-'
        MULT = enum.auto()    # '*'
        DIV = enum.auto()     # '/'

        # — Comparaciones —
        EQ = enum.auto()   # '=='
        NEQ = enum.auto()  # '!='
        LT = enum.auto()   # '<'
        GT = enum.auto()   # '>'
        LE = enum.auto()   # '<='
        GE = enum.auto()   # '>='

        # — Símbolos —
        LPAREN = enum.auto()
        RPAREN = enum.auto()
        LBRACE = enum.auto()
        RBRACE = enum.auto()
        LBRACKET = enum.auto()
        RBRACKET = enum.auto()
        COMMA = enum.auto()
        SEMICOLON = enum.auto()
        COLON = enum.auto()

        # — Funciones especiales de video —
        VIDEO_RESIZE = enum.auto()
        VIDEO_FLIP = enum.auto()
        VIDEO_VELOCIDAD = enum.auto()
        VIDEO_FADEIN = enum.auto()
        VIDEO_FADEOUT = enum.auto()
        VIDEO_SILENCIO = enum.auto()
        VIDEO_EXTRAER_AUDIO = enum.auto()
        VIDEO_QUITAR_AUDIO = enum.auto()
        VIDEO_AGREGAR_MUSICA = enum.auto()
        VIDEO_CONCATENAR = enum.auto()
        VIDEO_CORTAR = enum.auto()

        # — Especiales —
        EOF = enum.auto()
        ERROR = enum.auto()


# Mapeo único de lexemas a tipos de token. Cada entrada
# relaciona el texto que aparece en el programa con el
# tipo de token que debe generarse.
LEXEME_TO_TOKEN: dict[str, TokenSpec.Type] = {
    # keywords
    "main": TokenSpec.Type.MAIN,
    "if": TokenSpec.Type.IF,
    "else": TokenSpec.Type.ELSE,
    "while": TokenSpec.Type.WHILE,
    "exportar": TokenSpec.Type.EXPORT,
    "como": TokenSpec.Type.AS,

    # tipos
    "int": TokenSpec.Type.INT_TYPE,
    "float": TokenSpec.Type.FLOAT_TYPE,
    "string": TokenSpec.Type.STRING_TYPE,
    "video": TokenSpec.Type.VIDEO_TYPE,
    "audio": TokenSpec.Type.AUDIO_TYPE,

    # literales lógicos
    "not": TokenSpec.Type.NOT,
    "and": TokenSpec.Type.AND,
    "or": TokenSpec.Type.OR,

    # operadores compuestos
    "==": TokenSpec.Type.EQ,
    "!=": TokenSpec.Type.NEQ,
    "<=": TokenSpec.Type.LE,
    ">=": TokenSpec.Type.GE,

    # operadores y símbolos simples
    "=": TokenSpec.Type.ASSIGN,
    "+": TokenSpec.Type.PLUS,
    "-": TokenSpec.Type.MINUS,
    "*": TokenSpec.Type.MULT,
    "/": TokenSpec.Type.DIV,
    "<": TokenSpec.Type.LT,
    ">": TokenSpec.Type.GT,
    ":": TokenSpec.Type.COLON,
    ",": TokenSpec.Type.COMMA,
    "{": TokenSpec.Type.LBRACE,
    "}": TokenSpec.Type.RBRACE,
    "[": TokenSpec.Type.LBRACKET,
    "]": TokenSpec.Type.RBRACKET,
    "(": TokenSpec.Type.LPAREN,
    ")": TokenSpec.Type.RPAREN,
    ";": TokenSpec.Type.SEMICOLON,

    # video-funciones
    "@resize": TokenSpec.Type.VIDEO_RESIZE,
    "@flip": TokenSpec.Type.VIDEO_FLIP,
    "@velocidad": TokenSpec.Type.VIDEO_VELOCIDAD,
    "@fadein": TokenSpec.Type.VIDEO_FADEIN,
    "@fadeout": TokenSpec.Type.VIDEO_FADEOUT,
    "@silencio": TokenSpec.Type.VIDEO_SILENCIO,
    "@extraer_audio": TokenSpec.Type.VIDEO_EXTRAER_AUDIO,
    "@quitar_audio": TokenSpec.Type.VIDEO_QUITAR_AUDIO,
    "@agregar_musica": TokenSpec.Type.VIDEO_AGREGAR_MUSICA,
    "@concatenar": TokenSpec.Type.VIDEO_CONCATENAR,
    "@cortar": TokenSpec.Type.VIDEO_CORTAR,
}

# Representación de un token individual producido por el lexer.
@dataclass(frozen=True)
class Token:
    type: TokenSpec.Type
    value: str
    line: int
    column: int

    def __str__(self) -> str:
        return f"{self.type.name:20} [ {self.value} ] -> {self.line}:{self.column}"


# Alias para facilitar el acceso desde otros módulos
TokenType = TokenSpec.Type

# Tablas derivadas útiles para el lexer
# Conjuntos de palabras clave y operadores, extraídos del diccionario
# principal para una búsqueda rápida.
KEYWORDS = {k: v for k, v in LEXEME_TO_TOKEN.items() if k.isalpha()}
compound_ops = {
    k: v
    for k, v in LEXEME_TO_TOKEN.items()
    if len(k) == 2 and not k.isalpha() and not k.startswith('@')
}

# Símbolos de un solo carácter que representan paréntesis, llaves, etc.
symbols = {
    k: v
    for k, v in LEXEME_TO_TOKEN.items()
    if len(k) == 1 and not k.isalnum()
}

# Funciones de video que comienzan con '@'
VIDEO_FUNCS = {k: v for k, v in LEXEME_TO_TOKEN.items() if k.startswith('@')}
