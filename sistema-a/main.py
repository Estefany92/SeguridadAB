from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import httpx
from services.kms_service import cifrar_dato
from middleware.auth import validar_token

app = FastAPI(title="Sistema A - Emisor")

class PayloadEnvio(BaseModel):
    mensaje: str

@app.post("/api/enviar-a-b")
async def enviar_datos_a_b(payload: PayloadEnvio, token_data: dict = Depends(validar_token)):
    try:
        # Extraemos el nombre de usuario desde el token (SSO)
        usuario = token_data.get('preferred_username', 'Desconocido')
        print(f"\n--- ACCESO AUTORIZADO ---")
        print(f"Usuario interactuando: {usuario}")
        
        # 1. Encriptar el mensaje usando Vault
        texto_cifrado = await cifrar_dato(payload.mensaje)
        print(f"--> [Sistema A] Mensaje original encriptado. Trama generada: {texto_cifrado[:20]}...")
        
        # 2. Enviar la trama cifrada al Sistema B por la red
        url_sistema_b = "http://localhost:3002/api/recepcion"
        
        async with httpx.AsyncClient() as client:
            respuesta_de_b = await client.post(
                url_sistema_b, 
                json={"datosCifrados": texto_cifrado}
            )
            
        # 3. Procesar lo que nos respondió el Sistema B
        if respuesta_de_b.status_code == 200:
            return {
                "status": "Transacción Segura Exitosa",
                "usuario_autenticado": usuario,
                "mensaje_ingresado": payload.mensaje,
                "trama_viajando_por_red": texto_cifrado,
                "respuesta_del_sistema_b": respuesta_de_b.json()
            }
        else:
            raise HTTPException(status_code=respuesta_de_b.status_code, detail="El Sistema B falló")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en Sistema A: {str(e)}")