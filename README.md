# Persistent Memory (Auto Memory Saver Enhanced)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenWebUI](https://img.shields.io/badge/OpenWebUI-Compatible-green.svg)](https://github.com/open-webui/open-webui)
[![Version](https://img.shields.io/badge/version-2.6.5-brightgreen.svg)](https://github.com/asturwebs/memoria-persistente-auto-memory-saver-enhanced)

**Filter for OpenWebUI** that automatically manages conversation memories. Injects relevant memories and saves conversations for future context.

## Features

- **Automatic Memory Injection**: Injects relevant memories into conversations
- **Auto-Save**: Saves user questions and assistant responses
- **Slash Commands**: Interactive memory management
- **Thread-Safe Cache**: Performance optimization with TTL
- **Security**: Input validation, SQL injection prevention

## Installation

1. Open OpenWebUI administration panel
2. Go to **Functions** tab
3. Click **+** to create new function
4. Copy code from `src/memoria_persistente_auto_memory_saver_enhanced.py`
5. Save and activate

## Comandos Disponibles (Slash Commands)

Gestiona tu memoria persistente directamente desde el chat:

### Gestión Básica
| Comando | Descripción |
|---------|-------------|
| `/memories [página]` | Lista tus memorias guardadas (paginado). |
| `/memory_search <término>` | Busca memorias específicas por contenido. |
| `/memory_recent [n]` | Muestra las N memorias más recientes (default: 5). |
| `/memory_count` | Muestra el número total de memorias guardadas. |
| `/clear_memories` | **¡Cuidado!** Elimina permanentemente todas tus memorias. |

### Configuración y Estado
| Comando | Descripción |
|---------|-------------|
| `/memory_config` | Muestra la configuración actual de tus Valves. |
| `/memory_stats` | Muestra estadísticas detalladas de uso y almacenamiento. |
| `/memory_status` | Verifica el estado operativo del sistema de memoria. |
| `/private_mode [on/off]` | Activa/desactiva el modo privado (no guarda memorias). |
| `/memory_limit <n>` | Establece tu límite personal de memorias (0 = ilimitado). |
| `/memory_prefix <texto>` | Define un prefijo para tus nuevas memorias. |

### Herramientas Avanzadas
| Comando | Descripción |
|---------|-------------|
| `/memory_export` | Exporta todas tus memorias a un formato de texto. |
| `/memory_cleanup` | Ejecuta limpieza manual de duplicados y optimización. |
| `/memory_backup` | Crea una copia de seguridad de tus memorias actuales. |
| `/memory_restore` | Restaura memorias desde una copia de seguridad interna. |
| `/memory_analytics` | Análisis profundo de tus patrones de memoria. |
| `/memory_help` | Muestra esta lista de ayuda. |

> **Tip**: Usa el comando nativo de OpenWebUI `/add_memory <texto>` para agregar memorias manualmente.

## Configuración (Valves)

El sistema es altamente configurable a través de **Valves**. Puedes ajustar estos valores desde:
`Panel de Admin > Funciones > Memoria Persistente > Valves (engranaje)`

### Sistema y Comportamiento (Valves Globales)
- **enabled**: Activa o desactiva todo el sistema de memoria.
- **enable_memory_commands**: Activa/desactiva el uso de comandos (slash commands) en el chat.
- **debug_mode**: Activa logs detallados para depuración.
- **enable_cache**: Usa caché en memoria para mejorar el rendimiento (recomendado).
- **cache_ttl_minutes**: Tiempo de vida del caché en minutos (default: 60).

### Inyección y Recuperación
- **inject_memories**: Inyecta memorias relevantes al inicio de nuevas conversaciones.
- **max_memories_to_inject**: Cantidad máxima de memorias a inyectar (default: 5).
- **max_memories_to_scan**: Cuantas memorias recientes analizar para relevancia (default: 300).
- **relevance_threshold**: Nivel mínimo de relevancia (0.0-1.0) para inyectar una memoria (default: 0.05).
- **skip_injection_for_casual**: Evita gastar tokens en saludos simples (Hola, Buenos días).
- **max_injection_chars**: Límite duro de caracteres para prevenir contextos gigantes (default: 3500).

### Guardado y Optimización
- **auto_save_responses**: Guarda automáticamente información útil de las respuestas del asistente.
- **enable_smart_summarization**: Usa LLM para resumir la conversación antes de guardar (Ahorra espacio).
- **summarization_prompt**: El prompt usado para resumir conversaciones.
- **min_content_for_summary**: Mínimo de caracteres para activar el resumen.
- **min_response_length**: Longitud mínima de la respuesta para ser guardada (default: 10).
- **max_response_length**: Longitud máxima de la respuesta para ser guardada (default: 2000).
- **filter_duplicates**: Evita guardar memorias idénticas o muy similares.
- **similarity_threshold**: Sensibilidad para detectar duplicados (0.8 = 80% similar).
- **auto_cleanup**: Activa limpieza periódica de memorias antiguas (default: False).
- **max_memories_per_user**: Límite global de memorias por usuario (default: 100).

### Preferencias de Usuario (UserValves)
Estas opciones pueden ser configuradas individualmente por cada usuario:
- **show_status**: Muestra indicadores de estado ("Guardando memoria...") en el chat.
- **show_memory_count**: Indica cuántas memorias se inyectaron al inicio del chat.
- **show_save_confirmation**: Muestra un mensaje de confirmación cuando se guarda una memoria.
- **private_mode**: Si está activo, el sistema no guardará nada de lo que hables.
- **custom_memory_prefix**: Texto que se añadirá al principio de cada memoria nueva.
- **max_personal_memories**: Límite personal de memorias (0 = usa configuración global).
- **notify_on_cleanup**: Notifica cuando se realiza una limpieza automática de memorias.
- **notify_on_error**: Muestra alertas si ocurre un error en el sistema.

## AI Compatibility

- **Automatic memory** (injection/saving): Works on **all AI models**
- **Slash commands**: Best results with Claude, Grok, Gemini (via OpenRouter), GPT-4.1-mini

## Project Structure

```text
 src/
    memoria_persistente_auto_memory_saver_enhanced.py
 docs/
    CHANGELOG.md
    ARCHITECTURE.md
    release_notes_v*.md
 README.md
 requirements.txt
```

## Credits

- **Enhanced by**: Pedro Luis Cuevas Villarrubia ([@AsturWebs](https://github.com/AsturWebs))
- **Original concept**: [@linbanana](https://github.com/linbanana)

## License

MIT License - See [LICENSE](LICENSE)
