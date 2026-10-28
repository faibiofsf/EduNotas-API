from fastapi import FastAPI, HTTPException, status
from typing import List, Optional
from uuid import uuid4

from app.schemas import (
    LancarNotaDTO,
    NotaResponseDTO,
    BoletimAlunoDTO,
    MensagemErroDTO
)

app = FastAPI(
    title="EduNotas API — Serviço de Consulta Acadêmica",
    description="Web Service RESTful de demonstração para consulta e lançamento de notas.",
    version="1.0.0"
)

# --- Base de Dados Simulada em Memória ---
ALUNOS_DB = {
    "20262BCC0012": "Eliel Santos",
    "20262BCC0045": "Maria Oliveira"
}

NOTAS_DB = {}

# --- ENDPOINTS RESTful ---

@app.post(
    "/api/v1/notas",
    response_model=NotaResponseDTO,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": MensagemErroDTO}, 404: {"model": MensagemErroDTO}},
    summary="Lançar nota de avaliação",
    tags=["Notas"]
)
def lancar_nota(payload: LancarNotaDTO):
    """
    Cadastra uma nova nota para o aluno e retorna o registro formatado.
    """
    if payload.matricula_aluno not in ALUNOS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Matrícula '{payload.matricula_aluno}' não encontrada no cadastro acadêmico."
        )

    situacao = "APROVADO_PARCIAL" if payload.nota >= 7.0 else "EM_RECUPERACAO"

    id_registro = f"REG-{uuid4().hex[:6].upper()}"
    novo_registro = {
        "id_registro": id_registro,
        "matricula_aluno": payload.matricula_aluno,
        "disciplina": payload.disciplina,
        "sigla_avaliacao": payload.sigla_avaliacao,
        "nota": payload.nota,
        "situacao": situacao
    }

    NOTAS_DB[id_registro] = novo_registro
    return novo_registro


@app.get(
    "/api/v1/alunos/{matricula}/boletim",
    response_model=BoletimAlunoDTO,
    status_code=status.HTTP_200_OK,
    responses={404: {"model": MensagemErroDTO}},
    summary="Consultar boletim do aluno",
    tags=["Consultas Acadêmicas"]
)
def obter_boletim(matricula: str):
    """
    Retorna o histórico de notas e calcula a média parcial do aluno.
    """
    if matricula not in ALUNOS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aluno com matrícula '{matricula}' não foi encontrado."
        )

    nome_aluno = ALUNOS_DB[matricula]
    notas_aluno = [n for n in NOTAS_DB.values() if n["matricula_aluno"] == matricula]

    media = sum(n["nota"] for n in notas_aluno) / len(notas_aluno) if notas_aluno else 0.0

    return {
        "matricula_aluno": matricula,
        "nome_aluno": nome_aluno,
        "media_parcial": round(media, 2),
        "historico_notas": notas_aluno
    }


@app.delete(
    "/api/v1/notas/{id_registro}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": MensagemErroDTO}},
    summary="Remover lançamento de nota",
    tags=["Notas"]
)
def remover_nota(id_registro: str):
    """
    Remover um registro de nota lançado incorretamente pelo seu ID de registro.
    """
    if id_registro not in NOTAS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Registro de nota '{id_registro}' não encontrado."
        )
    del NOTAS_DB[id_registro]
    return None