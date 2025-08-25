// Datos de materias individuales para Google Calendar
const MATERIAS_INDIVIDUALES = {
    "calculo": {
        nombre: "Cálculo Multivariable",
        profesor: "ORTIZ REYES RAUL",
        horarios: [
            { dia: "MO", inicio: "17:00", fin: "18:00" },
            { dia: "WE", inicio: "17:30", fin: "18:00" }
        ],
        color: "#FFD966"
    },
    "algoritmos": {
        nombre: "Algoritmos y Estructuras de Datos", 
        profesor: "PEÑA OLIVO CRISTÓBAL",
        horarios: [
            { dia: "TU", inicio: "17:30", fin: "18:00" },
            { dia: "SA", inicio: "07:00", fin: "10:00" }
        ],
        color: "#9BC2E6"
    },
    "algebra": {
        nombre: "Álgebra Lineal",
        profesor: "LARA USCANGA SERGIO TULIO", 
        horarios: [
            { dia: "TU", inicio: "18:00", fin: "19:00" },
            { dia: "WE", inicio: "18:00", fin: "19:00" },
            { dia: "FR", inicio: "17:00", fin: "18:00" }
        ],
        color: "#A9D08E"
    },
    "diseno-digital": {
        nombre: "Fundamentos de Diseño Digital",
        profesor: "AGUILAR VELA ÁLVARO",
        horarios: [
            { dia: "TU", inicio: "19:00", fin: "20:00" },
            { dia: "TU", inicio: "21:00", fin: "21:30" },
            { dia: "WE", inicio: "19:00", fin: "20:00" },
            { dia: "TH", inicio: "19:00", fin: "20:00" }
        ],
        color: "#F4B183"
    },
    "finanzas": {
        nombre: "Finanzas Empresariales", 
        profesor: "ARROYO SANCHEZ OSCAR RAYMUNDO",
        horarios: [
            { dia: "MO", inicio: "20:00", fin: "21:30" },
            { dia: "TU", inicio: "20:00", fin: "21:00" },
            { dia: "WE", inicio: "20:00", fin: "21:30" },
            { dia: "TH", inicio: "21:00", fin: "21:30" }
        ],
        color: "#C6E0B4"
    },
    "etica": {
        nombre: "Ingeniería, Ética y Sociedad",
        profesor: "CAMPOAMOR ROLDAN SERGIO",
        horarios: [
            { dia: "TH", inicio: "20:00", fin: "21:00" },
            { dia: "FR", inicio: "20:00", fin: "21:30" },
            { dia: "SA", inicio: "10:00", fin: "13:00" }
        ],
        color: "#D9D2E9"
    }
};

// Función para generar URL de Google Calendar para una materia específica
function generateSubjectCalendarURL(subjectKey) {
    const materia = MATERIAS_INDIVIDUALES[subjectKey];
    if (!materia) return null;

    const fechaInicio = "20250825"; // 25 agosto 2025 (inicio del semestre - OFICIAL ISEC)
    const fechaFin = "20251231"; // 31 diciembre 2025 (fin del semestre - OFICIAL ISEC)
    
    // Generar RRULE para horarios recurrentes
    let rrules = [];
    materia.horarios.forEach(horario => {
        const rrule = `FREQ=WEEKLY;BYDAY=${horario.dia};UNTIL=20251231T235959Z`;
        rrules.push(rrule);
    });

    // Crear descripción detallada
    const description = encodeURIComponent(`📚 ${materia.nombre}
👨‍🏫 Profesor: ${materia.profesor}

📅 Horarios:
${materia.horarios.map(h => `• ${getDayName(h.dia)}: ${h.inicio} - ${h.fin}`).join('\n')}

🏫 ISEC Universidad - Semestre Ago-Dic 2025
🎓 Ingeniería en Inteligencia Artificial

⚠️ Días festivos excluidos automáticamente`);

    // Usar el primer horario como base para el evento
    const primerHorario = materia.horarios[0];
    const horaInicio = primerHorario.inicio.replace(':', '') + '00';
    const horaFin = primerHorario.fin.replace(':', '') + '00';

    const calendarURL = `https://calendar.google.com/calendar/render?action=TEMPLATE` +
        `&text=${encodeURIComponent(materia.nombre)}` +
        `&dates=${fechaInicio}T${horaInicio}/${fechaInicio}T${horaFin}` +
        `&details=${description}` +
        `&recur=${encodeURIComponent(rrules[0])}` +
        `&location=${encodeURIComponent('ISEC Universidad')}` +
        `&ctz=America/Mexico_City`;

    return calendarURL;
}

// Función auxiliar para convertir códigos de día a nombres
function getDayName(dayCode) {
    const days = {
        'MO': 'Lunes',
        'TU': 'Martes', 
        'WE': 'Miércoles',
        'TH': 'Jueves',
        'FR': 'Viernes',
        'SA': 'Sábado',
        'SU': 'Domingo'
    };
    return days[dayCode] || dayCode;
}

// Función para configurar los botones de materias individuales
function setupSubjectButtons() {
    const subjectButtons = document.querySelectorAll('.add-subject-btn');
    
    subjectButtons.forEach(button => {
        const subjectKey = button.getAttribute('data-subject');
        
        button.addEventListener('click', function() {
            const calendarURL = generateSubjectCalendarURL(subjectKey);
            
            if (calendarURL) {
                // Cambiar el estado del botón
                button.classList.add('added');
                button.innerHTML = `
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                    </svg>
                    Añadido
                `;
                
                // Abrir Google Calendar
                window.open(calendarURL, '_blank');
                
                // Mostrar notificación
                const materia = MATERIAS_INDIVIDUALES[subjectKey];
                showNotification(`✅ ${materia.nombre} añadida a Google Calendar`, 'success');
                
                // Registrar en consola
                console.log(`✅ Materia añadida: ${materia.nombre}`);
                
                // Resetear el botón después de 3 segundos
                setTimeout(() => {
                    button.classList.remove('added');
                    button.innerHTML = `
                        <svg viewBox="0 0 24 24" fill="currentColor">
                            <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>
                        </svg>
                        Añadir
                    `;
                }, 3000);
            } else {
                showNotification('❌ Error al generar enlace de calendario', 'error');
            }
        });
    });
}

// Datos del horario EXACTO según tu imagen real
const horarioData = [
    // Lunes
    { dia: "Lunes", hora_inicio: "17:00", hora_fin: "18:00", materia: "Cálculo multivariable", profesor: "ORTIZ REYES RAUL", tipo: "Clase" },
    { dia: "Lunes", hora_inicio: "20:00", hora_fin: "21:30", materia: "Finanzas empresariales", profesor: "ARROYO SANCHEZ OSCAR RAYMUNDO", tipo: "Clase" },
    
    // Martes
    { dia: "Martes", hora_inicio: "17:30", hora_fin: "18:00", materia: "Algoritmos y estructuras de datos", profesor: "PEÑA OLIVO CRISTÓBAL", tipo: "Clase" },
    { dia: "Martes", hora_inicio: "18:00", hora_fin: "19:00", materia: "Álgebra lineal", profesor: "LARA USCANGA SERGIO TULIO", tipo: "Clase" },
    { dia: "Martes", hora_inicio: "19:00", hora_fin: "20:00", materia: "Fundamentos de diseño digital", profesor: "AGUILAR VELA ÁLVARO", tipo: "Clase" },
    { dia: "Martes", hora_inicio: "20:00", hora_fin: "21:00", materia: "Finanzas empresariales", profesor: "ARROYO SANCHEZ OSCAR RAYMUNDO", tipo: "Clase" },
    { dia: "Martes", hora_inicio: "21:00", hora_fin: "21:30", materia: "Fundamentos de diseño digital", profesor: "AGUILAR VELA ÁLVARO", tipo: "Clase" },
    
    // Miércoles
    { dia: "Miércoles", hora_inicio: "17:30", hora_fin: "18:00", materia: "Cálculo multivariable", profesor: "ORTIZ REYES RAUL", tipo: "Clase" },
    { dia: "Miércoles", hora_inicio: "18:00", hora_fin: "19:00", materia: "Álgebra lineal", profesor: "LARA USCANGA SERGIO TULIO", tipo: "Clase" },
    { dia: "Miércoles", hora_inicio: "19:00", hora_fin: "20:00", materia: "Fundamentos de diseño digital", profesor: "AGUILAR VELA ÁLVARO", tipo: "Clase" },
    { dia: "Miércoles", hora_inicio: "20:00", hora_fin: "21:00", materia: "Finanzas empresariales", profesor: "ARROYO SANCHEZ OSCAR RAYMUNDO", tipo: "Clase" },
    { dia: "Miércoles", hora_inicio: "21:00", hora_fin: "21:30", materia: "Finanzas empresariales", profesor: "ARROYO SANCHEZ OSCAR RAYMUNDO", tipo: "Clase" },
    
    // Jueves
    { dia: "Jueves", hora_inicio: "19:00", hora_fin: "20:00", materia: "Fundamentos de diseño digital", profesor: "AGUILAR VELA ÁLVARO", tipo: "Clase" },
    { dia: "Jueves", hora_inicio: "20:00", hora_fin: "21:00", materia: "Ingeniería, ética y sociedad", profesor: "CAMPOAMOR ROLDAN SERGIO", tipo: "Clase" },
    { dia: "Jueves", hora_inicio: "21:00", hora_fin: "21:30", materia: "Finanzas empresariales", profesor: "ARROYO SANCHEZ OSCAR RAYMUNDO", tipo: "Clase" },
    
    // Viernes
    { dia: "Viernes", hora_inicio: "17:00", hora_fin: "18:00", materia: "Álgebra lineal", profesor: "LARA USCANGA SERGIO TULIO", tipo: "Clase" },
    { dia: "Viernes", hora_inicio: "20:00", hora_fin: "21:00", materia: "Ingeniería, ética y sociedad", profesor: "CAMPOAMOR ROLDAN SERGIO", tipo: "Clase" },
    { dia: "Viernes", hora_inicio: "21:00", hora_fin: "21:30", materia: "Ingeniería, ética y sociedad", profesor: "CAMPOAMOR ROLDAN SERGIO", tipo: "Clase" },
    
    // Sábado
    { dia: "Sábado", hora_inicio: "07:00", hora_fin: "09:00", materia: "Algoritmos y estructuras de datos", profesor: "PEÑA OLIVO CRISTÓBAL", tipo: "Clase" },
    { dia: "Sábado", hora_inicio: "09:00", hora_fin: "10:00", materia: "Algoritmos y estructuras de datos", profesor: "PEÑA OLIVO CRISTÓBAL", tipo: "Clase" },
    { dia: "Sábado", hora_inicio: "10:00", hora_fin: "11:00", materia: "Ingeniería, ética y sociedad", profesor: "CAMPOAMOR ROLDAN SERGIO", tipo: "Clase" },
    { dia: "Sábado", hora_inicio: "11:00", hora_fin: "12:00", materia: "Ingeniería, ética y sociedad", profesor: "CAMPOAMOR ROLDAN SERGIO", tipo: "Clase" },
    { dia: "Sábado", hora_inicio: "12:00", hora_fin: "13:00", materia: "Ingeniería, ética y sociedad", profesor: "CAMPOAMOR ROLDAN SERGIO", tipo: "Clase" }
];

// Mapeo de materias a clases CSS (actualizado según tu horario real)
const materiaClases = {
    "Cálculo multivariable": "calculo",
    "Finanzas empresariales": "finanzas",
    "Algoritmos y estructuras de datos": "algoritmos",
    "Fundamentos de diseño digital": "diseno-digital",
    "Álgebra lineal": "algebra",
    "Ingeniería, ética y sociedad": "etica",
    "Receso": "break-block"
};

// Iconos para cada día
const diaIconos = {
    "Lunes": "📅",
    "Martes": "📆",
    "Miércoles": "📅",
    "Jueves": "📆",
    "Viernes": "📅",
    "Sábado": "📆"
};

// URL de Google Calendar (cargada dinámicamente desde archivo generado)
let GOOGLE_CALENDAR_URL = "https://calendar.google.com/calendar/render?action=TEMPLATE&text=Horario%20UNEGario%20-%20Semestre%20Ago-Dic%202025&dates=20250825T170000/20250825T220000&details=%F0%9F%93%9A%20HORARIO%20SEMESTRE%20AGO-DIC%202025%250A%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%250A%250A%F0%9F%93%85%20LUNES%250A%20%20%E2%80%A2%2017%3A00-18%3A00%20%7C%20C%C3%A1lculo%20multivariable%250A%20%20%20%20Profesor%3A%20ORTIZ%20REYES%20RAUL%250A%20%20%E2%80%A2%2020%3A00-21%3A30%20%7C%20Finanzas%20empresariales%250A%20%20%20%20Profesor%3A%20ARROYO%20SANCHEZ%20OSCAR%20RAYMUNDO%250A%250A%F0%9F%93%85%20MARTES%250A%20%20%E2%80%A2%2017%3A30-18%3A00%20%7C%20Algoritmos%20y%20estructuras%20de%20datos%250A%20%20%20%20Profesor%3A%20PE%C3%91A%20OLIVO%20CRIST%C3%93BAL%250A%20%20%E2%80%A2%2018%3A00-19%3A00%20%7C%20%C3%81lgebra%20lineal%250A%20%20%20%20Profesor%3A%20LARA%20USCANGA%20SERGIO%20TULIO%250A%20%20%E2%80%A2%2019%3A00-20%3A00%20%7C%20Fundamentos%20de%20dise%C3%B1o%20digital%250A%20%20%20%20Profesor%3A%20AGUILAR%20VELA%20%C3%81LVARO%250A%20%20%E2%80%A2%2020%3A00-21%3A00%20%7C%20Finanzas%20empresariales%250A%20%20%20%20Profesor%3A%20ARROYO%20SANCHEZ%20OSCAR%20RAYMUNDO%250A%20%20%E2%80%A2%2021%3A00-21%3A30%20%7C%20Fundamentos%20de%20dise%C3%B1o%20digital%250A%20%20%20%20Profesor%3A%20AGUILAR%20VELA%20%C3%81LVARO%250A%250A%F0%9F%93%85%20MI%C3%89RCOLES%250A%20%20%E2%80%A2%2017%3A30-18%3A00%20%7C%20C%C3%A1lculo%20multivariable%250A%20%20%20%20Profesor%3A%20ORTIZ%20REYES%20RAUL%250A%20%20%E2%80%A2%2018%3A00-19%3A00%20%7C%20%C3%81lgebra%20lineal%250A%20%20%20%20Profesor%3A%20LARA%20USCANGA%20SERGIO%20TULIO%250A%20%20%E2%80%A2%2019%3A00-20%3A00%20%7C%20Fundamentos%20de%20dise%C3%B1o%20digital%250A%20%20%20%20Profesor%3A%20AGUILAR%20VELA%20%C3%81LVARO%250A%20%20%E2%80%A2%2020%3A00-21%3A00%20%7C%20Finanzas%20empresariales%250A%20%20%20%20Profesor%3A%20ARROYO%20SANCHEZ%20OSCAR%20RAYMUNDO%250A%20%20%E2%80%A2%2021%3A00-21%3A30%20%7C%20Finanzas%20empresariales%250A%20%20%20%20Profesor%3A%20ARROYO%20SANCHEZ%20OSCAR%20RAYMUNDO%250A%250A%F0%9F%93%�%20JUEVES%250A%20%20%E2%80%A2%2019%3A00-20%3A00%20%7C%20Fundamentos%20de%20dise%C3%B1o%20digital%250A%20%20%20%20Profesor%3A%20AGUILAR%20VELA%20%C3%81LVARO%250A%20%20%E2%80%A2%2020%3A00-21%3A00%20%7C%20Ingenier%C3%ADa%2C%20%C3%A9tica%20y%20sociedad%250A%20%20%20%20Profesor%3A%20CAMPOAMOR%20ROLDAN%20SERGIO%250A%20%20%E2%80%A2%2021%3A00-21%3A30%20%7C%20Finanzas%20empresariales%250A%20%20%20%20Profesor%3A%20ARROYO%20SANCHEZ%20OSCAR%20RAYMUNDO%250A%250A%F0%9F%93%85%20VIERNES%250A%20%20%E2%80%A2%2017%3A00-18%3A00%20%7C%20%C3%81lgebra%20lineal%250A%20%20%20%20Profesor%3A%20LARA%20USCANGA%20SERGIO%20TULIO%250A%20%20%E2%80%A2%2020%3A00-21%3A00%20%7C%20Ingenier%C3%ADa%2C%20%C3%A9tica%20y%20sociedad%250A%20%20%20%20Profesor%3A%20CAMPOAMOR%20ROLDAN%20SERGIO%250A%20%20%E2%80%A2%2021%3A00-21%3A30%20%7C%20Ingenier%C3%ADa%2C%20%C3%A9tica%20y%20sociedad%250A%20%20%20%20Profesor%3A%20CAMPOAMOR%20ROLDAN%20SERGIO%250A%250A%F0%9F%93%85%20S%C3%81BADO%250A%20%20%E2%80%A2%2007%3A00-09%3A00%20%7C%20Algoritmos%20y%20estructuras%20de%20datos%250A%20%20%20%20Profesor%3A%20PE%C3%91A%20OLIVO%20CRIST%C3%93BAL%250A%20%20%E2%80%A2%2009%3A00-10%3A00%20%7C%20Algoritmos%20y%20estructuras%20de%20datos%250A%20%20%20%20Profesor%3A%20PE%C3%91A%20OLIVO%20CRIST%C3%93BAL%250A%20%20%E2%80%A2%2010%3A00-11%3A00%20%7C%20Ingenier%C3%ADa%2C%20%C3%A9tica%20y%20sociedad%250A%20%20%20%20Profesor%3A%20CAMPOAMOR%20ROLDAN%20SERGIO%250A%20%20%E2%80%A2%2011%3A00-12%3A00%20%7C%20Ingenier%C3%ADa%2C%20%C3%A9tica%20y%20sociedad%250A%20%20%20%20Profesor%3A%20CAMPOAMOR%20ROLDAN%20SERGIO%250A%20%20%E2%80%A2%2012%3A00-13%3A00%20%7C%20Ingenier%C3%ADa%2C%20%C3%A9tica%20y%20sociedad%250A%20%20%20%20Profesor%3A%20CAMPOAMOR%20ROLDAN%20SERGIO%250A%250A%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%E2%94%81%250A%F0%9F%94%97%20M%C3%A1s%20informaci%C3%B3n%3A%20https%3A%2F%2Fedbetosolutions.tech%2FUNEGarios%250A%250A%E2%9A%A0%EF%B8%8F%20D%C3%8DAS%20SIN%20CLASES%3A%250A%E2%80%A2%2016%20sep%20-%20D%C3%ADa%20de%20la%20Independencia%250A%E2%80%A2%202%20nov%20-%20D%C3%ADa%20de%20Muertos%250A%E2%80%A2%2017%20nov%20-%20Revoluci%C3%B3n%20Mexicana%250A%E2%80%A2%208%20dic%20-%20Inmaculada%20Concepci%C3%B3n%250A%E2%80%A2%2022%20dic%20-%206%20ene%20-%20Vacaciones%20de%20Invierno&location=Universidad%20ISEC%20-%20Campus%20Principal&ctz=America%2FMexico_City&recur=RRULE%3AFREQ%3DWEEKLY%3BBYDAY%3DMO%2CTU%2CWE%2CTH%2CFR%2CSA%3BUNTIL%3D20251231T235959Z%250AEXDATE%3BVALUE%3DDATE%3A20250825T000000Z%252C20250831T000000Z%252C20250916T000000Z%252C20250929T000000Z%252C20250930T000000Z%252C20251010T000000Z%252C20251102T000000Z%252C20251117T000000Z%252C20251208T000000Z%252C20251222T000000Z%252C20251223T000000Z%252C20251224T000000Z%252C20251225T000000Z%252C20251226T000000Z%252C20251229T000000Z%252C20251230T000000Z%252C20251231T000000Z%252C20260101T000000Z%252C20260102T000000Z%252C20260105T000000Z%252C20260106T000000Z%252C20260112T000000Z%252C20260119T000000Z%252C20260126T000000Z%252C20260203T000000Z%252C20260216T000000Z";

// Función para cargar datos dinámicamente desde JSON
async function loadHorarioData() {
    try {
        // Intenta cargar desde el archivo generado por Python
        const response = await fetch('./horario_data.json');
        if (response.ok) {
            const data = await response.json();
            console.log('📊 Datos cargados desde JSON generado');
            return data;
        }
    } catch (error) {
        console.warn('⚠️ No se pudo cargar JSON dinámico, usando datos estáticos');
    }
    
    // Fallback a datos estáticos si no se puede cargar el JSON
    return horarioData;
}

// Función para cargar URL de Google Calendar dinámicamente
async function loadCalendarURL() {
    try {
        const response = await fetch('./google_calendar_url.txt');
        if (response.ok) {
            const url = await response.text();
            GOOGLE_CALENDAR_URL = url.trim();
            console.log('🔗 URL de calendario cargada dinámicamente');
            return url.trim();
        }
    } catch (error) {
        console.warn('⚠️ No se pudo cargar URL dinámica, usando URL estática');
    }
    
    return GOOGLE_CALENDAR_URL;
}

// Función para renderizar el horario
function renderSchedule(horarioDataToRender = horarioData) {
    const scheduleContent = document.getElementById('scheduleContent');
    let currentDay = '';
    let daySection = null;
    let dayClasses = null;

    horarioDataToRender.forEach(clase => {
        if (clase.dia !== currentDay) {
            // Crear nueva sección de día
            currentDay = clase.dia;
            
            daySection = document.createElement('div');
            daySection.className = 'day-section';
            
            const dayHeader = document.createElement('div');
            dayHeader.className = 'day-header';
            dayHeader.innerHTML = `${diaIconos[currentDay] || '📅'} ${currentDay}`;
            
            daySection.appendChild(dayHeader);
            
            dayClasses = document.createElement('div');
            dayClasses.className = 'day-classes';
            daySection.appendChild(dayClasses);
            
            scheduleContent.appendChild(daySection);
        }

        // Crear bloque de clase
        const classBlock = document.createElement('div');
        classBlock.className = `class-block ${materiaClases[clase.materia] || ''}`;
        
        const timeSlot = document.createElement('div');
        timeSlot.className = 'time-slot';
        timeSlot.textContent = `${clase.hora_inicio} - ${clase.hora_fin}`;
        
        const classInfo = document.createElement('div');
        classInfo.className = 'class-info';
        
        const className = document.createElement('div');
        className.className = 'class-name';
        className.textContent = clase.tipo === 'Receso' ? '☕ Receso' : clase.materia;
        
        classInfo.appendChild(className);
        
        if (clase.profesor) {
            const professor = document.createElement('div');
            professor.className = 'professor';
            professor.textContent = `👨‍🏫 ${clase.profesor}`;
            classInfo.appendChild(professor);
        }
        
        classBlock.appendChild(timeSlot);
        classBlock.appendChild(classInfo);
        
        dayClasses.appendChild(classBlock);
    });
}

// Función para configurar el botón de Google Calendar
function setupCalendarButton() {
    const addToCalendarBtn = document.getElementById('addToCalendarBtn');
    if (addToCalendarBtn) {
        addToCalendarBtn.href = GOOGLE_CALENDAR_URL;
        
        // Añadir evento de click para tracking (opcional)
        addToCalendarBtn.addEventListener('click', function() {
            console.log('✅ Usuario hizo clic en "Añadir a Google Calendar"');
            
            // Opcional: Mostrar mensaje de confirmación
            setTimeout(() => {
                showNotification('🔗 Abriendo Google Calendar...', 'info');
            }, 100);
        });
    }
}

// Función para mostrar notificaciones (opcional)
function showNotification(message, type = 'info') {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'info' ? '#007bff' : '#28a745'};
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: 500;
        z-index: 1000;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        animation: slideInRight 0.3s ease;
    `;
    notification.textContent = message;
    
    // Añadir al DOM
    document.body.appendChild(notification);
    
    // Remover después de 3 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Función para calcular estadísticas del horario
function calculateStats(horarioDataToCalc = horarioData) {
    let totalHoras = 0;
    let horasClase = 0;
    let horasReceso = 0;
    const materias = new Set();
    const profesores = new Set();
    
    horarioDataToCalc.forEach(clase => {
        const [horaIni, minIni] = clase.hora_inicio.split(':').map(Number);
        const [horaFin, minFin] = clase.hora_fin.split(':').map(Number);
        
        const duracion = (horaFin * 60 + minFin) - (horaIni * 60 + minIni);
        totalHoras += duracion;
        
        if (clase.tipo === 'Clase') {
            horasClase += duracion;
            materias.add(clase.materia);
            if (clase.profesor) {
                profesores.add(clase.profesor);
            }
        } else {
            horasReceso += duracion;
        }
    });
    
    return {
        totalHoras: Math.round(totalHoras / 60 * 100) / 100,
        horasClase: Math.round(horasClase / 60 * 100) / 100,
        horasReceso: Math.round(horasReceso / 60 * 100) / 100,
        cantidadMaterias: materias.size,
        cantidadProfesores: profesores.size
    };
}

// Función para añadir estadísticas (opcional)
function addStatsSection(horarioDataForStats = horarioData) {
    const stats = calculateStats(horarioDataForStats);
    const scheduleContainer = document.querySelector('.schedule-container');
    
    const statsHTML = `
        <div class="stats-section" style="margin-top: 30px; padding: 20px; background: #e3f2fd; border-radius: 12px; border-left: 4px solid #2196f3;">
            <div style="font-weight: 600; color: #1565c0; margin-bottom: 15px; display: flex; align-items: center; gap: 8px;">
                📊 Estadísticas del Semestre
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; color: #1565c0;">
                <div><strong>${stats.horasClase}h</strong><br><small>Horas de clase</small></div>
                <div><strong>${stats.horasReceso}h</strong><br><small>Horas de receso</small></div>
                <div><strong>${stats.cantidadMaterias}</strong><br><small>Materias</small></div>
                <div><strong>${stats.cantidadProfesores}</strong><br><small>Profesores</small></div>
            </div>
        </div>
    `;
    
    // Insertar antes de la leyenda
    const legend = scheduleContainer.querySelector('.legend');
    legend.insertAdjacentHTML('beforebegin', statsHTML);
}

// Función para manejar errores
function handleError(error) {
    console.error('❌ Error en UNEGario:', error);
    showNotification('⚠️ Ocurrió un error al cargar el horario', 'error');
}

// Función para verificar compatibilidad del navegador
function checkBrowserCompatibility() {
    const requiredFeatures = [
        'querySelector',
        'addEventListener',
        'createElement'
    ];
    
    const supported = requiredFeatures.every(feature => 
        typeof document[feature] === 'function'
    );
    
    if (!supported) {
        console.warn('⚠️ Navegador no totalmente compatible');
        return false;
    }
    
    return true;
}

// Función principal de inicialización
async function initUNEGario() {
    try {
        console.log('🚀 Iniciando UNEGario...');
        
        // Verificar compatibilidad
        if (!checkBrowserCompatibility()) {
            throw new Error('Navegador no compatible');
        }
        
        // Cargar datos dinámicamente
        const horarioDataLoaded = await loadHorarioData();
        const calendarURL = await loadCalendarURL();
        
        // Renderizar horario con datos cargados
        renderSchedule(horarioDataLoaded);
        
        // Configurar botón de calendario
        setupCalendarButton();
        
        // Configurar botones de materias individuales
        setupSubjectButtons();
        
        // Añadir estadísticas usando los datos cargados
        addStatsSection(horarioDataLoaded);
        
        console.log('✅ UNEGario iniciado correctamente');
        
        // Mostrar mensaje de bienvenida
        setTimeout(() => {
            showNotification('🎓 ¡Bienvenido a UNEGario! Tu horario está listo.', 'success');
        }, 1000);
        
    } catch (error) {
        handleError(error);
    }
}

// Función para actualizar URL del calendario (para usar con el script Python)
function updateCalendarURL(newURL) {
    if (newURL && typeof newURL === 'string') {
        GOOGLE_CALENDAR_URL = newURL;
        setupCalendarButton();
        console.log('🔄 URL de Google Calendar actualizada');
    }
}

// Función para exportar datos (para debugging)
function exportScheduleData() {
    const data = {
        horario: horarioData,
        estadisticas: calculateStats(),
        fechas: {
            inicio: '2025-08-18',
            fin: '2025-12-12'
        },
        version: '1.0.0'
    };
    
    console.log('📋 Datos del horario:', data);
    return data;
}

// Estilos CSS adicionales para animaciones
const additionalStyles = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;

// Añadir estilos adicionales al documento
function addAdditionalStyles() {
    const styleSheet = document.createElement('style');
    styleSheet.textContent = additionalStyles;
    document.head.appendChild(styleSheet);
}

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        addAdditionalStyles();
        initUNEGario();
    });
} else {
    addAdditionalStyles();
    initUNEGario();
}

// Exponer funciones globales para uso externo
window.UNEGario = {
    init: initUNEGario,
    updateURL: updateCalendarURL,
    exportData: exportScheduleData,
    showNotification: showNotification
};
