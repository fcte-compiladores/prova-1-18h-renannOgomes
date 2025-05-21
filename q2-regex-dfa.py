"""
A figura q2.svg mostra uma maquina de estados (ou autômato finito
deterministico, DFA) que reconhece a linguagem formadas por a's e b's. Uma
string é aceita se comecando no estado "start" e fazendo apenas as transicões
definidas na figura, a string termina no estado "accept".

Dê alguns exemplos de strings que sao aceitas e outras que sao recusadas nessa
linguagem preenchendo as variaveis abaixo.

Depois crie uma expressao regular que reconheca a mesma linguagem.
"""

# Menor string possivel nessa linguagem (0.5pt)
menor = "abb"

# Uma string valida com exatamente 5 caracteres  (0.5pt)
string_5 = "ababb"

# Menor string que o numero de a's é igual ao numero de b's (0.5pt)
menor_ab = "aabb"

# 3 exemplos de strings validas diferentes (exceto as anteriores) (1.0pt)
accept_3 = ["aababb", "abaaabb", "abaabaabb"]

# Para cada exemplo acima, gere uma string invalida somente rearranjando os
# caracteres da string valida na mesma posicao que em accept_3  (1.0pt)
reject_3 = ["aaabbb", "baaabb", "abbaabab"]

# Regex que descreve a linguagem (1.5pt)
# Dica tente simplificar o grafo tirando transicões desnecessarias
regex = r"^a(?:a*ba+)*a*ba*b$"
