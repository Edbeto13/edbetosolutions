#!/usr/bin/env python3
"""
🚀 Script de construcción consolidado para UNEGario
Automatiza todo el proceso de generación y despliegue
Versión: 2.0.0 - Consolidado de UNEGariobuild.py y build.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class UNEGarioBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.backend_dir = self.project_root / "src" / "backend"
        self.frontend_dir = self.project_root / "src" / "frontend" / "UNEGario"
        self.output_dir = self.project_root / "src" / "output"
        
        print("🏗️ UNEGario Builder v2.0.0 - Consolidado")
        print("=" * 50)
        print(f"📁 Proyecto: {self.project_root}")
        print(f"⚙️ Backend: {self.backend_dir}")
        print(f"🎨 Frontend: {self.frontend_dir}")
        print(f"📤 Output: {self.output_dir}")
        print()

    def check_dependencies(self):
        """Verifica que todas las dependencias estén instaladas"""
        print("🔍 Verificando dependencias...")
        
        try:
            import openpyxl
            print("   ✅ openpyxl encontrado")
        except ImportError:
            print("   ❌ openpyxl no encontrado")
            print("   📦 Instalando openpyxl...")
            subprocess.run([sys.executable, "-m", "pip", "install", "openpyxl>=3.0.0"], 
                         check=True)
            print("   ✅ openpyxl instalado correctamente")
        
        # Verificar estructura de archivos
        required_files = [
            self.backend_dir / "UNEGario_GoogleCalendar.py",
            self.frontend_dir / "UNEGario.html",
            self.frontend_dir / "unegario.js",
        ]
        
        for file_path in required_files:
            if file_path.exists():
                print(f"   ✅ {file_path.name}")
            else:
                print(f"   ❌ {file_path.name} - No encontrado")
                return False
        
        return True

    def generate_schedule_data(self):
        """Genera los datos del horario ejecutando el script Python"""
        print("\n📊 Generando datos del horario...")
        
        os.chdir(self.backend_dir)
        try:
            result = subprocess.run([sys.executable, "UNEGario_GoogleCalendar.py"], 
                                  capture_output=True, text=True, check=True)
            print("   ✅ Datos generados exitosamente")
            print(f"   📋 Output: {result.stdout.strip()}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Error generando datos: {e}")
            print(f"   📋 Stderr: {e.stderr}")
            return False

    def verify_output_files(self):
        """Verifica que los archivos de salida se generaron correctamente"""
        print("\n🔍 Verificando archivos generados...")
        
        output_files = [
            self.output_dir / "horario_data.json",
            self.output_dir / "google_calendar_url.txt"
        ]
        
        for file_path in output_files:
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"   ✅ {file_path.name} ({size} bytes)")
            else:
                print(f"   ❌ {file_path.name} - No encontrado")
                return False
        
        return True

    def test_local_server(self):
        """Inicia un servidor local para probar la aplicación"""
        print("\n🌐 Iniciando servidor local de prueba...")
        print("   🔗 URL: http://localhost:8080/UNEGario.html")
        print("   ⏹️ Presiona Ctrl+C para detener")
        
        os.chdir(self.frontend_dir)
        try:
            subprocess.run([sys.executable, "-m", "http.server", "8080"])
        except KeyboardInterrupt:
            print("\n   ✅ Servidor detenido")

    def deploy_to_server(self, server_ip="146.190.249.76", server_path="/var/www/html/"):
        """Despliega los archivos al servidor de producción"""
        print(f"\n🚀 Desplegando a servidor {server_ip}...")
        
        try:
            # Copiar directorio UNEGario
            cmd1 = [
                "scp", "-r", 
                "-o", "StrictHostKeyChecking=no", 
                "-o", "UserKnownHostsFile=/dev/null",
                str(self.frontend_dir), 
                f"root@{server_ip}:{server_path}"
            ]
            subprocess.run(cmd1, check=True)
            print("   ✅ Archivos frontend copiados")
            
            # Copiar directorio output
            cmd2 = [
                "scp", "-r", 
                "-o", "StrictHostKeyChecking=no", 
                "-o", "UserKnownHostsFile=/dev/null",
                str(self.output_dir), 
                f"root@{server_ip}:{server_path}UNEGario/"
            ]
            subprocess.run(cmd2, check=True)
            print("   ✅ Archivos de datos copiados")
            
            print(f"   🌍 Sitio disponible en: https://edbetosolutions.tech/UNEGario/UNEGario.html")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Error en despliegue: {e}")
            return False

    def create_distribution(self):
        """Crea un paquete de distribución con todos los archivos necesarios"""
        print("\n📦 Creando paquete de distribución...")
        
        dist_dir = self.project_root / "dist" / "UNEGario"
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
        
        dist_dir.mkdir(parents=True, exist_ok=True)
        
        # Copiar archivos frontend
        shutil.copytree(self.frontend_dir, dist_dir / "UNEGario")
        
        # Copiar archivos output
        if self.output_dir.exists():
            shutil.copytree(self.output_dir, dist_dir / "UNEGario" / "output")
        
        # Crear archivo ZIP
        shutil.make_archive(str(dist_dir), 'zip', str(dist_dir))
        
        print(f"   ✅ Paquete creado: {dist_dir}.zip")
        return True

    def build_all(self):
        """Ejecuta todo el proceso de construcción"""
        print("🏗️ INICIANDO CONSTRUCCIÓN COMPLETA")
        print("=" * 50)
        
        steps = [
            ("🔍 Verificar dependencias", self.check_dependencies),
            ("📊 Generar datos", self.generate_schedule_data),
            ("✅ Verificar archivos", self.verify_output_files),
            ("📦 Crear distribución", self.create_distribution)
        ]
        
        for step_name, step_func in steps:
            print(f"\n{step_name}...")
            if not step_func():
                print(f"❌ FALLO EN: {step_name}")
                return False
        
        print("\n" + "=" * 50)
        print("🎉 ¡CONSTRUCCIÓN COMPLETADA EXITOSAMENTE!")
        print("🌍 Para probar localmente: python build.py --test")
        print("🚀 Para desplegar: python build.py --deploy")
        print("=" * 50)
        return True

def main():
    builder = UNEGarioBuilder()
    
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg == "--test":
            if builder.check_dependencies() and builder.generate_schedule_data():
                builder.test_local_server()
        elif arg == "--deploy":
            if builder.build_all():
                builder.deploy_to_server()
        elif arg == "--build":
            builder.build_all()
        elif arg == "--check":
            builder.check_dependencies()
            builder.verify_output_files()
        else:
            print("❌ Argumento no reconocido")
            print("Uso: python build.py [--build|--test|--deploy|--check]")
    else:
        builder.build_all()

if __name__ == "__main__":
    main()
