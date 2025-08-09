# edbetosolutions · Clima CDMX

## Estructura
```
etl/                    # scripts de extracción/transformación
web/                    # frontend estático (raíz del sitio)
  ├─ index.html
  ├─ styles.css
  ├─ app.js
  └─ chatbot/bot.js
data/                   # salidas JSON del ETL (expuestas a /data/)
scripts/
  └─ deploy_symlinks.sh
```

## Requisitos
- Python 3.11+ (`zoneinfo` estándar)
- `pip install requests`

## Generar datos
Desde la raíz:
```bash
python etl/fetch_conagua_cdmx.py
```
Esto crea:
- `data/latest_conagua_cdmx.json`
- `data/snapshots/conagua_*.json`

## Exponer datos al frontend
```bash
bash scripts/deploy_symlinks.sh
```
Sirve **web/** como raíz. El frontend lee `./data/latest_conagua_cdmx.json`.

### Nginx (ejemplo)
```
server {
  server_name edbetosolutions.tech;
  root /var/www/edbetosolutions/web;

  location / { try_files $uri /index.html; }
  # (Opcional) Si prefieres sin symlink:
  # location /data/ { alias /var/www/edbetosolutions/data/; autoindex off; }
}
```

## Actualización automática
Cada 90 min con cron:
```
*/90 * * * * cd /var/www/edbetosolutions && /usr/bin/python3 etl/fetch_conagua_cdmx.py >> log.txt 2>&1
```

## Desarrollo local
```bash
python etl/fetch_conagua_cdmx.py
bash scripts/deploy_symlinks.sh
# servidor estático rápido:
python -m http.server -d web 8080
# abrir http://localhost:8080
```
