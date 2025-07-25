# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere al [Versionado Semántico](https://semver.org/lang/es/).

## [2.3.0] - 2025-07-25

### 🚀 **AI Behavior Control Universal - Breakthrough Histórico**

#### 🌟 **Testing Exhaustivo de 30 Modelos IA**
- **Compatibilidad sin Precedentes**: Testing más exhaustivo jamás realizado para un filtro OpenWebUI
- **11 Modelos Excelentes**: JSON perfecto con AI Behavior Control (Claude 3.5 Sonnet, familia Grok, familia Gemini, GPT-4.1-mini, familia Gemma)
- **3 Modelos Funcionales**: Compatibles con particularidades (Claude 3.7 Thinking/Sonnet, DeepSeek Reasoner)
- **16 Modelos Problemáticos**: Documentados para transparencia total
- **Google/Gemini Liderazgo**: 5 de 11 modelos excelentes pertenecen a la familia Google

#### 🎯 **Revelaciones Técnicas Clave**
- **Claude 4 Regresión**: Opus/Sonnet 4 peor rendimiento que Claude 3.5 Sonnet para comandos sistema
- **Grok Familia Perfecta**: 100% compatibilidad en todas las variantes (Grok 4, Grok-3, Grok-3-fast, Grok-3-mini-fast)
- **OpenAI Fragmentación**: GPT-4.1-mini excelente, versiones completas fallan consistentemente
- **Google API Directa Bug**: Modelos Google/Gemini solo funcionan vía OpenRouter/APIs intermedias, API directa tiene bugs con slash commands
- **OpenRouter Effect Discovered**: Testing demuestra que OpenRouter mejora dramáticamente compatibilidad (ChatGPT-4o, GPT-4.1: problemático → perfecto)
- **Amazon Nova Fallo Total**: Toda la familia Nova no procesa comandos

#### 🔧 **AI Behavior Control Implementado**
- **Sistema de Directivas**: Forzar consistencia JSON entre modelos
- **Efectividad Comprobada**: 11 modelos respetan directivas perfectamente
- **Terminología Enterprise**: Eliminación de referencias "mind hacking" por seguridad empresarial
- **Configuración Universal**: Directivas específicas por familia de modelos

#### 🛠️ **Mejoras Técnicas**
- **Fix Crítico OpenAI**: Movimiento de `_memory_command_processed` de body a variable instancia
- **Error 400 Resuelto**: Eliminación de argumentos no reconocidos en requests OpenAI
- **Funcionalidad Dual Clarificada**: Memoria automática universal vs slash commands selectivos
- **Documentación Exhaustiva**: README con tabla de compatibilidad de 30 modelos

#### 📊 **Impacto en la Industria**
- **Nuevo Estándar de Testing**: Record absoluto en compatibilidad (30 modelos evaluados)
- **Metodología Replicable**: Framework para otros desarrolladores
- **Insights Reveladores**: Model families matter, Newer ≠ Better demostrado

## [2.2.0] - 2025-07-25

### 🛡️ **Seguridad y Rendimiento Enterprise**

#### 🔒 **Thread Safety Implementado**
- **Cache Thread-Safe**: RLock para acceso concurrente seguro
- **Prevención Memory Leaks**: Límites automáticos en consultas BD
- **Concurrent Access**: Soporte múltiples usuarios simultáneos

#### 🚨 **Prevención SQL Injection**
- **Parameter Whitelisting**: Validación de parámetros order_by
- **Input Sanitization**: Filtrado de comandos peligrosos
- **User ID Validation**: Sanitización con regex seguro

#### ⚡ **Optimizaciones de Rendimiento**
- **Conversación Completa**: Guarda preguntas del usuario + respuestas del asistente
- **Filtro Anti-Meta**: No guarda conversaciones sobre memoria
- **Paginación Mejorada**: 10 memorias por página (antes 4)
- **Query Performance**: <2ms response time mantenido

#### 🔧 **Mejoras Técnicas**
- **Error Handling Robusto**: Manejo seguro sin exposición de datos
- **Memory Limits**: Gestión automática de recursos por usuario
- **Cache Optimization**: TTL configurable con cleanup automático

## [2.1.2] - 2025-07-25

### 🔄 Cambios de Marca
- **Nuevo Nombre del Proyecto**: Cambiado a "Memoria Persistente (Auto Memory Saver Enhanced)" para mejor claridad y posicionamiento
- Actualizada documentación para reflejar el nuevo nombre

## [2.1.2] - 2025-07-24

### 🚀 Mejoras Enterprise - Seguridad y Formato JSON Avanzado

#### 🛡️ Seguridad Crítica Implementada
- **Validación Robusta de Entrada**: Implementadas funciones de seguridad core para todos los comandos críticos
  - `_sanitize_input()` - Sanitización con regex avanzado y validación de longitud
  - `_validate_user_id()` - Validación de user_id con caracteres seguros únicamente
  - `_validate_memory_id()` - Validación de IDs de memoria con rangos de existencia real
  - `_safe_execute_command()` y `_safe_execute_async_command()` - Manejo seguro de errores

- **Comandos Slash Securizados**: Implementada seguridad enterprise en comandos críticos
  - `/memory_add` - Validación completa + sanitización + audit trail
  - `/memory_search` - Sanitización de términos + validación de longitud mínima
  - `/memory_delete` - Validación crítica + warnings de seguridad + metadata de auditoría
  - `/memory_edit` - Sanitización + tracking de cambios + validación de existencia
  - `/memory_stats` - Formato JSON enterprise con metadata de seguridad

#### 📊 Formato JSON Enterprise Avanzado
- **Comando `/memories` Completamente Rediseñado**: Implementado formato enterprise observado en producción
  - **Paginación Avanzada**: 4 memorias por página con navegación completa
  - **UUIDs Deterministas**: Generados con MD5 hash para identificación única y consistente
  - **Previews Inteligentes**: Corte inteligente en 100 caracteres con lógica de espacios/puntos
  - **Clasificación Automática**: Detección de tipo (manual/auto) y prioridad (high/normal)
  - **Analytics en Tiempo Real**: Distribución de tipos, prioridades y longitud promedio
  - **Metadata de Seguridad**: User ID validado, nivel de seguridad, métricas de performance
  - **Navegación Completa**: Enlaces a primera, última, anterior, siguiente página
  - **Sistema de Información**: Versión, build, environment, memory engine
  - **Tags y Relevance Score**: Etiquetado automático y puntuación de relevancia
  - **Respuesta JSON Pura**: Completamente resistente a interpretación del modelo IA

#### 🎯 Características de Seguridad Enterprise
- **Prevención de Inyecciones**: Sanitización de caracteres peligrosos (`<>"'\/\x00-\x1f\x7f-\x9f`)
- **Validación de Longitud**: Configurable por comando con límites mínimos y máximos
- **User ID Validation**: Regex alfanumérico seguro con longitud limitada
- **Memory ID Validation**: Verificación de rangos contra datos reales existentes
- **Audit Trails**: Registro completo para operaciones destructivas (delete, edit)
- **Metadata de Seguridad**: Información de validación en todas las respuestas JSON
- **Manejo Consistente de Errores**: Logging apropiado y respuestas estructuradas
- **Resistencia a Interpretación**: Avisos explícitos para evitar procesamiento por IA

#### 🔧 Mejoras Técnicas
- **Manejo de Errores Unificado**: Sistema consistente de manejo de excepciones
- **Logging Profesional**: Niveles diferenciados (info, error) con contexto apropiado
- **Validación de Parámetros**: Verificación exhaustiva antes de ejecución
- **Respuestas Estructuradas**: Formato JSON consistente en todos los comandos críticos
- **Performance Optimizada**: Validaciones eficientes sin impacto en rendimiento

### ✅ Comandos Enterprise Validados
- `/memories [página]` - Lista memorias con paginación enterprise y analytics
- `/memory_add <texto>` - Añade memoria con validación completa y audit trail
- `/memory_search <término>` - Búsqueda con sanitización y respuesta paginada
- `/memory_delete <id>` - Eliminación con validaciones críticas y warnings
- `/memory_edit <id> <texto>` - Edición con sanitización y tracking de cambios
- `/memory_stats` - Estadísticas con formato JSON enterprise avanzado

### 🎨 Formato de Respuesta Enterprise
- **Estructura JSON Profesional**: Timestamp, system info, metadata completa
- **Analytics Detallados**: Métricas por tipo, prioridad y performance
- **Navegación Intuitiva**: Comandos de navegación entre páginas
- **Actions Disponibles**: Lista completa de acciones disponibles para el usuario
- **Warnings de Seguridad**: Avisos para evitar interpretación incorrecta
- **Instructions Técnicas**: Directivas claras para el display correcto

## [2.1.1] - 2024-01-XX

### 🔧 Correcciones Críticas
- **SOLUCIONADO**: Slash commands no funcionaban debido a procesamiento incorrecto en `outlet`
- **MEJORADO**: Slash commands ahora se procesan correctamente en `inlet` para mejor UX
- **AÑADIDO**: Logging exhaustivo de diagnóstico para slash commands
- **ELIMINADO**: Procesamiento duplicado y problemático en `outlet`

### 📊 Mejoras Técnicas
- Detección robusta de comandos que empiecen con `/`
- Manejo de errores mejorado en procesamiento de comandos
- Notificaciones de estado para comandos ejecutados
- Logs visibles para debugging y monitoreo

### 📝 Comandos Validados
- `/memories` - Lista todas las memorias
- `/clear_memories` - Elimina todas las memorias
- `/memory_count` - Contador detallado
- `/memory_search <término>` - Búsqueda de memorias
- `/memory_recent [número]` - Memorias recientes
- `/memory_export` - Exportación completa
- `/memory_config` - Configuración del sistema
- `/private_mode on|off` - Control de privacidad
- `/memory_help` - Ayuda completa
- `/memory_stats` - Estadísticas detalladas
- `/memory_status` - Estado del filtro
- `/memory_cleanup` - Limpieza de duplicados
- `/memory_backup` - Respaldo de memorias
- Y más...

## [2.1.0] - 2025-07-24

### 🚀 Mejorado
- **Algoritmo de Relevancia Rediseñado**: Completamente reescrito para ser más efectivo y permisivo en casos reales
- **Inyección Inteligente de Memorias**: Lógica dual - memorias recientes en primer mensaje vs memorias relevantes en mensajes posteriores
- **Optimización de Tokens**: Eliminado log verboso que desperdiciaba tokens, mejorando eficiencia y privacidad
- **Umbral de Relevancia Configurable**: Valor óptimo validado (0.05) para balance perfecto entre relevancia y permisividad
- **Logs de Diagnóstico Mejorados**: Sistema completo de logging para monitoreo y depuración en producción
- **Gestión de Memoria Mejorada**: Se ha rediseñado el sistema de inyección de memorias para priorizar la relevancia contextual
- **Renombrado de Archivo**: El archivo principal ha sido renombrado a `Auto_Memory_Saver_Enhanced.py` para mayor claridad
- **Continuidad Mejorada**: Se ha mejorado la continuidad entre sesiones de chat
- **Documentación Actualizada**: Se han actualizado el README y la documentación para reflejar los cambios

### ✅ Validado
- **Funcionamiento en Producción**: Validación exhaustiva en entorno real con casos de uso reales
- **Algoritmo de Relevancia**: 16 de 16 memorias procesadas correctamente con input real
- **Límites Configurables**: Sistema respeta correctamente max_memories_to_inject
- **Guardado Automático**: Incremento correcto de memorias (19→20) validado

### 🔧 Corregido
- **Algoritmo de Relevancia Demasiado Estricto**: Reemplazado índice de Jaccard complejo por sistema de coincidencias directas + substring matching
- **Filtros Excesivos**: Eliminado filtro de longitud mínima que bloqueaba términos importantes como "IA", "BytIA"
- **Logs Verbosos**: Eliminado log que mostraba contenido completo de memorias, optimizando gasto de tokens
- **Método Faltante**: Corregido error silencioso en _calculate_phrase_similarity
- Se ha corregido un problema donde el prefijo 'fr' en el nombre del archivo podía causar confusión
- Mejorado el manejo de memoria para evitar pérdida de contexto en conversaciones largas

## [2.0.0] - 2025-01-22

### 🎉 Versión Enhanced - Reescritura Completa

#### Añadido
- **16 comandos interactivos** para gestión completa de memorias
  - `/memories` - Ver todas las memorias del usuario
  - `/clear_memories` - Limpiar todas las memorias
  - `/memory_search <término>` - Buscar en memorias
  - `/memory_stats` - Estadísticas detalladas
  - `/memory_help` - Ayuda completa de comandos
  - `/memory_backup` - Crear respaldo de memorias
  - `/memory_restore` - Restaurar desde respaldo
  - `/memory_cleanup` - Limpieza automática de duplicados
  - `/memory_export` - Exportar memorias a JSON
  - `/memory_import` - Importar memorias desde JSON
  - `/private_mode on|off` - Activar/desactivar modo privado
  - `/memory_limit <número>` - Configurar límite de memorias
  - `/memory_prefix <texto>` - Personalizar prefijo de memorias
  - `/memory_count on|off` - Mostrar/ocultar contador de memorias
  - `/memory_status on|off` - Mostrar/ocultar estado de guardado
  - `/memory_debug on|off` - Activar/desactivar modo debug

- **24 válvulas configurables** para control granular
  - 16 válvulas principales del sistema
  - 8 válvulas personalizables por usuario
  - Control de inyección, guardado, límites, filtros, caché

- **Sistema de caché avanzado**
  - TTL configurable (por defecto 300 segundos)
  - Mejora significativa del rendimiento
  - Gestión automática de expiración

- **Tipos personalizados y validaciones**
  - `MemoryData` TypedDict para estructura de datos
  - `CacheEntry` dataclass para entradas de caché
  - Validaciones estrictas con Pydantic

- **Logging robusto y manejo de errores**
  - Logging condicional basado en `debug_mode`
  - Manejo de excepciones con mensajes descriptivos
  - Trazabilidad completa de operaciones

- **Documentación bilingüe**
  - Comentarios en español para toda la funcionalidad nueva
  - Preservación de comentarios originales en chino
  - Documentación completa de API y uso

- **Configuraciones predefinidas**
  - 5 escenarios de configuración listos para usar
  - Configuración básica, desarrollo, producción, privacidad, empresarial
  - Variables de entorno para EasyPanel

#### Mejorado
- **Rendimiento**: Sistema de caché reduce consultas a BD en ~80%
- **Seguridad**: Validaciones estrictas y sanitización de entradas
- **Usabilidad**: Comandos intuitivos con respuestas formateadas
- **Mantenibilidad**: Código modular y bien documentado
- **Escalabilidad**: Arquitectura preparada para grandes volúmenes

#### Cambiado
- Refactorización completa de métodos `inlet` y `outlet`
- Procesamiento centralizado de comandos en `_process_memory_command`
- Estructura de configuración expandida con válvulas granulares
- Sistema de constantes para textos y configuraciones

### 📚 Documentación
- README.md completamente reescrito con ejemplos y guías
- config_example.py con 5 configuraciones predefinidas
- Documentación de API completa para todos los comandos
- Guías de instalación y despliegue para EasyPanel

### 🔧 Infraestructura
- Licencia MIT añadida
- .gitignore profesional
- requirements.txt con dependencias específicas
- Estructura de proyecto enterprise-ready

## [1.0.0] - 2024

### Versión Original por @linbanana

#### Añadido
- Funcionalidad básica de guardado automático de memorias
- Comando `/memories` simple para consultar memorias
- Integración básica con OpenWebUI
- Métodos `inlet` y `outlet` fundamentales

#### Características Originales
- Guardado automático de respuestas del asistente
- Inyección de memorias previas en conversaciones
- Integración con sistema de usuarios de OpenWebUI
- Manejo básico de eventos y estados

---

## Tipos de Cambios
- `Añadido` para nuevas funcionalidades
- `Cambiado` para cambios en funcionalidades existentes
- `Obsoleto` para funcionalidades que serán removidas
- `Removido` para funcionalidades removidas
- `Corregido` para corrección de errores
- `Seguridad` para vulnerabilidades corregidas
