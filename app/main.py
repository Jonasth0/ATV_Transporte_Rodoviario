from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import viagens
from app.exceptions.viagem import ViagemValidationError


app = FastAPI(
    title="API de Normalização de Viagens",
    description="API para normalização de dados de viagens de diferentes companhias.",
    version="1.0.0",
)


@app.exception_handler(ViagemValidationError)
async def tratar_erro_viagem(
    request: Request,
    exc: ViagemValidationError,
):
    return JSONResponse(
        status_code=422,
        content={
            "detail": {
                "indice": exc.indice,
                "empresa_identificada": exc.empresa_identificada,
                "campo": exc.campo,
                "mensagem": exc.mensagem,
            }
        },
    )


app.include_router(viagens.router)