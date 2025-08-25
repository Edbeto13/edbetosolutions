# 🚀 Instrucciones para Implementar NVIDIA API Server

Estas instrucciones detallan el proceso para implementar el servidor NVIDIA API para Llama 4 en el servidor de producción.

## 📋 Requisitos

- Acceso SSH al servidor (146.190.249.76)
- Credenciales de root o usuario con permisos sudo
- API key de NVIDIA NIM: `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`

## 1️⃣ Conexión al servidor

Usa tu cliente SSH favorito para conectarte al servidor:

```powershell
ssh -i "C:\sshkeys\id_ed25519" root@146.190.249.76
```

## 2️⃣ Configurar el entorno

Una vez conectado, navega al directorio del proyecto:

```bash
cd /var/www/html/edbetosolutions/backend
```

Asegúrate de tener las dependencias necesarias:

```bash
pip3 install requests
```

## 3️⃣ Actualizar archivos

Sube los archivos actualizados al servidor. Puedes usar SCP, SFTP o actualizar directamente en el servidor con un editor.

### Usando SCP (desde tu PC local):

```powershell
# Sube el archivo nvidia_api_server.py
scp -i "C:\sshkeys\id_ed25519" "c:\edbetosolutions\backend\nvidia_api_server.py" root@146.190.249.76:/var/www/html/edbetosolutions/backend/

# Sube el script de administración
scp -i "C:\sshkeys\id_ed25519" "c:\edbetosolutions\backend\scripts\run_nvidia_server.sh" root@146.190.249.76:/var/www/html/edbetosolutions/backend/scripts/
```

### O edita directamente en el servidor:

```bash
# Usa tu editor preferido (nano/vim)
nano nvidia_api_server.py
```

## 4️⃣ Configurar el script de administración

```bash
# Navega al directorio de scripts
cd /var/www/html/edbetosolutions/backend/scripts

# Da permisos de ejecución al script
chmod +x run_nvidia_server.sh
```

## 5️⃣ Configurar la API key de NVIDIA como variable de entorno

Para una sesión temporal:

```bash
export NVIDIA_API_KEY="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"
```

Para configuración permanente:

```bash
# Crear archivo .env en el directorio backend
echo 'NVIDIA_API_KEY="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"' > /var/www/html/edbetosolutions/backend/.env

# O añadir al perfil del sistema
echo 'export NVIDIA_API_KEY="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"' >> /root/.bashrc
source /root/.bashrc
```

## 6️⃣ Iniciar el servidor

Usando el script de administración:

```bash
# Navegar al directorio de scripts
cd /var/www/html/edbetosolutions/backend/scripts

# Iniciar el servidor
./run_nvidia_server.sh start
```

O manualmente:

```bash
cd /var/www/html/edbetosolutions/backend
nohup python3 nvidia_api_server.py > nvidia_server.log 2>&1 &
```

## 7️⃣ Verificar estado

Comprueba que el servidor esté funcionando correctamente:

```bash
# Ver estado con el script de administración
./run_nvidia_server.sh status

# Ver logs
./run_nvidia_server.sh logs

# O comprobar el proceso manualmente
ps aux | grep nvidia_api_server.py
```

Prueba los endpoints:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/status
curl http://localhost:8000/api/chat/status
```

## 8️⃣ Configuración de Nginx

Asegúrate de que Nginx esté configurado para redireccionar los endpoints del API:

```bash
nano /etc/nginx/sites-available/edbetosolutions.tech
```

Verifica que exista la configuración para los endpoints del API:

```nginx
# Dentro del bloque server
location /api/chat {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

location /api/chat/status {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

location /api/status {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

Si hiciste cambios, reinicia Nginx:

```bash
nginx -t  # Verifica configuración
systemctl restart nginx
```

## 9️⃣ Prueba final

Desde tu navegador, accede a:
- https://edbetosolutions.tech/frontend/llama4/index.html

Verifica que puedas enviar mensajes y recibir respuestas del modelo Llama 4 a través de NVIDIA NIM.

## 🔍 Solución de problemas

### El servidor no inicia:
Verifica los logs:
```bash
cat /var/www/html/edbetosolutions/backend/nvidia_server.log
```

### Error de conexión a NVIDIA:
Verifica la API key:
```bash
echo $NVIDIA_API_KEY
```

### El frontend no se conecta al backend:
Verifica la configuración de Nginx y que el servidor esté escuchando:
```bash
netstat -tulpn | grep 8000
curl -s http://localhost:8000/health
```

## 📞 Contacto de soporte

Si tienes problemas durante la implementación, contacta a:
- Email: soporte@edbetosolutions.tech
- Teléfono: +52 987 654 3210
