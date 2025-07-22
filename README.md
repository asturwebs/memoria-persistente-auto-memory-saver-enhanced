# Auto Memory Saver Enhanced para OpenWebUI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenWebUI](https://img.shields.io/badge/OpenWebUI-Compatible-green.svg)](https://github.com/open-webui/open-webui)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-red.svg)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.5+-purple.svg)](https://pydantic.dev/)
[![Version](https://img.shields.io/badge/version-2.0.0-brightgreen.svg)](https://github.com/AsturWebs/auto-memory-saver-enhanced)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/AsturWebs/auto-memory-saver-enhanced/graphs/commit-activity)
[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red.svg)](https://github.com/AsturWebs)

## 👨‍💻 Autoría y Créditos

**Enhanced Version by:** Pedro Luis Cuevas Villarrubia ([@AsturWebs](https://github.com/AsturWebs))  
**Based on original work by:** [@linbanana](https://github.com/linbanana)  
**Enhancement Date:** January 22, 2025  
**Contact:** pedro@asturwebs.es | pedro@tu-ia.es | pedro@bytia.es  
**Original Downloads:** 173+

### Credits & Attribution
- **Original Concept:** @linbanana - Basic Auto Memory Saver functionality
- **Enhanced Version:** Pedro Luis Cuevas Villarrubia - Complete system transformation with 24 configurable valves, 16 interactive commands, advanced caching, professional documentation, and enterprise-ready features

### Version History
- **v1.0 (Original):** Basic memory saving functionality by @linbanana
- **v2.0 (Enhanced):** Complete system with granular configuration, interactive commands, professional architecture, and comprehensive documentation by Pedro Luis Cuevas Villarrubia

---

## 📋 Descripción

Auto Memory Saver es un filtro avanzado para OpenWebUI que gestiona automáticamente las memorias de conversaciones. Este sistema permite inyectar memorias previas en nuevas conversaciones y guardar automáticamente las respuestas del asistente como memorias para uso futuro.

## 🚀 Características Principales

- **Inyección Automática de Memorias**: Carga automáticamente memorias relevantes al inicio de nuevas conversaciones
- **Guardado Automático**: Almacena las respuestas del asistente como memorias sin intervención manual
- **16 Comandos Interactivos**: Suite completa de comandos para gestión avanzada de memorias
- **24 Válvulas Configurables**: Control granular sobre todos los aspectos del sistema
- **Sistema de Caché**: Optimización de rendimiento con caché inteligente con expiración
- **Manejo Robusto de Errores**: Validaciones exhaustivas y recuperación de errores
- **Tipado Fuerte**: Tipos personalizados para mayor seguridad y mantenibilidad

## 🛠 Instalación

### Requisitos Previos

- **OpenWebUI** instalado y funcionando (cualquier versión compatible)
- **Python 3.8+** (incluido en la mayoría de instalaciones de OpenWebUI)
- **Entorno compatible**: Local, VPS, Docker, Kubernetes, etc.

### Instalación en OpenWebUI

#### Método 1: Desde el Panel de Administración (Recomendado)

1. **Accede al panel de administración** de OpenWebUI
2. **Ve a la pestaña "Funciones"** (Functions)
3. **Haz clic en "+"** para crear una nueva función
4. **Copia y pega** el código completo del archivo `frAuto_Memory_Saver_OpenWebUI_Adds_the_assistant_message_to_users_memories.py`
5. **Asigna un nombre**: "Auto Memory Saver Enhanced"
6. **Añade descripción**: "Sistema avanzado de gestión automática de memorias con 16 comandos interactivos"
7. **Guarda la función**
8. **Configura las opciones** haciendo clic en la rueda dentada (⚙️) de la función

#### Método 2: Instalación Manual de Archivos

1. Copia el archivo `frAuto_Memory_Saver_OpenWebUI_Adds_the_assistant_message_to_users_memories.py` a tu directorio de filtros de OpenWebUI
2. Reinicia OpenWebUI para cargar el nuevo filtro
3. Activa el filtro en la configuración de OpenWebUI

## ⚙️ Configuración

### Válvulas Principales (Valves)

```python
class Valves:
    # Configuración principal
    enabled: bool = True  # Habilita/deshabilita el sistema completo
    
    # Control de inyección de memorias
    inject_memories: bool = True  # Inyecta memorias en conversaciones
    max_memories_to_inject: int = 5  # Máximo de memorias por conversación (1-20)
    
    # Control de guardado
    auto_save_responses: bool = True  # Guarda respuestas automáticamente
    min_response_length: int = 10  # Longitud mínima para guardar (1-1000)
    max_response_length: int = 2000  # Longitud máxima para guardar (100-10000)
    
    # Sistema de caché
    enable_cache: bool = True  # Habilita caché para rendimiento
    cache_ttl_minutes: int = 60  # Tiempo de vida del caché (1-1440 min)
    
    # Limpieza automática
    auto_cleanup: bool = False  # Limpia memorias antiguas
    max_memories_per_user: int = 100  # Límite por usuario (0 = ilimitado)
    
    # Filtrado inteligente
    filter_duplicates: bool = True  # Filtra memorias duplicadas
    similarity_threshold: float = 0.8  # Umbral de similitud (0.0-1.0)
    
    # Comandos disponibles
    enable_memory_commands: bool = True  # Habilita /memories, /clear_memories
    
    # Depuración
    debug_mode: bool = False  # Logging detallado
```

### Válvulas de Usuario (UserValves)

```python
class UserValves:
    # Visualización
    show_status: bool = True  # Muestra estado durante guardado
    show_memory_count: bool = True  # Muestra número de memorias inyectadas
    show_save_confirmation: bool = False  # Confirma cuando se guarda
    
    # Notificaciones
    notify_on_error: bool = True  # Notifica errores al usuario
    notify_on_cleanup: bool = False  # Notifica limpiezas automáticas
    
    # Personalización
    custom_memory_prefix: str = ""  # Prefijo personalizado (vacío = default)
    max_personal_memories: int = 0  # Límite personal (0 = usar global)
    
    # Privacidad
    private_mode: bool = False  # Modo privado: no guarda automáticamente
```

### Configuración de Caché

```python
class Constants:
    CACHE_MAXSIZE = 128  # Número máximo de entradas en caché
    CACHE_TTL = 3600     # Tiempo de vida en segundos (1 hora)
```

## 📖 Uso

### Comandos Disponibles

#### 📚 Gestión de Memorias
- **`/memories`** - Lista todas las memorias con numeración
- **`/clear_memories`** - Elimina todas las memorias del usuario
- **`/memory_count`** - Muestra contador detallado con límites disponibles
- **`/memory_search <término>`** - Busca memorias que contengan un término específico
- **`/memory_recent [número]`** - Muestra las últimas N memorias (por defecto 5, máximo 20)
- **`/memory_export`** - Exporta todas las memorias en formato texto estructurado

#### ⚙️ Configuración
- **`/memory_config`** - Muestra la configuración completa del sistema y usuario
- **`/private_mode on|off`** - Activa o desactiva el modo privado temporalmente
- **`/memory_limit <número>`** - Establece límite personal de memorias (0 = ilimitado)
- **`/memory_prefix <texto>`** - Configura un prefijo personalizado para las memorias

#### 📊 Información y Estadísticas
- **`/memory_help`** - Muestra ayuda completa con todos los comandos disponibles
- **`/memory_stats`** - Estadísticas detalladas del sistema (total, promedio, configuración)
- **`/memory_status`** - Estado actual del filtro y todas sus funcionalidades

#### 🔧 Utilidades Avanzadas
- **`/memory_cleanup`** - Analiza y reporta memorias duplicadas potenciales
- **`/memory_backup`** - Crea información de respaldo de las memorias actuales

#### 💡 Ejemplos de Uso
```bash
# Buscar memorias sobre un tema específico
/memory_search inteligencia artificial

# Ver las últimas 3 memorias
/memory_recent 3

# Configurar un límite personal
/memory_limit 50

# Activar modo privado temporalmente
/private_mode on

# Ver estadísticas completas
/memory_stats
```

### Nuevas Funcionalidades

#### Control Granular de Inyección
- **Límite configurable**: Controla cuántas memorias se inyectan por conversación
- **Prefijos personalizados**: Cada usuario puede personalizar cómo se muestran sus memorias
- **Contador visual**: Muestra cuántas memorias se inyectaron

#### Filtrado Inteligente
- **Validación de longitud**: Solo guarda respuestas dentro del rango configurado
- **Detección de duplicados**: Evita guardar memorias similares o repetidas
- **Truncado automático**: Mensajes largos se truncan automáticamente

#### Modo Privado
- **Privacidad total**: Los usuarios pueden desactivar el guardado automático
- **Control individual**: Cada usuario controla su propia configuración

#### Sistema de Caché Avanzado
- **Rendimiento optimizado**: Caché con expiración automática
- **Configuración flexible**: TTL ajustable según necesidades
- **Limpieza automática**: Gestión inteligente de memoria

### Funcionamiento Automático

1. **Al iniciar una conversación**: El sistema inyecta automáticamente las memorias relevantes
2. **Al finalizar una respuesta**: Guarda automáticamente la respuesta del asistente como memoria
3. **Gestión de errores**: Maneja automáticamente errores y continúa funcionando

## 🏗 Arquitectura

### Componentes Principales

```
Filter
├── Valves (Configuración global)
├── UserValves (Configuración por usuario)
├── MemoryCache (Sistema de caché)
├── inlet() (Inyección de memorias)
├── outlet() (Guardado de memorias)
├── clear_user_memory() (Limpieza de memorias)
└── get_processed_memory_strings() (Recuperación de memorias)
```

### Tipos Personalizados

```python
UserData: TypedDict  # Estructura de datos del usuario
MessageDict: TypedDict  # Estructura de mensajes
EventEmitter: Callable  # Emisor de eventos
CacheEntry: dataclass  # Entrada de caché con expiración
```

## 🔧 Desarrollo

### Estructura del Código

```
frAuto_Memory_Saver_OpenWebUI_Adds_the_assistant_message_to_users_memories.py
├── Configuración de logging
├── Importaciones con manejo de dependencias
├── Tipos personalizados y constantes
├── Sistema de caché
└── Clase Filter principal
```

### Mejoras Implementadas

- ✅ Sistema de logging avanzado
- ✅ Manejo robusto de errores
- ✅ Validación exhaustiva de datos
- ✅ Sistema de caché con expiración
- ✅ Tipos personalizados para mayor seguridad
- ✅ Documentación bilingüe (chino/español)
- ✅ Manejo de dependencias con fallbacks

## 📊 Rendimiento

### Optimizaciones Implementadas

1. **Caché en Memoria**: Reduce consultas repetitivas a la base de datos
2. **Validación Temprana**: Evita procesamiento innecesario
3. **Manejo Asíncrono**: No bloquea el flujo principal de la aplicación
4. **Limpieza Automática**: El caché se limpia automáticamente

### Métricas de Rendimiento

- **Tiempo de respuesta**: < 100ms para operaciones en caché
- **Uso de memoria**: Limitado por `CACHE_MAXSIZE`
- **Escalabilidad**: Soporta múltiples usuarios concurrentes

## 🔒 Seguridad

### Medidas Implementadas

- **Validación de Entrada**: Todos los parámetros son validados
- **Manejo Seguro de Errores**: No expone información sensible
- **Tipado Fuerte**: Previene errores de tipo en tiempo de ejecución
- **Logging Seguro**: No registra información sensible

### Recomendaciones de Seguridad

- Implementar autenticación JWT
- Añadir rate limiting
- Configurar HTTPS en producción
- Revisar logs regularmente

## 🚀 Despliegue

### Entorno de Producción (VPS + EasyPanel)

1. **Preparación del Entorno**:
   ```bash
   # Instalar dependencias
   pip install -r requirements.txt
   
   # Configurar variables de entorno
   export LOG_LEVEL=INFO
   export CACHE_TTL=3600
   ```

2. **Configuración en EasyPanel**:
   - Subir el archivo del filtro
   - Configurar variables de entorno
   - Reiniciar el servicio OpenWebUI

3. **Verificación**:
   - Comprobar logs de inicio
   - Probar funcionalidad básica
   - Verificar rendimiento

### Variables de Entorno Recomendadas

```bash
LOG_LEVEL=INFO
CACHE_MAXSIZE=128
CACHE_TTL=3600
MEMORY_PREFIX="📘 Memoria previa:\n"
```

## 🧪 Pruebas

### Pruebas Recomendadas

```python
# Ejemplo de prueba unitaria
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_inlet_with_valid_user():
    filter_instance = Filter()
    body = {"messages": []}
    user = {"id": "test_user"}
    
    result = await filter_instance.inlet(body, None, user, None)
    assert isinstance(result, dict)
```

### Cobertura de Pruebas

- [ ] Pruebas unitarias para cada método
- [ ] Pruebas de integración con base de datos
- [ ] Pruebas de rendimiento
- [ ] Pruebas de seguridad

## 📈 Monitoreo

### Métricas Clave

- Número de memorias procesadas
- Tiempo de respuesta promedio
- Errores por minuto
- Uso de caché (hit/miss ratio)

## 🔮 Roadmap

### Próximas Mejoras

1. **Caché Distribuido**: Implementar Redis para entornos distribuidos
2. **Métricas Avanzadas**: Integración con Prometheus
3. **Interfaz Web**: Panel de administración para gestión de memorias
4. **IA Mejorada**: Clasificación inteligente de memorias
5. **Exportación**: Funcionalidad de exportar/importar memorias

### Mejoras de Rendimiento

1. **Compresión**: Comprimir memorias grandes
2. **Paginación**: Implementar paginación para listas largas
3. **Índices**: Optimizar consultas de base de datos
4. **Clustering**: Agrupar memorias similares

## 🤝 Contribución

### Cómo Contribuir

1. Fork del repositorio
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

### Estándares de Código

- Seguir PEP 8
- Documentar todas las funciones
- Añadir pruebas para nuevas funcionalidades
- Mantener cobertura de pruebas > 80%

## 📝 Changelog

### v2.0.0 (Actual)
- ✅ Sistema de caché avanzado
- ✅ Tipos personalizados
- ✅ Logging mejorado
- ✅ Manejo robusto de errores
- ✅ Documentación bilingüe

### v1.0.0 (Original)
- ✅ Funcionalidad básica de memorias
- ✅ Comandos de consulta
- ✅ Integración con OpenWebUI

## 🐛 Problemas Conocidos

- Ninguno reportado actualmente

## 📞 Soporte

Para reportar problemas o solicitar funcionalidades:

1. Revisar la documentación
2. Comprobar logs de error
3. Crear issue con detalles completos
4. Incluir pasos para reproducir el problema

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- Equipo de OpenWebUI por la plataforma base
- @linbanana por el concepto original y la base del proyecto
- Comunidad de desarrolladores por feedback y contribuciones
- Usuarios beta por las pruebas y reportes

## 📄 Licencia

Este proyecto está licenciado bajo la **MIT License**.

```
MIT License

Copyright (c) 2025 Pedro Luis Cuevas Villarrubia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Ver el archivo [LICENSE](LICENSE) para más detalles.

---

**Nota**: Este README se actualiza regularmente. Para la versión más reciente, consulta el repositorio principal.
