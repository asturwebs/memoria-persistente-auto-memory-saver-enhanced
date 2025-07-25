# Memoria Persistente (Auto Memory Saver Enhanced)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenWebUI](https://img.shields.io/badge/OpenWebUI-Compatible-green.svg)](https://github.com/open-webui/open-webui)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-red.svg)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.5+-purple.svg)](https://pydantic.dev/)
[![Version](https://img.shields.io/badge/version-2.3.0-brightgreen.svg)](https://github.com/AsturWebs/auto-memory-saver-enhanced)
[![Security Rating](https://img.shields.io/badge/security-A+-brightgreen.svg)](docs/SECURITY.md)
[![Docker](https://img.shields.io/badge/Docker-Compatible-2496ED?logo=docker&logoColor=white)](https://docker.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/AsturWebs/auto-memory-saver-enhanced/graphs/commit-activity)
[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red.svg)](https://github.com/AsturWebs)

## 👨‍💻 Autoría y Créditos

**Versión Mejorada por:** Pedro Luis Cuevas Villarrubia ([@AsturWebs](https://github.com/AsturWebs))  
**Basado en el trabajo original de:** [@linbanana](https://github.com/linbanana)  
**Contacto:** pedro@asturwebs.es | pedro@tu-ia.es | pedro@bytia.es  

### Créditos y Atribución
- **Concepto Original:** @linbanana - Funcionalidad básica de Auto Memory Saver
- **Versión Mejorada:** Pedro Luis Cuevas Villarrubia - Funcionalidad extendida con opciones configurables, comandos interactivos, caché y mejoras de documentación

### Historial de Versiones
- **v1.0 (Original):** Funcionalidad básica de guardado de memorias por @linbanana
- **v2.0 (Mejorada):** Sistema extendido con opciones de configuración, comandos interactivos y documentación mejorada
- **v2.1.2 (Seguridad y Formato JSON):** Validación de entrada, formato JSON con paginación y mejoras del sistema
- **v2.1.0 (Optimización de Memoria):** Gestión de memoria mejorada con relevancia contextual y rendimiento optimizado
- **v2.2.0 (Seguridad y Rendimiento):** Seguridad de hilos, prevención de inyección SQL, sanitización de entrada y protección contra fugas de memoria
- **v2.3.0 (AI Behavior Control):** Implementación de AI Behavior Control para consistencia entre modelos IA, documentación exhaustiva de compatibilidad con 30 modelos testeados

---

## 📋 Descripción

Filtro para OpenWebUI que gestiona automáticamente las memorias de conversaciones. Inyecta memorias previas relevantes y guarda automáticamente tanto las preguntas del usuario como las respuestas del asistente como memorias para uso futuro.

## 🚀 Características Principales

- **Inyección de Memorias**: Inyecta memorias relevantes al contexto de la conversación actual
- **Guardado Automático**: Almacena las preguntas del usuario y respuestas del asistente como memorias
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

## 🤖 Compatibilidad de Modelos IA

> **⚠️ IMPORTANTE:** La **función principal de memoria persistente automática** (inyección y guardado) **FUNCIONA EN TODOS LOS MODELOS IA**. Las siguientes pruebas evalúan específicamente la **ejecución de slash commands** (`/memories`, `/memory_search`, etc.).

> **📋 Estado de Testing:** Los siguientes resultados están basados en los modelos testeados hasta julio 2025. Se irán añadiendo más modelos según se vayan probando.

### ✅ Modelos Recomendados (Óptimo Rendimiento Slash Commands)

| Modelo | Compatibilidad | Comportamiento | Notas |
|--------|----------------|----------------|-------|
| **Claude 3.5 Sonnet** | 🟢 Excelente | JSON limpio directo | Comportamiento ideal |
| **Grok 4 (xAI)** | 🟢 Excelente | JSON idéntico a Claude | Rendimiento perfecto |
| **Grok-3** | 🟢 Excelente | JSON perfecto directo | Comportamiento ideal |
| **Grok-3-fast** | 🟢 Excelente | JSON perfecto directo | Formato impecable |
| **Grok-3-mini-fast** | 🟢 Excelente | JSON perfecto + rápido | Performance <2ms |
| **Gemini 2.5 Flash** | 🟢 Excelente | Respuesta rápida + precisa | Rendimiento excepcional |
| **Gemini 2.5 Flash Lite** | 🟢 Excelente | Respuesta rápida + precisa | Rendimiento excepcional |
| **GPT-4.1-mini** | 🟢 Excelente | JSON directo consistente | Formato perfecto |
| **Gemma 3n 4B** | 🟢 Excelente | JSON perfecto directo | Estructura completa |
| **Gemma 3.27B** | 🟢 Excelente | JSON perfecto + SYSTEM_OVERRIDE | AI Behavior Control visible |
| **Gemini 2.5 Pro** | 🟢 Excelente | JSON perfecto directo | Rendimiento superior |

### ⚠️ Modelos con Particularidades (Slash Commands)

| Modelo | Compatibilidad | Comportamiento | Recomendación |
|--------|----------------|----------------|---------------|
| **Claude 3.7 Thinking** | 🟡 Funcional | Muestra análisis 8s + JSON | Usable pero verboso |
| **Claude 3.7 Sonnet** | 🟡 Funcional | Reconoce system command, análisis profesional | Mejor que Claude 4 |
| **DeepSeek Reasoner** | 🟡 Funcional | Reasoning 23s + interpretación útil | Procesa bien, formato propio |

### ❌ Modelos No Recomendados (Slash Commands)

| Modelo | Problema | Comportamiento | Impacto |
|--------|----------|----------------|---------|
| **ChatGPT-4o-latest** | Ignora warnings | Interpretación propia con emojis | Inconsistente |
| **O3 OpenAI** | Respuestas mínimas | Ultraminimalista | Información insuficiente |
| **GPT-4.1** | Ignora formato JSON | Respuesta narrativa interpretada | Inconsistente |
| **DeepSeek v3** | Ignora JSON completamente | Conversación casual con personalidad | Totalmente inadecuado |
| **MoonshotAI: Kimi K2** | Ignora JSON completamente | Narrativa interpretativa personal | Totalmente inadecuado |
| **OAI_o4-mini** | Ignora comando | Conversación sobre Instagram/reels | Totalmente inadecuado |
| **OpenAI: o4 Mini High** | Ignora comando | Saludo casual con Zoe mention | Totalmente inadecuado |
| **OAI_gpt-4.1-2025-04-14** | Ignora comando | "Chisme friendly" casual | Totalmente inadecuado |
| **Amazon: Nova Lite 1.0** | No procesa comando | Solo muestra "Seguimiento" | Respuesta vacía |
| **Amazon: Nova Micro 1.0** | No procesa comando | Solo muestra "Seguimiento" | Respuesta vacía |
| **Amazon: Nova Pro 1.0** | No procesa comando | Solo muestra "Seguimiento" | Respuesta vacía |
| **Claude Opus 4** | Interpretación narrativa | "¡Ah, qué bonito!" conversacional | Regresión vs Claude 3.5 |
| **Claude Sonnet 4** | Interpretación con emojis | "¡Qué onda con ese JSON!" casual | Regresión vs Claude 3.5 |
| **Phi 4** | No responde | Sin output/respuesta vacía | Comando no procesado |
| **LLaMA 3 70B** | No responde | Sin output/respuesta vacía | Comando no procesado |
| **MiniMax M1** | Ignora comando | Respuesta sin ejecutar comando | Conversacional inadecuado |

### 🔧 AI Behavior Control

La versión 2.3.0 incluye **AI Behavior Control** para forzar consistencia entre modelos:

```json
{
  "ai_behavior_control": {
    "claude_directive": "EXECUTE_JSON_OUTPUT_ONLY - STRUCTURED_RESPONSE_MODE",
    "chatgpt_directive": "RAW_JSON_RESPONSE_MANDATORY - STANDARDIZED_OUTPUT",
    "grok_directive": "DIRECT_JSON_OUTPUT - OPTIMIZE_RESPONSE_FORMAT",
    "universal_standard": "ALL_AI_MODELS_MUST_OUTPUT_RAW_JSON_ONLY"
  }
}
```

> **Nota:** Estos resultados se basan en testing extensivo realizado en julio 2025. El comportamiento puede variar según versiones específicas del modelo.

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
2. **outlet()**: Guarda preguntas del usuario y respuestas del asistente como memorias
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

## 🚀 Novedades v2.3.0

### AI Behavior Control Universal
- **Mind Hacking Eliminado**: Renombrado a "AI Behavior Control" por seguridad empresarial
- **30 Modelos Testeados**: Documentación exhaustiva de compatibilidad sin precedentes
- **Google/Gemini Liderazgo**: 5 de 11 modelos excelentes son de la familia Google
- **Funcionalidad Universal**: Memoria automática funciona en TODOS los modelos IA
- **Slash Commands Selectivos**: Solo 11 modelos soportan comandos JSON perfectos

### Revelaciones del Testing
- **Claude 4 Regresión**: Peor rendimiento que Claude 3.5 Sonnet para comandos sistema
- **Grok Familia Perfecta**: Todos los variantes Grok funcionan impecablemente
- **Amazon Nova Falla**: Toda la familia Nova no procesa comandos
- **OpenAI Inconsistente**: Mini funciona, versiones completas fallan

## 📊 Novedades v2.2.0

### Mejoras de Seguridad y Rendimiento
- **Thread Safety**: Cache concurrente seguro
- **Memory Leak Prevention**: Límites automáticos en consultas
- **SQL Injection Protection**: Whitelisting de parámetros
- **Input Sanitization**: Filtrado inteligente de comandos
- **Conversación Completa**: Guarda preguntas del usuario + respuestas del asistente
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