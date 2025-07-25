# Memoria Persistente (Auto Memory Saver Enhanced)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenWebUI](https://img.shields.io/badge/OpenWebUI-Compatible-green.svg)](https://github.com/open-webui/open-webui)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-red.svg)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.5+-purple.svg)](https://pydantic.dev/)
[![Version](https://img.shields.io/badge/version-2.2.0-brightgreen.svg)](https://github.com/AsturWebs/auto-memory-saver-enhanced)
[![Security Rating](https://img.shields.io/badge/security-A+-brightgreen.svg)](docs/SECURITY.md)
[![Docker](https://img.shields.io/badge/Docker-Compatible-2496ED?logo=docker&logoColor=white)](https://docker.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/AsturWebs/auto-memory-saver-enhanced/graphs/commit-activity)
[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red.svg)](https://github.com/AsturWebs)

## 👨‍💻 Autoría y Créditos

**Enhanced Version by:** Pedro Luis Cuevas Villarrubia ([@AsturWebs](https://github.com/AsturWebs))  
**Based on original work by:** [@linbanana](https://github.com/linbanana)  
**Contact:** pedro@asturwebs.es | pedro@tu-ia.es | pedro@bytia.es  

### Credits & Attribution
- **Original Concept:** @linbanana - Basic Auto Memory Saver functionality
- **Enhanced Version:** Pedro Luis Cuevas Villarrubia - Extended functionality with configurable options, interactive commands, caching, and documentation improvements

### Version History
- **v1.0 (Original):** Basic memory saving functionality by @linbanana
- **v2.0 (Enhanced):** Extended system with configuration options, interactive commands, and improved documentation
- **v2.1.2 (Security & JSON Format):** Input validation, JSON format with pagination, and system improvements
- **v2.1.0 (Memory Optimization):** Improved memory management with contextual relevance and optimized performance
- **v2.2.0 (Security & Performance):** Thread safety, SQL injection prevention, input sanitization, and memory leak protection

---

## 📋 Descripción

Filtro para OpenWebUI que gestiona automáticamente las memorias de conversaciones. Inyecta memorias previas relevantes y guarda automáticamente las respuestas del asistente como memorias para uso futuro.

## 🚀 Características Principales

- **Inyección de Memorias**: Inyecta memorias relevantes al contexto de la conversación actual
- **Guardado Automático**: Almacena las respuestas del asistente como memorias
- **Comandos Interactivos**: Comandos para gestión de memorias (`/memories`, `/memory_search`, etc.)
- **Configuración Flexible**: Múltiples opciones configurables según necesidades
- **Sistema de Caché**: Optimización de rendimiento con caché y expiración
- **Validación de Entrada**: Sanitización de inputs y prevención de inyecciones
- **Compatibilidad**: Integra con comandos nativos de OpenWebUI (`/add_memory`)

## 📁 Estructura del Proyecto

```
auto-memory-saver-enhanced/
├── src/
│   ├── memoria_persistente_auto_memory_saver_enhanced.py  # Sistema principal
│   └── legacy/
│       └── Auto_Memory_Saver.py                          # v1.0.0 by @linbanana
├── docs/                                                 # Documentación técnica
│   ├── ARCHITECTURE.md
│   ├── SECURITY.md
│   └── release_notes_v*.md
├── README.md
├── CHANGELOG.md
├── LICENSE
└── requirements.txt
```

## 🛠 Instalación

### Requisitos Previos
- **OpenWebUI** instalado y funcionando
- **Python 3.8+** (incluido en la mayoría de instalaciones de OpenWebUI)

### Instalación en OpenWebUI

1. **Accede al panel de administración** de OpenWebUI
2. **Ve a la pestaña "Functions"**
3. **Haz clic en "+"** para crear una nueva función
4. **Copia y pega** el código completo del archivo `src/memoria_persistente_auto_memory_saver_enhanced.py`
5. **Asigna un nombre**: "Auto Memory Saver Enhanced"
6. **Guarda y activa la función**

## ⚙️ Configuración

### Válvulas Principales (Valves)

```python
class Valves:
    # Configuración principal
    enabled: bool = True                        # Habilita/deshabilita el sistema
    inject_memories: bool = True                # Inyecta memorias en conversaciones
    auto_save_responses: bool = True            # Guarda respuestas automáticamente
    
    # Control de memorias
    max_memories_to_inject: int = 5             # Máximo de memorias por conversación
    max_memories_per_user: int = 100            # Límite por usuario
    relevance_threshold: float = 0.05           # Umbral de relevancia (0.0-1.0)
    
    # Sistema de caché
    enable_cache: bool = True                   # Habilita caché para rendimiento
    cache_ttl_minutes: int = 60                 # Tiempo de vida del caché
    
    # Filtrado inteligente
    filter_duplicates: bool = True              # Filtra memorias duplicadas
    filter_short_responses: bool = True         # Filtra respuestas muy cortas
    
    # Comandos y notificaciones
    enable_memory_commands: bool = True         # Habilita comandos interactivos
    show_injection_status: bool = True          # Muestra estado de inyección
    debug_mode: bool = False                    # Logging detallado
```

## 📖 Comandos Disponibles

### Comandos Nativos OpenWebUI (Recomendados)
- **`/add_memory <texto>`** - Añade memoria directamente al sistema (comando nativo)

### Comandos Personalizados
- **`/memories [página]`** - Lista memorias con formato JSON, paginación (10 por página)
- **`/memory_search <término>`** - Busca memorias que contengan el término
- **`/memory_stats`** - Estadísticas del sistema con formato JSON
- **`/memory_count`** - Contador de memorias del usuario
- **`/memory_recent [número]`** - Muestra las últimas N memorias
- **`/clear_memories`** - Elimina todas las memorias del usuario

### Comandos Avanzados
- **`/memory_delete <id>`** - Elimina una memoria específica
- **`/memory_edit <id> <texto>`** - Edita el contenido de una memoria
- **`/memory_export`** - Exporta memorias en formato texto
- **`/memory_config`** - Muestra configuración actual

### Ejemplos de Uso
```bash
# Buscar memorias sobre un tema
/memory_search inteligencia artificial

# Ver las últimas 5 memorias
/memory_recent 5

# Ver estadísticas
/memory_stats
```

## 🏗 Arquitectura

### Componentes Principales
- **Filter**: Clase principal que maneja inlet/outlet
- **Valves**: Configuración global del sistema
- **UserValves**: Configuración específica por usuario
- **MemoryCache**: Sistema de caché con expiración TTL
- **Security Functions**: Validación y sanitización de inputs

### Funcionamiento
1. **inlet()**: Inyecta memorias relevantes al inicio de conversaciones
2. **outlet()**: Guarda respuestas del asistente como memorias
3. **Comandos**: Procesamiento de comandos interactivos de gestión

## 🔒 Seguridad

### Características de Seguridad v2.2.0
- **Thread Safety**: Cache thread-safe con RLock
- **SQL Injection Prevention**: Validación de parámetros order_by
- **Input Sanitization**: Filtrado de comandos peligrosos
- **Memory Leak Protection**: Paginación de consultas BD
- **User ID Validation**: Sanitización con regex
- **Command Filtering**: Bloqueo de conversaciones sobre memoria

### Validaciones Implementadas
- Sanitización de inputs con límites de longitud
- Prevención de caracteres peligrosos (`;`, `&`, `|`, etc.)
- Validación de user_id y memory_id
- Manejo seguro de errores sin exposición de datos

## 📊 Novedades v2.2.0

### Mejoras de Seguridad y Rendimiento
- **Thread Safety**: Cache concurrente seguro
- **Memory Leak Prevention**: Límites automáticos en consultas
- **SQL Injection Protection**: Whitelisting de parámetros
- **Input Sanitization**: Filtrado inteligente de comandos
- **Conversación Completa**: Guarda input del usuario + output de IA
- **Filtro Anti-Meta**: No guarda conversaciones sobre memoria
- **Paginación Mejorada**: 10 memorias por página (antes 4)

### Compatibilidad
- Integración con comando nativo `/add_memory` de OpenWebUI
- Mantiene compatibilidad con todas las versiones anteriores
- Sin cambios breaking en la API

## 🤝 Contribución

1. Fork del repositorio
2. Crear rama de feature
3. Commit de cambios
4. Crear Pull Request

### Estándares
- Seguir PEP 8
- Documentar funciones
- Añadir pruebas para nuevas funcionalidades

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- **OpenWebUI team** por la plataforma base
- **@linbanana** por el concepto original
- **Comunidad** por feedback y contribuciones

---

**Nota**: Para la documentación técnica completa, ver la carpeta `docs/`