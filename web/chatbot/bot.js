// web/chatbot/bot.js
const log = document.getElementById("chatlog");
const form = document.getElementById("chat");
const input = document.getElementById("q");
const scopeSel = document.getElementById("scope");

function add(role, text) {
  const div = document.createElement("div");
  div.className = role;
  div.textContent = text;
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
}

function normalize(s) {
  return (s || "").normalize("NFKD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
}

function intent(q) {
  const n = normalize(q);
  return {
    rain: /(lluvia|llover|precip)/.test(n),
    prob: /(prob|probabilidad)/.test(n),
    temp: /(temp|temperatura|min|max|frio|calor)/.test(n),
    wind: /(viento|rafaga|rafagas)/.test(n),
    today: /(hoy)/.test(n),
    tomorrow: /(manana|mañana)/.test(n),
    after: /(pasado manana|pasado mañana)/.test(n),
  };
}

function resolveSeries(q, json) {
  // Prioridad: alcaldía en texto > select del chat > CDMX
  const n = normalize(q);
  const names = Object.keys(json.alcaldias);
  const hit = names.find(x => n.includes(normalize(x)));
  if (hit) return { name: hit, daily: json.alcaldias[hit].daily };
  if (scopeSel.value === "cdmx") return { name: json.cdmx.name, daily: json.cdmx.daily };
  return { name: scopeSel.value, daily: json.alcaldias[scopeSel.value]?.daily || [] };
}

function pickDay(i, series) {
  const idx = Math.min(i, series.daily.length - 1);
  return series.daily[idx];
}

function fmtDate(s) {
  try { return new Date(s).toLocaleDateString("es-MX", { weekday: "long", month: "short", day: "numeric" }); }
  catch { return s; }
}

function answer(q, json) {
  const it = intent(q);
  const series = resolveSeries(q, json);
  if (!series.daily.length) return "No tengo datos para ese ámbito.";

  let d;
  if (it.today) d = pickDay(0, series);
  else if (it.tomorrow) d = pickDay(1, series);
  else if (it.after) d = pickDay(2, series);
  else d = pickDay(0, series);

  const u = json.units;

  if (it.rain && it.prob) {
    const v = d.precip_prob_pct;
    return v != null
      ? `Probabilidad de lluvia ${series.name} ${fmtDate(d.date)}: ${v}%`
      : `No hay probabilidad disponible para ${fmtDate(d.date)}.`;
  }

  if (it.rain) {
    const v = d.precip_mm;
    return v != null
      ? `Precipitación estimada ${series.name} ${fmtDate(d.date)}: ${v} ${u.precip}.`
      : `No hay precipitación disponible para ${fmtDate(d.date)}.`;
  }

  if (it.temp) {
    const min = d.tmin, max = d.tmax;
    if (min != null && max != null) return `Temperaturas ${series.name} ${fmtDate(d.date)}: min ${min}°${u.temp}, max ${max}°${u.temp}.`;
    if (min != null) return `Temperatura mínima ${series.name} ${fmtDate(d.date)}: ${min}°${u.temp}.`
    if (max != null) return `Temperatura máxima ${series.name} ${fmtDate(d.date)}: ${max}°${u.temp}.`
    return `No tengo temperaturas para ${fmtDate(d.date)}.`;
  }

  if (it.wind) {
    const v = d.wind_kmh;
    return v != null
      ? `Viento promedio ${series.name} ${fmtDate(d.date)}: ${v} ${u.wind_speed}.`
      : `No tengo viento disponible para ${fmtDate(d.date)}.`;
  }

  // Resumen por defecto
  return [
    `Resumen ${series.name} ${fmtDate(d.date)}:`,
    d.sky ? `Cielo: ${d.sky}.` : null,
    d.tmin != null && d.tmax != null ? `Temp: ${d.tmin}–${d.tmax} °${u.temp}.` : null,
    d.precip_mm != null ? `Precip: ${d.precip_mm} ${u.precip}.` : null,
    d.precip_prob_pct != null ? `Prob: ${d.precip_prob_pct}%.` : null,
    d.wind_kmh != null ? `Viento: ${d.wind_kmh} ${u.wind_speed}.` : null,
  ].filter(Boolean).join(" ");
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const q = input.value.trim();
  if (!q) return;
  add("user", q);
  const json = window.__CLIMA_JSON__;
  if (!json) { add("bot", "Aún no cargo los datos."); return; }
  add("bot", answer(q, json));
  input.value = "";
});
