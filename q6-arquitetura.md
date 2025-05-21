De modo abstrato, o compilador é um programa que converte código de uma
linguagem para outra. Como se fosse uma funcao do tipo `compilador(str) -> str`.
No caso de compiladores que emitem código de maquina ou bytecode, seria mais
preciso dizer `compilador(str) -> bytes`, mas a idéia basica é a mesma.

De forma geral o processo é dividido em etapas como abaixo

```python
def compilador(x1: str) -> str | bytes:
    x2 = lex(x1)        # analise léxica
    x3 = parse(x2)      # analise sintatica
    x4 = analysis(x3)   # analise semântica
    x5 = optimize(x4)   # otimizacao
    x6 = codegen(x5)    # geracao de código
    return x6
```

Defina brevemente o que cada uma dessas etapas realizam e marque quais seriam os
tipos de entrada e saida de cada uma dessas funcões. Explique de forma clara o
que eles representam. Você pode usar exemplos de linguagens e/ou compiladores
conhecidos para ilustrar sua resposta. Salve sua resposta nesse arquivo.

# lex(?) -> ?
Complete as ? e responda aqui!
 
# parse(?) -> ?
Complete as ? e responda aqui!

# analysis(?) -> ?
Complete as ? e responda aqui!

# optimize(?) -> ?
Complete as ? e responda aqui!

# codegen(?) -> ?
Complete as ? e responda aqui!