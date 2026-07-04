from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Sistema A - Backend Seguro")

# 1. Configuración de CORS: Permite la conexión desde los Frontends locales
# Esto soluciona el error 404 OPTIONS y el bloqueo de origen cruzado
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:5174", 
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Modelo de datos
class MensajeRequest(BaseModel):
    mensaje: str

# 3. Endpoint principal
@app.post("/api/enviar")
async def recibir_mensaje(datos: MensajeRequest, authorization: str = Header(None)):
    
    # Validación del Token JWT proveniente de Keycloak
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token no proporcionado o inválido")

    # Aquí recibimos el mensaje de React
    mensaje = datos.mensaje
    
    print(f"✅ Petición recibida correctamente. Mensaje: {mensaje}")
    
    # Respuesta exitosa para el Frontend
    return {
        "status": "éxito",
        "mensaje_cifrado": f"🔐 VAULT_ENCRYPTED_{mensaje[::-1]}",
        "original": mensaje,
        "info": "Procesado por Sistema A"
    }

# 4. Endpoint de salud
@app.get("/")
def health_check():
    return {"status": "ok", "mensaje": "Servidor de Python activo"}