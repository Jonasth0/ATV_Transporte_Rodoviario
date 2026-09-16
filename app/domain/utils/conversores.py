from datetime import datetime
from decimal import Decimal, InvalidOperation
from zoneinfo import ZoneInfo

from app.exceptions.viagem import ViagemValidationError


def converter_data(
    valor: str,
    formato: str | None = None,
    campo: str = "data",
) -> datetime:

    try:
        if formato:
            data = datetime.strptime(valor, formato)
        else:
            data = datetime.fromisoformat(valor)

    except (ValueError, TypeError):
        raise ViagemValidationError(
            campo=campo,
            mensagem="A data informada é inválida.",
        )

    if data.tzinfo is None:
        data = data.replace(
            tzinfo=ZoneInfo("America/Bahia")
        )

    return data


def converter_duracao(
    valor: str | int,
) -> int:

    try:
        if isinstance(valor, int):
            return valor

        horas, minutos = valor.split(":")

        return int(horas) * 60 + int(minutos)

    except (ValueError, TypeError, AttributeError):
        raise ViagemValidationError(
            campo="duracao",
            mensagem="A duração informada é inválida.",
        )

# Principio DRY ( Don't Repeat Yourself ).
def converter_preco_br(
    valor: str,
) -> Decimal:

    try:
        return Decimal( # Decimal é mais preciso que float. ( História do FOGUETE EUROPEU AE ).
            valor.replace(".", "").replace(",", ".")
        )

    except (ValueError, TypeError, AttributeError):
        raise ViagemValidationError(
            campo="preco",
            mensagem="O preço informado é inválido.",
        )


def converter_preco_centavos(
    valor: int,
) -> Decimal:

    try:
        return Decimal(valor) / 100

    except (ValueError, TypeError, InvalidOperation):
        raise ViagemValidationError(
            campo="preco",
            mensagem="O preço informado é inválido.",
        )


def converter_assentos(
    valor: str | int,
) -> int:

    try:
        return int(valor)

    except (ValueError, TypeError):
        raise ViagemValidationError(
            campo="assentos",
            mensagem="A quantidade de assentos informada é inválida.",
        )