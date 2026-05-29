from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verificar_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    # En desarrollo, esto permite pasar cualquier token que tenga formato Bearer
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token requerido")
    
    # Retornamos un usuario ficticio para continuar con el flujo
    return {"sub": "usuario_prueba_local"}