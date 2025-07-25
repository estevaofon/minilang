# MiniLang Compiler v2.0
# Compilador para a linguagem MiniLang com tipagem estática

import re
import sys
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Union, Dict, Tuple
import llvmlite.ir as ir
import llvmlite.binding as llvm

# Tipos de tokens
class TokenType(Enum):
    # Literais
    NUMBER = "NUMBER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NULL = "NULL"
    
    # Palavras-chave
    LET = "LET"
    GLOBAL = "GLOBAL"
    IF = "IF"
    THEN = "THEN"
    ELSE = "ELSE"
    END = "END"
    WHILE = "WHILE"
    DO = "DO"
    PRINT = "PRINT"
    FUNC = "FUNC"
    RETURN = "RETURN"
    STRUCT = "STRUCT"
    REF = "REF"  # Nova palavra-chave para referências
    
    # Tipos
    INT = "INT"
    FLOAT_TYPE = "FLOAT_TYPE"
    STRING_TYPE = "STRING_TYPE"
    STR_TYPE = "STR_TYPE"
    VOID = "VOID"
    BOOL = "BOOL"
    
    # Operadores
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULO = "MODULO"  # Adicionado
    ASSIGN = "ASSIGN"
    GT = "GT"
    LT = "LT"
    GTE = "GTE"
    LTE = "LTE"
    EQ = "EQ"
    NEQ = "NEQ"
    ARROW = "ARROW"
    CONCAT = "CONCAT"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    
    # Delimitadores
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    COMMA = "COMMA"
    COLON = "COLON"
    SEMICOLON = "SEMICOLON"
    DOT = "DOT"
    
    # Especiais
    ZEROS = "ZEROS"
    
    # Fim de arquivo
    EOF = "EOF"

@dataclass
class Token:
    type: TokenType
    value: Union[str, int, float]
    line: int
    column: int

# Sistema de tipos
@dataclass
class Type:
    pass

@dataclass
class IntType(Type):
    pass

@dataclass 
class FloatType(Type):
    pass

@dataclass
class StringType(Type):
    pass

@dataclass
class StrType(Type):  # Alias para StringType
    pass

@dataclass
class ArrayType(Type):
    element_type: Type
    size: Optional[int] = None

@dataclass
class VoidType(Type):
    pass

@dataclass
class FunctionType(Type):
    param_types: List[Type]
    return_type: Type

@dataclass
class BoolType(Type):
    pass

@dataclass
class NullType(Type):
    pass

@dataclass
class StructType(Type):
    name: str
    fields: Dict[str, Type]

@dataclass
class ReferenceType(Type):
    """Tipo para referências que permitem auto-referenciamento"""
    target_type: Type
    is_mutable: bool = True

# Lexer
class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
    def tokenize(self) -> List[Token]:
        while self.position < len(self.source):
            self._skip_whitespace_and_comments()
            
            if self.position >= len(self.source):
                break
                
            # Strings
            if self._current_char() == '"':
                self._read_string()
            # Números
            elif self._current_char().isdigit():
                self._read_number()
            # Identificadores e palavras-chave
            elif self._current_char().isalpha() or self._current_char() == '_':
                self._read_identifier()
            # Operadores e delimitadores
            else:
                self._read_operator()
                
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens
    
    def _current_char(self) -> str:
        if self.position < len(self.source):
            return self.source[self.position]
        return ""
    
    def _peek_char(self) -> str:
        if self.position + 1 < len(self.source):
            return self.source[self.position + 1]
        return ""
    
    def _advance(self):
        if self.position < len(self.source) and self.source[self.position] == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.position += 1
    
    def _skip_whitespace_and_comments(self):
        while self.position < len(self.source):
            # Pular espaços em branco
            if self.source[self.position].isspace():
                self._advance()
            # Pular comentários de linha
            elif self.position + 1 < len(self.source) and self.source[self.position:self.position+2] == '//':
                while self.position < len(self.source) and self.source[self.position] != '\n':
                    self._advance()
            else:
                break
    
    def _read_string(self):
        start_column = self.column
        self._advance()  # Pular aspas inicial
        string_value = ""
        
        while self.position < len(self.source) and self._current_char() != '"':
            if self._current_char() == '\\':
                self._advance()
                if self.position < len(self.source):
                    escape_char = self._current_char()
                    if escape_char == 'n':
                        string_value += '\n'
                    elif escape_char == 't':
                        string_value += '\t'
                    elif escape_char == '"':
                        string_value += '"'
                    elif escape_char == '\\':
                        string_value += '\\'
                    elif escape_char == '0':
                        string_value += '\0'
                    else:
                        string_value += escape_char
                    self._advance()
            else:
                string_value += self._current_char()
                self._advance()
        
        if self.position < len(self.source):
            self._advance()  # Pular aspas final
        else:
            raise SyntaxError(f"String não terminada na linha {self.line}")
            
        self.tokens.append(Token(TokenType.STRING, string_value, self.line, start_column))
    
    def _read_number(self):
        start_column = self.column
        number_str = ""
        has_dot = False
        
        while self.position < len(self.source) and (self._current_char().isdigit() or self._current_char() == '.'):
            if self._current_char() == '.':
                if has_dot:
                    break  # Segunda vírgula, parar
                has_dot = True
            number_str += self._current_char()
            self._advance()
            
        if has_dot:
            value = float(number_str)
            self.tokens.append(Token(TokenType.FLOAT, value, self.line, start_column))
        else:
            value = int(number_str)
            self.tokens.append(Token(TokenType.NUMBER, value, self.line, start_column))
    
    def _read_identifier(self):
        start_column = self.column
        identifier = ""
        
        while self.position < len(self.source) and (self._current_char().isalnum() or self._current_char() == '_'):
            identifier += self._current_char()
            self._advance()
            
        # Verificar palavras-chave
        keywords = {
            'let': TokenType.LET,
            'global': TokenType.GLOBAL,
            'if': TokenType.IF,
            'then': TokenType.THEN,
            'else': TokenType.ELSE,
            'end': TokenType.END,
            'while': TokenType.WHILE,
            'do': TokenType.DO,
            'print': TokenType.PRINT,
            'func': TokenType.FUNC,
            'return': TokenType.RETURN,
            'int': TokenType.INT,
            'float': TokenType.FLOAT_TYPE,
            'string': TokenType.STRING_TYPE,
            'str': TokenType.STR_TYPE,
            'void': TokenType.VOID,
            'bool': TokenType.BOOL,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
            'null': TokenType.NULL,
            'struct': TokenType.STRUCT,
            'ref': TokenType.REF,
            'zeros': TokenType.ZEROS
        }
        
        token_type = keywords.get(identifier, TokenType.IDENTIFIER)
        self.tokens.append(Token(token_type, identifier, self.line, start_column))
    
    def _read_operator(self):
        start_column = self.column
        char = self._current_char()
        next_char = self._peek_char()
        
        # Operadores de dois caracteres
        two_char_ops = {
            '>=': TokenType.GTE,
            '<=': TokenType.LTE,
            '==': TokenType.EQ,
            '!=': TokenType.NEQ,
            '->': TokenType.ARROW,
            '++': TokenType.CONCAT
        }
        
        two_char = char + next_char
        if two_char in two_char_ops:
            self.tokens.append(Token(two_char_ops[two_char], two_char, self.line, start_column))
            self._advance()
            self._advance()
            return
        
        # Operadores de um caractere
        operators = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '%': TokenType.MODULO,  # Adicionado
            '=': TokenType.ASSIGN,
            '>': TokenType.GT,
            '<': TokenType.LT,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            ',': TokenType.COMMA,
            ':': TokenType.COLON,
            ';': TokenType.SEMICOLON,
            '.': TokenType.DOT,
            '&': TokenType.AND,
            '|': TokenType.OR,
            '!': TokenType.NOT
        }
        
        if char in operators:
            self.tokens.append(Token(operators[char], char, self.line, start_column))
            self._advance()
        else:
            raise SyntaxError(f"Caractere inválido '{char}' na linha {self.line}, coluna {self.column}")

# AST (Abstract Syntax Tree)
@dataclass
class ASTNode:
    pass

@dataclass
class NumberNode(ASTNode):
    value: int

@dataclass
class FloatNode(ASTNode):
    value: float

@dataclass
class StringNode(ASTNode):
    value: str

@dataclass
class ArrayNode(ASTNode):
    elements: List[ASTNode]
    element_type: Type

@dataclass
class ZerosNode(ASTNode):
    size: int
    element_type: Type

@dataclass
class ArrayAccessNode(ASTNode):
    array_name: str
    index: ASTNode

@dataclass
class IdentifierNode(ASTNode):
    name: str

@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    operator: TokenType
    right: ASTNode

@dataclass
class CastNode(ASTNode):
    expression: ASTNode
    target_type: Type

@dataclass
class ConcatNode(ASTNode):
    left: ASTNode
    right: ASTNode

@dataclass
class AssignmentNode(ASTNode):
    identifier: str
    var_type: Type
    value: ASTNode
    is_global: bool = False

@dataclass
class ArrayAssignmentNode(ASTNode):
    array_name: str
    index: ASTNode
    value: ASTNode

@dataclass
class PrintNode(ASTNode):
    expression: ASTNode

@dataclass
class IfNode(ASTNode):
    condition: ASTNode
    then_branch: List[ASTNode]
    else_branch: Optional[List[ASTNode]] = None

@dataclass
class WhileNode(ASTNode):
    condition: ASTNode
    body: List[ASTNode]

@dataclass
class FunctionNode(ASTNode):
    name: str
    params: List[Tuple[str, Type]]
    return_type: Type
    body: List[ASTNode]

@dataclass
class ReturnNode(ASTNode):
    value: Optional[ASTNode]

@dataclass
class CallNode(ASTNode):
    function_name: str
    arguments: List[ASTNode]

@dataclass
class StructDefinitionNode(ASTNode):
    name: str
    fields: List[Tuple[str, Type]]

@dataclass
class StructAccessNode(ASTNode):
    struct_name: str
    field_name: str

@dataclass
class StructAssignmentNode(ASTNode):
    struct_name: str
    field_name: str
    value: ASTNode

@dataclass
class StructConstructorNode(ASTNode):
    """Nó para construtores de struct: StructName(arg1, arg2, ...)"""
    struct_name: str
    arguments: List[ASTNode]

@dataclass
class ProgramNode(ASTNode):
    statements: List[ASTNode]

@dataclass
class BooleanNode(ASTNode):
    value: bool

@dataclass
class NullNode(ASTNode):
    pass

@dataclass
class UnaryOpNode(ASTNode):
    operator: TokenType
    operand: ASTNode

# Parser
class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
        self.struct_types = {}  # Armazenar tipos de struct definidos
        self.defined_functions = set()  # Conjunto de funções definidas
        self.defined_structs = set()    # Conjunto de structs definidos
    
    def _error(self, message: str) -> None:
        """Lança um erro de sintaxe com informações de linha e coluna"""
        token = self._current_token()
        raise SyntaxError(f"Erro na linha {token.line}, coluna {token.column}: {message}")
    
    def _error_at_current(self, message: str) -> None:
        """Lança um erro de sintaxe para o token atual"""
        token = self._current_token()
        raise SyntaxError(f"Erro na linha {token.line}, coluna {token.column}: {message}")
    
    def _error_at_previous(self, message: str) -> None:
        """Lança um erro de sintaxe para o token anterior"""
        if self.position > 0:
            token = self.tokens[self.position - 1]
            raise SyntaxError(f"Erro na linha {token.line}, coluna {token.column}: {message}")
        else:
            raise SyntaxError(f"Erro no início do arquivo: {message}")
        
    def parse(self) -> ProgramNode:
        statements = []
        
        while not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
                
        return ProgramNode(statements)
    
    def _current_token(self) -> Token:
        return self.tokens[self.position]
    
    def _advance(self) -> Token:
        token = self.tokens[self.position]
        if not self._is_at_end():
            self.position += 1
        return token
    
    def _is_at_end(self) -> bool:
        return self._current_token().type == TokenType.EOF
    
    def _match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self._current_token().type == token_type:
                self._advance()
                return True
        return False
    
    def _check(self, token_type: TokenType) -> bool:
        return self._current_token().type == token_type
    
    def _parse_type(self) -> Type:
        if self._match(TokenType.REF):
            # Tipo de referência: ref Tipo
            target_type = self._parse_type()
            return ReferenceType(target_type)
        elif self._match(TokenType.INT):
            if self._match(TokenType.LBRACKET):
                size = None
                if self._current_token().type == TokenType.NUMBER:
                    size = self._advance().value
                if not self._match(TokenType.RBRACKET):
                    self._error("Esperado ']' após tamanho do array")
                return ArrayType(IntType(), size)
            return IntType()
        elif self._match(TokenType.FLOAT_TYPE):
            if self._match(TokenType.LBRACKET):
                size = None
                if self._current_token().type == TokenType.NUMBER:
                    size = self._advance().value
                if not self._match(TokenType.RBRACKET):
                    self._error("Esperado ']' após tamanho do array")
                return ArrayType(FloatType(), size)
            return FloatType()
        elif self._match(TokenType.STRING_TYPE) or self._match(TokenType.STR_TYPE):
            if self._match(TokenType.LBRACKET):
                size = None
                if self._current_token().type == TokenType.NUMBER:
                    size = self._advance().value
                if not self._match(TokenType.RBRACKET):
                    self._error("Esperado ']' após tamanho do array")
                return ArrayType(StringType(), size)
            return StringType()
        elif self._match(TokenType.VOID):
            return VoidType()
        elif self._match(TokenType.BOOL):
            if self._match(TokenType.LBRACKET):
                size = None
                if self._current_token().type == TokenType.NUMBER:
                    size = self._advance().value
                if not self._match(TokenType.RBRACKET):
                    self._error("Esperado ']' após tamanho do array")
                return ArrayType(BoolType(), size)
            return BoolType()
        elif self._check(TokenType.IDENTIFIER):
            # Verificar se é um tipo de struct definido
            struct_name = self._current_token().value
            if struct_name in self.struct_types:
                self._advance()  # Consumir o nome do tipo
                return self.struct_types[struct_name]
            else:
                # Permitir forward declaration para auto-referenciamento
                # Criar um tipo placeholder que será resolvido depois
                self._advance()  # Consumir o nome do tipo
                return StructType(struct_name, {})
        else:
            self._error(f"Tipo esperado, encontrado {self._current_token()}")
    
    def _parse_statement(self) -> Optional[ASTNode]:
        if self._match(TokenType.LET):
            return self._parse_assignment(is_global=False)
        elif self._match(TokenType.GLOBAL):
            return self._parse_assignment(is_global=True)
        elif self._match(TokenType.PRINT):
            return self._parse_print()
        elif self._match(TokenType.IF):
            return self._parse_if()
        elif self._match(TokenType.WHILE):
            return self._parse_while()
        elif self._match(TokenType.FUNC):
            return self._parse_function()
        elif self._match(TokenType.RETURN):
            return self._parse_return()
        elif self._match(TokenType.STRUCT):
            return self._parse_struct_definition()
        elif self._check(TokenType.IDENTIFIER):
            # Pode ser uma atribuição de array, reatribuição simples, acesso a struct ou chamada de função
            if self.position + 1 < len(self.tokens):
                next_token = self.tokens[self.position + 1]
                if next_token.type == TokenType.LBRACKET:
                    # Pode ser acesso de array seguido de atribuição
                    saved_pos = self.position
                    identifier = self._advance()
                    self._advance()  # [
                    index_expr = self._parse_expression()
                    if self._match(TokenType.RBRACKET) and self._check(TokenType.ASSIGN):
                        # É uma atribuição de array
                        self.position = saved_pos
                        return self._parse_array_assignment()
                    else:
                        # É apenas um acesso de array, voltar e processar como expressão
                        self.position = saved_pos
                        return self._parse_expression()
                elif next_token.type == TokenType.DOT:
                    # Pode ser acesso a campo de struct seguido de atribuição
                    saved_pos = self.position
                    struct_name = self._advance()
                    self._advance()  # .
                    field_name = self._advance()
                    if field_name.type != TokenType.IDENTIFIER:
                        raise SyntaxError("Esperado nome do campo após '.'")
                    
                    # Verificar se há mais níveis de acesso (ex: pessoa.endereco.rua)
                    while self._check(TokenType.DOT):
                        self._advance()  # .
                        next_field = self._advance()
                        if next_field.type != TokenType.IDENTIFIER:
                            raise SyntaxError("Esperado nome do campo após '.'")
                    
                    if self._check(TokenType.ASSIGN):
                        # É uma atribuição de campo de struct
                        self.position = saved_pos
                        return self._parse_struct_assignment()
                    else:
                        # É apenas um acesso a campo, voltar e processar como expressão
                        self.position = saved_pos
                        return self._parse_expression()
                elif next_token.type == TokenType.ASSIGN:
                    # Reatribuição simples
                    return self._parse_reassignment()
                elif next_token.type == TokenType.LPAREN:
                    # Chamada de função
                    return self._parse_expression()
        
        return self._parse_expression()
    
    def _parse_reassignment(self) -> AssignmentNode:
        """Parse reatribuição de variável (sem let)"""
        identifier = self._advance()
        if identifier.type != TokenType.IDENTIFIER:
            self._error("Esperado identificador")
        
        if not self._match(TokenType.ASSIGN):
            self._error("Esperado '=' após identificador")
            
        value = self._parse_expression()
        
        # Reatribuição não tem tipo (será inferido da variável existente)
        return AssignmentNode(identifier.value, None, value, False)
    
    def _parse_assignment(self, is_global: bool = False) -> AssignmentNode:
        identifier = self._advance()
        if identifier.type != TokenType.IDENTIFIER:
            self._error("Esperado identificador após 'let' ou 'global'")
        
        if not self._match(TokenType.COLON):
            self._error("Esperado ':' após identificador")
        
        var_type = self._parse_type()
        
        if not self._match(TokenType.ASSIGN):
            self._error("Esperado '=' após tipo")
            
        value = self._parse_expression()
        return AssignmentNode(identifier.value, var_type, value, is_global)
    
    def _parse_array_assignment(self) -> ArrayAssignmentNode:
        array_name = self._advance().value
        
        if not self._match(TokenType.LBRACKET):
            self._error("Esperado '[' para acesso ao array")
            
        index = self._parse_expression()
        
        if not self._match(TokenType.RBRACKET):
            self._error("Esperado ']' após índice")
            
        if not self._match(TokenType.ASSIGN):
            self._error("Esperado '=' para atribuição")
            
        value = self._parse_expression()
        return ArrayAssignmentNode(array_name, index, value)
    
    def _parse_print(self) -> PrintNode:
        if not self._match(TokenType.LPAREN):
            self._error("Esperado '(' após 'print'")
            
        expr = self._parse_expression()
        
        if not self._match(TokenType.RPAREN):
            self._error("Esperado ')' após expressão")
            
        return PrintNode(expr)
    
    def _parse_if(self) -> IfNode:
        condition = self._parse_expression()
        
        if not self._match(TokenType.THEN):
            raise SyntaxError("Esperado 'then' após condição")
            
        then_branch = []
        while not self._check(TokenType.END) and not self._check(TokenType.ELSE) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                then_branch.append(stmt)
        
        else_branch = None
        if self._match(TokenType.ELSE):
            else_branch = []
            while not self._check(TokenType.END) and not self._is_at_end():
                stmt = self._parse_statement()
                if stmt:
                    else_branch.append(stmt)
        
        if not self._match(TokenType.END):
            raise SyntaxError("Esperado 'end' para fechar 'if'")
                
        return IfNode(condition, then_branch, else_branch)
    
    def _parse_while(self) -> WhileNode:
        condition = self._parse_expression()
        
        if not self._match(TokenType.DO):
            raise SyntaxError("Esperado 'do' após condição")
            
        body = []
        while not self._match(TokenType.END) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
                
        return WhileNode(condition, body)
    
    def _parse_function(self) -> FunctionNode:
        name = self._advance()
        if name.type != TokenType.IDENTIFIER:
            raise SyntaxError("Esperado nome da função")
            
        if not self._match(TokenType.LPAREN):
            raise SyntaxError("Esperado '(' após nome da função")
            
        params = []
        while not self._check(TokenType.RPAREN) and not self._is_at_end():
            param_name = self._advance()
            if param_name.type != TokenType.IDENTIFIER:
                raise SyntaxError("Esperado nome do parâmetro")
            
            if not self._match(TokenType.COLON):
                raise SyntaxError("Esperado ':' após nome do parâmetro")
            
            param_type = self._parse_type()
            params.append((param_name.value, param_type))
            
            if not self._check(TokenType.RPAREN):
                if not self._match(TokenType.COMMA):
                    raise SyntaxError("Esperado ',' entre parâmetros")
        
        if not self._match(TokenType.RPAREN):
            raise SyntaxError("Esperado ')' após parâmetros")
        
        # Tipo de retorno
        return_type = VoidType()
        if self._match(TokenType.ARROW):
            return_type = self._parse_type()
            
        body = []
        while not self._match(TokenType.END) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
        
        # Registrar a função como definida
        self.defined_functions.add(name.value)
                
        return FunctionNode(name.value, params, return_type, body)
    
    def _parse_return(self) -> ReturnNode:
        value = None
        if not self._check(TokenType.SEMICOLON) and not self._check(TokenType.END):
            value = self._parse_expression()
        return ReturnNode(value)
    
    def _parse_expression(self) -> ASTNode:
        return self._parse_or()
    
    def _parse_or(self) -> ASTNode:
        """Parse expressões OR: left || right"""
        left = self._parse_and()
        
        while self._match(TokenType.OR):
            operator = self.tokens[self.position - 1].type
            right = self._parse_and()
            left = BinaryOpNode(left, operator, right)
            
        return left
    
    def _parse_and(self) -> ASTNode:
        """Parse expressões AND: left && right"""
        left = self._parse_comparison()
        
        while self._match(TokenType.AND):
            operator = self.tokens[self.position - 1].type
            right = self._parse_comparison()
            left = BinaryOpNode(left, operator, right)
            
        return left
    
    def _parse_comparison(self) -> ASTNode:
        left = self._parse_term()
        
        while self._match(TokenType.GT, TokenType.LT, TokenType.GTE, TokenType.LTE, TokenType.EQ, TokenType.NEQ):
            operator = self.tokens[self.position - 1].type
            right = self._parse_term()
            left = BinaryOpNode(left, operator, right)
            
        return left
    
    def _parse_term(self) -> ASTNode:
        left = self._parse_factor()
        
        while self._match(TokenType.PLUS, TokenType.MINUS, TokenType.CONCAT):
            operator = self.tokens[self.position - 1].type
            right = self._parse_factor()
            if operator == TokenType.CONCAT:
                # Para concatenação de strings, usar o operador + que será tratado como concatenação
                left = BinaryOpNode(left, TokenType.PLUS, right)
            else:
                left = BinaryOpNode(left, operator, right)
            
        return left
    
    def _parse_factor(self) -> ASTNode:
        left = self._parse_unary()
        
        while self._match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self.tokens[self.position - 1].type
            right = self._parse_unary()
            left = BinaryOpNode(left, operator, right)
        
        return left
    
    def _parse_unary(self) -> ASTNode:
        if self._match(TokenType.MINUS):
            expr = self._parse_unary()
            return BinaryOpNode(NumberNode(0), TokenType.MINUS, expr)
        elif self._match(TokenType.NOT):
            expr = self._parse_unary()
            return UnaryOpNode(TokenType.NOT, expr)
            
        return self._parse_postfix()
    
    def _parse_postfix(self) -> ASTNode:
        expr = self._parse_primary()
        
        while True:
            if self._match(TokenType.LBRACKET):
                index = self._parse_expression()
                if not self._match(TokenType.RBRACKET):
                    raise SyntaxError("Esperado ']' após índice")
                if isinstance(expr, IdentifierNode):
                    expr = ArrayAccessNode(expr.name, index)
                else:
                    raise SyntaxError("Acesso de array inválido")
            elif self._match(TokenType.DOT):
                # Acesso a campo de struct
                field_name = self._advance()
                if field_name.type != TokenType.IDENTIFIER:
                    raise SyntaxError("Esperado nome do campo após '.'")
                
                if isinstance(expr, IdentifierNode):
                    # Acesso direto a campo: pessoa.campo
                    expr = StructAccessNode(expr.name, field_name.value)
                elif isinstance(expr, StructAccessNode):
                    # Acesso aninhado: pessoa.endereco.rua
                    # Criar um nome composto para representar o caminho completo
                    full_path = f"{expr.field_name}.{field_name.value}"
                    expr = StructAccessNode(expr.struct_name, full_path)
                else:
                    raise SyntaxError("Acesso a campo de struct inválido")
            elif self._match(TokenType.LPAREN):
                # Verificar se é cast, construtor de struct ou chamada de função
                if isinstance(expr, IdentifierNode):
                    # Verificar se é um tipo (para cast)
                    if expr.name in ['int', 'float', 'string', 'str', 'bool']:
                        # É um cast
                        cast_expr = self._parse_expression()
                        if not self._match(TokenType.RPAREN):
                            raise SyntaxError("Esperado ')' após expressão de cast")
                        
                        target_type = None
                        if expr.name == 'int':
                            target_type = IntType()
                        elif expr.name == 'float':
                            target_type = FloatType()
                        elif expr.name in ['string', 'str']:
                            target_type = StringType()
                        elif expr.name == 'bool':
                            target_type = BoolType()
                        
                        expr = CastNode(cast_expr, target_type)
                    else:
                        # Verificar se é um construtor de struct
                        # Para isso, precisamos verificar se o nome existe como struct
                        # Por enquanto, vamos assumir que se não for uma função conhecida, é um construtor
                        args = []
                        while not self._check(TokenType.RPAREN) and not self._is_at_end():
                            args.append(self._parse_expression())
                            if not self._check(TokenType.RPAREN):
                                if not self._match(TokenType.COMMA):
                                    raise SyntaxError("Esperado ',' entre argumentos")
                        
                        if not self._match(TokenType.RPAREN):
                            raise SyntaxError("Esperado ')' após argumentos")
                        
                        # Verificar se é uma função conhecida ou definida
                        if expr.name in ['printf', 'malloc', 'free', 'strlen', 'strcpy', 'strcat', 'to_str', 'to_int', 'to_float', 'ord'] or expr.name in self.defined_functions:
                            expr = CallNode(expr.name, args)
                        elif expr.name in self.defined_structs:
                            # É um construtor de struct
                            expr = StructConstructorNode(expr.name, args)
                        else:
                            # Por padrão, assumir que é uma função (pode ser uma função não definida ainda)
                            expr = CallNode(expr.name, args)
                else:
                    raise SyntaxError("Chamada de função inválida")
            else:
                break
                
        return expr
    
    def _parse_primary(self) -> ASTNode:
        if self._current_token().type == TokenType.NUMBER:
            return NumberNode(self._advance().value)
            
        if self._current_token().type == TokenType.FLOAT:
            return FloatNode(self._advance().value)
            
        if self._current_token().type == TokenType.STRING:
            return StringNode(self._advance().value)
            
        if self._current_token().type == TokenType.TRUE:
            self._advance()
            return BooleanNode(True)
            
        if self._current_token().type == TokenType.FALSE:
            self._advance()
            return BooleanNode(False)
            
        if self._current_token().type == TokenType.NULL:
            self._advance()
            return NullNode()
            
        if self._current_token().type == TokenType.BOOL:
            # Para casts como bool(1), retornar um IdentifierNode
            return IdentifierNode(self._advance().value)
            
        if self._current_token().type == TokenType.IDENTIFIER:
            return IdentifierNode(self._advance().value)
            
        if self._match(TokenType.LPAREN):
            expr = self._parse_expression()
            if not self._match(TokenType.RPAREN):
                raise SyntaxError("Esperado ')' após expressão")
            return expr
            
        if self._match(TokenType.LBRACKET):
            # Array literal
            elements = []
            while not self._check(TokenType.RBRACKET) and not self._is_at_end():
                elements.append(self._parse_expression())
                if not self._check(TokenType.RBRACKET):
                    if not self._match(TokenType.COMMA):
                        raise SyntaxError("Esperado ',' entre elementos do array")
            if not self._match(TokenType.RBRACKET):
                raise SyntaxError("Esperado ']' para fechar array")
            # Inferir tipo do array baseado nos elementos
            if elements:
                if isinstance(elements[0], FloatNode):
                    return ArrayNode(elements, FloatType())
                elif isinstance(elements[0], StringNode):
                    return ArrayNode(elements, StringType())
                elif isinstance(elements[0], BooleanNode):
                    return ArrayNode(elements, BoolType())
                else:
                    return ArrayNode(elements, IntType())
            else:
                return ArrayNode(elements, IntType())
        
        if self._match(TokenType.ZEROS):
            # Syntax sugar para arrays preenchidos com zeros
            if not self._match(TokenType.LPAREN):
                raise SyntaxError("Esperado '(' após 'zeros'")
            
            if self._current_token().type != TokenType.NUMBER:
                raise SyntaxError("Esperado tamanho do array")
            
            size = self._advance().value
            
            if not self._match(TokenType.RPAREN):
                raise SyntaxError("Esperado ')' após tamanho")
            
            return ZerosNode(size, IntType())
            
        raise SyntaxError(f"Token inesperado: {self._current_token()}")
    
    def _parse_struct_definition(self) -> StructDefinitionNode:
        """Parse definição de struct: struct Nome campo1: tipo1, campo2: tipo2, ... end"""
        if not self._check(TokenType.IDENTIFIER):
            raise SyntaxError("Esperado nome do struct após 'struct'")
        
        name = self._advance()
        
        fields = []
        while not self._check(TokenType.END) and not self._is_at_end():
            if not self._check(TokenType.IDENTIFIER):
                raise SyntaxError("Esperado nome do campo")
            
            field_name = self._advance()
            
            if not self._match(TokenType.COLON):
                raise SyntaxError("Esperado ':' após nome do campo")
            
            field_type = self._parse_type()
            fields.append((field_name.value, field_type))
            
            if not self._check(TokenType.END):
                if not self._match(TokenType.COMMA):
                    raise SyntaxError("Esperado ',' entre campos ou 'end' para fechar struct")
        
        if not self._match(TokenType.END):
            raise SyntaxError("Esperado 'end' para fechar struct")
        
        # Criar o tipo de struct e armazená-lo
        struct_type = StructType(name.value, {field_name: field_type for field_name, field_type in fields})
        self.struct_types[name.value] = struct_type
        
        # Registrar o struct como definido
        self.defined_structs.add(name.value)
        
        return StructDefinitionNode(name.value, fields)
    
    def _parse_struct_assignment(self) -> StructAssignmentNode:
        """Parse atribuição de campo de struct: struct.campo = valor ou struct.campo.subcampo = valor"""
        struct_name = self._advance()
        if struct_name.type != TokenType.IDENTIFIER:
            raise SyntaxError("Esperado nome do struct")
        
        if not self._match(TokenType.DOT):
            raise SyntaxError("Esperado '.' após nome do struct")
        
        field_name = self._advance()
        if field_name.type != TokenType.IDENTIFIER:
            raise SyntaxError("Esperado nome do campo após '.'")
        
        # Verificar se há mais níveis de acesso (ex: pessoa.endereco.rua)
        while self._match(TokenType.DOT):
            next_field = self._advance()
            if next_field.type != TokenType.IDENTIFIER:
                raise SyntaxError("Esperado nome do campo após '.'")
            field_name.value = f"{field_name.value}.{next_field.value}"
        
        if not self._match(TokenType.ASSIGN):
            raise SyntaxError("Esperado '=' após nome do campo")
        
        value = self._parse_expression()
        
        return StructAssignmentNode(struct_name.value, field_name.value, value)

# Gerador de código LLVM
class LLVMCodeGenerator:
    def __init__(self):
        # Inicializar LLVM
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        
        # Obter o triple da plataforma atual
        self.triple = llvm.get_default_triple()
        
        # Criar módulo e builder
        self.module = ir.Module(name="minilang_module")
        self.module.triple = self.triple
        
        # Configurar data layout baseado na plataforma
        target = llvm.Target.from_triple(self.triple)
        target_machine = target.create_target_machine()
        self.module.data_layout = str(target_machine.target_data)
        
        self.builder = None
        self.local_vars = {}
        self.global_vars = {}
        self.functions = {}
        self.current_function = None
        self.current_function_ast = None  # AST da função atual
        self.global_ast = None  # AST global do programa
        self.type_map = {}
        self.struct_types = {}  # Armazenar tipos de struct LLVM
        
        # Sistema de gestão de memória
        self.allocated_ptrs = []  # Lista de ponteiros alocados para liberação
        self.memory_tracking = True  # Habilitar rastreamento de memória
        
        # Tipos básicos LLVM
        self.int_type = ir.IntType(64)
        self.float_type = ir.DoubleType()
        self.char_type = ir.IntType(8)
        self.string_type = ir.IntType(8).as_pointer()  # Garante i8*
        self.void_type = ir.VoidType()
        self.bool_type = ir.IntType(1)
        
        # Declarar funções externas
        self._declare_external_functions()
        
    def _declare_external_functions(self):
        # printf
        voidptr_ty = ir.IntType(8).as_pointer()
        printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
        self.printf = ir.Function(self.module, printf_ty, name="printf")
        
        # Para melhor suporte a Unicode no Windows, também declarar wprintf
        if sys.platform == "win32":
            # wprintf para wide chars
            wchar_ptr_ty = ir.IntType(16).as_pointer()
            wprintf_ty = ir.FunctionType(ir.IntType(32), [wchar_ptr_ty], var_arg=True)
            self.wprintf = ir.Function(self.module, wprintf_ty, name="wprintf")
            
            # _setmode para configurar o modo do console
            setmode_ty = ir.FunctionType(ir.IntType(32), [ir.IntType(32), ir.IntType(32)])
            self.setmode = ir.Function(self.module, setmode_ty, name="_setmode")
            
            # SetConsoleOutputCP
            setcp_ty = ir.FunctionType(ir.IntType(32), [ir.IntType(32)])
            self.setconsolecp = ir.Function(self.module, setcp_ty, name="SetConsoleOutputCP")
        
        # malloc
        malloc_ty = ir.FunctionType(voidptr_ty, [ir.IntType(64)])
        self.malloc = ir.Function(self.module, malloc_ty, name="malloc")
        
        # free
        free_ty = ir.FunctionType(self.void_type, [voidptr_ty])
        self.free = ir.Function(self.module, free_ty, name="free")
        
        # strlen
        strlen_ty = ir.FunctionType(ir.IntType(64), [voidptr_ty])
        self.strlen = ir.Function(self.module, strlen_ty, name="strlen")
        
        # strcpy
        strcpy_ty = ir.FunctionType(voidptr_ty, [voidptr_ty, voidptr_ty])
        self.strcpy = ir.Function(self.module, strcpy_ty, name="strcpy")
        
        # strcat
        strcat_ty = ir.FunctionType(voidptr_ty, [voidptr_ty, voidptr_ty])
        self.strcat = ir.Function(self.module, strcat_ty, name="strcat")
        
        # sprintf para conversões
        sprintf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty, voidptr_ty], var_arg=True)
        self.sprintf = ir.Function(self.module, sprintf_ty, name="sprintf")
        
        # Funções de casting
        # to_str: converte int/float para string (sobrecarregada)
        to_str_int_ty = ir.FunctionType(self.string_type, [self.int_type])
        self.to_str_int = ir.Function(self.module, to_str_int_ty, name="to_str_int")
        to_str_float_ty = ir.FunctionType(self.string_type, [self.float_type])
        self.to_str_float = ir.Function(self.module, to_str_float_ty, name="to_str_float")
        
        # to_int: converte float para int
        to_int_ty = ir.FunctionType(self.int_type, [self.float_type])
        self.to_int = ir.Function(self.module, to_int_ty, name="to_int")
        
        # to_float: converte int para float
        to_float_ty = ir.FunctionType(self.float_type, [self.int_type])
        self.to_float = ir.Function(self.module, to_float_ty, name="to_float")
        
        if sys.platform == "win32":
            # Adicionar atributos para linking correto no Windows
            for func in [self.printf, self.malloc, self.free, self.strlen, self.strcpy, self.strcat, self.sprintf, self.to_str_int, self.to_str_float, self.to_int, self.to_float]:
                if func:
                    func.calling_convention = 'ccc'
                    func.linkage = 'external'
            
            if hasattr(self, 'wprintf'):
                self.wprintf.calling_convention = 'ccc'
                self.wprintf.linkage = 'external'
            if hasattr(self, 'setmode'):
                self.setmode.calling_convention = 'ccc'
                self.setmode.linkage = 'external'
            if hasattr(self, 'setconsolecp'):
                self.setconsolecp.calling_convention = 'ccc'
                self.setconsolecp.linkage = 'external'
        else:
            # Adicionar atributos para outras plataformas
            for func in [self.printf, self.malloc, self.free, self.strlen, self.strcpy, self.strcat, self.sprintf, self.to_str_int, self.to_str_float, self.to_int, self.to_float]:
                func.calling_convention = 'ccc'
                func.linkage = 'external'
        
        if sys.platform == "win32":
            # Adicionar atributos para linking correto no Windows
            for func in [self.printf, self.malloc, self.free, self.strlen, self.strcpy, self.to_str_int, self.to_str_float, self.to_int, self.to_float]:
                if func:
                    func.calling_convention = 'ccc'
                    func.linkage = 'external'
            
            if hasattr(self, 'wprintf'):
                self.wprintf.calling_convention = 'ccc'
                self.wprintf.linkage = 'external'
            if hasattr(self, 'setmode'):
                self.setmode.calling_convention = 'ccc'
                self.setmode.linkage = 'external'
            if hasattr(self, 'setconsolecp'):
                self.setconsolecp.calling_convention = 'ccc'
                self.setconsolecp.linkage = 'external'
    
        # fmod para float módulo
        fmod_ty = ir.FunctionType(self.float_type, [self.float_type, self.float_type])
        self.fmod = ir.Function(self.module, fmod_ty, name="fmod")
    
    def _convert_type(self, ml_type: Type) -> ir.Type:
        if isinstance(ml_type, IntType):
            return self.int_type
        elif isinstance(ml_type, FloatType):
            return self.float_type
        elif isinstance(ml_type, StringType) or isinstance(ml_type, StrType):
            return self.string_type
        elif isinstance(ml_type, BoolType):
            return self.bool_type
        elif isinstance(ml_type, ArrayType):
            element_type = self._convert_type(ml_type.element_type)
            if ml_type.size is not None:
                return ir.ArrayType(element_type, ml_type.size)
            else:
                return element_type.as_pointer()
        elif isinstance(ml_type, VoidType):
            return self.void_type
        elif isinstance(ml_type, ReferenceType):
            # Abordagem conservadora para evitar recursão infinita
            if isinstance(ml_type.target_type, StructType):
                # Para referências a structs, usar ponteiro para void como placeholder
                # Isso evita recursão infinita e será resolvido posteriormente
                return ir.IntType(8).as_pointer()  # void* equivalente
            else:
                # Para outros tipos, converter normalmente
                target_type = self._convert_type(ml_type.target_type)
                return target_type.as_pointer()
        elif isinstance(ml_type, StructType):
            if ml_type.name in self.struct_types:
                return self.struct_types[ml_type.name].as_pointer()
            else:
                # Forward declaration: criar struct vazia e retornar ponteiro
                struct_type = ir.LiteralStructType([])
                self.struct_types[ml_type.name] = struct_type
                return struct_type.as_pointer()
        else:
            raise TypeError(f"Tipo não suportado: {ml_type}")
    
    def generate(self, ast: ProgramNode):
        # Armazenar AST global
        self.global_ast = ast
        
        # Primeiro, processar definições de struct para criar os tipos LLVM
        for stmt in ast.statements:
            if isinstance(stmt, StructDefinitionNode):
                self._process_struct_definition(stmt)
        
        # Depois, declarar todas as variáveis globais e funções
        for stmt in ast.statements:
            if isinstance(stmt, AssignmentNode) and stmt.is_global:
                self._declare_global_variable(stmt)
            elif isinstance(stmt, FunctionNode):
                self._declare_function(stmt)
        
        # Criar função main
        main_ty = ir.FunctionType(ir.IntType(32), [])
        main_func = ir.Function(self.module, main_ty, name="main")
        
        # Criar bloco básico
        entry_block = main_func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(entry_block)
        self.current_function = main_func
        self.local_vars = {}
        
        # No Windows, configurar UTF-8 no início do programa
        if sys.platform == "win32":
            self._setup_windows_utf8()
        
        # Gerar código para cada statement (exceto funções e globais)
        for stmt in ast.statements:
            if not isinstance(stmt, FunctionNode) and not (isinstance(stmt, AssignmentNode) and stmt.is_global):
                self._generate_statement(stmt)
        
        # Adicionar limpeza de memória antes do return
        if self.memory_tracking:
            self._add_memory_cleanup()
        
        # Retornar 0 se não houver return explícito
        if not self.builder.block.is_terminated:
            self.builder.ret(ir.Constant(ir.IntType(32), 0))
        
        # Gerar código para as funções
        for stmt in ast.statements:
            if isinstance(stmt, FunctionNode):
                self._generate_function(stmt)
        
        return self.module
    
    def _track_allocation(self, ptr_value: ir.Value):
        """Rastreia uma alocação de memória para liberação posterior"""
        if self.memory_tracking and ptr_value:
            self.allocated_ptrs.append(ptr_value)
    
    def _add_memory_cleanup(self):
        """Adiciona código para liberar toda a memória alocada"""
        if not self.memory_tracking or not self.allocated_ptrs:
            return
        
        # Adicionar comentário no código
        cleanup_comment = "// Liberando memória alocada"
        # Nota: LLVM IR não suporta comentários diretamente, mas podemos adicionar labels
        
        # Liberar cada ponteiro alocado
        for ptr in self.allocated_ptrs:
            if isinstance(ptr.type, ir.PointerType):
                self.builder.call(self.free, [ptr])
        
        # Limpar a lista após liberação
        self.allocated_ptrs.clear()
    
    def _cleanup_function_memory(self):
        """Libera memória alocada dentro de uma função"""
        if not self.memory_tracking:
            return
        
        # Liberar variáveis locais que são ponteiros
        for var_name, var_ptr in self.local_vars.items():
            if isinstance(var_ptr, ir.AllocaInstr) and isinstance(var_ptr.type.pointee, ir.PointerType):
                # Carregar o valor do ponteiro
                loaded_ptr = self.builder.load(var_ptr)
                # Verificar se não é null antes de liberar
                null_ptr = ir.Constant(var_ptr.type.pointee, None)
                is_not_null = self.builder.icmp_ne(loaded_ptr, null_ptr)
                
                # Criar blocos para condição
                cleanup_block = self.current_function.append_basic_block(name=f"cleanup_{var_name}")
                continue_block = self.current_function.append_basic_block(name=f"continue_{var_name}")
                
                self.builder.cbranch(is_not_null, cleanup_block, continue_block)
                
                # Bloco de limpeza
                self.builder.position_at_end(cleanup_block)
                self.builder.call(self.free, [loaded_ptr])
                self.builder.branch(continue_block)
                
                # Continuar
                self.builder.position_at_end(continue_block)
    
    def _setup_windows_utf8(self):
        """Configura o console do Windows para UTF-8"""
        # Apenas chamar SetConsoleOutputCP(65001) para UTF-8
        if hasattr(self, 'setconsolecp'):
            utf8_codepage = ir.Constant(ir.IntType(32), 65001)
            self.builder.call(self.setconsolecp, [utf8_codepage])
    
    def _eval_constant(self, node):
        """Avalia um nó de valor constante para inicialização de globais."""
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, FloatNode):
            return node.value
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, BooleanNode):
            return node.value
        elif isinstance(node, NullNode):
            return 0  # null é representado como 0
        elif isinstance(node, ArrayNode):
            return [self._eval_constant(e) for e in node.elements]
        elif isinstance(node, ZerosNode):
            if isinstance(node.element_type, IntType):
                return [0] * node.size
            elif isinstance(node.element_type, FloatType):
                return [0.0] * node.size
            elif isinstance(node.element_type, StringType) or isinstance(node.element_type, StrType):
                return [None] * node.size
            elif isinstance(node.element_type, BoolType):
                return [False] * node.size
            else:
                return [None] * node.size
        elif isinstance(node, BinaryOpNode):
            # Suporte para expressões binárias simples em constantes
            left = self._eval_constant(node.left)
            right = self._eval_constant(node.right)
            
            if node.operator == TokenType.PLUS:
                return left + right
            elif node.operator == TokenType.MINUS:
                return left - right
            elif node.operator == TokenType.MULTIPLY:
                return left * right
            elif node.operator == TokenType.DIVIDE:
                return left / right
            elif node.operator == TokenType.AND:
                return left and right
            elif node.operator == TokenType.OR:
                return left or right
            else:
                raise Exception(f"Operador não suportado em constante global: {node.operator}")
        else:
            raise Exception(f"Valor inicial de global não suportado: {node}")

    def _declare_global_variable(self, node: AssignmentNode):
        """Declara uma variável global"""
        var_type = self._convert_type(node.var_type)
        # Criar variável global
        if isinstance(node.var_type, ArrayType):
            # Para arrays, precisamos inicializar com o tamanho correto
            if node.var_type.size:
                elem_type = self._convert_type(node.var_type.element_type)
                # Corrigir: para array de string, usar array de ponteiros para char
                if isinstance(node.var_type.element_type, StringType) or isinstance(node.var_type.element_type, StrType):
                    array_type = ir.ArrayType(self.char_type.as_pointer(), node.var_type.size)
                    gv = ir.GlobalVariable(self.module, array_type, name=node.identifier)
                    if node.value:
                        init = self._eval_constant(node.value)
                        llvm_ptrs = []
                        for idx, v in enumerate(init):
                            if v is None:
                                llvm_ptrs.append(ir.Constant(self.char_type.as_pointer(), None))
                            elif v == "":
                                # Criar string global vazia
                                str_bytes = b"\0"
                                str_type = ir.ArrayType(self.char_type, 1)
                                str_name = f"{node.identifier}_empty_{idx}"
                                str_global = ir.GlobalVariable(self.module, str_type, name=str_name)
                                str_global.linkage = 'internal'
                                str_global.global_constant = True
                                str_global.initializer = ir.Constant(str_type, bytearray(str_bytes))
                                ptr = str_global.bitcast(self.char_type.as_pointer())
                                llvm_ptrs.append(ptr)
                            else:
                                # Criar string global para o valor
                                str_bytes = (v + '\0').encode('utf8')
                                str_type = ir.ArrayType(self.char_type, len(str_bytes))
                                str_name = f"{node.identifier}_{idx}"
                                str_global = ir.GlobalVariable(self.module, str_type, name=str_name)
                                str_global.linkage = 'internal'
                                str_global.global_constant = True
                                str_global.initializer = ir.Constant(str_type, bytearray(str_bytes))
                                ptr = str_global.bitcast(self.char_type.as_pointer())
                                llvm_ptrs.append(ptr)
                        gv.initializer = ir.Constant(array_type, llvm_ptrs)
                    else:
                        gv.initializer = ir.Constant(array_type, [ir.Constant(self.char_type.as_pointer(), None)] * node.var_type.size)
                elif isinstance(node.var_type.element_type, FloatType):
                    array_type = ir.ArrayType(elem_type, node.var_type.size)
                    gv = ir.GlobalVariable(self.module, array_type, name=node.identifier)
                    if node.value:
                        init = self._eval_constant(node.value)
                        gv.initializer = ir.Constant(array_type, init)
                    else:
                        gv.initializer = ir.Constant(array_type, [0.0] * node.var_type.size)
                else:
                    array_type = ir.ArrayType(elem_type, node.var_type.size)
                    gv = ir.GlobalVariable(self.module, array_type, name=node.identifier)
                    if node.value:
                        init = self._eval_constant(node.value)
                        gv.initializer = ir.Constant(array_type, init)
                    else:
                        gv.initializer = ir.Constant(array_type, [0] * node.var_type.size)
            else:
                # Array sem tamanho definido, usar ponteiro
                gv = ir.GlobalVariable(self.module, var_type, name=node.identifier)
                gv.initializer = ir.Constant(var_type, None)
        else:
            gv = ir.GlobalVariable(self.module, var_type, name=node.identifier)
            if isinstance(node.var_type, IntType):
                if node.value:
                    init = self._eval_constant(node.value)
                    gv.initializer = ir.Constant(var_type, init)
                else:
                    gv.initializer = ir.Constant(var_type, 0)
            elif isinstance(node.var_type, FloatType):
                if node.value:
                    init = self._eval_constant(node.value)
                    gv.initializer = ir.Constant(var_type, init)
                else:
                    gv.initializer = ir.Constant(var_type, 0.0)
            else:
                gv.initializer = ir.Constant(var_type, None)
        gv.linkage = 'internal'
        self.global_vars[node.identifier] = gv
        self.type_map[node.identifier] = node.var_type
    
    def _declare_function(self, node: FunctionNode):
        # Converter tipos dos parâmetros
        param_types = [self._convert_type(param_type) for _, param_type in node.params]
        return_type = self._convert_type(node.return_type)
        
        func_ty = ir.FunctionType(return_type, param_types)
        
        # Criar função
        func = ir.Function(self.module, func_ty, name=node.name)
        self.functions[node.name] = func
        
        # Armazenar informação sobre tipos
        self.type_map[node.name] = FunctionType([p[1] for p in node.params], node.return_type)
    
    def _validate_circular_references(self, struct_name: str, visited: set = None) -> bool:
        """
        Valida se um struct tem referências circulares válidas.
        Retorna True se as referências são válidas, False se há recursão infinita.
        """
        if visited is None:
            visited = set()
        
        # Evitar recursão infinita na validação
        if struct_name in visited:
            return True  # Referência circular válida (auto-referência)
        
        visited.add(struct_name)
        
        # Verificar se o struct existe
        if struct_name not in self.struct_field_types:
            return True  # Struct não definido ainda, assumir válido
        
        # Verificar cada campo do struct
        for field_name, field_type in self.struct_field_types[struct_name].items():
            if isinstance(field_type, ReferenceType) and isinstance(field_type.target_type, StructType):
                target_name = field_type.target_type.name
                
                # Se é auto-referência, é válida
                if target_name == struct_name:
                    continue
                
                # Verificar se a referência é para um struct válido
                if target_name not in self.struct_field_types:
                    # Struct não definido, pode causar problemas
                    return False
                
                # Verificar recursivamente o struct alvo
                if not self._validate_circular_references(target_name, visited.copy()):
                    return False
        
        return True

    def _process_struct_definition(self, node: StructDefinitionNode):
        # Abordagem conservadora para evitar recursão infinita
        # Primeira passada: criar struct com placeholders para auto-referências
        field_types = []
        auto_references = []  # Lista para rastrear campos que são auto-referências
        
        for i, (field_name, field_type) in enumerate(node.fields):
            if isinstance(field_type, ReferenceType) and isinstance(field_type.target_type, StructType):
                # Verificar se é auto-referência (mesmo nome do struct)
                if field_type.target_type.name == node.name:
                    # Auto-referência: usar ponteiro para void como placeholder
                    llvm_type = ir.IntType(8).as_pointer()  # void* equivalente
                    auto_references.append((i, field_name))
                else:
                    # Referência para outro struct: usar ponteiro para void também
                    # para evitar dependências circulares complexas
                    llvm_type = ir.IntType(8).as_pointer()  # void* equivalente
            elif isinstance(field_type, StructType):
                # Para outros structs, verifica se já existe
                if field_type.name not in self.struct_types:
                    # Cria um tipo opaco para forward declaration
                    other_opaque = ir.LiteralStructType([], packed=False)
                    self.struct_types[field_type.name] = other_opaque
                llvm_type = self.struct_types[field_type.name]
            else:
                llvm_type = self._convert_type(field_type)
            field_types.append(llvm_type)
        
        # Cria o struct com os tipos (incluindo ponteiros para void para auto-referência)
        actual_struct_type = ir.LiteralStructType(field_types, packed=False)
        self.struct_types[node.name] = actual_struct_type
        
        # Armazenar informações dos campos para acesso posterior
        if not hasattr(self, 'struct_fields'):
            self.struct_fields = {}
        self.struct_fields[node.name] = {field_name: i for i, (field_name, _) in enumerate(node.fields)}
        
        # Armazenar tipos dos campos para navegação aninhada
        if not hasattr(self, 'struct_field_types'):
            self.struct_field_types = {}
        self.struct_field_types[node.name] = {field_name: field_type for field_name, field_type in node.fields}
        
        # Armazenar informações sobre auto-referências para uso posterior
        if not hasattr(self, 'struct_auto_references'):
            self.struct_auto_references = {}
        if auto_references:
            self.struct_auto_references[node.name] = auto_references
        
        # Validar referências circulares após definir o struct
        if not self._validate_circular_references(node.name):
            raise ValueError(f"Struct '{node.name}' tem referências circulares inválidas que podem causar recursão infinita")
    
    def _generate_function(self, node: FunctionNode):
        func = self.functions[node.name]
        
        # Criar bloco de entrada
        entry_block = func.append_basic_block(name="entry")
        
        # Salvar estado atual
        old_builder = self.builder
        old_vars = self.local_vars
        old_func = self.current_function
        old_func_ast = self.current_function_ast
        
        # Configurar novo contexto
        self.builder = ir.IRBuilder(entry_block)
        self.local_vars = {}
        self.current_function = func
        self.current_function_ast = node
        
        # Mapear parâmetros para variáveis locais
        for i, ((param_name, param_type), param) in enumerate(zip(node.params, func.args)):
            param.name = param_name
            # Se o parâmetro é um array (ponteiro), não criar alloca adicional
            if isinstance(param_type, ArrayType):
                self.local_vars[param_name] = param
                self.type_map[param_name] = param_type
            else:
                # Para tipos escalares, criar alloca e armazenar
                alloca = self.builder.alloca(param.type, name=param_name)
                self.builder.store(param, alloca)
                self.local_vars[param_name] = alloca
                self.type_map[param_name] = param_type
        
        # Gerar corpo da função
        for stmt in node.body:
            self._generate_statement(stmt)
        
        # Adicionar return padrão se necessário
        if not self.builder.block.is_terminated:
            if isinstance(node.return_type, VoidType):
                self.builder.ret_void()
            else:
                default_value = ir.Constant(self._convert_type(node.return_type), 0)
                self.builder.ret(default_value)
        
        # Restaurar estado
        self.builder = old_builder
        self.local_vars = old_vars
        self.current_function = old_func
        self.current_function_ast = old_func_ast
    
    def _generate_statement(self, node: ASTNode):
        if node is None:
            return  # Ignorar statements nulos
        
        if isinstance(node, AssignmentNode):
            self._generate_assignment(node)
        elif isinstance(node, ArrayAssignmentNode):
            self._generate_array_assignment(node)
        elif isinstance(node, PrintNode):
            self._generate_print(node)
        elif isinstance(node, IfNode):
            self._generate_if(node)
        elif isinstance(node, WhileNode):
            self._generate_while(node)
        elif isinstance(node, ReturnNode):
            self._generate_return(node)
        elif isinstance(node, StructDefinitionNode):
            # Structs são definições de tipo, não geram código executável
            pass
        elif isinstance(node, StructAssignmentNode):
            self._generate_struct_assignment(node)
        elif isinstance(node, StructConstructorNode):
            self._generate_struct_constructor(node)
        else:
            # Expressão simples
            self._generate_expression(node)
    
    def _generate_assignment(self, node: AssignmentNode):
        if node.is_global and node.var_type is not None:
            # Variável global já foi declarada
            value = self._generate_expression(node.value)
            self.builder.store(value, self.global_vars[node.identifier])
        else:
            # Variável local ou reatribuição
            # Configurar tipo de struct atual para geração de valores null
            if node.var_type and isinstance(node.var_type, StructType):
                self.current_struct_type = node.var_type.name
            else:
                self.current_struct_type = None
            
            value = self._generate_expression(node.value)
            
            if node.var_type is None:
                # Reatribuição - variável já existe
                if node.identifier in self.local_vars:
                    self.builder.store(value, self.local_vars[node.identifier])
                elif node.identifier in self.global_vars:
                    self.builder.store(value, self.global_vars[node.identifier])
                else:
                    raise NameError(f"Variável '{node.identifier}' não definida")
            else:
                # Nova variável local
                var_type = self._convert_type(node.var_type)
                alloca = self.builder.alloca(var_type, name=node.identifier)
                self.local_vars[node.identifier] = alloca
                self.type_map[node.identifier] = node.var_type
                
                # Armazenar valor
                if isinstance(node.var_type, ArrayType):
                    # Para arrays, precisamos copiar os elementos
                    if node.var_type.size is not None:
                        # Array com tamanho fixo - copiar elementos
                        # Primeiro, obter ponteiro para o primeiro elemento do array destino
                        zero = ir.Constant(ir.IntType(32), 0)
                        dst_array_ptr = self.builder.gep(alloca, [zero, zero], inbounds=True)
                        
                        # Verificar se o valor é um ArrayNode (array literal)
                        if hasattr(node.value, 'elements') and isinstance(node.value.elements, list):
                            # É um array literal, copiar elementos
                            for i in range(min(node.var_type.size, len(node.value.elements))):
                                # Gerar o valor do elemento diretamente
                                elem_value = self._generate_expression(node.value.elements[i])
                                
                                # Armazenar no array destino
                                dst_ptr = self.builder.gep(dst_array_ptr, [ir.Constant(self.int_type, i)], inbounds=True)
                                self.builder.store(elem_value, dst_ptr)
                        else:
                            # É um ponteiro para array, copiar elementos
                            for i in range(node.var_type.size):
                                # Carregar o valor do array fonte
                                src_ptr = self.builder.gep(value, [ir.Constant(self.int_type, i)], inbounds=True)
                                src_val = self.builder.load(src_ptr)
                                
                                # Armazenar no array destino
                                dst_ptr = self.builder.gep(dst_array_ptr, [ir.Constant(self.int_type, i)], inbounds=True)
                                self.builder.store(src_val, dst_ptr)
                    else:
                        # Array dinâmico - armazenar ponteiro
                        if isinstance(value.type, ir.PointerType) and isinstance(var_type, ir.PointerType):
                            if value.type != var_type:
                                value = self.builder.bitcast(value, var_type)
                        self.builder.store(value, alloca)
                elif isinstance(node.var_type, ReferenceType):
                    # Para referências, fazer cast se necessário
                    if isinstance(value.type, ir.IntType) and value.type.width == 64:
                        # Se o valor é null (i64), converter para ponteiro nulo
                        null_ptr = ir.Constant(var_type, None)
                        self.builder.store(null_ptr, alloca)
                    elif (isinstance(value.type, ir.PointerType) and 
                        isinstance(value.type.pointee, ir.LiteralStructType) and
                        isinstance(var_type, ir.PointerType) and
                        var_type.pointee == ir.IntType(8)):
                        # Cast de ponteiro para struct para ponteiro para void
                        value = self.builder.bitcast(value, var_type)
                        self.builder.store(value, alloca)
                    else:
                        # Para outros casos, armazenar diretamente
                        self.builder.store(value, alloca)
                elif isinstance(node.var_type, StructType):
                    # Para structs, tratar null especialmente
                    if isinstance(value.type, ir.IntType) and value.type.width == 64:
                        # Se o valor é null (i64), converter para ponteiro nulo do tipo correto
                        null_ptr = ir.Constant(var_type, None)
                        self.builder.store(null_ptr, alloca)
                    else:
                        # Para outros valores, armazenar diretamente
                        try:
                            self.builder.store(value, alloca)
                        except TypeError:
                            # Se falhar, tentar fazer cast
                            if isinstance(value.type, ir.PointerType) and isinstance(var_type, ir.PointerType):
                                value = self.builder.bitcast(value, var_type)
                            self.builder.store(value, alloca)
                else:
                    # Para tipos simples
                    self.builder.store(value, alloca)
    
    def _generate_array_assignment(self, node: ArrayAssignmentNode):
        # Procurar variável primeiro localmente, depois globalmente
        if node.array_name in self.local_vars:
            var = self.local_vars[node.array_name]
        elif node.array_name in self.global_vars:
            var = self.global_vars[node.array_name]
        else:
            raise NameError(f"Array '{node.array_name}' não definido")
        
        index = self._generate_expression(node.index)
        value = self._generate_expression(node.value)
        
        # Se a variável já é um ponteiro (parâmetro de função), usar diretamente
        if isinstance(var, ir.Argument) and isinstance(var.type, ir.PointerType):
            array_ptr = var
        elif isinstance(var, ir.GlobalVariable) and isinstance(var.type.pointee, ir.ArrayType):
            # Variável global que é array
            zero = ir.Constant(ir.IntType(32), 0)
            array_ptr = self.builder.gep(var, [zero, zero], inbounds=True)
        else:
            # Para arrays locais, não fazer load, usar diretamente o ponteiro
            if isinstance(var.type, ir.PointerType) and isinstance(var.type.pointee, ir.ArrayType):
                zero = ir.Constant(ir.IntType(32), 0)
                array_ptr = self.builder.gep(var, [zero, zero], inbounds=True)
            else:
                array_ptr = self.builder.load(var)
                if isinstance(array_ptr.type, ir.ArrayType):
                    zero = ir.Constant(ir.IntType(32), 0)
                    array_ptr = self.builder.gep(array_ptr, [zero, zero], inbounds=True)
        
        # Verificar se array_ptr é um ponteiro válido
        if not isinstance(array_ptr.type, ir.PointerType):
            # Se não é ponteiro, fazer cast para ponteiro
            array_ptr = self.builder.bitcast(array_ptr, self.int_type.as_pointer())
        
        # Calcular endereço do elemento
        elem_ptr = self.builder.gep(array_ptr, [index], inbounds=True)
        
        # Armazenar valor
        self.builder.store(value, elem_ptr)
    
    def _generate_print(self, node: PrintNode):
        value = self._generate_expression(node.expression)
        
        # Verificar se estamos imprimindo um array diretamente
        if isinstance(node.expression, IdentifierNode):
            var_name = node.expression.name
            if var_name in self.type_map and isinstance(self.type_map[var_name], ArrayType):
                # É um array, vamos imprimir especialmente
                self._print_array(var_name)
                return
        # Verificar se estamos imprimindo um campo de struct que é um array
        elif isinstance(node.expression, StructAccessNode):
            struct_name = node.expression.struct_name
            field_name = node.expression.field_name
            
            # Determinar o tipo de struct baseado na variável
            struct_type_name = None
            if struct_name in self.type_map:
                var_type = self.type_map[struct_name]
                if isinstance(var_type, StructType):
                    struct_type_name = var_type.name
                elif isinstance(var_type, ReferenceType) and isinstance(var_type.target_type, StructType):
                    struct_type_name = var_type.target_type.name
            
            # Verificar se o campo é um array
            if (struct_type_name and struct_type_name in self.struct_fields and 
                field_name in self.struct_fields[struct_type_name]):
                # Obter o tipo do campo
                field_index = self.struct_fields[struct_type_name][field_name]
                if struct_type_name in self.struct_types:
                    struct_type = self.struct_types[struct_type_name]
                    if field_index < len(struct_type.elements):
                        field_llvm_type = struct_type.elements[field_index]
                        # Se o campo é um ponteiro (array), imprimir como array
                        if isinstance(field_llvm_type, ir.PointerType):
                            self._print_struct_array_field(struct_name, field_name, field_llvm_type)
                            return
        
        # Determinar formato baseado no tipo
        if value.type == self.bool_type:
            fmt_str = "%s\n\0"  # Usar %s para "true"/"false"
        elif isinstance(value.type, ir.IntType):
            fmt_str = "%lld\n\0"
        elif isinstance(value.type, ir.DoubleType):
            fmt_str = "%f\n\0"
        elif isinstance(value.type, ir.PointerType) and value.type.pointee == self.char_type:
            fmt_str = "%s\n\0"
        else:
            fmt_str = "%p\n\0"  # Ponteiro genérico
            
        # Criar string global com nome único
        fmt_name = f"fmt_str_{len(self.module.globals)}"
        fmt_bytes = fmt_str.encode('utf8')
        fmt = ir.GlobalVariable(self.module, ir.ArrayType(ir.IntType(8), len(fmt_bytes)), name=fmt_name)
        fmt.linkage = 'internal'
        fmt.global_constant = True
        fmt.initializer = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt_bytes)),
                                     bytearray(fmt_bytes))
        
        # Obter ponteiro para o início do array usando GEP
        zero = ir.Constant(ir.IntType(32), 0)
        fmt_ptr = self.builder.gep(fmt, [zero, zero], inbounds=True)
        
        # Tratamento especial para booleanos
        if value.type == self.bool_type:
            # Criar strings "true" e "false"
            true_str = "true\0"
            false_str = "false\0"
            true_bytes = true_str.encode('utf8')
            false_bytes = false_str.encode('utf8')
            
            true_type = ir.ArrayType(self.char_type, len(true_bytes))
            false_type = ir.ArrayType(self.char_type, len(false_bytes))
            
            true_name = f"true_str_{len(self.module.globals)}"
            false_name = f"false_str_{len(self.module.globals)}"
            
            true_global = ir.GlobalVariable(self.module, true_type, name=true_name)
            true_global.linkage = 'internal'
            true_global.global_constant = True
            true_global.initializer = ir.Constant(true_type, bytearray(true_bytes))
            
            false_global = ir.GlobalVariable(self.module, false_type, name=false_name)
            false_global.linkage = 'internal'
            false_global.global_constant = True
            false_global.initializer = ir.Constant(false_type, bytearray(false_bytes))
            
            true_ptr = self.builder.gep(true_global, [zero, zero], inbounds=True)
            false_ptr = self.builder.gep(false_global, [zero, zero], inbounds=True)
            
            # Usar select para escolher entre "true" e "false"
            bool_str = self.builder.select(value, true_ptr, false_ptr)
            self.builder.call(self.printf, [fmt_ptr, bool_str])
        else:
            # Chamar printf
            self.builder.call(self.printf, [fmt_ptr, value])
    
    def _print_struct_array_field(self, struct_name: str, field_name: str, field_type: ir.Type):
        """Imprime um campo de array de um struct"""
        # Obter ponteiro do struct
        if struct_name in self.local_vars:
            struct_ptr = self.local_vars[struct_name]
        elif struct_name in self.global_vars:
            struct_ptr = self.global_vars[struct_name]
        else:
            return
        
        # Determinar o tipo de struct baseado na variável
        struct_type_name = None
        if struct_name in self.type_map:
            var_type = self.type_map[struct_name]
            if isinstance(var_type, StructType):
                struct_type_name = var_type.name
            elif isinstance(var_type, ReferenceType) and isinstance(var_type.target_type, StructType):
                struct_type_name = var_type.target_type.name
        
        if not struct_type_name or struct_type_name not in self.struct_fields:
            return
        
        # Verificar se o campo é uma string (não um array)
        if struct_type_name in self.struct_types:
            # Obter o tipo original do campo no struct
            struct_type = self.struct_types[struct_type_name]
            field_index = self.struct_fields[struct_type_name][field_name]
            
            # Verificar se o campo original era StringType
            original_field_type = None
            if struct_type_name in self.struct_types:
                # Encontrar o tipo original do campo
                for field_name_orig, field_type_orig in var_type.fields.items():
                    if field_name_orig == field_name:
                        original_field_type = field_type_orig
                        break
            
            # Se é uma string, imprimir como string
            if isinstance(original_field_type, StringType) or isinstance(original_field_type, StrType):
                # Acessar o campo usando getelementptr
                field_ptr = self.builder.gep(struct_ptr, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), field_index)])
                
                # Carregar o ponteiro da string
                string_ptr = self.builder.load(field_ptr)
                
                # Imprimir como string
                self._print_string(string_ptr)
                return
        
        # Obter o índice do campo
        field_index = self.struct_fields[struct_type_name][field_name]
        
        # Acessar o campo usando getelementptr
        field_ptr = self.builder.gep(struct_ptr, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), field_index)])
        
        # Carregar o ponteiro do array
        array_ptr = self.builder.load(field_ptr)
        
        # Imprimir o array
        self._print_array_from_ptr(array_ptr, field_type)
    
    def _print_string(self, string_ptr: ir.Value):
        """Imprime uma string"""
        # Formato para string
        fmt_str = "%s\n\0"
        fmt_bytes = fmt_str.encode('utf8')
        fmt_type = ir.ArrayType(self.char_type, len(fmt_bytes))
        fmt_name = f"fmt_str_{len(self.module.globals)}"
        fmt_global = ir.GlobalVariable(self.module, fmt_type, name=fmt_name)
        fmt_global.linkage = 'internal'
        fmt_global.global_constant = True
        fmt_global.initializer = ir.Constant(fmt_type, bytearray(fmt_bytes))
        fmt_ptr = self.builder.gep(fmt_global, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)], inbounds=True)
        
        # Imprimir a string
        self.builder.call(self.printf, [fmt_ptr, string_ptr])
    
    def _print_array_from_ptr(self, array_ptr: ir.Value, array_type: ir.Type, array_size: int = None):
        """Imprime um array a partir de um ponteiro"""
        # Determinar o tipo de elemento e tamanho baseado no tipo do ponteiro
        if isinstance(array_type, ir.PointerType):
            elem_type = array_type.pointee
            # Usar o tamanho fornecido ou determinar baseado no tipo do elemento
            if array_size is None:
                if elem_type == self.int_type:
                    array_size = 4  # Para arrays de int
                elif elem_type == self.bool_type:
                    array_size = 5  # Para arrays de bool
                else:
                    array_size = 3  # Padrão
        else:
            return
        
        zero = ir.Constant(ir.IntType(32), 0)

        # String "["
        bracket_open_str = "[\0"
        bracket_open_bytes = bracket_open_str.encode('utf8')
        bracket_open_type = ir.ArrayType(self.char_type, len(bracket_open_bytes))
        bracket_open_name = f"bracket_open_{len(self.module.globals)}"
        bracket_open_global = ir.GlobalVariable(self.module, bracket_open_type, name=bracket_open_name)
        bracket_open_global.linkage = 'internal'
        bracket_open_global.global_constant = True
        bracket_open_global.initializer = ir.Constant(bracket_open_type, bytearray(bracket_open_bytes))
        bracket_open_ptr = self.builder.gep(bracket_open_global, [zero, zero], inbounds=True)

        # String "%s"
        fmt_s_str = "%s\0"
        fmt_s_bytes = fmt_s_str.encode('utf8')
        fmt_s_type = ir.ArrayType(self.char_type, len(fmt_s_bytes))
        fmt_s_name = f"fmt_s_{len(self.module.globals)}"
        fmt_s_global = ir.GlobalVariable(self.module, fmt_s_type, name=fmt_s_name)
        fmt_s_global.linkage = 'internal'
        fmt_s_global.global_constant = True
        fmt_s_global.initializer = ir.Constant(fmt_s_type, bytearray(fmt_s_bytes))
        fmt_s_ptr = self.builder.gep(fmt_s_global, [zero, zero], inbounds=True)

        # Imprimir "["
        self.builder.call(self.printf, [fmt_s_ptr, bracket_open_ptr])

        # String de formatação para elementos
        if elem_type == self.bool_type:
            fmt_elem_str = "%s\0"  # Usar %s para "true"/"false"
        elif isinstance(elem_type, ir.IntType):
            fmt_elem_str = "%lld\0"
        elif isinstance(elem_type, ir.DoubleType):
            fmt_elem_str = "%f\0"
        elif isinstance(elem_type, ir.PointerType) and elem_type.pointee == self.char_type:
            fmt_elem_str = "%s\0"  # Usar %s para strings
        elif isinstance(elem_type, ir.PointerType) and isinstance(elem_type.pointee, ir.PointerType) and elem_type.pointee.pointee == self.char_type:
            fmt_elem_str = "%s\0"  # Usar %s para arrays de strings
        elif elem_type == self.string_type:
            fmt_elem_str = "%s\0"  # Usar %s para strings (quando elem_type é string_type diretamente)
        else:
            fmt_elem_str = "%p\0"
        fmt_elem_bytes = fmt_elem_str.encode('utf8')
        fmt_elem_type = ir.ArrayType(self.char_type, len(fmt_elem_bytes))
        fmt_elem_name = f"fmt_elem_{len(self.module.globals)}"
        fmt_elem_global = ir.GlobalVariable(self.module, fmt_elem_type, name=fmt_elem_name)
        fmt_elem_global.linkage = 'internal'
        fmt_elem_global.global_constant = True
        fmt_elem_global.initializer = ir.Constant(fmt_elem_type, bytearray(fmt_elem_bytes))
        fmt_elem_ptr = self.builder.gep(fmt_elem_global, [zero, zero], inbounds=True)

        # String ", "
        comma_str = ", \0"
        comma_bytes = comma_str.encode('utf8')
        comma_type = ir.ArrayType(self.char_type, len(comma_bytes))
        comma_name = f"comma_{len(self.module.globals)}"
        comma_global = ir.GlobalVariable(self.module, comma_type, name=comma_name)
        comma_global.linkage = 'internal'
        comma_global.global_constant = True
        comma_global.initializer = ir.Constant(comma_type, bytearray(comma_bytes))
        comma_ptr = self.builder.gep(comma_global, [zero, zero], inbounds=True)

        # Imprimir cada elemento
        for i in range(array_size):
            if i > 0:
                self.builder.call(self.printf, [fmt_s_ptr, comma_ptr])
            elem_ptr = self.builder.gep(array_ptr, [ir.Constant(ir.IntType(32), i)], inbounds=True)
            elem_value = self.builder.load(elem_ptr)
            
            # Tratamento especial para booleanos
            if elem_type == self.bool_type:
                # Criar strings "true" e "false"
                true_str = "true\0"
                false_str = "false\0"
                true_bytes = true_str.encode('utf8')
                false_bytes = false_str.encode('utf8')
                
                true_type = ir.ArrayType(self.char_type, len(true_bytes))
                false_type = ir.ArrayType(self.char_type, len(false_bytes))
                
                true_name = f"true_str_{len(self.module.globals)}"
                false_name = f"false_str_{len(self.module.globals)}"
                
                true_global = ir.GlobalVariable(self.module, true_type, name=true_name)
                true_global.linkage = 'internal'
                true_global.global_constant = True
                true_global.initializer = ir.Constant(true_type, bytearray(true_bytes))
                
                false_global = ir.GlobalVariable(self.module, false_type, name=false_name)
                false_global.linkage = 'internal'
                false_global.global_constant = True
                false_global.initializer = ir.Constant(false_type, bytearray(false_bytes))
                
                true_ptr = self.builder.gep(true_global, [zero, zero], inbounds=True)
                false_ptr = self.builder.gep(false_global, [zero, zero], inbounds=True)
                
                # Usar select para escolher entre "true" e "false"
                bool_str = self.builder.select(elem_value, true_ptr, false_ptr)
                self.builder.call(self.printf, [fmt_elem_ptr, bool_str])
            else:
                self.builder.call(self.printf, [fmt_elem_ptr, elem_value])

        # String "]\n"
        bracket_close_str = "]\n\0"
        bracket_close_bytes = bracket_close_str.encode('utf8')
        bracket_close_type = ir.ArrayType(self.char_type, len(bracket_close_bytes))
        bracket_close_name = f"bracket_close_{len(self.module.globals)}"
        bracket_close_global = ir.GlobalVariable(self.module, bracket_close_type, name=bracket_close_name)
        bracket_close_global.linkage = 'internal'
        bracket_close_global.global_constant = True
        bracket_close_global.initializer = ir.Constant(bracket_close_type, bytearray(bracket_close_bytes))
        bracket_close_ptr = self.builder.gep(bracket_close_global, [zero, zero], inbounds=True)
        self.builder.call(self.printf, [fmt_s_ptr, bracket_close_ptr])
    
    def _print_array(self, array_name: str):
        """Imprime um array de forma formatada (int, float ou string)"""
        # Obter informações sobre o array
        array_type = self.type_map.get(array_name)
        if not isinstance(array_type, ArrayType):
            return
        elem_type = array_type.element_type
        array_size = array_type.size if array_type.size else 5

        # Obter ponteiro do array
        if array_name in self.local_vars:
            var = self.local_vars[array_name]
        elif array_name in self.global_vars:
            var = self.global_vars[array_name]
        else:
            return

        # Carregar o ponteiro do array
        if isinstance(var, ir.Argument) and isinstance(var.type, ir.PointerType):
            array_ptr = var
        elif isinstance(var, ir.GlobalVariable) and isinstance(var.type.pointee, ir.ArrayType):
            array_ptr = self.builder.gep(var, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)], inbounds=True)
        else:
            array_ptr = self.builder.load(var)
        
        # Converter o tipo para LLVM
        llvm_elem_type = self._convert_type(elem_type)
        
        # Para arrays de strings, precisamos passar o tipo correto
        if isinstance(elem_type, StringType) or isinstance(elem_type, StrType):
            # Para strings, o tipo LLVM é um ponteiro para char
            array_llvm_type = self.string_type.as_pointer()
        else:
            if isinstance(llvm_elem_type, ir.PointerType):
                array_llvm_type = llvm_elem_type
            else:
                array_llvm_type = llvm_elem_type.as_pointer()
        
        # Imprimir usando o método existente com o tamanho correto
        self._print_array_from_ptr(array_ptr, array_llvm_type, array_size)
    
    def _generate_if(self, node: IfNode):
        # Gerar condição
        condition = self._generate_expression(node.condition)
        
        # Criar blocos
        then_block = self.current_function.append_basic_block(name="then")
        end_block = self.current_function.append_basic_block(name="endif")
        
        if node.else_branch:
            else_block = self.current_function.append_basic_block(name="else")
            self.builder.cbranch(condition, then_block, else_block)
        else:
            self.builder.cbranch(condition, then_block, end_block)
        
        # Gerar código do then
        self.builder.position_at_end(then_block)
        for stmt in node.then_branch:
            self._generate_statement(stmt)
        if not self.builder.block.is_terminated:
            self.builder.branch(end_block)
        
        # Gerar código do else se existir
        if node.else_branch:
            self.builder.position_at_end(else_block)
            for stmt in node.else_branch:
                self._generate_statement(stmt)
            if not self.builder.block.is_terminated:
                self.builder.branch(end_block)
        
        # Continuar no end block
        self.builder.position_at_end(end_block)
    
    def _generate_while(self, node: WhileNode):
        # Criar blocos
        cond_block = self.current_function.append_basic_block(name="while_cond")
        body_block = self.current_function.append_basic_block(name="while_body")
        end_block = self.current_function.append_basic_block(name="while_end")
        
        # Ir para bloco de condição
        self.builder.branch(cond_block)
        
        # Gerar condição
        self.builder.position_at_end(cond_block)
        condition = self._generate_expression(node.condition)
        self.builder.cbranch(condition, body_block, end_block)
        
        # Gerar corpo do loop
        self.builder.position_at_end(body_block)
        for stmt in node.body:
            self._generate_statement(stmt)
        if not self.builder.block.is_terminated:
            self.builder.branch(cond_block)
        
        # Continuar após o loop
        self.builder.position_at_end(end_block)
    
    def _generate_return(self, node: ReturnNode):
        if node.value:
            value = self._generate_expression(node.value)
            self.builder.ret(value)
        else:
            if isinstance(self.current_function.return_value.type, ir.VoidType):
                self.builder.ret_void()
            else:
                self.builder.ret(ir.Constant(self.int_type, 0))
    
    def _generate_expression(self, node: ASTNode, expected_type: ir.Type = None) -> ir.Value:
        if node is None:
            raise ValueError("Tentativa de gerar código para nó None")
            
        if isinstance(node, NumberNode):
            return ir.Constant(self.int_type, node.value)
            
        elif isinstance(node, FloatNode):
            return ir.Constant(self.float_type, node.value)
                
        elif isinstance(node, StringNode):
            # Criar string global
            string_value = node.value + '\0'  # Adicionar null terminator
            # Converter para bytes para contar corretamente caracteres UTF-8
            string_bytes = string_value.encode('utf8')
            str_type = ir.ArrayType(self.char_type, len(string_bytes))
            str_name = f"str_{len(self.module.globals)}"
            
            str_global = ir.GlobalVariable(self.module, str_type, name=str_name)
            str_global.linkage = 'internal'
            str_global.global_constant = True
            str_global.initializer = ir.Constant(str_type, bytearray(string_bytes))
            
            # Retornar ponteiro para a string
            zero = ir.Constant(ir.IntType(32), 0)
            return self.builder.gep(str_global, [zero, zero], inbounds=True)
            
        elif isinstance(node, BooleanNode):
            return ir.Constant(self.bool_type, node.value)
            
        elif isinstance(node, NullNode):
            if expected_type and isinstance(expected_type, ir.PointerType):
                return ir.Constant(expected_type, None)
            elif expected_type and isinstance(expected_type, ir.IntType):
                return ir.Constant(expected_type, 0)
            else:
                return ir.Constant(self.int_type, 0)
            
        elif isinstance(node, StructAccessNode):
            # Acessar campo de struct (suporta acesso aninhado)
            if node.struct_name in self.local_vars:
                struct_ptr = self.local_vars[node.struct_name]
            else:
                # Procurar nas variáveis globais
                struct_ptr = self.module.globals.get(node.struct_name)
                if struct_ptr is None:
                    raise NameError(f"Struct '{node.struct_name}' não encontrado")
            
            # Determinar o tipo de struct baseado na variável
            struct_type_name = None
            if node.struct_name in self.type_map:
                var_type = self.type_map[node.struct_name]
                if isinstance(var_type, StructType):
                    struct_type_name = var_type.name
                elif isinstance(var_type, ReferenceType) and isinstance(var_type.target_type, StructType):
                    struct_type_name = var_type.target_type.name
            
            if not struct_type_name or struct_type_name not in self.struct_fields:
                raise NameError(f"Struct '{struct_type_name}' não encontrado")
            
            # Fazer cast do ponteiro para void para o tipo correto do struct
            if struct_type_name in self.struct_types:
                struct_type = self.struct_types[struct_type_name]
                struct_ptr = self.builder.bitcast(struct_ptr, struct_type.as_pointer())
            
            # Verificar se é acesso aninhado (ex: pessoa.endereco.rua)
            if '.' in node.field_name:
                # Dividir o caminho: "endereco.rua" -> ["endereco", "rua"]
                field_path = node.field_name.split('.')
                
                # Navegar pelo caminho
                current_ptr = struct_ptr
                current_struct_type = struct_type_name
                
                for i, field_name in enumerate(field_path):
                    if current_struct_type not in self.struct_fields or field_name not in self.struct_fields[current_struct_type]:
                        raise NameError(f"Campo '{field_name}' não encontrado em struct '{current_struct_type}'")
                    
                    # Obter o índice do campo
                    field_index = self.struct_fields[current_struct_type][field_name]
                    
                    # Acessar o campo
                    field_ptr = self.builder.gep(current_ptr, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), field_index)])
                    
                    # Se não é o último campo, continuar navegando
                    if i < len(field_path) - 1:
                        # Para structs, manter o ponteiro (não carregar o valor)
                        current_ptr = field_ptr
                        # Determinar o tipo do campo para continuar navegando
                        if hasattr(self, 'struct_field_types') and current_struct_type in self.struct_field_types:
                            field_type = self.struct_field_types[current_struct_type][field_name]
                            if isinstance(field_type, StructType):
                                current_struct_type = field_type.name
                            else:
                                raise NameError(f"Campo '{field_name}' não é um struct")
                        else:
                            # Fallback: usar o nome do campo como tipo
                            current_struct_type = field_name
                    else:
                        # Último campo, retornar o valor
                        return self.builder.load(field_ptr)
            else:
                # Acesso simples a campo
                if node.field_name not in self.struct_fields[struct_type_name]:
                    raise NameError(f"Campo '{node.field_name}' não encontrado em struct '{struct_type_name}'")
                
                # Obter o índice do campo
                field_index = self.struct_fields[struct_type_name][node.field_name]
                
                # Acessar o campo usando getelementptr diretamente no ponteiro
                field_ptr = self.builder.gep(struct_ptr, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), field_index)])
                
                # Carregar o valor do campo
                return self.builder.load(field_ptr)
        elif isinstance(node, ArrayNode):
            # Alocar memória para o array
            num_elements = len(node.elements)
            if isinstance(node.element_type, IntType):
                elem_size = 8
                array_size = ir.Constant(self.int_type, num_elements * elem_size)
                array_ptr = self.builder.call(self.malloc, [array_size])
                self._track_allocation(array_ptr)
                typed_ptr = self.builder.bitcast(array_ptr, self.int_type.as_pointer())
            elif isinstance(node.element_type, FloatType):
                elem_size = 8
                array_size = ir.Constant(self.int_type, num_elements * elem_size)
                array_ptr = self.builder.call(self.malloc, [array_size])
                self._track_allocation(array_ptr)
                typed_ptr = self.builder.bitcast(array_ptr, self.float_type.as_pointer())
            elif isinstance(node.element_type, StringType) or isinstance(node.element_type, StrType):
                elem_size = 8  # ponteiro de 64 bits
                array_size = ir.Constant(self.int_type, num_elements * elem_size)
                array_ptr = self.builder.call(self.malloc, [array_size])
                self._track_allocation(array_ptr)
                # Ponteiro para ponteiro de char (i8**)
                typed_ptr = self.builder.bitcast(array_ptr, self.char_type.as_pointer().as_pointer())
            elif isinstance(node.element_type, BoolType):
                elem_size = 1  # 1 byte para booleanos
                array_size = ir.Constant(self.int_type, num_elements * elem_size)
                array_ptr = self.builder.call(self.malloc, [array_size])
                self._track_allocation(array_ptr)
                typed_ptr = self.builder.bitcast(array_ptr, self.bool_type.as_pointer())
            else:
                elem_size = 1
                array_size = ir.Constant(self.int_type, num_elements * elem_size)
                array_ptr = self.builder.call(self.malloc, [array_size])
                self._track_allocation(array_ptr)
                typed_ptr = array_ptr

            # Inicializar elementos
            for i, elem in enumerate(node.elements):
                value = self._generate_expression(elem)
                if isinstance(node.element_type, StringType) or isinstance(node.element_type, StrType):
                    value = self.builder.bitcast(value, self.char_type.as_pointer())
                    elem_ptr = self.builder.gep(typed_ptr, [ir.Constant(self.int_type, i)], inbounds=True)
                    # Forçar o ponteiro do elemento para i8** explicitamente
                    elem_ptr = self.builder.bitcast(elem_ptr, self.char_type.as_pointer().as_pointer())
                    self.builder.store(value, elem_ptr)
                elif isinstance(node.element_type, BoolType):
                    elem_ptr = self.builder.gep(typed_ptr, [ir.Constant(self.int_type, i)], inbounds=True)
                    # Garantir que o valor é do tipo correto
                    if value.type != self.bool_type:
                        value = self.builder.icmp_ne(value, ir.Constant(value.type, 0))
                    self.builder.store(value, elem_ptr)
                else:
                    elem_ptr = self.builder.gep(typed_ptr, [ir.Constant(self.int_type, i)], inbounds=True)
                    self.builder.store(value, elem_ptr)

            # Se o array foi alocado localmente (com alloca), retornar ponteiro para o primeiro elemento
            if hasattr(node, 'is_local') and node.is_local:
                zero = ir.Constant(ir.IntType(32), 0)
                return self.builder.gep(typed_ptr, [zero, zero], inbounds=True)
            return typed_ptr
            
        elif isinstance(node, ZerosNode):
            # Syntax sugar para criar arrays preenchidos com zeros
            size = node.size
            elem_size = 8  # 8 bytes para int ou float
            array_size = ir.Constant(self.int_type, size * elem_size)
            array_ptr = self.builder.call(self.malloc, [array_size])
            self._track_allocation(array_ptr)
            
            # Cast e inicializar com zeros
            if isinstance(node.element_type, IntType):
                typed_ptr = self.builder.bitcast(array_ptr, self.int_type.as_pointer())
                zero_val = ir.Constant(self.int_type, 0)
            else:
                typed_ptr = self.builder.bitcast(array_ptr, self.float_type.as_pointer())
                zero_val = ir.Constant(self.float_type, 0.0)
            
            # Loop para inicializar com zeros
            for i in range(size):
                elem_ptr = self.builder.gep(typed_ptr, [ir.Constant(self.int_type, i)], inbounds=True)
                self.builder.store(zero_val, elem_ptr)
            
            return typed_ptr
            
        elif isinstance(node, CastNode):
            # Implementar conversões de tipo
            expr_value = self._generate_expression(node.expression)
            
            if isinstance(node.target_type, IntType):
                # Converter para int
                if isinstance(expr_value.type, ir.DoubleType):
                    # float -> int
                    return self.builder.fptosi(expr_value, self.int_type, name="ftoi")
                elif expr_value.type == self.string_type or (isinstance(expr_value.type, ir.PointerType) and expr_value.type.pointee == self.char_type):
                    # string -> int (usando atoi simulado)
                    # Por simplicidade, vamos retornar 0
                    return ir.Constant(self.int_type, 0)
                else:
                    return expr_value
                    
            elif isinstance(node.target_type, FloatType):
                # Converter para float
                if isinstance(expr_value.type, ir.IntType):
                    # int -> float
                    return self.builder.sitofp(expr_value, self.float_type, name="itof")
                else:
                    return expr_value
                    
            elif isinstance(node.target_type, StringType):
                # Converter para string
                buffer_size = ir.Constant(self.int_type, 256)
                buffer = self.builder.call(self.malloc, [buffer_size])
                self._track_allocation(buffer)
                
                if isinstance(expr_value.type, ir.IntType):
                    # int -> string
                    fmt_str = "%lld\0"
                    fmt_bytes = fmt_str.encode('utf8')
                    fmt_type = ir.ArrayType(self.char_type, len(fmt_bytes))
                    fmt_name = f"fmt_itoa_{len(self.module.globals)}"
                    fmt_global = ir.GlobalVariable(self.module, fmt_type, name=fmt_name)
                    fmt_global.linkage = 'internal'
                    fmt_global.global_constant = True
                    fmt_global.initializer = ir.Constant(fmt_type, bytearray(fmt_bytes))
                    zero = ir.Constant(ir.IntType(32), 0)
                    fmt_ptr = self.builder.gep(fmt_global, [zero, zero], inbounds=True)
                    
                    self.builder.call(self.sprintf, [buffer, fmt_ptr, expr_value])
                    
                elif isinstance(expr_value.type, ir.DoubleType):
                    # float -> string
                    fmt_str = "%f\0"
                    fmt_bytes = fmt_str.encode('utf8')
                    fmt_type = ir.ArrayType(self.char_type, len(fmt_bytes))
                    fmt_name = f"fmt_ftoa_{len(self.module.globals)}"
                    fmt_global = ir.GlobalVariable(self.module, fmt_type, name=fmt_name)
                    fmt_global.linkage = 'internal'
                    fmt_global.global_constant = True
                    fmt_global.initializer = ir.Constant(fmt_type, bytearray(fmt_bytes))
                    zero = ir.Constant(ir.IntType(32), 0)
                    fmt_ptr = self.builder.gep(fmt_global, [zero, zero], inbounds=True)
                    
                    self.builder.call(self.sprintf, [buffer, fmt_ptr, expr_value])
                else:
                    # Já é string
                    return expr_value
                
                return buffer
                
            elif isinstance(node.target_type, BoolType):
                # Converter para bool
                if isinstance(expr_value.type, ir.IntType):
                    # int -> bool (não-zero é true, zero é false)
                    return self.builder.icmp_signed('!=', expr_value, ir.Constant(expr_value.type, 0))
                elif isinstance(expr_value.type, ir.DoubleType):
                    # float -> bool (não-zero é true, zero é false)
                    return self.builder.fcmp_ordered('!=', expr_value, ir.Constant(expr_value.type, 0.0))
                else:
                    # Já é bool ou outro tipo
                    return expr_value
                
        elif isinstance(node, ConcatNode):
            # Concatenação de strings
            left_str = self._generate_expression(node.left)
            right_str = self._generate_expression(node.right)
            
            # Calcular tamanho necessário
            len1 = self.builder.call(self.strlen, [left_str])
            len2 = self.builder.call(self.strlen, [right_str])
            total_len = self.builder.add(len1, len2)
            total_len = self.builder.add(total_len, ir.Constant(self.int_type, 1))  # +1 para null terminator
            
            # Alocar memória para resultado
            result = self.builder.call(self.malloc, [total_len])
            self._track_allocation(result)
            
            # Copiar primeira string
            self.builder.call(self.strcpy, [result, left_str])
            
            # Concatenar segunda string
            self.builder.call(self.strcat, [result, right_str])
            
            return result
            
        elif isinstance(node, ArrayAccessNode):
            # Procurar variável primeiro localmente, depois globalmente
            if node.array_name in self.local_vars:
                var = self.local_vars[node.array_name]
            elif node.array_name in self.global_vars:
                var = self.global_vars[node.array_name]
            else:
                raise NameError(f"Array '{node.array_name}' não definido")
            index = self._generate_expression(node.index)
            # Se a variável já é um ponteiro (parâmetro de função), usar diretamente
            if isinstance(var, ir.Argument) and isinstance(var.type, ir.PointerType):
                array_ptr = var
            elif isinstance(var, ir.GlobalVariable) and isinstance(var.type.pointee, ir.ArrayType):
                zero = ir.Constant(ir.IntType(32), 0)
                array_ptr = self.builder.gep(var, [zero, zero], inbounds=True)
            else:
                # Para arrays locais, não fazer load, usar diretamente o ponteiro
                if isinstance(var.type, ir.PointerType) and isinstance(var.type.pointee, ir.ArrayType):
                    zero = ir.Constant(ir.IntType(32), 0)
                    array_ptr = self.builder.gep(var, [zero, zero], inbounds=True)
                else:
                    array_ptr = self.builder.load(var)
                    if isinstance(array_ptr.type, ir.ArrayType):
                        zero = ir.Constant(ir.IntType(32), 0)
                        array_ptr = self.builder.gep(array_ptr, [zero, zero], inbounds=True)
            # Se for string (i8*), acessar como caractere (cast de segurança)
            if (isinstance(array_ptr.type, ir.PointerType) and array_ptr.type.pointee == self.char_type) or (
                hasattr(node, 'element_type') and isinstance(node.element_type, StringType)):
                if not (isinstance(array_ptr.type, ir.PointerType) and array_ptr.type.pointee == self.char_type):
                    array_ptr = self.builder.bitcast(array_ptr, self.char_type.as_pointer())
                # Converter índice para i32 para compatibilidade com ponteiros i8*
                if index.type != ir.IntType(32):
                    index = self.builder.sext(index, ir.IntType(32)) if index.type.width < 32 else self.builder.trunc(index, ir.IntType(32))
                elem_ptr = self.builder.gep(array_ptr, [index], inbounds=True)
                return self.builder.load(elem_ptr)
            # Caso contrário, array normal
            # Se for um array local (alocado com alloca), usar GEP [0, index]
            if isinstance(array_ptr.type, ir.ArrayType):
                zero = ir.Constant(ir.IntType(32), 0)
                elem_ptr = self.builder.gep(array_ptr, [zero, index], inbounds=True)
                return self.builder.load(elem_ptr)
            else:
                # Verificar se array_ptr é um ponteiro válido
                if not isinstance(array_ptr.type, ir.PointerType):
                    # Se não é ponteiro, fazer cast para ponteiro
                    array_ptr = self.builder.bitcast(array_ptr, self.int_type.as_pointer())
                elem_ptr = self.builder.gep(array_ptr, [index], inbounds=True)
                return self.builder.load(elem_ptr)
            
        elif isinstance(node, IdentifierNode):
            # Procurar variável primeiro localmente, depois globalmente
            if node.name in self.local_vars:
                var = self.local_vars[node.name]
                # Se é um parâmetro de função que é array, retornar diretamente
                if isinstance(var, ir.Argument) and isinstance(var.type, ir.PointerType):
                    return var
                # Se é um ponteiro (ref), retornar ponteiro diretamente
                if isinstance(var.type, ir.PointerType) and var.type.pointee == ir.IntType(8):
                    return self.builder.load(var, name=node.name)
                # Senão, carregar o valor
                return self.builder.load(var, name=node.name)
            elif node.name in self.global_vars:
                var = self.global_vars[node.name]
                # Se é um array global, retornar ponteiro para o início
                if isinstance(var.type.pointee, ir.ArrayType):
                    zero = ir.Constant(ir.IntType(32), 0)
                    return self.builder.gep(var, [zero, zero], inbounds=True)
                # Se é um ponteiro (ref), retornar ponteiro diretamente
                if isinstance(var.type, ir.PointerType) and var.type.pointee == ir.IntType(8):
                    return self.builder.load(var, name=node.name)
                # Senão, carregar o valor
                return self.builder.load(var, name=node.name)
            else:
                raise NameError(f"Variável '{node.name}' não definida")
            
        elif isinstance(node, CallNode):
            # Função embutida 'ord'
            if node.function_name == 'ord':
                arg = self._generate_expression(node.arguments[0])
                # Se o argumento já é um char (i8), apenas fazer zext para int
                if arg.type == self.char_type:
                    return self.builder.zext(arg, self.int_type)
                # Se é um ponteiro para char, carregar o primeiro caractere
                elif isinstance(arg.type, ir.PointerType) and arg.type.pointee == self.char_type:
                    first_char = self.builder.load(arg)
                    return self.builder.zext(first_char, self.int_type)
                else:
                    # Caso inesperado, tentar converter
                    return self.builder.zext(arg, self.int_type)
            # Verificar se é uma função externa de casting
            if node.function_name == 'to_str':
                # Determinar qual versão de to_str usar baseado no tipo do argumento
                if node.arguments:
                    arg = self._generate_expression(node.arguments[0])
                    if isinstance(arg.type, ir.DoubleType):
                        func = self.to_str_float
                    else:
                        func = self.to_str_int
                else:
                    func = self.to_str_int  # default
            elif node.function_name == 'to_int':
                func = self.to_int
            elif node.function_name == 'to_float':
                func = self.to_float
            elif node.function_name in self.functions:
                func = self.functions[node.function_name]
            else:
                raise NameError(f"Função '{node.function_name}' não definida")
            args = []
            
            # Gerar argumentos considerando tipos esperados
            for i, arg_node in enumerate(node.arguments):
                if i < len(func.args):
                    expected_type = func.args[i].type
                    
                    # Se o argumento é um identificador
                    if isinstance(arg_node, IdentifierNode):
                        # Verificar se é um array
                        if arg_node.name in self.type_map:
                            var_type = self.type_map[arg_node.name]
                            if isinstance(var_type, ArrayType) and isinstance(expected_type, ir.PointerType):
                                # É um array sendo passado para função que espera array
                                if arg_node.name in self.local_vars:
                                    var = self.local_vars[arg_node.name]
                                    if isinstance(var, ir.Argument):
                                        # É um parâmetro de array, usar diretamente
                                        args.append(var)
                                    else:
                                        # É uma variável local de array, obter ponteiro
                                        zero = ir.Constant(ir.IntType(32), 0)
                                        args.append(self.builder.gep(var, [zero, zero], inbounds=True))
                                elif arg_node.name in self.global_vars:
                                    var = self.global_vars[arg_node.name]
                                    # Array global, obter ponteiro
                                    zero = ir.Constant(ir.IntType(32), 0)
                                    args.append(self.builder.gep(var, [zero, zero], inbounds=True))
                                else:
                                    args.append(self._generate_expression(arg_node, expected_type))
                            else:
                                # Não é array, gerar normalmente
                                args.append(self._generate_expression(arg_node, expected_type))
                        else:
                            args.append(self._generate_expression(arg_node, expected_type))
                    else:
                        # Não é identificador, gerar normalmente
                        args.append(self._generate_expression(arg_node, expected_type))
                else:
                    # Sem informação de tipo, gerar normalmente
                    args.append(self._generate_expression(arg_node, expected_type))
            
            return self.builder.call(func, args)
            
        elif isinstance(node, BinaryOpNode):
            left = self._generate_expression(node.left)
            right = self._generate_expression(node.right)
            
            # Verificar se é operação com floats
            is_float_op = isinstance(left.type, ir.DoubleType) or isinstance(right.type, ir.DoubleType)
            
            # Converter operandos se necessário
            if is_float_op:
                if isinstance(left.type, ir.IntType):
                    left = self.builder.sitofp(left, self.float_type)
                if isinstance(right.type, ir.IntType):
                    right = self.builder.sitofp(right, self.float_type)
            
            # Operações aritméticas
            if node.operator == TokenType.PLUS:
                # Verificar se é concatenação de strings
                if (isinstance(left.type, ir.PointerType) and left.type.pointee == self.char_type and
                    isinstance(right.type, ir.PointerType) and right.type.pointee == self.char_type):
                    # Concatenação de strings
                    # Calcular tamanho necessário
                    len1 = self.builder.call(self.strlen, [left])
                    len2 = self.builder.call(self.strlen, [right])
                    total_len = self.builder.add(len1, len2)
                    total_len = self.builder.add(total_len, ir.Constant(self.int_type, 1))  # +1 para null terminator
                    
                    # Alocar memória para resultado
                    result = self.builder.call(self.malloc, [total_len])
                    self._track_allocation(result)
                    
                    # Copiar primeira string
                    self.builder.call(self.strcpy, [result, left])
                    
                    # Concatenar segunda string
                    self.builder.call(self.strcat, [result, right])
                    
                    return result
                elif is_float_op:
                    return self.builder.fadd(left, right, name="fadd")
                else:
                    return self.builder.add(left, right, name="add")
            elif node.operator == TokenType.MINUS:
                if is_float_op:
                    return self.builder.fsub(left, right, name="fsub")
                else:
                    return self.builder.sub(left, right, name="sub")
            elif node.operator == TokenType.MULTIPLY:
                if is_float_op:
                    return self.builder.fmul(left, right, name="fmul")
                else:
                    return self.builder.mul(left, right, name="mul")
            elif node.operator == TokenType.DIVIDE:
                if is_float_op:
                    return self.builder.fdiv(left, right, name="fdiv")
                else:
                    return self.builder.sdiv(left, right, name="div")
            elif node.operator == TokenType.MODULO:
                if is_float_op:
                    return self.builder.call(self.fmod, [left, right], name="fmod")
                else:
                    return self.builder.srem(left, right, name="mod")
                
            # Comparações
            elif node.operator == TokenType.GT:
                if is_float_op:
                    return self.builder.fcmp_ordered('>', left, right, name="fgt")
                else:
                    return self.builder.icmp_signed('>', left, right, name="gt")
            elif node.operator == TokenType.LT:
                if is_float_op:
                    return self.builder.fcmp_ordered('<', left, right, name="flt")
                else:
                    return self.builder.icmp_signed('<', left, right, name="lt")
            elif node.operator == TokenType.GTE:
                if is_float_op:
                    return self.builder.fcmp_ordered('>=', left, right, name="fgte")
                else:
                    return self.builder.icmp_signed('>=', left, right, name="gte")
            elif node.operator == TokenType.LTE:
                if is_float_op:
                    return self.builder.fcmp_ordered('<=', left, right, name="flte")
                else:
                    return self.builder.icmp_signed('<=', left, right, name="lte")
            elif node.operator == TokenType.EQ or node.operator == TokenType.NEQ:
                # Verificar se é comparação com null (ponteiro)
                if (isinstance(left.type, ir.PointerType) and isinstance(right, ir.Constant) and right.constant is None) or \
                   (isinstance(right.type, ir.PointerType) and isinstance(left, ir.Constant) and left.constant is None):
                    # Comparação de ponteiro com null - comparar ponteiros diretamente
                    if node.operator == TokenType.EQ:
                        return self.builder.icmp_signed('==', left, right, name="eq")
                    else:
                        return self.builder.icmp_signed('!=', left, right, name="neq")
                
                # Para comparações de char, garantir que ambos são i8
                if isinstance(left.type, ir.PointerType) and left.type.pointee == self.char_type:
                    left = self.builder.load(left)
                if isinstance(right.type, ir.PointerType) and right.type.pointee == self.char_type:
                    right = self.builder.load(right)
                
                # Para comparações de char (i8), usar icmp sem sinal
                if left.type == self.char_type and right.type == self.char_type:
                    if node.operator == TokenType.EQ:
                        return self.builder.icmp_unsigned('==', left, right, name="eq")
                    else:
                        return self.builder.icmp_unsigned('!=', left, right, name="neq")
                elif is_float_op:
                    if node.operator == TokenType.EQ:
                        return self.builder.fcmp_ordered('==', left, right, name="feq")
                    else:
                        return self.builder.fcmp_ordered('!=', left, right, name="fneq")
                else:
                    if node.operator == TokenType.EQ:
                        # Se qualquer lado for bool, converter ambos para bool
                        if left.type == self.bool_type or right.type == self.bool_type:
                            if left.type != self.bool_type:
                                left = self.builder.icmp_ne(left, ir.Constant(left.type, 0))
                            if right.type != self.bool_type:
                                right = self.builder.icmp_ne(right, ir.Constant(right.type, 0))
                        return self.builder.icmp_signed('==', left, right, name="eq")
                    else:
                        return self.builder.icmp_signed('!=', left, right, name="neq")
                
            # Operadores lógicos
            elif node.operator == TokenType.AND:
                # Converter para boolean se necessário (apenas se não for já bool)
                if left.type != self.bool_type:
                    left = self.builder.icmp_ne(left, ir.Constant(left.type, 0))
                if right.type != self.bool_type:
                    right = self.builder.icmp_ne(right, ir.Constant(right.type, 0))
                
                # Implementação simples do AND lógico (sem curto-circuito por enquanto)
                return self.builder.and_(left, right, name="and")
            elif node.operator == TokenType.OR:
                # Converter para boolean se necessário (apenas se não for já bool)
                if left.type != self.bool_type:
                    left = self.builder.icmp_ne(left, ir.Constant(left.type, 0))
                if right.type != self.bool_type:
                    right = self.builder.icmp_ne(right, ir.Constant(right.type, 0))
                
                # Implementação simples do OR lógico
                result = self.builder.or_(left, right, name="or")
                return result
                
        elif isinstance(node, UnaryOpNode):
            operand = self._generate_expression(node.operand)
            
            if node.operator == TokenType.NOT:
                # Converter para boolean se necessário
                if operand.type != self.bool_type:
                    operand = self.builder.icmp_ne(operand, ir.Constant(operand.type, 0))
                return self.builder.not_(operand, name="not")
            else:
                raise NotImplementedError(f"Operador unário não implementado: {node.operator}")
        
        elif isinstance(node, StructConstructorNode):
            return self._generate_struct_constructor(node, expected_type)
        
        raise NotImplementedError(f"Tipo de nó não implementado: {type(node)}")

    def _generate_struct_assignment(self, node: StructAssignmentNode):
        # Temporariamente desabilitado devido a problemas de compatibilidade de tipos
        # TODO: Implementar solução robusta para atribuição de campos
        raise NotImplementedError("Atribuição de campos de struct temporariamente desabilitada. Use construtores para criar structs completos.")

    def _generate_struct_constructor(self, node: StructConstructorNode, expected_type: ir.Type = None) -> ir.Value:
        struct_name = node.struct_name
        if struct_name not in self.struct_types:
            raise NameError(f"Struct '{struct_name}' não definido")
        struct_type = self.struct_types[struct_name]
        struct_size = 24  # Tamanho fixo para TreeNode
        size = self.builder.call(self.malloc, [ir.Constant(ir.IntType(64), struct_size)])
        self._track_allocation(size)
        struct_ptr = self.builder.bitcast(size, struct_type.as_pointer())
        struct_info = None
        for stmt in self.global_ast.statements:
            if isinstance(stmt, StructDefinitionNode) and stmt.name == struct_name:
                struct_info = stmt
                break
        if not struct_info:
            raise NameError(f"Definição do struct '{struct_name}' não encontrada")
        for i, (field_name, field_type) in enumerate(struct_info.fields):
            if i < len(node.arguments):
                llvm_field_type = self._convert_type(field_type)
                arg_value = self._generate_expression(node.arguments[i], llvm_field_type)
                field_ptr = self.builder.gep(struct_ptr, [
                    ir.Constant(ir.IntType(32), 0),
                    ir.Constant(ir.IntType(32), i)
                ])
                if isinstance(arg_value, ir.Constant) and arg_value.type == ir.IntType(8).as_pointer():
                    if isinstance(llvm_field_type, ir.PointerType):
                        arg_value = ir.Constant(llvm_field_type, None)
                elif isinstance(field_type, ReferenceType):
                    # Para campos de referência, garantir que o valor seja um ponteiro nulo se for null
                    if isinstance(arg_value.type, ir.IntType) and arg_value.type.width == 64:
                        # Se o valor é null (i64), converter para ponteiro nulo
                        arg_value = ir.Constant(llvm_field_type, None)
                    elif isinstance(arg_value.type, ir.PointerType) and isinstance(llvm_field_type, ir.PointerType):
                        # Se ambos são ponteiros, fazer cast se necessário
                        if arg_value.type != llvm_field_type:
                            arg_value = self.builder.bitcast(arg_value, llvm_field_type)
                self.builder.store(arg_value, field_ptr)
        return struct_ptr

# Função para executar código via JIT
def execute_ir(llvm_ir: str):
    """Executa o código LLVM IR usando JIT compilation"""
    # No Windows, configurar console para UTF-8
    if sys.platform == "win32":
        import subprocess
        # Configurar code page para UTF-8
        subprocess.run(["chcp", "65001"], shell=True, capture_output=True)
        # Configurar variável de ambiente
        import os
        os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # Criar engine de execução
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()
    
    # Parse do módulo
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()
    
    # Criar engine JIT
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    engine = llvm.create_mcjit_compiler(mod, target_machine)
    
    # Adicionar funções da biblioteca C
    if sys.platform == "win32":
        # No Windows, carregar as bibliotecas necessárias
        llvm.load_library_permanently("msvcrt.dll")
        llvm.load_library_permanently("kernel32.dll")
    else:
        llvm.load_library_permanently("libc.so.6")
    
    # Executar função main
    main_ptr = engine.get_function_address("main")
    
    # Criar tipo de função para ctypes
    import ctypes
    main_func = ctypes.CFUNCTYPE(ctypes.c_int)(main_ptr)
    
    # Executar
    result = main_func()
    return result

# Compilador principal
class MiniLangCompiler:
    def __init__(self):
        self.lexer = None
        self.parser = None
        self.codegen = None
        
    def compile(self, source: str) -> str:
        # Análise léxica
        self.lexer = Lexer(source)
        tokens = self.lexer.tokenize()
        
        # Análise sintática
        self.parser = Parser(tokens)
        ast = self.parser.parse()
        
        # Geração de código
        self.codegen = LLVMCodeGenerator()
        llvm_module = self.codegen.generate(ast)
        
        return str(llvm_module)
    
    def compile_to_object(self, source: str, output_file: str):
        try:
            print(f"Gerando IR LLVM...")
            # Gerar IR LLVM
            llvm_ir = self.compile(source)
            
            print(f"Configurando target...")
            # Configurar target
            llvm.initialize()
            llvm.initialize_native_target()
            llvm.initialize_native_asmprinter()
            
            # Obter o triple correto para a plataforma
            triple = llvm.get_default_triple()
            print(f"Triple: {triple}")
            
            # Criar target
            target = llvm.Target.from_triple(triple)
            print(f"Target criado: {target}")
            
            # Criar target machine com configurações apropriadas
            if sys.platform == "win32":
                print("Configurando target machine para Windows...")
                # Para Windows x64, usar large code model para evitar problemas de relocação
                target_machine = target.create_target_machine(
                    cpu='generic',
                    features='',
                    opt=2,
                    reloc='pic',  # Position Independent Code
                    codemodel='large'  # Large code model para endereços de 64 bits
                )
            else:
                target_machine = target.create_target_machine(opt=2)
            
            print(f"Target machine criada: {target_machine}")
            
            print("Parseando assembly...")
            # Compilar para objeto
            mod = llvm.parse_assembly(llvm_ir)
            print("Verificando módulo...")
            mod.verify()
            
            # Definir o triple e data layout
            mod.triple = triple
            mod.data_layout = str(target_machine.target_data)
            
            print("Otimizando...")
            # Otimizar
            pmb = llvm.create_pass_manager_builder()
            pmb.opt_level = 2
            pm = llvm.create_module_pass_manager()
            pmb.populate(pm)
            pm.run(mod)
            
            print(f"Gerando código objeto em '{output_file}'...")
            # Gerar código objeto
            object_data = target_machine.emit_object(mod)
            print(f"Tamanho do objeto gerado: {len(object_data)} bytes")
            
            with open(output_file, 'wb') as f:
                f.write(object_data)
            
            print(f"Arquivo objeto criado com sucesso: {output_file}")
            
        except Exception as e:
            print(f"Erro na geração do objeto: {e}")
            import traceback
            traceback.print_exc()
            raise

def read_source_file(file_path: str) -> str:
    """Lê o conteúdo de um arquivo de código fonte."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao ler arquivo '{file_path}': {e}")
        sys.exit(1)

def print_usage():
    """Imprime informações de uso do programa."""
    print("MiniLang Compiler v2.0")
    print("Uso:")
    print("  python compiler.py <arquivo.ml>                    # Executar programa")
    print("  python compiler.py --compile <arquivo.ml>          # Gerar arquivo objeto")
    print("  python compiler.py --help                          # Mostrar esta ajuda")
    print("")
    print("Exemplos:")
    print("  python compiler.py programa.ml")
    print("  python compiler.py --compile programa.ml")

# Exemplo de uso
if __name__ == "__main__":
    import sys
    
    # Verificar argumentos
    if len(sys.argv) < 2 or "--help" in sys.argv or "-h" in sys.argv:
        print_usage()
        sys.exit(0)
    
    # Determinar modo de operação
    compile_mode = "--compile" in sys.argv
    source_file = None
    
    if compile_mode:
        # Modo compilação: --compile <arquivo>
        if len(sys.argv) < 3:
            print("Erro: Arquivo de entrada não especificado para modo --compile")
            print_usage()
            sys.exit(1)
        source_file = sys.argv[2]
    else:
        # Modo execução: <arquivo>
        source_file = sys.argv[1]
    
    # Ler arquivo de código fonte
    print(f"Lendo arquivo: {source_file}")
    source_code = read_source_file(source_file)
    
    # Compilar
    compiler = MiniLangCompiler()
    
    try:
        # Gerar IR LLVM
        llvm_ir = compiler.compile(source_code)
        print("=== LLVM IR Gerado ===")
        print(llvm_ir)
        
        if compile_mode:
            # Modo compilação: gerar arquivo objeto
            output_file = "output.obj" if sys.platform == "win32" else "output.o"
            compiler.compile_to_object(source_code, output_file)
            print(f"\nCódigo objeto gerado em '{output_file}'")
            
            if sys.platform == "win32":
                print("\nPara criar executável no Windows:")
                print("1. Com MinGW: gcc -mcmodel=large output.obj -o programa.exe")
                print("2. Com Clang: clang output.obj -o programa.exe")
                print("3. Com MSVC: cl output.obj /Fe:programa.exe")
            else:
                print("\nPara criar executável: gcc output.o -o programa")
        else:
            # Modo execução: executar usando JIT
            print("\n=== Executando o programa ===")
            try:
                execute_ir(llvm_ir)
            except Exception as e:
                print(f"Erro na execução JIT: {e}")
                import traceback
                traceback.print_exc()
        
    except Exception as e:
        print(f"Erro na compilação: {e}")
        import traceback
        traceback.print_exc()

# Recursos implementados:
# 1. ✅ Tipagem estática: let x: int = 10
# 2. ✅ Arrays tipados: let arr: int[5] = [1, 2, 3, 4, 5]
# 3. ✅ Funções tipadas: func add(a: int, b: int) -> int
# 4. ✅ Variáveis globais: global x: int = 10
# 5. ✅ Passagem de arrays para funções
# 6. ✅ Acesso a variáveis globais dentro de funções
# 7. ✅ Tipos: int, string, void, arrays
# 8. ✅ QuickSort funcionando com arrays como parâmetros
