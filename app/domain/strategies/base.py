from abc import ABC, abstractmethod
from typing import Any

from app.domain.models.viagem import ViagemNormalizada


class ViagemStrategy(ABC):

    @abstractmethod
    def identifica(self, playload: dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def normaliza(self, playload: dict[str, Any]) ->ViagemNormalizada:
        pass

    @abstractmethod
    def nome_empresa(self) -> str:
        pass
    