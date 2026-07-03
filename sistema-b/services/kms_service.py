import base64
import hvac
from fastapi import HTTPException

# El Sistema B también se conecta al KMS de Vault
try:
    cliente_vault = hvac.Client(url='http://localhost:8200', token='llave-maestra-vault')
except Exception as e:
    print(f"Error al conectar con Vault: {e}")

async def descifrar_dato(ciphertext: str) -> str:
    try:
        # Invocamos la desencriptación
        respuesta = cliente_vault.secrets.transit.decrypt_data(
            name='llave-proyecto',
            ciphertext=ciphertext
        )
        
        # Decodificamos el resultado devuelto por Vault
        plaintext_b64 = respuesta['data']['plaintext']
        decoded_bytes = base64.b64decode(plaintext_b64)
        return decoded_bytes.decode('utf-8')
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error KMS (Sistema B) al descifrar: {str(e)}")