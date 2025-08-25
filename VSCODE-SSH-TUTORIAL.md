# 🚀 Tutorial: VS Code Remote SSH para Llama4 Chat

## 🎯 **Objetivo**: Subir y deployar Llama4 Chat al droplet usando VS Code

---

## 📋 **Paso a Paso Detallado**

### **Paso 1: Abrir Command Palette**
1. **Presiona**: `Ctrl + Shift + P`
2. **Escribe**: `Remote-SSH: Connect to Host`
3. **Selecciona** la opción que aparece

### **Paso 2: Agregar Host SSH**
1. **Si es la primera vez**, selecciona: `Add New SSH Host`
2. **Escribe**: `root@146.190.249.76`
3. **Presiona Enter**
4. **Selecciona** el archivo de configuración (generalmente el primero)

### **Paso 3: Conectar al Droplet**
1. **Vuelve a presionar**: `Ctrl + Shift + P`
2. **Escribe**: `Remote-SSH: Connect to Host`
3. **Selecciona**: `146.190.249.76` o `root@146.190.249.76`
4. **Selecciona**: `Linux` cuando pregunte el tipo de sistema
5. **Ingresa la contraseña** del droplet cuando la pida

### **Paso 4: Abrir Directorio en el Droplet**
1. Una vez conectado, **presiona**: `Ctrl + O`
2. **Navega a**: `/var/www/`
3. **Crea carpeta** `llama4-chat` si no existe:
   - Click derecho → `New Folder`
   - Nombre: `llama4-chat`

### **Paso 5: Subir Archivos**
**Opción A - Drag & Drop (Más fácil):**
1. **Abre Explorer** en Windows: `C:\Users\edbet\AppData\Local\Temp\llama4-chat-clean\`
2. **Selecciona todos** los archivos (`Ctrl + A`)
3. **Arrastra y suelta** en VS Code en la carpeta `/var/www/llama4-chat/`

**Opción B - SFTP Extension:**
1. **Instala extensión SFTP** si no la tienes
2. **Presiona**: `Ctrl + Shift + P`
3. **Escribe**: `SFTP: Upload Folder`
4. **Selecciona** el directorio local: `C:\Users\edbet\AppData\Local\Temp\llama4-chat-clean\`

### **Paso 6: Ejecutar Deployment**
1. **Abre terminal** en VS Code: `Ctrl + Shift + `` ` `` (backtick)
2. **Navega** al directorio:
   ```bash
   cd /var/www/llama4-chat
   ```
3. **Hacer ejecutable** el script:
   ```bash
   chmod +x deploy.sh
   ```
4. **Ejecutar deployment**:
   ```bash
   sudo ./deploy.sh
   ```

### **Paso 7: Verificar Deployment**
1. **El script debe mostrar**:
   - ✅ Cliente NIM inicializado correctamente
   - ✅ Servicios antiguos limpiados
   - ✅ Nginx configurado
   - ✅ Supervisor configurado
   - ✅ Aplicación ejecutándose

2. **Verificar en navegador**: `http://146.190.249.76:8000`

---

## 🆘 **Resolución de Problemas**

### **Problema: No puede conectar SSH**
```bash
# Verificar que SSH está activo
sudo systemctl status ssh
sudo systemctl start ssh
```

### **Problema: Permisos denegados**
```bash
# Dar permisos correctos
sudo chown -R root:root /var/www/llama4-chat
sudo chmod -R 755 /var/www/llama4-chat
```

### **Problema: Puerto ocupado**
```bash
# Verificar qué usa el puerto 8000
sudo netstat -tlnp | grep :8000
# Detener proceso si es necesario
sudo kill -9 [PID]
```

---

## 📁 **Archivos que Vas a Subir**
- ✅ `app.py` (4.8KB) - Aplicación principal
- ✅ `requirements.txt` (102B) - Dependencias
- ✅ `deploy.sh` (4.9KB) - Script de deployment
- ✅ `.env` (456B) - Variables de entorno
- ✅ `nginx-llama4-chat.conf` (2.3KB) - Config Nginx
- ✅ `src/` - Código fuente (nim_client.py, models.py, settings.py)
- ✅ `config/` - Configuraciones
- ✅ `templates/` - Frontend HTML
- ✅ `static/` - CSS y JavaScript

---

## 🌐 **URLs Finales**
- **Aplicación**: http://146.190.249.76:8000
- **Con Nginx**: http://146.190.249.76
- **API Status**: http://146.190.249.76:8000/api/status
- **API Health**: http://146.190.249.76:8000/api/health

---

**💡 Consejo**: Mantén VS Code conectado al droplet para monitorear logs y hacer cambios rápidamente.
