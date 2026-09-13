class ViagemValidationError(Exception):

    def __init__(
        self,
        campo: str | None,
        mensagem: str,
        indice: int | None = None,
        empresa_identificada: str | None = None,
    ):
        self.campo = campo
        self.mensagem = mensagem
        self.indice = indice
        self.empresa_identificada = empresa_identificada

        super().__init__(mensagem)