from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Importaciones de nuestros módulos locales
from middleware.auth import verificar_token
from services.kms_service import cifrar_dato, descifrar_dato

app = FastAPI(title="Sistema de Seguridad en Python")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Cambiar por el dominio de tu frontend en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para validar lo que envía el Frontend
class DatosPayload(BaseModel):
    dato: str

@app.post("/api/cifrar")
async def endpoint_cifrar(payload: DatosPayload, usuario: dict = Depends(verificar_token)):
    # Depende de verificar_token: si el token no es válido, no ejecuta esta línea
    resultado = await cifrar_dato(payload.dato)
    return {
        "success": True,
        "usuario_id": usuario.get("sub"),
        "datosCifrados": resultado
    }

@app.post("/api/descifrar")
async def endpoint_descifrar(payload: DatosPayload, usuario: dict = Depends(verificar_token)):
    resultado = await descifrar_dato(payload.dato)
    return {
        "success": True,
        "datosClaros": resultado
    }

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Servidor funcionando correctamente"}