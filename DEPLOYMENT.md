# EdBetoSolutions - Deployment Guide

## 🌐 Configuración para edbetosolutions.tech

### Estructura de Producción

```
edbetosolutions.tech/
├── index.html              # Página principal del portafolio
├── frontend/               # Aplicaciones frontend (estáticas)
│   ├── clima/             # Sistema meteorológico
│   ├── llama4/            # Chat frontend
│   ├── micveahc/          # CV interactivo
│   └── UNEGario/          # Sistema universitario
└── backend/               # APIs y servicios (requiere servidor)
    └── llama4/            # API del chat con Llama 4
```

## 🚀 Despliegue Frontend (Estático)

### Opción 1: GitHub Pages
1. Configurar repositorio como público
2. Habilitar GitHub Pages desde `Settings > Pages`
3. Seleccionar rama `main` como fuente
4. El sitio estará disponible en `https://username.github.io/edbetosolutions`

### Opción 2: Netlify
1. Conectar repositorio a Netlify
2. Configurar build settings:
   - Build command: (vacío)
   - Publish directory: `/`
3. Configurar dominio personalizado: `edbetosolutions.tech`

### Opción 3: Vercel
1. Importar proyecto desde GitHub
2. Configurar:
   - Framework Preset: `Other`
   - Root Directory: `/`
   - Build Command: (vacío)
   - Output Directory: (vacío)

## 🖥️ Despliegue Backend

### Requisitos del Servidor
- Python 3.8+
- Puerto disponible (recomendado: 8000)
- Variables de entorno configuradas

### Configuración de Variables de Entorno
```bash
# backend/llama4/.env
NVIDIA_API_KEY=your_nvidia_api_key_here
API_BASE_URL=https://integrate.api.nvidia.com/v1
MODEL_NAME=meta/llama-3.1-70b-instruct
```

### Despliegue en VPS/Cloud
```bash
# 1. Clonar repositorio
git clone https://github.com/Edbeto13/edbetosolutions.git
cd edbetosolutions

# 2. Configurar backend
cd backend/llama4
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 5. Ejecutar en producción
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Usando Docker (Recomendado)
```dockerfile
# Dockerfile para backend/llama4
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔧 Configuración DNS

### Para edbetosolutions.tech
```
# Registros DNS necesarios
A     @     IP_DEL_SERVIDOR
CNAME www   edbetosolutions.tech
```

### Subdominios (Opcional)
```
A     api   IP_DEL_SERVIDOR_BACKEND    # Para api.edbetosolutions.tech
```

## 🔐 SSL/HTTPS

### Certificados SSL Gratuitos
```bash
# Usando Certbot (Let's Encrypt)
sudo certbot --nginx -d edbetosolutions.tech -d www.edbetosolutions.tech
```

## 📊 Monitoreo y Analytics

### Google Analytics
Agregar al `<head>` de cada página:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## 🛡️ Seguridad

### Headers de Seguridad
```nginx
# Configuración Nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self'" always;
```

## 🔄 CI/CD (Continua Integración)

### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy Frontend
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./
```

## 📝 Lista de Verificación Pre-Despliegue

### Frontend ✅
- [x] Rutas actualizadas a estructura `/frontend/`
- [x] Enlaces relativos funcionando
- [x] Imágenes y assets optimizados
- [x] Meta tags SEO configurados
- [x] Responsive design verificado

### Backend ✅
- [x] Variables de entorno configuradas
- [x] CORS habilitado para dominio de producción
- [x] Rate limiting implementado
- [x] Logs configurados
- [x] Health check endpoint disponible

### Seguridad ✅
- [x] API keys en variables de entorno
- [x] HTTPS configurado
- [x] Headers de seguridad implementados
- [x] Validación de entrada en APIs

## 🆘 Troubleshooting

### Problemas Comunes

1. **Error 404 en rutas frontend**
   - Verificar que las rutas en `index.html` apunten a `/frontend/`

2. **CORS error en API**
   - Configurar origins permitidos en FastAPI backend

3. **SSL certificate error**
   - Renovar certificado Let's Encrypt

4. **Backend no responde**
   - Verificar que el servicio esté ejecutándose
   - Comprobar firewall y puertos abiertos

## 📞 Soporte

- **Email**: edbeto13@gmail.com
- **GitHub Issues**: https://github.com/Edbeto13/edbetosolutions/issues
- **Documentación**: Ver READMEs específicos de cada proyecto
