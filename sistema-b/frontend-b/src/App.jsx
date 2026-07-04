import React, { useEffect, useState } from 'react';
import Keycloak from 'keycloak-js';

const keycloak = new Keycloak({
  url: 'http://localhost:8080',
  realm: 'SeguridadRealm',
  clientId: 'cliente-sistema-b' // <-- MUY IMPORTANTE: cliente-sistema-b
});

function App() {
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    keycloak.init({ 
      onLoad: 'login-required',
      checkLoginIframe: false 
    })
    .then(auth => {
      setAuthenticated(auth);
    })
    .catch(error => {
      console.error("Error al conectar con Keycloak:", error);
    });
  }, []);

  const logout = () => {
    keycloak.logout({ redirectUri: 'http://localhost:5174' });
  };

  if (!authenticated) return <div style={{padding: '20px'}}>Iniciando sesión segura en Sistema B...</div>;

  return (
    <div style={{ padding: '50px', backgroundColor: '#fff3e0', height: '100vh', fontFamily: 'Arial' }}>
      <h1>🖥️ APLICACIÓN - SISTEMA B</h1>
      <h2>Bienvenido, {keycloak.tokenParsed.preferred_username}</h2>
      <p>Has ingresado de manera transparente mediante Single Sign-On (SSO).</p>
      <button onClick={logout} style={{ padding: '10px 20px', background: 'red', color: 'white', border: 'none', cursor: 'pointer' }}>
        Cerrar Sesión Global
      </button>
    </div>
  );
}

export default App;