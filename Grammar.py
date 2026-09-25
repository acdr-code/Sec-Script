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
             | shell_stmt

    if_stmt: "if" "(" expr ")" "{" statement+ "}" ["else" "{" statement+ "}"]

    func_call: NAME "(" args ")"
    args: (expr ("," expr)*)?

    let_stmt: "let" NAME "be" expr

    for_stmt: "for" NAME "from" expr "to" expr "{" statement+ "}"

    while_stmt: "while" expr "{" statement+ "}"

    foreach_stmt: "for" NAME "in" NAME "{" statement+ "}"

    function_stmt: "function" NAME "(" params ")" "{" statement+ "}"
    params: (NAME ("," NAME)*)?

    return_stmt: "give" expr

    COMMENT: /\/\/[^\n]*/

    dict: "{" (pair (";" pair)*)? ";"? "}"
    pair: NAME ":" expr

    ?expr: comparison
         | atom
         | list
         | math_ing
         | connect_ing
         | dict

    list: "[" (expr ("," expr)*)? "]"

    index_access: NAME "[" expr "]"

    scan_stmt: "scan" expr "ports" expr "::" expr "delay" expr

    webindex_stmt: "find" expr "in" expr

    sniffing_stmt: "sniff" "::"  "iface" expr "count" expr "filter" expr "delay" expr

    shell_stmt: "sshConnect" expr "password" expr "on" "port" expr "{" statement+ "}"
    run_ing: "run" expr

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
        | scan_stmt
        | webindex_stmt
        | sniffing_stmt
        | run_ing

    COMP_OP: "==" | "!=" | "<" | ">" | "<=" | ">="
    MATH_OP: "+" | "-" | "/" | "*"
    CONNECT_OP: "&"
    TRUE: "true"
    FALSE: "false"

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS
    %ignore COMMENT
"""

parser = Lark(grammar, start="start", parser="lalr")