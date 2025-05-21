# Preencha Informacões basicas
nome = "Renann"
matricula = "20/0043030"
github = "@renannOgomes"
turma = "18h"  # ou "18h"

# Faca 5 das 6 questões da prova. Você deve escolher explicitamente quais
# questões devem ser corrigidas. Cada questao vale 5pts. Comente a questao que
# você deseja pular e descomente todas as outras.
questoes = {
    "q1",
    "q2",
    "q3",
    "q4",
    "q5",
    # "q6",
}

################################################################################
#    Seleciona a prova de acordo com a matricula e inicializa os arquivos
#################################################################################
if __name__ == "__main__":
    import re  # noqa: E402
    import shutil  # noqa: E402
    from pathlib import Path  # noqa: E402

    REPO = Path(__file__).parent

    if not re.fullmatch(r"[0-9]{2}\/[0-9]+", matricula):
        exit("[ERRO] Matricula invalida. Formato esperado: 12/34567")
    if matricula == "12/34567":
        exit("[ERRO] Digite sua matricula corretamente.")
    if turma not in {"16h", "18h"}:
        exit("[ERRO] Turma invalida. Formato esperado: 16h ou 18h")

    exam_id = str(int(matricula.replace("/", "")) // 10 % 16 + 1)

    print(f"Nome: {nome}")
    print(f"Matricula: {matricula}")
    if input("Confirma as informacões? [s/N] ").lower() != "s":
        exit("[ERRO] Edite o arquivo prova.py com as informacões corretas")
    if input(f"ID da prova: *{exam_id}*, Copio arquivos? [s/N] ").lower() != "s":
        exit("[ERRO] Arquivos nao copiados. Saindo...")

    base = REPO / "provas" / f"prova-{exam_id}"
    shutil.copytree(base, REPO, dirs_exist_ok=True)
