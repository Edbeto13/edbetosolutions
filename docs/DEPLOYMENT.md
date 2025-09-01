# 🚀 Guía de Deployment - EdBetoSolutions

## 📋 Información del Servidor

- **IP del Servidor**: `146.190.249.76`
- **Proveedor**: DigitalOcean Droplet
- **Sistema Operativo**: Ubuntu
- **Ruta de Deployment**: `/var/www/html/edbetosolutions`
- **URL del Sitio**: [https://edbetosolutions.tech](https://edbetosolutions.tech)

## 🔧 Configuración Inicial Completada

✅ Servidor configurado y funcionando  
✅ Dominio apuntando correctamente  
✅ SSL configurado  
✅ Git repository clonado  
✅ Permisos configurados  

## 🚀 Deployment Manual (Recomendado)

### Opción 1: SSH Directo

```bash
# Conectar al servidor
ssh -i "$SSH_KEY_PATH" $SERVER_USER@$SERVER_IP

# Una vez conectado, ejecutar:
cd $REMOTE_PATH
git pull origin main
chown -R www-data:www-data /var/www/html/edbetosolutions
chmod -R 755 /var/www/html/edbetosolutions
```

### Opción 2: Script PowerShell Local

```powershell
# Comando único para deployment completo
ssh -i "C:\betroplet_openssh" root@146.190.249.76 "cd /var/www/html/edbetosolutions && git fetch origin && git reset --hard origin/main && git pull origin main && chown -R www-data:www-data /var/www/html/edbetosolutions && chmod -R 755 /var/www/html/edbetosolutions && echo 'Deployment completed successfully!'"
```

## 🔄 Workflow Automático (GitHub Actions)

### Estado Actual: ✅ SOLUCIONADO
- ✅ **Workflow simplificado**: Solo validación y testing
- ✅ **No más workflows atascados**: Auto-deployment deshabilitado
- ✅ **Validaciones funcionando**: HTML, CSS, JS, estructura del proyecto

### ¿Por qué se Cambiaron los Workflows?

Los workflows automáticos se atascaban porque:
1. **❌ Falta de SSH Secret**: GitHub no tenía acceso a la llave privada
2. **❌ Timeouts**: Conexiones SSH fallaban ocasionalmente  
3. **❌ Permisos**: Problemas con permisos de archivos
4. **❌ Dependencias**: Fallos en dependencias de deployment

### ✅ Solución Implementada

```yaml
name: Build and Test  # ← Cambió de "Auto Deploy"
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:  # ← Cambió de "deploy"
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
    - name: Validate HTML files      # ← Nuevo
    - name: Validate CSS files       # ← Nuevo  
    - name: Validate JavaScript files # ← Nuevo
    - name: Check project structure  # ← Nuevo
    - name: Verify documentation     # ← Nuevo
```

## 🌐 URLs del Sitio en Producción

### Sitio Principal
- **🏠 Landing Page**: https://edbetosolutions.tech/
- **🎯 Portafolio Completo**: https://edbetosolutions.tech/frontend/Portafolio/

### Aplicaciones Individuales
- **🌦️ Sistema Meteorológico**: https://edbetosolutions.tech/frontend/clima/
- **🦙 Chat con Llama 4**: https://edbetosolutions.tech/frontend/llama4/
- **👨‍💼 CV Web Interactivo**: https://edbetosolutions.tech/frontend/micveahc/
- **📚 Sistema Universitario**: https://edbetosolutions.tech/frontend/UNEGario/

## 🔐 Configuración SSH (Opcional para Auto-deployment)

Si en el futuro quieres restaurar el auto-deployment:

### 1. Agregar SSH Key a GitHub Secrets

1. Ve a tu repositorio en GitHub
2. `Settings > Secrets and variables > Actions`
3. Crea un nuevo secret llamado: `DO_SSH_PRIVATE_KEY`
4. Copia el contenido completo de `C:\betroplet_openssh`

### 2. Restaurar Workflow Original

```yaml
- name: Setup SSH
  uses: webfactory/ssh-agent@v0.7.0
  with:
    ssh-private-key: ${{ secrets.DO_SSH_PRIVATE_KEY }}

- name: Deploy to DigitalOcean
  run: |
    ssh -o StrictHostKeyChecking=no root@146.190.249.76 << 'EOF'
      cd /var/www/html/edbetosolutions
      git pull origin main
      # ... resto del deployment
    EOF
```

## 🚨 Solución a Workflows Atascados

### ✅ Pasos Implementados

1. **Workflow Simplificado**: Removido auto-deployment problemático
2. **Solo Validaciones**: Testing y verificación de estructura
3. **Sin SSH Dependencies**: No requiere llaves ni conexiones externas
4. **Deployment Manual**: Control total sobre cuándo y cómo hacer deploy

### 🔧 Comandos de Deployment Manual

```powershell
# Comando completo (copia y pega esto)
ssh -i "C:\betroplet_openssh" root@146.190.249.76 "cd /var/www/html/edbetosolutions && echo 'Starting deployment...' && git fetch origin && git reset --hard origin/main && git pull origin main && chown -R www-data:www-data /var/www/html/edbetosolutions && chmod -R 755 /var/www/html/edbetosolutions && find /var/www/html/edbetosolutions -type f -exec chmod 644 {} \; && echo '✅ Deployment completed successfully!' && echo '🌐 Site available at: https://edbetosolutions.tech'"
```

### 🔍 Verificación del Deployment

```powershell
# Verificar que el sitio esté funcionando
ssh -i "C:\betroplet_openssh" root@146.190.249.76 "curl -I http://localhost && echo 'Server status check completed'"
```

## 📊 Monitoreo del Servidor

### Estado del Servidor
```bash
ssh -i "C:\betroplet_openssh" root@146.190.249.76 "systemctl status nginx"
```

### Logs en Tiempo Real
```bash
ssh -i "C:\betroplet_openssh" root@146.190.249.76 "tail -f /var/log/nginx/access.log"
```

### Espacio en Disco
```bash
ssh -i "C:\betroplet_openssh" root@146.190.249.76 "df -h"
```

## 🚨 Troubleshooting

### Problemas de Conexión SSH
```powershell
# Test de conexión básica
ssh -i "C:\betroplet_openssh" root@146.190.249.76 "echo 'Conexión SSH exitosa'"
```

### Problemas de Permisos
```bash
# Ejecutar en el servidor si hay problemas de permisos
sudo chown -R www-data:www-data /var/www/html/edbetosolutions
sudo chmod -R 755 /var/www/html/edbetosolutions
sudo find /var/www/html/edbetosolutions -type f -exec chmod 644 {} \;
```

### Conflictos de Git
```bash
# Si hay conflictos de Git en el servidor
cd /var/www/html/edbetosolutions
git fetch origin
git reset --hard origin/main
git pull origin main
```

### Cancelar Workflows Atascados (si aún los tienes)
1. Ve a tu repositorio en GitHub
2. Click en la pestaña "Actions"
3. Click en los workflows en ejecución
4. Click "Cancel workflow"

---

## ✅ Resumen de la Solución

**🎯 Problema Original**: Workflows de GitHub Actions atascados en deployment automático  
**🔧 Solución Implementada**: Workflow simplificado sin auto-deployment  
**🚀 Resultado**: Sin más workflows atascados + deployment manual confiable  
**🌐 Estado**: Sitio funcionando perfectamente en https://edbetosolutions.tech  

**📅 Fecha de solución**: Enero 2025  
**👨‍💻 Implementado por**: Edson Alberto Herrera Cervantes

<!-- Deployment trigger: 2025-08-25 01:36:09 -->
