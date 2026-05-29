import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [mensaje, setMensaje] = useState("");
  const [resultado, setResultado] = useState("");

  const manejarEnvio = async () => {
    try {
      // Usamos un token de prueba (puedes inyectar el tuyo real aquí)
      const token = "TOKEN_DE_PRUEBA"; 

      // 1. Cifrar en Sistema A
const resCifrado = await axios.post('https://effective-guide-4xg6v5px5wq2jjpr-3000.app.github.dev/api/cifrar',        { dato: mensaje },
        { headers: { "Authorization": `Bearer ${token}` } }
      );
      
      const datoCifrado = resCifrado.data.datosCifrados;
      
      // 2. Descifrar en Sistema B
const resDescifrado = await axios.post('https://effective-guide-4xg6v5px5wq2jjpr-3002.app.github.dev/api/recepcion', {        datosCifrados: datoCifrado
      });

      setResultado(resDescifrado.data.datosProcesados);
    } catch (error) {
      console.error("Error:", error);
      setResultado("Error: Verifica que los servidores Python estén encendidos");
    }
  };

  return (
    <div className="App">
      <h1>Panel de Seguridad</h1>
      <input 
        value={mensaje} 
        onChange={(e) => setMensaje(e.target.value)} 
        placeholder="Mensaje secreto" 
      />
      <button onClick={manejarEnvio}>Cifrar y Enviar</button>
      <p>Resultado: <strong>{resultado}</strong></p>
    </div>
  );
}

export default App;