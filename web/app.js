// web/app.js
const DATA_URL = "./data/latest_conagua_cdmx.json";

const state = {
  json: null,
  scope: "cdmx",
};

const dateFmt = new Intl.DateTimeFormat("es-MX", { weekday: "short", year: "numeric", month: "short", day: "numeric" });

async function load() {
  const res = await fetch(DATA_URL, { cache: "no-store" });
  if (!res.ok) throw new Error("No pude cargar datos");
  const json = await res.json();
  state.json = json;
  window.__CLIMA_JSON__ = json;

  document.getElementById("generated").textContent =
    `Generado: ${new Date(json.generated_at).toLocaleString("es-MX")} · Fuente: Conagua`;

  // Selects
  const selA = document.getElementById("alcaldia");
  const selS = document.getElementById("scope");
  for (const nombre of Object.keys(json.alcaldias).sort()) {
    const o = document.createElement("option");
    o.value = nombre; o.textContent = nombre;
    selA.appendChild(o);
    const o2 = document.createElement("option");
    o2.value = nombre; o2.textContent = nombre;
    selS.appendChild(o2);
  }

  selA.addEventListener("change", (e) => {
    state.scope = e.target.value;
    render();
  });
  selS.addEventListener("change", (e) => {
    state.scope = e.target.value;
  });

  render();
}

function getSeries() {
  const j = state.json;
  if (!j) return { name: "…", daily: [] };
  if (state.scope === "cdmx") {
    return { name: j.cdmx.name, daily: j.cdmx.daily };
  }
  const alc = j.alcaldias[state.scope];
  return { name: state.scope, daily: alc?.daily || [] };
}

function render() {
  const series = getSeries();
  const units = state.json.units;

  // Summary cards (primer día disponible)
  const d0 = series.daily[0];
  const cards = document.getElementById("summary");
  if (d0) {
    cards.innerHTML = `
      <div class="card"><div class="k">Ámbito</div><div class="v">${series.name}</div></div>
      <div class="card"><div class="k">Temp min</div><div class="v">${d0.tmin ?? "—"} °${units.temp}</div></div>
      <div class="card"><div class="k">Temp max</div><div class="v">${d0.tmax ?? "—"} °${units.temp}</div></div>
      <div class="card"><div class="k">Precipitación</div><div class="v">${d0.precip_mm ?? "—"} ${units.precip}</div></div>
      <div class="card"><div class="k">Prob. precip</div><div class="v">${d0.precip_prob_pct ?? "—"} %</div></div>
      <div class="card"><div class="k">Viento</div><div class="v">${d0.wind_kmh ?? "—"} ${units.wind_speed}</div></div>
    `;
  } else {
    cards.innerHTML = `<div class="card"><div class="v">Sin datos</div></div>`;
  }

  // Tabla
  const rows = series.daily.slice(0, 7).map(d => `
    <tr>
      <td>${dateFmt.format(new Date(d.date))}</td>
      <td>${d.sky ?? "—"}</td>
      <td>${d.tmin ?? "—"} °${units.temp}</td>
      <td>${d.tmax ?? "—"} °${units.temp}</td>
      <td>${d.precip_mm ?? "—"} ${units.precip}</td>
      <td>${d.precip_prob_pct ?? "—"} %</td>
      <td>${d.wind_kmh ?? "—"} ${units.wind_speed}</td>
    </tr>
  `).join("");

  document.getElementById("table").innerHTML = `
    <table>
      <thead>
        <tr><th>Día</th><th>Cielo</th><th>T. min</th><th>T. max</th><th>Precip.</th><th>Prob.</th><th>Viento</th></tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}

load().catch(err => {
  console.error(err);
  document.getElementById("generated").textContent = "Error al cargar datos";
});
