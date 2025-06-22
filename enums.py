import enum
from dataclasses import dataclass

class TokenSpec:
    class Type(enum.Enum):
        # ---------- Palabras clave ----------
        MAIN   = "main"
        IF     = "if"
        ELSE   = "else"
        WHILE  = "while"
        EXPORT = "exportar"
        AS     = "como"

        # ---------- Tipos (solo los necesarios) ----------
        STRING_TYPE = "string"
        FLOAT_TYPE  = "float"
        INT_TYPE    = "int"
        VIDEO_TYPE  = "video"
        AUDIO_TYPE  = "audio"

        # ---------- Operadores lógicos ----------
        NOT = "not"
        AND = "and"
        OR  = "or"

        # ---------- Operadores matemáticos ----------
        CONCAT = "++"
        ASSIGN = "="
        PLUS   = "+"
        MINUS  = "-"
        MULT   = "*"
        DIV    = "/"
        CONCAT = "++"

        # ---------- Comparaciones ----------
        EQ   = "=="
        NEQ  = "!="
        LT   = "<"
        GT   = ">"
        LE   = "<="
        GE   = ">="

        # ---------- Símbolos ----------
        COMMENT = "//"
        LPAREN    = "("
        RPAREN    = ")"
        LBRACE    = "{"
        RBRACE    = "}"
        LBRACKET  = "["
        RBRACKET  = "]"
        COMMA     = ","
        SEMICOLON = ";"
        COLON     = ":"

        # ---------- Identificadores y literales ----------
        IDENTIFIER     = "identifier"
        INT_LITERAL    = "int_literal"
        FLOAT_LITERAL  = "float_literal"
        STRING_LITERAL = "string_literal"

        # ---------- Funciones especiales de video ----------
        VIDEO_RESIZE         = "@resize"
        VIDEO_FLIP           = "@flip"
        VIDEO_VELOCIDAD      = "@velocidad"
        VIDEO_FADEIN         = "@fadein"
        VIDEO_FADEOUT        = "@fadeout"
        VIDEO_SILENCIO       = "@silencio"
        VIDEO_EXTRAER_AUDIO  = "@extraer_audio"
        VIDEO_QUITAR_AUDIO   = "@quitar_audio"
        VIDEO_AGREGAR_MUSICA = "@agregar_musica"
        VIDEO_CONCATENAR     = "@concatenar"
        VIDEO_CORTAR         = "@cortar"

        # ---------- Especiales ----------
        EOF   = "eof"
        ERROR = "error"

@dataclass
class Token:
    type: TokenSpec.Type
    value: str
    line: int
    column: int

    def __str__(self) -> str:
        return f"{self.type.name:20} [ {self.value} ] -> {self.line}:{self.column}"
