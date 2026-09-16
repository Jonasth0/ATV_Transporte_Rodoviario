from abc import ABC, abstractmethod
from typing import Any

from app.domain.models.viagem import ViagemNormalizada

# Cada empresa precisa passar informações corretas, ex: nome_empresa. Caso contrário, recusa
class ViagemStrategy(ABC):

    @abstractmethod
    def identifica(self, playload: dict[str, Any]) -> bool: # Recebe Json Bruto e reconhece o formato ( T ou F ).
        pass

    @abstractmethod
    def normaliza(self, playload: dict[str, Any]) ->ViagemNormalizada: # Normaliza o Json Bruto e devolve um objeto ViagemNormalizada.
        pass

    @abstractmethod
    def nome_empresa(self) -> str: # Apenas preenche o nome da empresa.
        pass
    