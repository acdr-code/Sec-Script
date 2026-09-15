from lark import Lark

grammar = r"""
    start: statement+

    statement: func_call
             | let_stmt
             | if_stmt
             | for_stmt
             | while_stmt

    if_stmt: "if" "(" expr ")" "{" statement+ "}" ["else" "{" statement+ "}"]

    func_call: NAME "(" expr ")"

    let_stmt: "let" NAME "be" expr

    for_stmt: "for" NAME "from" expr "to" expr "{" statement+ "}"

    while_stmt: "while" expr "{" statement+ "}"

    ?expr: comparison
         | atom

    comparison: atom COMP_OP atom

    atom: NUMBER
        | ESCAPED_STRING
        | TRUE
        | FALSE
        | NAME

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