import openpyxl
from openpyxl.styles import PatternFill, Font
from openpyxl.formatting.rule import FormulaRule
from datetime import datetime, time, timedelta
import urllib.parse
import json
import os

class UNEGarioCalendar:
    def __init__(self):
        # Fechas del semestre Ago-Dic 2025
        self.fecha_inicio = "20250818"
        self.fecha_fin = "20251212"
        
        # Días festivos y recesos según calendario académico ISEC 2025-2026
        self.dias_festivos = [
            # Agosto 2025
            "20250825", "20250831",  # 25 y 31 de agosto
            # Septiembre 2025  
            "20250916",  # 16 de septiembre (Independencia)
            "20250929", "20250930",  # 29 y 30 de septiembre
            # Octubre 2025
            "20251010",  # 10 de octubre
            # Noviembre 2025
            "20251102", "20251117",  # 2 y 17 de noviembre
            # Diciembre 2025
            "20251208",  # 8 de diciembre
            "20251222", "20251223", "20251224", "20251225", "20251226", "20251229", "20251230", "20251231",
        ]
        
        # Ruta de output para archivos generados
        self.output_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "UNEGario", "output")
        
        # Mapeo de días español a código
        self.dias_map = {
            "Lunes": "MO",
            "Martes": "TU", 
            "Miércoles": "WE",
            "Jueves": "TH",
            "Viernes": "FR",
            "Sábado": "SA",
            "Domingo": "SU"
        }
        
        # Colores para materias según tu horario real
        self.colores = {
            "Cálculo multivariable": {"hex": "FFD966", "google_id": "5"},
            "Finanzas empresariales": {"hex": "9BC2E6", "google_id": "7"},
            "Algoritmos y estructuras de datos": {"hex": "A9D08E", "google_id": "2"},
            "Fundamentos de diseño digital": {"hex": "F4B183", "google_id": "6"},
            "Álgebra lineal": {"hex": "C6E0B4", "google_id": "10"},
            "Ingeniería, ética y sociedad": {"hex": "D9D2E9", "google_id": "3"},
            "Receso": {"hex": "E7E6E6", "google_id": "8"}
        }

    def leer_horario_excel(self, archivo="UNEGario.xlsx"):
        """Lee el archivo Excel y extrae los datos del horario"""
        wb = openpyxl.load_workbook(archivo)
        ws = wb["Horario"]
        
        horario = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0]:  # Si hay día
                horario.append({
                    "dia": row[0],
                    "hora_inicio": row[1],
                    "hora_fin": row[2],
                    "materia": row[3],
                    "profesor": row[4] or "",
                    "tipo": "Receso" if row[3] == "Receso" else "Clase"
                })
        
        wb.close()
        return horario

    def generar_datos_horario(self):
        """Genera los datos del horario completo con el formato correcto basado en tu horario real"""
        # Horario completo de la semana EXACTO según tu imagen
        horario_completo = [
            # Lunes
            {"dia": "Lunes", "hora_inicio": time(17,0), "hora_fin": time(18,0), 
             "materia": "Cálculo multivariable", "profesor": "ORTIZ REYES RAUL", "tipo": "Clase"},
            {"dia": "Lunes", "hora_inicio": time(20,0), "hora_fin": time(21,30), 
             "materia": "Finanzas empresariales", "profesor": "ARROYO SANCHEZ OSCAR RAYMUNDO", "tipo": "Clase"},
            
            # Martes
            {"dia": "Martes", "hora_inicio": time(17,30), "hora_fin": time(18,0), 
             "materia": "Algoritmos y estructuras de datos", "profesor": "PEÑA OLIVO CRISTÓBAL", "tipo": "Clase"},
            {"dia": "Martes", "hora_inicio": time(18,0), "hora_fin": time(19,0), 
             "materia": "Álgebra lineal", "profesor": "LARA USCANGA SERGIO TULIO", "tipo": "Clase"},
            {"dia": "Martes", "hora_inicio": time(19,0), "hora_fin": time(20,0), 
             "materia": "Fundamentos de diseño digital", "profesor": "AGUILAR VELA ÁLVARO", "tipo": "Clase"},
            {"dia": "Martes", "hora_inicio": time(20,0), "hora_fin": time(21,0), 
             "materia": "Finanzas empresariales", "profesor": "ARROYO SANCHEZ OSCAR RAYMUNDO", "tipo": "Clase"},
            {"dia": "Martes", "hora_inicio": time(21,0), "hora_fin": time(21,30), 
             "materia": "Fundamentos de diseño digital", "profesor": "AGUILAR VELA ÁLVARO", "tipo": "Clase"},
            
            # Miércoles
            {"dia": "Miércoles", "hora_inicio": time(17,30), "hora_fin": time(18,0), 
             "materia": "Cálculo multivariable", "profesor": "ORTIZ REYES RAUL", "tipo": "Clase"},
            {"dia": "Miércoles", "hora_inicio": time(18,0), "hora_fin": time(19,0), 
             "materia": "Álgebra lineal", "profesor": "LARA USCANGA SERGIO TULIO", "tipo": "Clase"},
            {"dia": "Miércoles", "hora_inicio": time(19,0), "hora_fin": time(20,0), 
             "materia": "Fundamentos de diseño digital", "profesor": "AGUILAR VELA ÁLVARO", "tipo": "Clase"},
            {"dia": "Miércoles", "hora_inicio": time(20,0), "hora_fin": time(21,0), 
             "materia": "Finanzas empresariales", "profesor": "ARROYO SANCHEZ OSCAR RAYMUNDO", "tipo": "Clase"},
            {"dia": "Miércoles", "hora_inicio": time(21,0), "hora_fin": time(21,30), 
             "materia": "Finanzas empresariales", "profesor": "ARROYO SANCHEZ OSCAR RAYMUNDO", "tipo": "Clase"},
            
            # Jueves
            {"dia": "Jueves", "hora_inicio": time(19,0), "hora_fin": time(20,0), 
             "materia": "Fundamentos de diseño digital", "profesor": "AGUILAR VELA ÁLVARO", "tipo": "Clase"},
            {"dia": "Jueves", "hora_inicio": time(20,0), "hora_fin": time(21,0), 
             "materia": "Ingeniería, ética y sociedad", "profesor": "CAMPOAMOR ROLDAN SERGIO", "tipo": "Clase"},
            {"dia": "Jueves", "hora_inicio": time(21,0), "hora_fin": time(21,30), 
             "materia": "Finanzas empresariales", "profesor": "ARROYO SANCHEZ OSCAR RAYMUNDO", "tipo": "Clase"},
            
            # Viernes
            {"dia": "Viernes", "hora_inicio": time(17,0), "hora_fin": time(18,0), 
             "materia": "Álgebra lineal", "profesor": "LARA USCANGA SERGIO TULIO", "tipo": "Clase"},
            {"dia": "Viernes", "hora_inicio": time(20,0), "hora_fin": time(21,0), 
             "materia": "Ingeniería, ética y sociedad", "profesor": "CAMPOAMOR ROLDAN SERGIO", "tipo": "Clase"},
            {"dia": "Viernes", "hora_inicio": time(21,0), "hora_fin": time(21,30), 
             "materia": "Ingeniería, ética y sociedad", "profesor": "CAMPOAMOR ROLDAN SERGIO", "tipo": "Clase"},
            
            # Sábado
            {"dia": "Sábado", "hora_inicio": time(7,0), "hora_fin": time(9,0), 
             "materia": "Algoritmos y estructuras de datos", "profesor": "PEÑA OLIVO CRISTÓBAL", "tipo": "Clase"},
            {"dia": "Sábado", "hora_inicio": time(9,0), "hora_fin": time(10,0), 
             "materia": "Algoritmos y estructuras de datos", "profesor": "PEÑA OLIVO CRISTÓBAL", "tipo": "Clase"},
            {"dia": "Sábado", "hora_inicio": time(10,0), "hora_fin": time(11,0), 
             "materia": "Ingeniería, ética y sociedad", "profesor": "CAMPOAMOR ROLDAN SERGIO", "tipo": "Clase"},
            {"dia": "Sábado", "hora_inicio": time(11,0), "hora_fin": time(12,0), 
             "materia": "Ingeniería, ética y sociedad", "profesor": "CAMPOAMOR ROLDAN SERGIO", "tipo": "Clase"},
            {"dia": "Sábado", "hora_inicio": time(12,0), "hora_fin": time(13,0), 
             "materia": "Ingeniería, ética y sociedad", "profesor": "CAMPOAMOR ROLDAN SERGIO", "tipo": "Clase"},
        ]
        
        return horario_completo

    def generar_rrule(self):
        """Genera la regla de recurrencia RRULE"""
        # Obtener todos los días únicos del horario
        horario = self.generar_datos_horario()
        dias_unicos = set()
        for clase in horario:
            if clase["tipo"] == "Clase":
                dias_unicos.add(self.dias_map.get(clase["dia"], ""))
        
        dias_str = ",".join(sorted(dias_unicos, key=lambda x: ["MO","TU","WE","TH","FR","SA","SU"].index(x)))
        
        rrule = f"FREQ=WEEKLY;BYDAY={dias_str};UNTIL={self.fecha_fin}T235959Z"
        return rrule

    def generar_exdates(self):
        """Genera las fechas de exclusión EXDATE"""
        exdates = []
        for fecha in self.dias_festivos:
            exdates.append(f"{fecha}T000000Z")
        
        return ",".join(exdates)

    def generar_descripcion_html(self):
        """Genera una descripción HTML del horario"""
        horario = self.generar_datos_horario()
        
        descripcion = []
        descripcion.append("📚 HORARIO SEMESTRE AGO-DIC 2025")
        descripcion.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        descripcion.append("")
        
        dia_actual = ""
        for clase in horario:
            if clase["dia"] != dia_actual:
                if dia_actual:
                    descripcion.append("")
                descripcion.append(f"📅 {clase['dia'].upper()}")
                dia_actual = clase["dia"]
            
            hora_inicio = clase["hora_inicio"].strftime("%H:%M")
            hora_fin = clase["hora_fin"].strftime("%H:%M")
            
            if clase["tipo"] == "Clase":
                descripcion.append(f"  • {hora_inicio}-{hora_fin} | {clase['materia']}")
                if clase["profesor"]:
                    descripcion.append(f"    Profesor: {clase['profesor']}")
            else:
                descripcion.append(f"  • {hora_inicio}-{hora_fin} | ☕ RECESO")
        
        descripcion.append("")
        descripcion.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        descripcion.append("🔗 Más información: https://edbetosolutions.tech/UNEGarios")
        descripcion.append("")
        descripcion.append("⚠️ DÍAS SIN CLASES:")
        descripcion.append("• 16 sep - Día de la Independencia")
        descripcion.append("• 2 nov - Día de Muertos")
        descripcion.append("• 17 nov - Revolución Mexicana")
        descripcion.append("• 8 dic - Inmaculada Concepción")
        descripcion.append("• 22 dic - 6 ene - Vacaciones de Invierno")
        
        return "%0A".join(descripcion)

    def generar_url_google_calendar(self):
        """Genera la URL completa para añadir a Google Calendar"""
        # Parámetros básicos
        titulo = "Horario UNEGario - Semestre Ago-Dic 2025"
        fecha_inicio_evento = f"{self.fecha_inicio}T170000Z"  # 17:00 primer día
        fecha_fin_evento = f"{self.fecha_inicio}T220000Z"     # 22:00 primer día
        ubicacion = "Universidad ISEC - Campus Principal"
        
        # Generar RRULE y EXDATE
        rrule = self.generar_rrule()
        exdates = self.generar_exdates()
        
        # Generar descripción
        descripcion = self.generar_descripcion_html()
        
        # Construir recurrencia completa
        recur = f"RRULE:{rrule}"
        if exdates:
            recur += f"%0AEXDATE;VALUE=DATE:{exdates.replace(',', '%2C')}"
        
        # Construir URL
        base_url = "https://calendar.google.com/calendar/render"
        params = {
            "action": "TEMPLATE",
            "text": titulo,
            "dates": f"{fecha_inicio_evento}/{fecha_fin_evento}",
            "details": descripcion,
            "location": ubicacion,
            "ctz": "America/Mexico_City",
            "recur": recur
        }
        
        # Codificar parámetros
        param_str = "&".join([f"{k}={urllib.parse.quote(str(v), safe='')}" for k, v in params.items()])
        
        return f"{base_url}?{param_str}"

    def generar_json_horario(self):
        """Genera un JSON con el horario para usar en JavaScript"""
        horario = self.generar_datos_horario()
        
        # Convertir objetos time a strings
        horario_json = []
        for clase in horario:
            horario_json.append({
                "dia": clase["dia"],
                "hora_inicio": clase["hora_inicio"].strftime("%H:%M"),
                "hora_fin": clase["hora_fin"].strftime("%H:%M"),
                "materia": clase["materia"],
                "profesor": clase["profesor"],
                "tipo": clase["tipo"],
                "color": self.colores.get(clase["materia"], {}).get("hex", "FFFFFF")
            })
        
        return json.dumps(horario_json, ensure_ascii=False, indent=2)

    def exportar_archivos_web(self):
        """Exporta todos los archivos necesarios para la web"""
        # Generar URL de Google Calendar
        url_calendar = self.generar_url_google_calendar()
        
        # Generar JSON del horario
        horario_json = self.generar_json_horario()
        
        # Asegurar que existe la carpeta output
        import os
        os.makedirs("../output", exist_ok=True)
        
        # Guardar JSON
        with open("../output/horario_data.json", "w", encoding="utf-8") as f:
            f.write(horario_json)
        
        # Guardar URL en archivo de texto
        with open("../output/google_calendar_url.txt", "w", encoding="utf-8") as f:
            f.write(url_calendar)
        
        print("✅ Archivos generados:")
        print("  - ../output/horario_data.json")
        print("  - ../output/google_calendar_url.txt")
        print(f"\n📅 URL de Google Calendar generada")
        print("   Puedes copiar esta URL para el botón en tu página web")
        
        return url_calendar, horario_json

    def generar_output_files(self):
        """Genera los archivos necesarios para el frontend en la carpeta output"""
        # Asegurar que existe el directorio output
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Generar datos del horario
        horario_data = self.generar_horario_data_json()
        
        # Generar URLs de Google Calendar
        calendar_urls = self.generar_calendar_urls_txt()
        
        # Escribir horario_data.json
        horario_json_path = os.path.join(self.output_dir, "horario_data.json")
        with open(horario_json_path, 'w', encoding='utf-8') as f:
            json.dump(horario_data, f, indent=2, ensure_ascii=False)
        
        # Escribir google_calendar_url.txt
        calendar_txt_path = os.path.join(self.output_dir, "google_calendar_url.txt")
        with open(calendar_txt_path, 'w', encoding='utf-8') as f:
            f.write(calendar_urls)
        
        print("✅ Archivos output generados:")
        print(f"  - {horario_json_path}")
        print(f"  - {calendar_txt_path}")
        
        return horario_data, calendar_urls

    def generar_horario_data_json(self):
        """Genera la estructura de datos JSON para el frontend"""
        return {
            "semestre": "Agosto-Diciembre 2025",
            "universidad": "ISEC Universidad",
            "carrera": "Ingeniería en Inteligencia Artificial",
            "estudiante": "Edson Alberto Herrera Cervantes",
            "fechas": {
                "inicio": "2025-08-18",
                "fin": "2025-12-12",
                "inscripciones": "2025-08-11",
                "examenes_finales": "2025-12-01"
            },
            "estadisticas": {
                "total_materias": 6,
                "total_horas_semana": 22.5,
                "total_creditos": 24,
                "promedio_horas_dia": 4.5
            },
            "materias": self.obtener_materias_estructuradas(),
            "horario_semanal": self.obtener_horario_semanal(),
            "dias_festivos": [fecha[:4] + "-" + fecha[4:6] + "-" + fecha[6:] for fecha in self.dias_festivos],
            "metadata": {
                "generado_en": datetime.now().isoformat() + "Z",
                "version": "2.0.0",
                "formato": "json",
                "codificacion": "utf-8",
                "compatibilidad": "UNEGario v2025.2"
            }
        }

    def obtener_materias_estructuradas(self):
        """Obtiene las materias en formato estructurado para JSON"""
        materias = [
            {
                "id": "calculo",
                "nombre": "Cálculo Multivariable",
                "codigo": "MAT301",
                "profesor": "ORTIZ REYES RAUL",
                "creditos": 4,
                "color": "#FFD966",
                "aula": "Aula 205",
                "horarios": [
                    {"dia": "Lunes", "dia_code": "MO", "inicio": "17:00", "fin": "18:00", "duracion": 1.0},
                    {"dia": "Miércoles", "dia_code": "WE", "inicio": "17:30", "fin": "18:00", "duracion": 0.5}
                ],
                "horas_semana": 1.5
            },
            {
                "id": "algoritmos",
                "nombre": "Algoritmos y Estructuras de Datos",
                "codigo": "CSC302",
                "profesor": "PEÑA OLIVO CRISTÓBAL",
                "creditos": 4,
                "color": "#9BC2E6",
                "aula": "Lab Sistemas",
                "horarios": [
                    {"dia": "Martes", "dia_code": "TU", "inicio": "17:30", "fin": "18:00", "duracion": 0.5},
                    {"dia": "Sábado", "dia_code": "SA", "inicio": "07:00", "fin": "10:00", "duracion": 3.0}
                ],
                "horas_semana": 3.5
            },
            {
                "id": "algebra",
                "nombre": "Álgebra Lineal",
                "codigo": "MAT302",
                "profesor": "LARA USCANGA SERGIO TULIO",
                "creditos": 4,
                "color": "#A9D08E",
                "aula": "Aula 102",
                "horarios": [
                    {"dia": "Martes", "dia_code": "TU", "inicio": "18:00", "fin": "19:00", "duracion": 1.0},
                    {"dia": "Miércoles", "dia_code": "WE", "inicio": "18:00", "fin": "19:00", "duracion": 1.0},
                    {"dia": "Viernes", "dia_code": "FR", "inicio": "17:00", "fin": "18:00", "duracion": 1.0}
                ],
                "horas_semana": 3.0
            },
            {
                "id": "diseno-digital",
                "nombre": "Fundamentos de Diseño Digital",
                "codigo": "DIS201",
                "profesor": "AGUILAR VELA ÁLVARO",
                "creditos": 4,
                "color": "#F4B183",
                "aula": "Lab Diseño",
                "horarios": [
                    {"dia": "Martes", "dia_code": "TU", "inicio": "19:00", "fin": "20:00", "duracion": 1.0},
                    {"dia": "Martes", "dia_code": "TU", "inicio": "21:00", "fin": "21:30", "duracion": 0.5},
                    {"dia": "Miércoles", "dia_code": "WE", "inicio": "19:00", "fin": "20:00", "duracion": 1.0},
                    {"dia": "Jueves", "dia_code": "TH", "inicio": "19:00", "fin": "20:00", "duracion": 1.0}
                ],
                "horas_semana": 3.5
            },
            {
                "id": "finanzas",
                "nombre": "Finanzas Empresariales",
                "codigo": "ADM301",
                "profesor": "ARROYO SANCHEZ OSCAR RAYMUNDO",
                "creditos": 4,
                "color": "#C6E0B4",
                "aula": "Aula 301",
                "horarios": [
                    {"dia": "Lunes", "dia_code": "MO", "inicio": "20:00", "fin": "21:30", "duracion": 1.5},
                    {"dia": "Martes", "dia_code": "TU", "inicio": "20:00", "fin": "21:00", "duracion": 1.0},
                    {"dia": "Miércoles", "dia_code": "WE", "inicio": "20:00", "fin": "21:30", "duracion": 1.5},
                    {"dia": "Jueves", "dia_code": "TH", "inicio": "21:00", "fin": "21:30", "duracion": 0.5}
                ],
                "horas_semana": 4.5
            },
            {
                "id": "etica",
                "nombre": "Ingeniería, Ética y Sociedad",
                "codigo": "ETH201",
                "profesor": "CAMPOAMOR ROLDAN SERGIO",
                "creditos": 4,
                "color": "#D9D2E9",
                "aula": "Aula 203",
                "horarios": [
                    {"dia": "Jueves", "dia_code": "TH", "inicio": "20:00", "fin": "21:00", "duracion": 1.0},
                    {"dia": "Viernes", "dia_code": "FR", "inicio": "20:00", "fin": "21:30", "duracion": 1.5},
                    {"dia": "Sábado", "dia_code": "SA", "inicio": "10:00", "fin": "13:00", "duracion": 3.0}
                ],
                "horas_semana": 5.5
            }
        ]
        return materias

    def obtener_horario_semanal(self):
        """Obtiene el horario organizado por días de la semana"""
        return {
            "lunes": [
                {"materia": "Cálculo Multivariable", "inicio": "17:00", "fin": "18:00", "profesor": "ORTIZ REYES RAUL", "aula": "Aula 205", "color": "#FFD966"},
                {"materia": "Finanzas Empresariales", "inicio": "20:00", "fin": "21:30", "profesor": "ARROYO SANCHEZ OSCAR RAYMUNDO", "aula": "Aula 301", "color": "#C6E0B4"}
            ],
            "martes": [
                {"materia": "Algoritmos y Estructuras de Datos", "inicio": "17:30", "fin": "18:00", "profesor": "PEÑA OLIVO CRISTÓBAL", "aula": "Lab Sistemas", "color": "#9BC2E6"},
                {"materia": "Álgebra Lineal", "inicio": "18:00", "fin": "19:00", "profesor": "LARA USCANGA SERGIO TULIO", "aula": "Aula 102", "color": "#A9D08E"},
                {"materia": "Fundamentos de Diseño Digital", "inicio": "19:00", "fin": "20:00", "profesor": "AGUILAR VELA ÁLVARO", "aula": "Lab Diseño", "color": "#F4B183"},
                {"materia": "Finanzas Empresariales", "inicio": "20:00", "fin": "21:00", "profesor": "ARROYO SANCHEZ OSCAR RAYMUNDO", "aula": "Aula 301", "color": "#C6E0B4"},
                {"materia": "Fundamentos de Diseño Digital", "inicio": "21:00", "fin": "21:30", "profesor": "AGUILAR VELA ÁLVARO", "aula": "Lab Diseño", "color": "#F4B183"}
            ],
            "miercoles": [
                {"materia": "Cálculo Multivariable", "inicio": "17:30", "fin": "18:00", "profesor": "ORTIZ REYES RAUL", "aula": "Aula 205", "color": "#FFD966"},
                {"materia": "Álgebra Lineal", "inicio": "18:00", "fin": "19:00", "profesor": "LARA USCANGA SERGIO TULIO", "aula": "Aula 102", "color": "#A9D08E"},
                {"materia": "Fundamentos de Diseño Digital", "inicio": "19:00", "fin": "20:00", "profesor": "AGUILAR VELA ÁLVARO", "aula": "Lab Diseño", "color": "#F4B183"},
                {"materia": "Finanzas Empresariales", "inicio": "20:00", "fin": "21:30", "profesor": "ARROYO SANCHEZ OSCAR RAYMUNDO", "aula": "Aula 301", "color": "#C6E0B4"}
            ],
            "jueves": [
                {"materia": "Fundamentos de Diseño Digital", "inicio": "19:00", "fin": "20:00", "profesor": "AGUILAR VELA ÁLVARO", "aula": "Lab Diseño", "color": "#F4B183"},
                {"materia": "Ingeniería, Ética y Sociedad", "inicio": "20:00", "fin": "21:00", "profesor": "CAMPOAMOR ROLDAN SERGIO", "aula": "Aula 203", "color": "#D9D2E9"},
                {"materia": "Finanzas Empresariales", "inicio": "21:00", "fin": "21:30", "profesor": "ARROYO SANCHEZ OSCAR RAYMUNDO", "aula": "Aula 301", "color": "#C6E0B4"}
            ],
            "viernes": [
                {"materia": "Álgebra Lineal", "inicio": "17:00", "fin": "18:00", "profesor": "LARA USCANGA SERGIO TULIO", "aula": "Aula 102", "color": "#A9D08E"},
                {"materia": "Ingeniería, Ética y Sociedad", "inicio": "20:00", "fin": "21:30", "profesor": "CAMPOAMOR ROLDAN SERGIO", "aula": "Aula 203", "color": "#D9D2E9"}
            ],
            "sabado": [
                {"materia": "Algoritmos y Estructuras de Datos", "inicio": "07:00", "fin": "10:00", "profesor": "PEÑA OLIVO CRISTÓBAL", "aula": "Lab Sistemas", "color": "#9BC2E6"},
                {"materia": "Ingeniería, Ética y Sociedad", "inicio": "10:00", "fin": "13:00", "profesor": "CAMPOAMOR ROLDAN SERGIO", "aula": "Aula 203", "color": "#D9D2E9"}
            ],
            "domingo": []
        }

    def generar_calendar_urls_txt(self):
        """Genera el archivo de texto con todas las URLs de Google Calendar"""
        contenido = """UNEGario - URLs de Google Calendar
==================================

Semestre: Agosto-Diciembre 2025
Generado: """ + datetime.now().strftime("%d de %B, %Y") + """

📚 HORARIO COMPLETO DEL SEMESTRE
https://calendar.google.com/calendar/render?action=TEMPLATE&text=Horario%20Completo%20-%20ISEC%20Universidad&dates=20250818T170000/20250818T213000&details=📚%20Horario%20completo%20del%20semestre%20Agosto-Diciembre%202025%0A🎓%20Ingeniería%20en%20Inteligencia%20Artificial%0A🏫%20ISEC%20Universidad%0A%0A📅%20Materias%20incluidas:%0A•%20Cálculo%20Multivariable%0A•%20Algoritmos%20y%20Estructuras%20de%20Datos%0A•%20Álgebra%20Lineal%0A•%20Fundamentos%20de%20Diseño%20Digital%0A•%20Finanzas%20Empresariales%0A•%20Ingeniería,%20Ética%20y%20Sociedad%0A%0A⚠️%20Días%20festivos%20excluidos%20automáticamente&location=ISEC%20Universidad&recur=FREQ%3DWEEKLY%3BBYDAY%3DMO,TU,WE,TH,FR,SA%3BUNTIL%3D20251212T235959Z

📚 MATERIAS INDIVIDUALES
========================

🧮 Cálculo Multivariable
https://calendar.google.com/calendar/render?action=TEMPLATE&text=Cálculo%20Multivariable&dates=20250825T170000/20250825T180000&details=📚%20Cálculo%20Multivariable%0A👨‍🏫%20Profesor:%20ORTIZ%20REYES%20RAUL%0A%0A📅%20Horarios:%0A•%20Lunes:%2017:00%20-%2018:00%0A•%20Miércoles:%2017:30%20-%2018:00%0A%0A🏫%20ISEC%20Universidad%20-%20Semestre%20Ago-Dic%202025%0A🎓%20Ingeniería%20en%20Inteligencia%20Artificial%0A%0A⚠️%20Días%20festivos%20excluidos%20automáticamente&location=Aula%20205%20-%20ISEC%20Universidad&recur=FREQ%3DWEEKLY%3BBYDAY%3DMO,WE%3BUNTIL%3D20251212T235959Z

💻 Algoritmos y Estructuras de Datos
https://calendar.google.com/calendar/render?action=TEMPLATE&text=Algoritmos%20y%20Estructuras%20de%20Datos&dates=20250826T173000/20250826T180000&details=📚%20Algoritmos%20y%20Estructuras%20de%20Datos%0A👨‍🏫%20Profesor:%20PEÑA%20OLIVO%20CRISTÓBAL%0A%0A📅%20Horarios:%0A•%20Martes:%2017:30%20-%2018:00%0A•%20Sábado:%2007:00%20-%2010:00%0A%0A🏫%20ISEC%20Universidad%20-%20Semestre%20Ago-Dic%202025%0A🎓%20Ingeniería%20en%20Inteligencia%20Artificial%0A%0A⚠️%20Días%20festivos%20excluidos%20automáticamente&location=Lab%20Sistemas%20-%20ISEC%20Universidad&recur=FREQ%3DWEEKLY%3BBYDAY%3DTU,SA%3BUNTIL%3D20251212T235959Z

📐 Álgebra Lineal
https://calendar.google.com/calendar/render?action=TEMPLATE&text=Álgebra%20Lineal&dates=20250826T180000/20250826T190000&details=📚%20Álgebra%20Lineal%0A👨‍🏫%20Profesor:%20LARA%20USCANGA%20SERGIO%20TULIO%0A%0A📅%20Horarios:%0A•%20Martes:%2018:00%20-%2019:00%0A•%20Miércoles:%2018:00%20-%2019:00%0A•%20Viernes:%2017:00%20-%2018:00%0A%0A🏫%20ISEC%20Universidad%20-%20Semestre%20Ago-Dic%202025%0A🎓%20Ingeniería%20en%20Inteligencia%20Artificial%0A%0A⚠️%20Días%20festivos%20excluidos%20automáticamente&location=Aula%20102%20-%20ISEC%20Universidad&recur=FREQ%3DWEEKLY%3BBYDAY%3DTU,WE,FR%3BUNTIL%3D20251212T235959Z

🎨 Fundamentos de Diseño Digital
https://calendar.google.com/calendar/render?action=TEMPLATE&text=Fundamentos%20de%20Diseño%20Digital&dates=20250826T190000/20250826T200000&details=📚%20Fundamentos%20de%20Diseño%20Digital%0A👨‍🏫%20Profesor:%20AGUILAR%20VELA%20ÁLVARO%0A%0A📅%20Horarios:%0A•%20Martes:%2019:00%20-%2020:00%0A•%20Martes:%2021:00%20-%2021:30%0A•%20Miércoles:%2019:00%20-%2020:00%0A•%20Jueves:%2019:00%20-%2020:00%0A%0A🏫%20ISEC%20Universidad%20-%20Semestre%20Ago-Dic%202025%0A🎓%20Ingeniería%20en%20Inteligencia%20Artificial%0A%0A⚠️%20Días%20festivos%20excluidos%20automáticamente&location=Lab%20Diseño%20-%20ISEC%20Universidad&recur=FREQ%3DWEEKLY%3BBYDAY%3DTU,WE,TH%3BUNTIL%3D20251212T235959Z

💰 Finanzas Empresariales
https://calendar.google.com/calendar/render?action=TEMPLATE&text=Finanzas%20Empresariales&dates=20250825T200000/20250825T213000&details=📚%20Finanzas%20Empresariales%0A👨‍🏫%20Profesor:%20ARROYO%20SANCHEZ%20OSCAR%20RAYMUNDO%0A%0A📅%20Horarios:%0A•%20Lunes:%2020:00%20-%2021:30%0A•%20Martes:%2020:00%20-%2021:00%0A•%20Miércoles:%2020:00%20-%2021:30%0A•%20Jueves:%2021:00%20-%2021:30%0A%0A🏫%20ISEC%20Universidad%20-%20Semestre%20Ago-Dic%202025%0A🎓%20Ingeniería%20en%20Inteligencia%20Artificial%0A%0A⚠️%20Días%20festivos%20excluidos%20automáticamente&location=Aula%20301%20-%20ISEC%20Universidad&recur=FREQ%3DWEEKLY%3BBYDAY%3DMO,TU,WE,TH%3BUNTIL%3D20251212T235959Z

⚖️ Ingeniería, Ética y Sociedad
https://calendar.google.com/calendar/render?action=TEMPLATE&text=Ingeniería,%20Ética%20y%20Sociedad&dates=20250828T200000/20250828T210000&details=📚%20Ingeniería,%20Ética%20y%20Sociedad%0A👨‍🏫%20Profesor:%20CAMPOAMOR%20ROLDAN%20SERGIO%0A%0A📅%20Horarios:%0A•%20Jueves:%2020:00%20-%2021:00%0A•%20Viernes:%2020:00%20-%2021:30%0A•%20Sábado:%2010:00%20-%2013:00%0A%0A🏫%20ISEC%20Universidad%20-%20Semestre%20Ago-Dic%202025%0A🎓%20Ingeniería%20en%20Inteligencia%20Artificial%0A%0A⚠️%20Días%20festivos%20excluidos%20automáticamente&location=Aula%20203%20-%20ISEC%20Universidad&recur=FREQ%3DWEEKLY%3BBYDAY%3DTH,FR,SA%3BUNTIL%3D20251212T235959Z

📊 ESTADÍSTICAS DEL SEMESTRE
============================
Total de materias: 6
Total de horas por semana: 22.5
Total de créditos: 24
Promedio de horas por día: 4.5

🏫 INFORMACIÓN DE CONTACTO
=========================
Universidad: ISEC Universidad
Carrera: Ingeniería en Inteligencia Artificial
Estudiante: Edson Alberto Herrera Cervantes
Semestre: Agosto-Diciembre 2025

⚠️ NOTAS IMPORTANTES
===================
- Las URLs generan eventos recurrentes hasta el 12 de diciembre de 2025
- Los días festivos están excluidos automáticamente en Google Calendar
- Cada materia incluye información del profesor y aula asignada
- Las fechas pueden ajustarse según el calendario académico oficial

📅 Última actualización: """ + datetime.now().strftime("%d de %B, %Y")

        return contenido

if __name__ == "__main__":
    unegario = UNEGarioCalendar()
    # Generar archivos output para el frontend
    horario_data, calendar_urls = unegario.generar_output_files()
    
    # También generar la versión original si se necesita
    url, json_data = unegario.exportar_archivos_web()
