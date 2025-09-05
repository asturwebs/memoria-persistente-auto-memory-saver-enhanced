# Example Configuration File for Auto Memory Saver Enhanced v2.3.0
# Copy this file and adjust values according to your needs

"""
EXAMPLE CONFIGURATION FOR AUTO MEMORY SAVER ENHANCED v2.3.0
===============================================================

With Universal AI Behavior Control and compatibility with 30+ AI models.

This file contains configuration examples for different usage scenarios.
Copy the configurations you need and adjust them according to your environment.

IMPORTANT: This is only an example file. Real configurations
are performed through valves in the OpenWebUI interface.

DUAL FUNCTIONALITY v2.3.0:
- Automatic Persistent Memory: WORKS ON ALL AI MODELS
- Slash Commands: Work perfectly on 11 excellent models

EXCELLENT MODELS (Slash Commands):
- Claude 3.5 Sonnet, Grok family, GPT-4.1-mini (direct APIs)
- ChatGPT-4o, GPT-4.1, Gemini family, Gemma family (via OpenRouter)
- OPENROUTER EFFECT: ~25+ excellent models vs 11 direct APIs
- IMPORTANT: Use OpenRouter for maximum compatibility
"""

# =============================================================================
# PREDEFINED CONFIGURATIONS FOR DIFFERENT USE CASES
# =============================================================================

# -----------------------------------------------------------------------------
# BASIC CONFIGURATION (Recommended for most users)
# -----------------------------------------------------------------------------
BASIC_CONFIG = {
    "valves": {
        # Main configuration
        "enabled": True,
        "inject_memories": True,
        "auto_save_responses": True,
        # Conservative limits
        "max_memories_to_inject": 3,
        "min_response_length": 20,
        "max_response_length": 1000,
        # Basic functionalities
        "enable_cache": True,
        "cache_ttl_minutes": 30,
        "filter_duplicates": True,
        "filter_short_responses": True,
        "enable_memory_commands": True,
        "show_injection_status": True,
        # No automatic cleanup for safety
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
# DEVELOPMENT CONFIGURATION (With detailed logging)
# -----------------------------------------------------------------------------
DEVELOPMENT_CONFIG = {
    "valves": {
        # Main configuration
        "enabled": True,
        "inject_memories": True,
        "auto_save_responses": True,
        # Testing limits
        "max_memories_to_inject": 2,
        "min_response_length": 5,
        "max_response_length": 500,
        # Fast cache for development
        "enable_cache": True,
        "cache_ttl_minutes": 5,
        "filter_duplicates": True,
        "enable_memory_commands": True,
        # Automatic cleanup for testing
        "auto_cleanup": True,
        "max_memories_per_user": 10,
        # DEBUG ENABLED
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
# PRODUCTION CONFIGURATION (Optimized for performance)
# -----------------------------------------------------------------------------
PRODUCTION_CONFIG = {
    "valves": {
        # Main configuration
        "enabled": True,
        "inject_memories": True,
        "auto_save_responses": True,
        # Optimized limits for production
        "max_memories_to_inject": 5,
        "min_response_length": 15,
        "max_response_length": 2000,
        # Optimized cache
        "enable_cache": True,
        "cache_ttl_minutes": 60,
        "filter_duplicates": True,
        "similarity_threshold": 0.85,
        "enable_memory_commands": True,
        # Automatic cleanup enabled
        "auto_cleanup": True,
        "max_memories_per_user": 100,
        # No debug in production
        "debug_mode": False,
    },
    "user_valves": {
        "show_status": False,  # Fewer notifications in production
        "show_memory_count": False,
        "show_save_confirmation": False,
        "notify_on_error": True,
        "notify_on_cleanup": False,
        "private_mode": False,
    },
}

# -----------------------------------------------------------------------------
# HIGH PRIVACY CONFIGURATION
# -----------------------------------------------------------------------------
PRIVACY_CONFIG = {
    "valves": {
        # Main configuration
        "enabled": True,
        "inject_memories": False,  # Do not inject by default
        "auto_save_responses": False,  # Do not save by default
        # Strict limits
        "max_memories_to_inject": 1,
        "min_response_length": 50,
        "max_response_length": 500,
        # Cache disabled for privacy
        "enable_cache": False,
        "filter_duplicates": True,
        "similarity_threshold": 0.95,  # Very strict
        "enable_memory_commands": True,  # Allow manual control
        # Aggressive automatic cleanup
        "auto_cleanup": True,
        "max_memories_per_user": 20,
        # No debug for privacy
        "debug_mode": False,
    },
    "user_valves": {
        "show_status": True,
        "show_memory_count": True,
        "show_save_confirmation": True,  # Always confirm
        "notify_on_error": True,
        "notify_on_cleanup": True,
        "private_mode": True,  # PRIVATE MODE ENABLED
    },
}

# -----------------------------------------------------------------------------
# ENTERPRISE CONFIGURATION (Balanced and secure)
# -----------------------------------------------------------------------------
ENTERPRISE_CONFIG = {
    "valves": {
        # Main configuration
        "enabled": True,
        "inject_memories": True,
        "auto_save_responses": True,
        # Enterprise limits
        "max_memories_to_inject": 7,
        "min_response_length": 25,
        "max_response_length": 3000,
        # Enterprise cache
        "enable_cache": True,
        "cache_ttl_minutes": 120,
        "filter_duplicates": True,
        "similarity_threshold": 0.8,
        "enable_memory_commands": True,
        # Automatic management
        "auto_cleanup": True,
        "max_memories_per_user": 200,
        # Conditional debug
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
# RECOMMENDED ENVIRONMENT VARIABLES
# =============================================================================

ENVIRONMENT_VARIABLES = {
    # Logging
    "LOG_LEVEL": "INFO",  # DEBUG, INFO, WARNING, ERROR
    "LOG_FORMAT": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    # Cache
    "DEFAULT_CACHE_TTL": "3600",  # 1 hour in seconds
    "MAX_CACHE_SIZE": "128",
    # Global limits
    "GLOBAL_MAX_MEMORIES": "1000",
    "GLOBAL_MAX_RESPONSE_LENGTH": "5000",
    # Security
    "ENABLE_RATE_LIMITING": "true",
    "MAX_REQUESTS_PER_MINUTE": "60",
    # Database (if applicable)
    "DB_POOL_SIZE": "10",
    "DB_TIMEOUT": "30",
}

# =============================================================================
# CONFIGURATION FOR EASYPANEL
# =============================================================================

EASYPANEL_CONFIG = {
    "environment": {
        # EasyPanel specific variables
        "PYTHONPATH": "/app",
        "PYTHONUNBUFFERED": "1",
        # OpenWebUI specific
        "OPENWEBUI_LOG_LEVEL": "INFO",
        "OPENWEBUI_MEMORY_FILTER_ENABLED": "true",
        # Memory configuration
        "MEMORY_CACHE_SIZE": "64",  # MB
        "MEMORY_CACHE_TTL": "1800",  # 30 minutes
        # Network configuration
        "PORT": "8080",
        "HOST": "0.0.0.0",
    },
    "resources": {
        # Recommended resources for VPS
        "memory": "512MB",  # Minimum recommended
        "cpu": "0.5",  # Half core
        "storage": "1GB",  # For logs and cache
    },
    "health_check": {
        "path": "/health",
        "interval": "30s",
        "timeout": "10s",
        "retries": 3,
    },
}

# =============================================================================
# UTILITY FUNCTIONS FOR CONFIGURATION
# =============================================================================


def get_config_by_environment(env_type="basic"):
    """
    Gets configuration according to environment type.

    Args:
        env_type (str): Environment type ('basic', 'development', 'production',
                       'privacy', 'enterprise')

    Returns:
        dict: Corresponding configuration
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
    Validates a configuration before applying it.

    Args:
        config (dict): Configuration to validate

    Returns:
        tuple: (is_valid, errors)
    """
    errors = []

    # Validate main valves
    valves = config.get("valves", {})

    # Validate numerical ranges
    if valves.get("max_memories_to_inject", 0) > 20:
        errors.append("max_memories_to_inject cannot be greater than 20")

    if valves.get("min_response_length", 0) > valves.get("max_response_length", 1000):
        errors.append("min_response_length cannot be greater than max_response_length")

    if not 0 <= valves.get("similarity_threshold", 0.8) <= 1:
        errors.append("similarity_threshold must be between 0.0 and 1.0")

    return len(errors) == 0, errors


def apply_config_to_filter(filter_instance, config):
    """
    Applies a configuration to a filter instance.

    Args:
        filter_instance: Auto Memory Saver filter instance
        config (dict): Configuration to apply
    """
    # Apply main valves
    valves_config = config.get("valves", {})
    for key, value in valves_config.items():
        if hasattr(filter_instance.valves, key):
            setattr(filter_instance.valves, key, value)

    print(f"Configuration applied: {len(valves_config)} valves configured")


# =============================================================================
# USAGE EXAMPLES
# =============================================================================

if __name__ == "__main__":
    # Example 1: Get basic configuration
    basic_config = get_config_by_environment("basic")
    print("Basic configuration:")
    print(f"- Max memories: {basic_config['valves']['max_memories_to_inject']}")
    print(f"- Cache enabled: {basic_config['valves']['enable_cache']}")

    # Example 2: Validate configuration
    is_valid, errors = validate_config(basic_config)
    print(f"\nConfiguration valid: {is_valid}")
    if errors:
        print("Errors found:")
        for error in errors:
            print(f"- {error}")

    # Example 3: Show EasyPanel configuration
    print("\nRecommended configuration for EasyPanel:")
    print(f"- Memory: {EASYPANEL_CONFIG['resources']['memory']}")
    print(f"- CPU: {EASYPANEL_CONFIG['resources']['cpu']}")
    print(f"- Port: {EASYPANEL_CONFIG['environment']['PORT']}")

# =============================================================================
# IMPORTANT NOTES
# =============================================================================

"""
DEPLOYMENT INSTRUCTIONS:

1. For VPS with EasyPanel:
   - Use PRODUCTION_CONFIG as base
   - Configure EASYPANEL_CONFIG environment variables
   - Assign resources according to EASYPANEL_CONFIG['resources']

2. For local development:
   - Use DEVELOPMENT_CONFIG
   - Enable debug_mode for troubleshooting

3. For high privacy environments:
   - Use PRIVACY_CONFIG
   - Consider completely disabling cache

4. Customization:
   - Copy the configuration closest to your needs
   - Adjust specific values
   - Validate with validate_config() before applying

COMMANDS AVAILABLE FOR USERS:

📚 MEMORY MANAGEMENT:
- /memories: List all memories with numbering
- /clear_memories: Delete all user memories
- /memory_count: Show detailed counter with limits
- /memory_search <term>: Search memories by content
- /memory_recent [number]: Last N memories (def: 5, max: 20)
- /memory_export: Export memories in text format

⚙️ CONFIGURATION:
- /memory_config: Show complete configuration
- /private_mode on|off: Enable/disable private mode
- /memory_limit <number>: Set personal limit (0 = unlimited)
- /memory_prefix <text>: Set custom prefix

📊 INFORMATION:
- /memory_help: Complete help with all commands
- /memory_stats: Detailed system statistics
- /memory_status: Current filter status

🔧 UTILITIES:
- /memory_cleanup: Analyze potential duplicates
- /memory_backup: Create backup information

USAGE EXAMPLES:
- /memory_search "artificial intelligence": Search memories about AI
- /memory_recent 3: View last 3 memories
- /memory_limit 50: Set limit of 50 memories
- /private_mode on: Enable private mode temporarily

MONITORING:
- Review logs regularly
- Monitor memory and CPU usage
- Adjust cache_ttl_minutes according to usage patterns
"""
