O exercicio anterior implementou suporte ao `while` na sintaxe. Agora vamos 
implementar o suporte ao `while` no interpretador implementando o método
`While.eval`.

Lembre-se de alguns detalhes da semântica do Lox:

1. O `while` avalia a condicao e somente executa o corpo se ela for verdadeira.
2. Somente `false` e `nil` sao considerados falsos, portanto os lacos abaixo
   nao terminam: 
   -  `while (0) do_something()`
   -  `while ("") do_something()`
3. Lox nao possui comandos como `break` e `continue`, o que facilita 
   consideravelmente a implementacao dos lacos.

Implemente o método `eval` na classe `While`. Depois, edite o arquivo
`maior.lox` e implemente um programa que imprime o maior numero entre duas
opcões. Importante: nossa linguagem nao possui if, entao temos que implementar o
programa usando whiles.

