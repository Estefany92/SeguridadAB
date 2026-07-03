import base64
import hvac
from fastapi import HTTPException

# Nos conectamos al contenedor de Vault
try:
    cliente_vault = hvac.Client(url='http://localhost:8200', token='llave-maestra-vault')
except Exception as e:
    print(f"Error al conectar con Vault: {e}")

async def cifrar_dato(dato: str) -> str:
    try:
        # Vault exige que el texto se envíe en formato base64 antes de encriptar
        dato_bytes = dato.encode('utf-8')
        dato_b64 = base64.b64encode(dato_bytes).decode('utf-8')
        
        # Invocamos la encriptación
        respuesta = cliente_vault.secrets.transit.encrypt_data(
            name='llave-proyecto',
            plaintext=dato_b64
        )
        
        # Extraemos solo el texto cifrado
        texto_cifrado = respuesta['data']['ciphertext']
        return texto_cifrado
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en KMS (Sistema A): {str(e)}")

async def descifrar_dato(dato_cifrado: str) -> str:
    # Mantenemos esta función por si necesitas pruebas locales en A
    try:
        respuesta = cliente_vault.secrets.transit.decrypt_data(
            name='llave-proyecto',
            ciphertext=dato_cifrado
        )
        plaintext_b64 = respuesta['data']['plaintext']
        decoded_bytes = base64.b64decode(plaintext_b64)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error descifrando: {str(e)}")