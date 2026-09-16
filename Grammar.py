from lark import Lark

grammar = r"""
    start: statement+

    statement: func_call
             | let_stmt
             | if_stmt
             | for_stmt
             | foreach_stmt
             | while_stmt
             | function_stmt
             | return_stmt

    if_stmt: "if" "(" expr ")" "{" statement+ "}" ["else" "{" statement+ "}"]

    func_call: NAME "(" args ")"
    args: (expr ("," expr)*)?

    let_stmt: "let" NAME "be" expr

    for_stmt: "for" NAME "from" expr "to" expr "{" statement+ "}"

    while_stmt: "while" expr "{" statement+ "}"

    foreach_stmt: "for" NAME "in" NAME "{" statement+ "}"

    function_stmt: "FUNCTION" NAME "(" params ")" "{" statement+ "}"
    params: (NAME ("," NAME)*)?

    return_stmt: "GIVE" expr

    COMMENT: /\/\/[^\n]*/

    ?expr: comparison
         | atom
         | list
         | math_ing
         | connect_ing

    list: "[" (expr ("," expr)*)? "]"

    index_access: NAME "[" expr "]"

    comparison: atom COMP_OP atom
    math_ing: atom MATH_OP atom
    connect_ing: atom CONNECT_OP atom

    atom: NUMBER
        | ESCAPED_STRING
        | TRUE
        | FALSE
        | NAME
        | index_access
        | func_call

    COMP_OP: "==" | "!=" | "<" | ">" | "<=" | ">="
    MATH_OP: "+" | "-" | "/" | "*"
    CONNECT_OP: "&"
    TRUE: "True"
    FALSE: "False"

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS
    %ignore COMMENT
"""

parser = Lark(grammar, start="start", parser="lalr")