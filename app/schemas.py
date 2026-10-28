from pydantic import BaseModel, Field
from typing import List, Optional

# --- DTO de Entrada (RequestDTO) ---
class LancarNotaDTO(BaseModel):
    matricula_aluno: str = Field(..., example="20262BCC0012", description="Matrícula do discente")
    disciplina: str = Field(..., example="Computação em Nuvem", description="Nome da disciplina")
    sigla_avaliacao: str = Field(..., example="1BI", description="Identificador da avaliação (1BI, 2BI, EXAME)")
    nota: float = Field(..., ge=0.0, le=10.0, example=8.5, description="Nota de 0.0 a 10.0")

# --- DTOs de Saída (ResponseDTO) ---
class NotaResponseDTO(BaseModel):
    id_registro: str = Field(..., example="REG-9912")
    matricula_aluno: str = Field(..., example="20262BCC0012")
    disciplina: str = Field(..., example="Computação em Nuvem")
    sigla_avaliacao: str = Field(..., example="1BI")
    nota: float = Field(..., example=8.5)
    situacao: str = Field(..., example="APROVADO_PARCIAL")

class BoletimAlunoDTO(BaseModel):
    matricula_aluno: str = Field(..., example="20262BCC0012")
    nome_aluno: str = Field(..., example="Eliel Santos")
    media_parcial: float = Field(..., example=8.5)
    historico_notas: List[NotaResponseDTO]

# --- DTO de Resposta de Erro Padronizada ---
class MensagemErroDTO(BaseModel):
    codigo_erro: str = Field(..., example="ALUNO_NAO_ENCONTRADO")
    mensagem: str = Field(..., example="O discente informado não consta no cadastro acadêmico.")