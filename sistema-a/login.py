import httpx
import asyncio

async def login():
    print("\n=== INICIO DE SESIÓN SEGURO (SISTEMA A) ===")
    username = input("Usuario: ")
    password = input("Contraseña: ")
    otp = input("Código de Google Authenticator (OTP): ")

    url = "http://localhost:8080/realms/SeguridadRealm/protocol/openid-connect/token"
    
    data = {
        "client_id": "cliente-sistema-a",
        "grant_type": "password",
        "username": username,
        "password": password,
        "totp": otp  # Aquí enviamos el 2do factor
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data)
        
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("\n✅ ¡LOGIN EXITOSO!")
        print(f"\nTu Token JWT es el siguiente (cópialo todo):\n")
        print(token)
        print("\n👉 Ahora ve a http://localhost:3001/docs, haz clic en 'Authorize' y pega este token.")
    else:
        print("\n❌ Error al iniciar sesión. Verifica tus credenciales o si el código OTP caducó.")
        print(response.json())

asyncio.run(login())