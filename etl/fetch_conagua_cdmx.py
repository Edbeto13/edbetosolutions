# etl/fetch_conagua_cdmx.py
import requests, unicodedata, json, os
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

URLS = [
    "https://smn.conagua.gob.mx/tools/GUI/webservices/?method=1",
    "https://smn.conagua.gob.mx/es/tools/GUI/webservices/?method=1",
]

TZ = ZoneInfo("America/Mexico_City")

def normalizar(s: str) -> str:
    if s is None: return ""
    return unicodedata.normalize("NFKD", s).encode("ASCII", "ignore").decode().strip().lower()

def fetch(timeout: float = 20.0):
    for url in URLS:
        try:
            r = requests.get(url, timeout=timeout, headers={"User-Agent": "ClimaCDMX/1.0"})
            r.raise_for_status()
            data = r.json()
            if isinstance(data, list) and data:
                return data
        except Exception:
            continue
    raise RuntimeError("No se pudo obtener datos del web service de Conagua.")

def coerce(row: dict) -> dict:
    def f(x): 
        try:
            return round(float(str(x).strip()), 1)
        except Exception:
            return None
    def i(x):
        try:
            return int(float(str(x).strip()))
        except Exception:
            return None
    out = dict(row)
    for k in ["tmax","tmin","probprec","prec","velvien","lat","lon"]:
        if k in out: out[k] = f(out.get(k))
    for k in ["ndia","dh"]:
        if k in out: out[k] = i(out.get(k))
    return out

def filtrar_cdmx(data: list) -> list:
    out = []
    for r in data:
        if normalizar(r.get("nes")) == "ciudad de mexico":
            out.append(coerce(r))
    return out

def agrupar_por_alcaldia(registros: list):
    hoy = datetime.now(TZ).date()
    grupos = defaultdict(lambda: {"meta": {"lat": None, "lon": None}, "daily": []})
    for r in registros:
        nmun = r.get("nmun") or "Desconocida"
        if grupos[nmun]["meta"]["lat"] is None and r.get("lat") is not None:
            grupos[nmun]["meta"]["lat"] = r.get("lat")
        if grupos[nmun]["meta"]["lon"] is None and r.get("lon") is not None:
            grupos[nmun]["meta"]["lon"] = r.get("lon")
        ndia = r.get("ndia") or 1
        fecha = hoy + timedelta(days=max(0, ndia - 1))
        grupos[nmun]["daily"].append({
            "date": fecha.isoformat(),
            "sky": r.get("desciel"),
            "tmin": r.get("tmin"),
            "tmax": r.get("tmax"),
            "precip_mm": r.get("prec"),
            "precip_prob_pct": r.get("probprec"),
            "wind_kmh": r.get("velvien"),
            "dloc": r.get("dloc"),
        })
    for k in grupos:
        grupos[k]["daily"].sort(key=lambda x: x["date"])
    return grupos

def agregar_cdmx(grupos: dict):
    fechas = sorted({d["date"] for g in grupos.values() for d in g["daily"]})
    daily = []
    for fecha in fechas:
        bucket = [d for g in grupos.values() for d in g["daily"] if d["date"] == fecha]
        if not bucket: 
            continue
        def avg(key):
            vals = [x[key] for x in bucket if isinstance(x.get(key), (int,float))]
            return round(sum(vals)/len(vals), 1) if vals else None
        def moda_sky():
            vals = [normalizar(x.get("sky")) for x in bucket if x.get("sky")]
            if not vals: return None
            c = Counter(vals)
            return c.most_common(1)[0][0]
        daily.append({
            "date": fecha,
            "sky": moda_sky(),
            "tmin": avg("tmin"),
            "tmax": avg("tmax"),
            "precip_mm": avg("precip_mm"),
            "precip_prob_pct": avg("precip_prob_pct"),
            "wind_kmh": avg("wind_kmh"),
        })
    return {
        "name": "CDMX (promedio de alcaldías)",
        "daily": daily
    }

def build_payload(grupos: dict):
    ahora = datetime.now().astimezone(TZ)
    payload = {
      "generated_at": ahora.astimezone().isoformat(),
      "location": { "name": "Ciudad de México", "tz": "America/Mexico_City" },
      "units": { "temp": "C", "precip": "mm", "wind_speed": "km/h" },
      "alcaldias": {},
      "cdmx": None,
      "source": { "provider": "SMN · Conagua", "endpoints": URLS }
    }
    for nombre, g in grupos.items():
        payload["alcaldias"][nombre] = {
            "lat": g["meta"]["lat"],
            "lon": g["meta"]["lon"],
            "daily": g["daily"]
        }
    payload["cdmx"] = agregar_cdmx(grupos)
    return payload

def save(payload: dict):
    os.makedirs("data/snapshots", exist_ok=True)
    with open("data/latest_conagua_cdmx.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    ts = payload["generated_at"].replace(":", "-")
    with open(f"data/snapshots/conagua_{ts}.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    raw = fetch()
    cdmx = filtrar_cdmx(raw)
    grupos = agrupar_por_alcaldia(cdmx)
    payload = build_payload(grupos)
    save(payload)
    print("✓ Actualizado:", payload["generated_at"], "| alcaldías:", len(payload["alcaldias"]))
