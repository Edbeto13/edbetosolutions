import { useEffect, useState } from 'react';

export default function ClimaCDMX() {
  const [clima, setClima] = useState([]);

  useEffect(() => {
    fetch('/api/clima-cdmx')
      .then(res => res.json())
      .then(json => setClima(json.data || []))
      .catch(err => console.error('Error cargando clima', err));
  }, []);

  return (
    <div>
      <h2>Clima por alcaldía (CDMX)</h2>
      <ul>
        {clima.map((m, i) => (
          <li key={i}>
            <strong>{m.municipio}:</strong> {m.temperaturaMax}°C / {m.temperaturaMin}°C - {m.descripcionCielo}
          </li>
        ))}
      </ul>
    </div>
  );
}
