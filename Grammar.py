from lark import Lark

grammar = r"""
    start: statement+

    statement: func_call
             | let_stmt
             | if_stmt
             | for_stmt
             | foreach_stmt
             | while_stmt

    if_stmt: "if" "(" expr ")" "{" statement+ "}" ["else" "{" statement+ "}"]

    func_call: NAME "(" expr ")"

    let_stmt: "let" NAME "be" expr

    for_stmt: "for" NAME "from" expr "to" expr "{" statement+ "}"

    while_stmt: "while" expr "{" statement+ "}"

    foreach_stmt: "for" NAME "in" NAME "{" statement+ "}"

    ?expr: comparison
         | atom
         | list

    list: "[" (expr ("," expr)*)? "]"

    index_access: NAME "[" expr "]"

    comparison: atom COMP_OP atom

    atom: NUMBER
        | ESCAPED_STRING
        | TRUE
        | FALSE
        | NAME
        | index_access

    COMP_OP: "==" | "!=" | "<" | ">" | "<=" | ">="
    TRUE: "True"
    FALSE: "False"

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS
"""

parser = Lark(grammar, start="start", parser="lalr")