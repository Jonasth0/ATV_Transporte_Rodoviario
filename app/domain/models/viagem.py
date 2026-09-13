from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

class Localidade(BaseModel):
    cidade: str
    uf: str

class Preco(BaseModel):
    valor: Decimal
    moeda: str

class ViagemNormalizada(BaseModel):
    id_viagem: str
    empresa: str
    origem: Localidade
    destino: Localidade 
    partida: datetime 
    chegada: datetime 
    duracao_minutos: int 
    preco: Preco 
    categoria: str 
    assentos_disponiveis: int 

class ViagensResponse(BaseModel):
    total: int
    viagens: list[ViagemNormalizada]

viagem = ViagemNormalizada(
    id_viagem= "TESTE-001",
    empresa="Empresa Teste",
    origem={
        "cidade": "Paulo Afonso",
        "uf": "BA"
    },
    destino={
        "cidade": "Recife",
        "uf": "PE"
    },
    partida=datetime.fromisoformat("2026-10-15T06:30:00-03:00"),
    chegada=datetime.fromisoformat("2026-10-15T12:50:00-03:00"),
    duracao_minutos=380,
    preco={
        "valor": Decimal("129.90"),
        "moeda": "BRL"
    },
    categoria="executivo",
    assentos_disponiveis=18
)