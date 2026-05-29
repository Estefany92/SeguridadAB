from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.kms_service import descifrar_dato

# El Sistema B vive lógicamente en el puerto 3002
app = FastAPI(title="Sistema B - Receptor Seguro")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definimos exactamente qué estructura de datos esperamos recibir
class RecepcionPayload(BaseModel):
    datosCifrados: str

@app.post("/api/recepcion")
async def endpoint_recepcion(payload: RecepcionPayload):
    """
    PUERTA DE RECEPCIÓN DE DATOS
    Recibe la información cifrada, la desencripta y la procesa.
    """
    # 1. Mandamos a descifrar el dato
    resultado_claro = await descifrar_dato(payload.datosCifrados)
    
    # 2. Aquí iría la lógica del Sistema B (guardarlo en base de datos, iniciar un trámite, etc)
    
    return {
        "success": True,
        "mensaje": "Datos recibidos y descifrados correctamente en Sistema B",
        "datosProcesados": resultado_claro
    }

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Sistema B funcionando y a la escucha."}