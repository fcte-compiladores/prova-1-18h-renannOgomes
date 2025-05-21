# Compiladores / Prova 1


## Instrucões 

Salve seu nome e matricula e horario da turma na qual você esta matriculado(a)
no arquivo provas.py. Depois execute esse script usando `python3 prova.py` (ou
`python prova.py`, vai depender da sua configuracao)` Ele selecionara uma das
versões de prova, ira salva-la na pasta atual e apagara as outras. **PREENCHA A
MATRiCULA CORRETAMENTE** para nao resolver a prova errada.

## Sobre a prova

Você deve selecionar 5 das 6 questões disponiveis. Edite o arquivo prova.py de 
acordo com as questões que você quer que sejam corrigidas.


## Regras

Você pode fazer a prova no computador do laboratório ou no computador pessoal e
durante a prova pode acessar alguns sites:

* O livro https://craftinginterpreters.com/contents.html
* O Github classroom da disciplina.
* O repositório do Github da turma.
* Seu repositório da prova.
* https://docs.astral.sh/uv/ para baixar o UV, se necessario

A utilizacao de qualquer outro site é proibida. Em particular a utilizacao de
modelos de linguagem como ChatGPT, DeepSeek, Gemini, Grok, etc esta
EXPRESSAMENTE PROIBIDA! A utilizacao de qualquer um desses modelos durante a
prova implica na anulacao da mesma.

Além disso, a utilizacao de qualquer sistema de mensageria (WhatsApp, Telegram,
Gmail, Instagram, TikTok etc) tanto no celular quanto no computador também
implica na anulacao da prova. Desligue as notificacões do celular durante a
prova e se precisar atender o celular em alguma emergência, fale antes com o
professor.


## Rodando os exemplos e testes

A prova usa o `uv` para gerenciar sua versao do Python. Você pode usar outras
ferramentas se quiser, mas ja esta tudo configurado para funcionar com o `uv`.
Os comandos abaixo podem ser uteis:

    # Roda os testes
    uv run pytest 
    uv run pytest --maxfail=1       # para no 1o erro
    uv run pytest tests/test_q1.py  # seleciona uma questao
    uv run pytest -l                # mostra variaveis locais no traceback
    uv run pytest --tb=no           # relatório curto, também aceita short, line

    # Executa o lox
    uv run lox --help
    uv run lox some_file.lox

    # Executa a questao 1
    uv run q1-regex.py


## Entrega

A prova sera entregue subindo um commit para a branch master. Você pode usar
comandos do git, mas ja sabendo que a rede da UnB bloqueia mais acessos que o
ideal, se planeje para ter que subir os arquivos importantes manualmente.

Somente os seguintes arquivos serao considerados na correcao:

* lox/ast.py
* lox/grammar.lark
* lox/transformer.py
* q1-regex.py
* q6-arquitetura.md
* fib.lox ou maior.lox, dependendo da prova.

Se precisar subir os arquivos manualmente, confira se todos dessa lista estao
no repositório.