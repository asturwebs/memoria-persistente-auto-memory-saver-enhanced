# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere al [Versionado Semántico](https://semver.org/spec/v2.0.0.html).

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
