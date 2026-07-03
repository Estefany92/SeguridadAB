from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import httpx

# Esto le dirá a FastAPI que use un "Candado" (Bearer Token) en la interfaz gráfica
security = HTTPBearer()

# La dirección donde Keycloak publica sus llaves públicas de seguridad
KEYCLOAK_CERTS_URL = "http://localhost:8080/realms/SeguridadRealm/protocol/openid-connect/certs"

async def get_public_key(kid):
    # Vamos a Keycloak a preguntarle por las llaves válidas actuales
    async with httpx.AsyncClient() as client:
        response = await client.get(KEYCLOAK_CERTS_URL)
        jwks = response.json()
    
    # Buscamos la llave que firmó el token del usuario
    for jwk in jwks.get('keys', []):
        if jwk.get('kid') == kid:
            return jwk
            
    raise HTTPException(status_code=401, detail="Llave pública no encontrada")

async def validar_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        # 1. Leemos la cabecera del token para saber qué llave usó Keycloak
        unverified_header = jwt.get_unverified_header(token)
        
        # 2. Obtenemos esa llave pública exacta
        public_key = await get_public_key(unverified_header['kid'])
        
        # 3. Validamos matemáticamente que el token no sea falso ni esté caducado
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            options={"verify_aud": False} # Simplificamos la validación de la audiencia
        )
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Acceso Denegado. Token inválido o expirado: {str(e)}")