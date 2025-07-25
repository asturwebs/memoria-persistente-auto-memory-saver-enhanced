# Archivo de Configuración de Ejemplo para Auto Memory Saver
# Copia este archivo y ajusta los valores según tus necesidades

"""
CONFIGURACIÓN DE EJEMPLO PARA AUTO MEMORY SAVER
===============================================

Este archivo contiene ejemplos de configuración para diferentes escenarios de uso.
Copia las configuraciones que necesites y ajústalas según tu entorno.

IMPORTANTE: Este es solo un archivo de ejemplo. Las configuraciones reales
se realizan a través de las válvulas en la interfaz de OpenWebUI.
"""

# =============================================================================
# CONFIGURACIONES PREDEFINIDAS PARA DIFERENTES CASOS DE USO
# =============================================================================

# -----------------------------------------------------------------------------
# CONFIGURACIÓN BÁSICA (Recomendada para la mayoría de usuarios)
# -----------------------------------------------------------------------------
BASIC_CONFIG = {
    "valves": {
        # Configuración principal
        "enabled": True,
        "inject_memories": True,
        "auto_save_responses": True,
        # Límites conservadores
        "max_memories_to_inject": 3,
        "min_response_length": 20,
        "max_response_length": 1000,
        # Funcionalidades básicas
        "enable_cache": True,
        "cache_ttl_minutes": 30,
        "filter_duplicates": True,
        "enable_memory_commands": True,
        # Sin limpieza automática por seguridad
        "auto_cleanup": False,
        "debug_mode": False,
    },
    "user_valves": {
        "show_status": True,
        "show_memory_count": True,
        "notify_on_error": True,
        "private_mode": False,
    },
}

# -----------------------------------------------------------------------------
# CONFIGURACIÓN PARA DESARROLLO (Con logging detallado)
# -----------------------------------------------------------------------------
DEVELOPMENT_CONFIG = {
    "valves": {
        # Configuración principal
        "enabled": True,
        "inject_memories": True,
        "auto_save_responses": True,
        # Límites para testing
        "max_memories_to_inject": 2,
        "min_response_length": 5,
        "max_response_length": 500,
        # Caché rápido para desarrollo
        "enable_cache": True,
        "cache_ttl_minutes": 5,
        "filter_duplicates": True,
        "enable_memory_commands": True,
        # Limpieza automática para testing
        "auto_cleanup": True,
        "max_memories_per_user": 10,
        # DEBUG ACTIVADO
        "debug_mode": True,
    },
    "user_valves": {
        "show_status": True,
        "show_memory_count": True,
        "show_save_confirmation": True,
        "notify_on_error": True,
        "notify_on_cleanup": True,
        "private_mode": False,
    },
}

# -----------------------------------------------------------------------------
# CONFIGURACIÓN PARA PRODUCCIÓN (Optimizada para rendimiento)
# -----------------------------------------------------------------------------
PRODUCTION_CONFIG = {
    "valves": {
        # Configuración principal
        "enabled": True,
        "inject_memories": True,
        "auto_save_responses": True,
        # Límites optimizados para producción
        "max_memories_to_inject": 5,
        "min_response_length": 15,
        "max_response_length": 2000,
        # Caché optimizado
        "enable_cache": True,
        "cache_ttl_minutes": 60,
        "filter_duplicates": True,
        "similarity_threshold": 0.85,
        "enable_memory_commands": True,
        # Limpieza automática habilitada
        "auto_cleanup": True,
        "max_memories_per_user": 100,
        # Sin debug en producción
        "debug_mode": False,
    },
    "user_valves": {
        "show_status": False,  # Menos notificaciones en producción
        "show_memory_count": False,
        "show_save_confirmation": False,
        "notify_on_error": True,
        "notify_on_cleanup": False,
        "private_mode": False,
    },
}

# -----------------------------------------------------------------------------
# CONFIGURACIÓN PARA ALTA PRIVACIDAD
# -----------------------------------------------------------------------------
PRIVACY_CONFIG = {
    "valves": {
        # Configuración principal
        "enabled": True,
        "inject_memories": False,  # No inyectar por defecto
        "auto_save_responses": False,  # No guardar por defecto
        # Límites estrictos
        "max_memories_to_inject": 1,
        "min_response_length": 50,
        "max_response_length": 500,
        # Caché deshabilitado por privacidad
        "enable_cache": False,
        "filter_duplicates": True,
        "similarity_threshold": 0.95,  # Muy estricto
        "enable_memory_commands": True,  # Permitir control manual
        # Limpieza automática agresiva
        "auto_cleanup": True,
        "max_memories_per_user": 20,
        # Sin debug por privacidad
        "debug_mode": False,
    },
    "user_valves": {
        "show_status": True,
        "show_memory_count": True,
        "show_save_confirmation": True,  # Confirmar siempre
        "notify_on_error": True,
        "notify_on_cleanup": True,
        "private_mode": True,  # MODO PRIVADO ACTIVADO
    },
}

# -----------------------------------------------------------------------------
# CONFIGURACIÓN PARA EMPRESAS (Balanceada y segura)
# -----------------------------------------------------------------------------
ENTERPRISE_CONFIG = {
    "valves": {
        # Configuración principal
        "enabled": True,
        "inject_memories": True,
        "auto_save_responses": True,
        # Límites empresariales
        "max_memories_to_inject": 7,
        "min_response_length": 25,
        "max_response_length": 3000,
        # Caché empresarial
        "enable_cache": True,
        "cache_ttl_minutes": 120,
        "filter_duplicates": True,
        "similarity_threshold": 0.8,
        "enable_memory_commands": True,
        # Gestión automática
        "auto_cleanup": True,
        "max_memories_per_user": 200,
        # Debug condicional
        "debug_mode": False,
    },
    "user_valves": {
        "show_status": True,
        "show_memory_count": True,
        "show_save_confirmation": False,
        "notify_on_error": True,
        "notify_on_cleanup": True,
        "private_mode": False,
    },
}

# =============================================================================
# VARIABLES DE ENTORNO RECOMENDADAS
# =============================================================================

ENVIRONMENT_VARIABLES = {
    # Logging
    "LOG_LEVEL": "INFO",  # DEBUG, INFO, WARNING, ERROR
    "LOG_FORMAT": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    # Caché
    "DEFAULT_CACHE_TTL": "3600",  # 1 hora en segundos
    "MAX_CACHE_SIZE": "128",
    # Límites globales
    "GLOBAL_MAX_MEMORIES": "1000",
    "GLOBAL_MAX_RESPONSE_LENGTH": "5000",
    # Seguridad
    "ENABLE_RATE_LIMITING": "true",
    "MAX_REQUESTS_PER_MINUTE": "60",
    # Base de datos (si aplicable)
    "DB_POOL_SIZE": "10",
    "DB_TIMEOUT": "30",
}

# =============================================================================
# CONFIGURACIÓN PARA EASYPANEL
# =============================================================================

EASYPANEL_CONFIG = {
    "environment": {
        # Variables específicas para EasyPanel
        "PYTHONPATH": "/app",
        "PYTHONUNBUFFERED": "1",
        # OpenWebUI específico
        "OPENWEBUI_LOG_LEVEL": "INFO",
        "OPENWEBUI_MEMORY_FILTER_ENABLED": "true",
        # Configuración de memoria
        "MEMORY_CACHE_SIZE": "64",  # MB
        "MEMORY_CACHE_TTL": "1800",  # 30 minutos
        # Configuración de red
        "PORT": "8080",
        "HOST": "0.0.0.0",
    },
    "resources": {
        # Recursos recomendados para VPS
        "memory": "512MB",  # Mínimo recomendado
        "cpu": "0.5",  # Medio core
        "storage": "1GB",  # Para logs y caché
    },
    "health_check": {
        "path": "/health",
        "interval": "30s",
        "timeout": "10s",
        "retries": 3,
    },
}

# =============================================================================
# FUNCIONES DE UTILIDAD PARA CONFIGURACIÓN
# =============================================================================


def get_config_by_environment(env_type="basic"):
    """
    Obtiene la configuración según el tipo de entorno.

    Args:
        env_type (str): Tipo de entorno ('basic', 'development', 'production',
                       'privacy', 'enterprise')

    Returns:
        dict: Configuración correspondiente
    """
    configs = {
        "basic": BASIC_CONFIG,
        "development": DEVELOPMENT_CONFIG,
        "production": PRODUCTION_CONFIG,
        "privacy": PRIVACY_CONFIG,
        "enterprise": ENTERPRISE_CONFIG,
    }

    return configs.get(env_type, BASIC_CONFIG)


def validate_config(config):
    """
    Valida una configuración antes de aplicarla.

    Args:
        config (dict): Configuración a validar

    Returns:
        tuple: (es_válida, errores)
    """
    errors = []

    # Validar válvulas principales
    valves = config.get("valves", {})

    # Validar rangos numéricos
    if valves.get("max_memories_to_inject", 0) > 20:
        errors.append("max_memories_to_inject no puede ser mayor a 20")

    if valves.get("min_response_length", 0) > valves.get("max_response_length", 1000):
        errors.append("min_response_length no puede ser mayor a max_response_length")

    if not 0 <= valves.get("similarity_threshold", 0.8) <= 1:
        errors.append("similarity_threshold debe estar entre 0.0 y 1.0")

    return len(errors) == 0, errors


def apply_config_to_filter(filter_instance, config):
    """
    Aplica una configuración a una instancia del filtro.

    Args:
        filter_instance: Instancia del filtro Auto Memory Saver
        config (dict): Configuración a aplicar
    """
    # Aplicar válvulas principales
    valves_config = config.get("valves", {})
    for key, value in valves_config.items():
        if hasattr(filter_instance.valves, key):
            setattr(filter_instance.valves, key, value)

    print(f"Configuración aplicada: {len(valves_config)} válvulas configuradas")


# =============================================================================
# EJEMPLOS DE USO
# =============================================================================

if __name__ == "__main__":
    # Ejemplo 1: Obtener configuración básica
    basic_config = get_config_by_environment("basic")
    print("Configuración básica:")
    print(f"- Memorias máximas: {basic_config['valves']['max_memories_to_inject']}")
    print(f"- Caché habilitado: {basic_config['valves']['enable_cache']}")

    # Ejemplo 2: Validar configuración
    is_valid, errors = validate_config(basic_config)
    print(f"\nConfiguración válida: {is_valid}")
    if errors:
        print("Errores encontrados:")
        for error in errors:
            print(f"- {error}")

    # Ejemplo 3: Mostrar configuración para EasyPanel
    print("\nConfiguración recomendada para EasyPanel:")
    print(f"- Memoria: {EASYPANEL_CONFIG['resources']['memory']}")
    print(f"- CPU: {EASYPANEL_CONFIG['resources']['cpu']}")
    print(f"- Puerto: {EASYPANEL_CONFIG['environment']['PORT']}")

# =============================================================================
# NOTAS IMPORTANTES
# =============================================================================

"""
INSTRUCCIONES DE DESPLIEGUE:

1. Para VPS con EasyPanel:
   - Usar PRODUCTION_CONFIG como base
   - Configurar variables de entorno de EASYPANEL_CONFIG
   - Asignar recursos según EASYPANEL_CONFIG['resources']

2. Para desarrollo local:
   - Usar DEVELOPMENT_CONFIG
   - Habilitar debug_mode para troubleshooting

3. Para entornos con alta privacidad:
   - Usar PRIVACY_CONFIG
   - Considerar deshabilitar caché completamente

4. Personalización:
   - Copiar la configuración más cercana a tus necesidades
   - Ajustar valores específicos
   - Validar con validate_config() antes de aplicar

COMANDOS DISPONIBLES PARA USUARIOS:

📚 GESTIÓN DE MEMORIAS:
- /memories: Lista todas las memorias con numeración
- /clear_memories: Elimina todas las memorias del usuario
- /memory_count: Muestra contador detallado con límites
- /memory_search <término>: Busca memorias por contenido
- /memory_recent [número]: Últimas N memorias (def: 5, máx: 20)
- /memory_export: Exporta memorias en formato texto

⚙️ CONFIGURACIÓN:
- /memory_config: Muestra configuración completa
- /private_mode on|off: Activa/desactiva modo privado
- /memory_limit <número>: Establece límite personal (0 = ilimitado)
- /memory_prefix <texto>: Configura prefijo personalizado

📊 INFORMACIÓN:
- /memory_help: Ayuda completa con todos los comandos
- /memory_stats: Estadísticas detalladas del sistema
- /memory_status: Estado actual del filtro

🔧 UTILIDADES:
- /memory_cleanup: Analiza duplicados potenciales
- /memory_backup: Crea información de respaldo

EJEMPLOS DE USO:
- /memory_search "inteligencia artificial": Busca memorias sobre IA
- /memory_recent 3: Ver últimas 3 memorias
- /memory_limit 50: Establecer límite de 50 memorias
- /private_mode on: Activar modo privado temporalmente

MONITOREO:
- Revisar logs regularmente
- Monitorear uso de memoria y CPU
- Ajustar cache_ttl_minutes según patrones de uso
"""
