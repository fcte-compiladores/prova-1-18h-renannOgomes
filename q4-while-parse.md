Nosso interpretador nao possui suporte a lacos. Nessa questao, vamos implementar
o suporte ao comando `while`.

A sintaxe do Lox é a mesma da familia C:

```lox
while (cond) {
    // comandos
}
```

Assim como em C, é possivel trocar o bloco de comandos por um unico comando 
simples, como por exemplo 

```lox
while (cond) print x;
```

No entando, nao podemos trocar o bloco por declaracões de classe, funcao ou 
variaveis.

```lox
while (cond) var x = 42; // invalido!
```

Implemente suporte para o `while` na linguagem primeiro editando o arquivo
grammar.lark e acrescentando as regras necessarias. Depois, modifique o arquivo
lox/ast.py e declare os atributos necessarios na classe `lox.ast.While`. Nao é
necessario implementar o método eval ainda. Finalmente, edite `lox.transformer.LoxTransformer` para realizar a conversao de arvores Lark para a nossa classe
especializada `lox.ast.While`.


## Apêndice: Gramatica Lox

```
// DECLARAcÕES
declaration    → classDecl
               | funDecl
               | varDecl
               | statement ;

classDecl      → "class" IDENTIFIER ( "<" IDENTIFIER )?
                 "{" function* "}" ;
funDecl        → "fun" function ;
varDecl        → "var" IDENTIFIER ( "=" expression )? ";" ;


// COMANDOS
statement      → exprStmt
               | forStmt
               | ifStmt
               | printStmt
               | returnStmt
               | whileStmt
               | block ;

exprStmt       → expression ";" ;
forStmt        → "for" "(" ( varDecl | exprStmt | ";" )
                           expression? ";"
                           expression? ")" statement ;
ifStmt         → "if" "(" expression ")" statement
                 ( "else" statement )? ;
printStmt      → "print" expression ";" ;
returnStmt     → "return" expression? ";" ;
whileStmt      → "while" "(" expression ")" statement ;
block          → "{" declaration* "}" ;


// EXPRESSÕES
expression     → assignment ;

assignment     → ( call "." )? IDENTIFIER "=" assignment
               | logic_or ;

logic_or       → logic_and ( "or" logic_and )* ;
logic_and      → equality ( "and" equality )* ;
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;

unary          → ( "!" | "-" ) unary | call ;
call           → primary ( "(" arguments? ")" | "." IDENTIFIER )* ;
primary        → "true" | "false" | "nil" | "this"
               | NUMBER | STRING | IDENTIFIER | "(" expression ")"
               | "super" "." IDENTIFIER ;

// OUTROS
function       → IDENTIFIER "(" parameters? ")" block ;
parameters     → IDENTIFIER ( "," IDENTIFIER )* ;
arguments      → expression ( "," expression )* ;
```