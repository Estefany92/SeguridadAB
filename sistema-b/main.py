from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.kms_service import descifrar_dato

app = FastAPI(title="Sistema B - Receptor")

# Definimos la estructura de lo que esperamos recibir
class PayloadReceptor(BaseModel):
    datosCifrados: str

@app.post("/api/recepcion")
async def recibir_datos(payload: PayloadReceptor):
    try:
        # 1. El Sistema B recibe la trama (completamente ilegible)
        texto_cifrado = payload.datosCifrados
        print(f"--> [Sistema B] Recibí esta trama cifrada de A: {texto_cifrado}")
        
        # 2. Llama a Vault para descifrarla
        texto_claro = await descifrar_dato(texto_cifrado)
        print(f"--> [Sistema B] Vault lo descifró. El mensaje real es: {texto_claro}")
        
        # 3. Retornamos la respuesta confirmando el éxito
        return {
            "mensaje": "Datos recibidos y descifrados correctamente en el Sistema B",
            "trama_cifrada_recibida": texto_cifrado,
            "trama_descifrada": texto_claro
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en Sistema B: {str(e)}")