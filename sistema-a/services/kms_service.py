import base64
from fastapi import HTTPException

async def cifrar_dato(dato: str) -> str:
    # Simulamos el cifrado convirtiendo a base64
    # En un entorno real, aquí usarías httpx para conectar a Vault o KMS
    try:
        encoded_bytes = base64.b64encode(dato.encode('utf-8'))
        return f"vault:v1:{encoded_bytes.decode('utf-8')}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en cifrado local: {str(e)}")

async def descifrar_dato(dato_cifrado: str) -> str:
    # Simulamos el descifrado eliminando el prefijo y decodificando
    try:
        if not dato_cifrado.startswith("vault:v1:"):
            raise ValueError("Formato de dato cifrado inválido")
            
        cifrado_puro = dato_cifrado.replace("vault:v1:", "")
        decoded_bytes = base64.b64decode(cifrado_puro)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en descifrado local: {str(e)}")