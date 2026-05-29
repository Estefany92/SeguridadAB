import base64
from fastapi import HTTPException

async def descifrar_dato(ciphertext: str) -> str:
    # Lógica simplificada de prueba
    if not ciphertext.startswith("vault:v1:"):
        raise HTTPException(status_code=400, detail="Formato inválido")
    
    cifrado_puro = ciphertext.replace("vault:v1:", "")
    return base64.b64decode(cifrado_puro).decode('utf-8')