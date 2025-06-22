# parser.py - Versión final corregida
# ----------------------------------------------------------------
from typing import List, Dict, Set
from dataclasses import dataclass
from enums import Token, TokenType, KEYWORDS, symbols, compound_ops
from grammar_def import PARSING_TABLE, START_SYMBOL, EPSILON

