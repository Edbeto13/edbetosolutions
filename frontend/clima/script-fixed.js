/**
 * Script principal para Clima CDMX
 * Sistema de monitoreo meteorológico para la Ciudad de México
 * 
 * @version 2.0.0
 * @author EdbETO Solutions Team
 * @repo https://github.com/Edbeto13/Hydredelback
 */

// Configuración global
const CONFIG = {
    API_BASE_URL: '/api',
    UPDATE_INTERVAL: 75 * 60 * 1000, // 75 minutos en milisegundos
    DEFAULT_ALCALDIA: 'cdmx',
    CHART_COLORS: {
        temperatura: 'rgba(255, 99, 132, 1)',
        precipitacion: 'rgba(54, 162, 235, 1)',
        humedad: 'rgba(153, 102, 255, 1)',
        viento: 'rgba(75, 192, 192, 1)'
    }
};

// Selectores DOM principales
const DOM = {
    status: document.getElementById('status'),
    timestamp: document.getElementById('timestamp'),
    alcaldiaSelect: document.getElementById('alcaldia-select'),
    temperatura: document.getElementById('temperatura'),
    humedad: document.getElementById('humedad'),
    viento: document.getElementById('viento'),
    precipitacion: document.getElementById('precipitacion'),
    pronostico: document.getElementById('pronostico'),
    stationName: document.getElementById('station-name'),
    lastUpdate: document.getElementById('last-update'),
    dataSource: document.getElementById('data-source'),
    timeseriesPeriod: document.getElementById('timeseries-period'),
    timeseriesMetric: document.getElementById('timeseries-metric'),
    timeseriesChart: document.getElementById('timeseries-chart'),
    timeseriesPoints: document.getElementById('timeseries-points'),
    timeseriesUpdated: document.getElementById('timeseries-updated'),
    modelsContainer: document.getElementById('models-container')
};

// Estado de la aplicación
let STATE = {
    alcaldiaActual: CONFIG.DEFAULT_ALCALDIA,
    lastFetchTime: null,
    weatherData: null,
    timeseriesData: null,
    chart: null,
    modelsLoaded: false,
    updateTimer: null,
    fetchingData: false
};

// ==============================================
// FUNCIONES PRINCIPALES
// ==============================================

/**
 * Inicializar la aplicación
 */
function initApp() {
    console.log('🌤️ Iniciando Clima CDMX v2.0.0');
    updateStatus('🔄 Iniciando sistema...');
    
    // Configurar eventos
    DOM.alcaldiaSelect.addEventListener('change', handleAlcaldiaChange);
    if (DOM.timeseriesPeriod) {
        DOM.timeseriesPeriod.addEventListener('change', handleTimeseriesChange);
    }
    if (DOM.timeseriesMetric) {
        DOM.timeseriesMetric.addEventListener('change', handleTimeseriesChange);
    }
    
    // Cargar datos iniciales
    fetchWeatherData(STATE.alcaldiaActual)
        .then(() => {
            if (DOM.timeseriesPeriod && DOM.timeseriesMetric) {
                fetchTimeseriesData(STATE.alcaldiaActual);
            }
            
            // Iniciar actualización periódica
            startPeriodicUpdates();
        })
        .catch(handleError);
    
    // Cargar modelos 3D si está disponible
    if (DOM.modelsContainer && typeof loadModels === 'function') {
        loadModels();
    }
}

/**
 * Actualizar el estado mostrado en la interfaz
 * @param {string} message - Mensaje a mostrar
 * @param {string} type - Tipo de mensaje (normal, success, error)
 */
function updateStatus(message, type = 'normal') {
    if (DOM.status) {
        DOM.status.textContent = message;
        DOM.status.className = 'status-bar';
        
        if (type === 'success') {
            DOM.status.classList.add('success');
        } else if (type === 'error') {
            DOM.status.classList.add('error');
        }
    }
    
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    
    if (DOM.timestamp) {
        DOM.timestamp.textContent = `Última actualización: ${timeString}`;
    }
}

/**
 * Manejar cambio de alcaldía seleccionada
 */
function handleAlcaldiaChange() {
    const newAlcaldia = DOM.alcaldiaSelect.value;
    console.log(`🔄 Cambiando a alcaldía: ${newAlcaldia}`);
    
    STATE.alcaldiaActual = newAlcaldia;
    updateStatus(`🔄 Cargando datos para ${newAlcaldia}...`);
    
    fetchWeatherData(newAlcaldia)
        .then(() => {
            if (DOM.timeseriesPeriod && DOM.timeseriesMetric) {
                fetchTimeseriesData(newAlcaldia);
            }
        })
        .catch(handleError);
}

/**
 * Manejar cambio en configuración de series temporales
 */
function handleTimeseriesChange() {
    if (!DOM.timeseriesPeriod || !DOM.timeseriesMetric) return;
    
    fetchTimeseriesData(STATE.alcaldiaActual);
}

/**
 * Iniciar actualizaciones periódicas
 */
function startPeriodicUpdates() {
    // Limpiar timer existente si hay alguno
    if (STATE.updateTimer) {
        clearInterval(STATE.updateTimer);
    }
    
    // Configurar nuevo timer
    STATE.updateTimer = setInterval(() => {
        console.log('⏱️ Actualización automática');
        updateStatus('🔄 Actualizando datos...');
        
        fetchWeatherData(STATE.alcaldiaActual)
            .then(() => {
                if (DOM.timeseriesPeriod && DOM.timeseriesMetric) {
                    fetchTimeseriesData(STATE.alcaldiaActual);
                }
            })
            .catch(handleError);
    }, CONFIG.UPDATE_INTERVAL);
    
    console.log(`⏰ Actualizaciones automáticas cada ${CONFIG.UPDATE_INTERVAL / 60000} minutos`);
}

/**
 * Manejar errores generales
 * @param {Error} error - El error producido
 */
function handleError(error) {
    console.error('❌ Error:', error);
    updateStatus(`❌ Error: ${error.message}`, 'error');
}

// ==============================================
// FUNCIONES DE COMUNICACIÓN CON EL API
// ==============================================

/**
 * Obtener datos del clima para una alcaldía
 * @param {string} alcaldia - Alcaldía a consultar
 * @returns {Promise} Promesa con la respuesta
 */
async function fetchWeatherData(alcaldia) {
    if (STATE.fetchingData) {
        console.log('⚠️ Ya hay una petición en curso, ignorando');
        return;
    }
    
    STATE.fetchingData = true;
    updateStatus(`🔄 Obteniendo datos para ${alcaldia}...`);
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/weather?alcaldia=${alcaldia}`);
        
        if (!response.ok) {
            throw new Error(`API respondió con: ${response.status}`);
        }
        
        const data = await response.json();
        STATE.weatherData = data;
        STATE.lastFetchTime = new Date();
        
        // Actualizar interfaz con los nuevos datos
        updateWeatherUI(data);
        
        // Actualizar estado
        updateStatus(`✅ Datos actualizados para ${alcaldia}`, 'success');
        STATE.fetchingData = false;
        
        return data;
    } catch (error) {
        STATE.fetchingData = false;
        throw error;
    }
}

/**
 * Obtener datos de series temporales para una alcaldía
 * @param {string} alcaldia - Alcaldía a consultar
 * @returns {Promise} Promesa con la respuesta
 */
async function fetchTimeseriesData(alcaldia) {
    if (!DOM.timeseriesPeriod || !DOM.timeseriesMetric) return;
    
    const hours = DOM.timeseriesPeriod.value;
    updateStatus(`🔄 Obteniendo series temporales (${hours}h)...`);
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/weather/timeseries?alcaldia=${alcaldia}&hours=${hours}`);
        
        if (!response.ok) {
            throw new Error(`API de series temporales respondió con: ${response.status}`);
        }
        
        const data = await response.json();
        STATE.timeseriesData = data;
        
        // Actualizar gráfico con los nuevos datos
        updateTimeseriesChart(data);
        
        return data;
    } catch (error) {
        console.error('❌ Error obteniendo series temporales:', error);
        if (DOM.timeseriesPoints) {
            DOM.timeseriesPoints.textContent = `Error: ${error.message}`;
        }
        throw error;
    }
}

// ==============================================
// FUNCIONES DE ACTUALIZACIÓN DE LA INTERFAZ
// ==============================================

/**
 * Actualizar la interfaz con los datos meteorológicos
 * @param {Object} data - Datos meteorológicos
 */
function updateWeatherUI(data) {
    // Actualizar valores principales
    if (DOM.temperatura) DOM.temperatura.textContent = data.temperatura || '--°C';
    if (DOM.humedad) DOM.humedad.textContent = data.humedad || '--%';
    if (DOM.viento) DOM.viento.textContent = data.viento || '-- km/h';
    if (DOM.precipitacion) DOM.precipitacion.textContent = data.precipitacion || '-- mm';
    
    // Actualizar información de la estación
    if (DOM.stationName) DOM.stationName.textContent = data.station_name || '--';
    if (DOM.dataSource) DOM.dataSource.textContent = data.source || 'Conagua/SMN';
    
    // Formatear fecha de última actualización
    if (DOM.lastUpdate && data.timestamp) {
        try {
            const date = new Date(data.timestamp);
            const formattedTime = date.toLocaleTimeString();
            DOM.lastUpdate.textContent = formattedTime;
        } catch (e) {
            DOM.lastUpdate.textContent = data.timestamp || '--';
        }
    }
    
    // Actualizar pronóstico
    updateForecastUI(data.pronostico || []);
}

/**
 * Actualizar la sección de pronóstico
 * @param {Array} forecastData - Datos de pronóstico
 */
function updateForecastUI(forecastData) {
    if (!DOM.pronostico) return;
    
    if (!forecastData || forecastData.length === 0) {
        DOM.pronostico.innerHTML = '<div class="error-message">No hay datos de pronóstico disponibles</div>';
        return;
    }
    
    // Crear elementos del pronóstico
    const forecastContainer = document.createElement('div');
    forecastContainer.className = 'forecast-days';
    
    forecastData.forEach(day => {
        const dayElement = document.createElement('div');
        dayElement.className = 'forecast-day';
        
        dayElement.innerHTML = `
            <div class="day-name">${day.dia || 'Hoy'}</div>
            <div class="day-temp">${day.temp_max || '--'}/${day.temp_min || '--'}</div>
            <div class="day-condition">${day.condicion || '--'}</div>
        `;
        
        forecastContainer.appendChild(dayElement);
    });
    
    // Reemplazar contenido anterior
    DOM.pronostico.innerHTML = '';
    DOM.pronostico.appendChild(forecastContainer);
}

/**
 * Actualizar el gráfico de series temporales
 * @param {Object} timeseriesData - Datos de series temporales
 */
function updateTimeseriesChart(timeseriesData) {
    if (!DOM.timeseriesChart || !DOM.timeseriesMetric) return;
    
    const metricType = DOM.timeseriesMetric.value;
    const series = timeseriesData.series || [];
    
    // Actualizar contador de puntos
    if (DOM.timeseriesPoints) {
        DOM.timeseriesPoints.textContent = `${series.length} puntos de datos`;
    }
    
    // Actualizar timestamp
    if (DOM.timeseriesUpdated && timeseriesData.lastUpdate) {
        try {
            const date = new Date(timeseriesData.lastUpdate);
            DOM.timeseriesUpdated.textContent = `Última actualización: ${date.toLocaleString()}`;
        } catch (e) {
            DOM.timeseriesUpdated.textContent = `Última actualización: ${timeseriesData.lastUpdate}`;
        }
    }
    
    // Preparar datos para el gráfico
    const labels = [];
    const data = [];
    
    series.forEach(point => {
        try {
            const date = new Date(point.t);
            labels.push(date.toLocaleTimeString());
            
            // Obtener el valor según el tipo de métrica
            switch (metricType) {
                case 'temp':
                    data.push(point.temp);
                    break;
                case 'pp':
                    data.push(point.pp);
                    break;
                case 'humedad':
                    data.push(point.humedad);
                    break;
                case 'viento':
                    data.push(point.viento);
                    break;
                default:
                    data.push(point.temp);
            }
        } catch (e) {
            console.error('Error procesando punto de serie temporal:', e);
        }
    });
    
    // Configurar dataset
    const datasets = [{
        label: getMetricLabel(metricType),
        data: data,
        borderColor: CONFIG.CHART_COLORS[metricType === 'pp' ? 'precipitacion' : metricType] || 'rgba(75, 192, 192, 1)',
        backgroundColor: (CONFIG.CHART_COLORS[metricType === 'pp' ? 'precipitacion' : metricType] || 'rgba(75, 192, 192, 0.2)').replace('1)', '0.2)'),
        tension: 0.2,
        fill: true
    }];
    
    // Crear o actualizar gráfico
    if (STATE.chart) {
        STATE.chart.data.labels = labels;
        STATE.chart.data.datasets = datasets;
        STATE.chart.update();
    } else {
        STATE.chart = new Chart(DOM.timeseriesChart, {
            type: 'line',
            data: {
                labels: labels,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    y: {
                        title: {
                            display: true,
                            text: getMetricUnit(metricType)
                        },
                        beginAtZero: metricType === 'pp' // Comenzar en cero solo para precipitación
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Hora'
                        }
                    }
                }
            }
        });
    }
}

/**
 * Obtener etiqueta para el tipo de métrica
 * @param {string} metricType - Tipo de métrica
 * @returns {string} Etiqueta de la métrica
 */
function getMetricLabel(metricType) {
    switch (metricType) {
        case 'temp': return 'Temperatura';
        case 'pp': return 'Precipitación';
        case 'humedad': return 'Humedad';
        case 'viento': return 'Velocidad del viento';
        default: return 'Valor';
    }
}

/**
 * Obtener unidad para el tipo de métrica
 * @param {string} metricType - Tipo de métrica
 * @returns {string} Unidad de la métrica
 */
function getMetricUnit(metricType) {
    switch (metricType) {
        case 'temp': return 'Temperatura (°C)';
        case 'pp': return 'Precipitación (mm)';
        case 'humedad': return 'Humedad (%)';
        case 'viento': return 'Velocidad (km/h)';
        default: return 'Valor';
    }
}

// ==============================================
// CONFIGURACIÓN DE MODELOS 3D
// ==============================================

// Configuración de modelos 3D
const modelsConfig = [
    {
        filename: '35cdce76-1631-4596-b83f-0e5d13f00ed1.glb',
        name: 'Modelo de Precipitación',
        description: 'Visualización 3D de patrones de lluvia'
    },
    {
        filename: '94c06f5f-2f88-4ac2-b087-1eda19cab03d.glb',
        name: 'Modelo de Temperatura',
        description: 'Distribución térmica en CDMX'
    },
    {
        filename: 'f8dbfcd2-b861-476f-8ae2-dbe12f725588.glb',
        name: 'Modelo de Vientos',
        description: 'Patrones de circulación atmosférica'
    }
];

/**
 * Cargar los modelos 3D en el contenedor
 */
function loadModels() {
    if (!DOM.modelsContainer || typeof customElements === 'undefined' || !customElements.get('model-viewer')) {
        console.warn('🔍 La visualización 3D no está disponible en este navegador');
        if (DOM.modelsContainer) {
            DOM.modelsContainer.innerHTML = '<div class="error-message">La visualización 3D no está disponible en este navegador</div>';
        }
        return;
    }
    
    console.log('🔍 Cargando modelos 3D...');
    DOM.modelsContainer.innerHTML = '';
    
    // Crear contenedor de grid
    const modelsGrid = document.createElement('div');
    modelsGrid.className = 'models-grid';
    
    // Crear tarjeta para cada modelo
    modelsConfig.forEach(model => {
        try {
            const card = createModelCard(model);
            modelsGrid.appendChild(card);
        } catch (e) {
            console.error(`Error creando tarjeta para ${model.filename}:`, e);
        }
    });
    
    DOM.modelsContainer.appendChild(modelsGrid);
    STATE.modelsLoaded = true;
    console.log(`✅ ${modelsConfig.length} modelos 3D cargados`);
}

/**
 * Crear una tarjeta de modelo 3D
 * @param {Object} modelConfig - Configuración del modelo
 * @returns {HTMLElement} Elemento de tarjeta
 */
function createModelCard(modelConfig) {
    const card = document.createElement('div');
    card.className = 'model-card';

    // Crear el visor del modelo
    const viewer = document.createElement('model-viewer');
    viewer.src = `3Dclimagbl/${modelConfig.filename}`;
    viewer.alt = modelConfig.name;
    viewer.setAttribute('auto-rotate', '');
    viewer.setAttribute('camera-controls', '');
    viewer.setAttribute('shadow-intensity', '1');
    viewer.setAttribute('exposure', '1');
    
    // Agregar manejo de errores
    viewer.addEventListener('error', (event) => {
        console.error(`Error cargando modelo: ${modelConfig.filename}`, event);
        viewer.style.display = 'none';
        const errorMsg = document.createElement('div');
        errorMsg.style.padding = '20px';
        errorMsg.style.color = '#ff0000';
        errorMsg.textContent = `⚠️ Error al cargar el modelo 3D`;
        card.appendChild(errorMsg);
    });

    // Agregar indicador de carga
    viewer.addEventListener('load', () => {
        console.log(`Modelo cargado: ${modelConfig.filename}`);
    });

    // Crear etiqueta del modelo
    const label = document.createElement('div');
    label.className = 'model-label';
    label.textContent = modelConfig.name;

    // Crear descripción
    const description = document.createElement('div');
    description.className = 'model-description';
    description.textContent = modelConfig.description;

    // Crear controles adicionales
    const controls = document.createElement('div');
    controls.className = 'model-controls';

    const resetButton = document.createElement('button');
    resetButton.textContent = '🔄 Resetear Vista';
    resetButton.onclick = () => {
        viewer.resetTurntableRotation();
        viewer.fieldOfView = 'auto';
    };

    const fullscreenButton = document.createElement('button');
    fullscreenButton.textContent = '🔳 Pantalla Completa';
    fullscreenButton.onclick = () => {
        if (viewer.requestFullscreen) {
            viewer.requestFullscreen();
        }
    };

    controls.appendChild(resetButton);
    controls.appendChild(fullscreenButton);

    // Ensamblar la tarjeta
    card.appendChild(viewer);
    card.appendChild(label);
    card.appendChild(description);
    card.appendChild(controls);

    return card;
}

// ==============================================
// INICIAR APLICACIÓN
// ==============================================

// Iniciar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}

// Exportar funciones para uso externo
window.climaCDMX = {
    fetchWeatherData,
    fetchTimeseriesData,
    loadModels,
    CONFIG
};
