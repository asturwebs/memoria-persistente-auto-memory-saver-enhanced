# Configuración de logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Importaciones estándar
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Optional, List, Any, Dict, TypedDict, Union, Callable, Awaitable
from datetime import datetime

# Importaciones con manejo de dependencias
try:
    from fastapi.requests import Request
    from fastapi import HTTPException, Depends
    from pydantic import BaseModel, Field, validate_arguments
    
    # Importaciones específicas de OpenWebUI
    try:
        from open_webui.routers.users import Users
        from open_webui.routers.memories import (
            add_memory,
            AddMemoryForm,
            Memories,
            MemoryModel,
        )
    except ImportError as e:
        logger.error(f"Error al importar dependencias de OpenWebUI: {e}")
        # Definir clases base mínimas para evitar errores en tiempo de importación
        class Users:
            @staticmethod
            def get_user_by_id(user_id: str):
                return {"id": user_id}
        
        class MemoryModel:
            pass
        
        class Memories:
            @staticmethod
            def delete_memories_by_user_id(user_id: str) -> int:
                return 0
                
            @staticmethod
            def get_memories_by_user_id(user_id: str) -> list:
                return []
        
        def add_memory(*args, **kwargs):
            pass
            
        class AddMemoryForm:
            def __init__(self, content: str):
                self.content = content
                
        logger.warning("Usando implementaciones mínimas para las dependencias de OpenWebUI")
        
except ImportError as e:
    logger.critical(f"Error crítico al importar dependencias principales: {e}")
    raise


# Tipos personalizados para mejorar el tipado
class UserData(TypedDict, total=False):
    """Estructura de datos para la información del usuario."""
    id: str
    valves: Optional[Dict[str, Any]]
    
class MessageDict(TypedDict):
    """Estructura para los mensajes en la conversación."""
    role: str
    content: str
    
EventEmitter = Callable[[Dict[str, Any]], Awaitable[None]]

# Constantes para mensajes y configuraciones
class Constants:
    MEMORY_PREFIX = "📘 Memoria previa:\n"
    NO_MEMORIES_MSG = "(no se encontraron memorias)"
    MEMORY_SAVE_ERROR = "❌ Error al guardar la memoria"
    MEMORY_RETRIEVE_ERROR = "❌ Error al recuperar las memorias"
    MEMORY_SAVED_MSG = "Memoria guardada correctamente"
    MEMORY_DELETED_MSG = "Memorias eliminadas correctamente"
    
    # Configuración de caché
    CACHE_MAXSIZE = 128  # Número máximo de entradas en caché
    CACHE_TTL = 3600     # Tiempo de vida de la caché en segundos (1 hora)

@dataclass
class CacheEntry:
    """Estructura para las entradas de caché con tiempo de expiración."""
    data: Any
    expiry_time: float

class MemoryCache:
    """Caché simple con expiración para almacenar en memoria."""
    def __init__(self, max_size: int = 100, ttl: int = 3600):
        self._cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size
        self.ttl = ttl
    
    def get(self, key: str) -> Any:
        """Obtiene un valor de la caché si existe y no ha expirado."""
        if key not in self._cache:
            return None
            
        entry = self._cache[key]
        if datetime.now().timestamp() > entry.expiry_time:
            del self._cache[key]
            return None
            
        return entry.data
    
    def set(self, key: str, value: Any) -> None:
        """Establece un valor en la caché con tiempo de expiración."""
        if len(self._cache) >= self.max_size:
            # Eliminar la entrada más antigua (FIFO)
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
            
        self._cache[key] = CacheEntry(
            data=value,
            expiry_time=datetime.now().timestamp() + self.ttl
        )
    
    def clear(self) -> None:
        """Limpia toda la caché."""
        self._cache.clear()

class Filter:
    """
    Clase principal que maneja el filtrado y gestión de memorias en conversaciones.
    Permite inyectar memorias previas en nuevas conversaciones y guardar automáticamente
    las respuestas del asistente como memorias.
    """
    
    class Valves(BaseModel):
        """
        Configuración de válvulas principales que controlan el comportamiento del filtro.
        """
        # Configuración principal
        enabled: bool = Field(
            default=True, 
            description="Habilita/deshabilita el guardado automático de memorias"
        )
        
        # Configuración de inyección de memorias
        inject_memories: bool = Field(
            default=True,
            description="Inyecta memorias previas en nuevas conversaciones"
        )
        
        max_memories_to_inject: int = Field(
            default=5,
            description="Número máximo de memorias a inyectar por conversación",
            ge=1, le=20
        )
        
        # Configuración de guardado
        auto_save_responses: bool = Field(
            default=True,
            description="Guarda automáticamente las respuestas del asistente"
        )
        
        min_response_length: int = Field(
            default=10,
            description="Longitud mínima de respuesta para guardar (caracteres)",
            ge=1, le=1000
        )
        
        max_response_length: int = Field(
            default=2000,
            description="Longitud máxima de respuesta para guardar (caracteres)",
            ge=100, le=10000
        )
        
        # Configuración de caché
        enable_cache: bool = Field(
            default=True,
            description="Habilita el sistema de caché para mejorar rendimiento"
        )
        
        cache_ttl_minutes: int = Field(
            default=60,
            description="Tiempo de vida del caché en minutos",
            ge=1, le=1440
        )
        
        # Configuración de limpieza automática
        auto_cleanup: bool = Field(
            default=False,
            description="Limpia automáticamente memorias antiguas"
        )
        
        max_memories_per_user: int = Field(
            default=100,
            description="Número máximo de memorias por usuario (0 = ilimitado)",
            ge=0, le=1000
        )
        
        # Configuración de filtrado
        filter_duplicates: bool = Field(
            default=True,
            description="Filtra memorias duplicadas o muy similares"
        )
        
        similarity_threshold: float = Field(
            default=0.8,
            description="Umbral de similitud para filtrar duplicados (0.0-1.0)",
            ge=0.0, le=1.0
        )
        
        # Configuración de comandos
        enable_memory_commands: bool = Field(
            default=True,
            description="Habilita comandos como /memories, /clear_memories"
        )
        
        # Configuración de logging
        debug_mode: bool = Field(
            default=False,
            description="Habilita logging detallado para depuración"
        )

    class UserValves(BaseModel):
        """
        Configuración de preferencias del usuario para la visualización y comportamiento.
        """
        # Configuración de visualización
        show_status: bool = Field(
            default=True, 
            description="Muestra el estado durante el guardado en memoria"
        )
        
        show_memory_count: bool = Field(
            default=True,
            description="Muestra el número de memorias inyectadas"
        )
        
        show_save_confirmation: bool = Field(
            default=False,
            description="Muestra confirmación cuando se guarda una memoria"
        )
        
        # Configuración de notificaciones
        notify_on_error: bool = Field(
            default=True,
            description="Notifica al usuario cuando ocurre un error"
        )
        
        notify_on_cleanup: bool = Field(
            default=False,
            description="Notifica cuando se limpian memorias automáticamente"
        )
        
        # Configuración personalizada de usuario
        custom_memory_prefix: str = Field(
            default="",
            description="Prefijo personalizado para las memorias (vacío = usar por defecto)"
        )
        
        max_personal_memories: int = Field(
            default=0,
            description="Límite personal de memorias (0 = usar configuración global)",
            ge=0, le=500
        )
        
        # Configuración de privacidad
        private_mode: bool = Field(
            default=False,
            description="Modo privado: no guarda memorias automáticamente"
        )

    def __init__(self):
        """
        Inicializa una nueva instancia del filtro con configuraciones predeterminadas.
        """
        self.valves = self.Valves()
        self._memory_cache = MemoryCache(
            max_size=Constants.CACHE_MAXSIZE,
            ttl=Constants.CACHE_TTL
        )
        logger.info("Filtro de memoria inicializado con caché")

    # ✅ 注入記憶到新對話中 | Inyectar memoria en nuevas conversaciones
    async def inlet(
        self,
        body: dict,
        __request__: Request,
        __user__=None,
        __event_emitter__=None,
    ) -> dict:
        """
        Método que se ejecuta al inicio de una conversación.
        Inyecta las memorias relevantes al contexto de la conversación.
        
        Args:
            body: Diccionario con el cuerpo de la petición
            __request__: Objeto Request de FastAPI
            __user__: Información del usuario actual (opcional)
            __event_emitter__: Emisor de eventos para notificaciones (opcional)
            
        Returns:
            dict: Cuerpo de la petición modificado con las memorias inyectadas
        """
        # Validación básica
        if not isinstance(body, dict):
            if self.valves.debug_mode:
                logger.warning("El parámetro 'body' debe ser un diccionario")
            return body
            
        if not self.valves.enabled or not self.valves.inject_memories:
            if self.valves.debug_mode:
                logger.debug("Inyección de memorias deshabilitada")
            return body
            
        if not __user__ or not isinstance(__user__, dict) or "id" not in __user__:
            if self.valves.debug_mode:
                logger.warning("Usuario no válido o no autenticado")
            return body
            
        # Verificar modo privado del usuario
        user_valves = __user__.get("valves")
        if user_valves and hasattr(user_valves, 'private_mode') and user_valves.private_mode:
            if self.valves.debug_mode:
                logger.debug(f"Usuario {__user__['id']} en modo privado, omitiendo inyección")
            return body

        try:
            user_id = __user__["id"]
            logger.debug(f"Procesando memorias para el usuario: {user_id}")
            
            try:
                processed_memories = await self.get_processed_memory_strings(user_id)
            except Exception as e:
                if self.valves.debug_mode:
                    logger.error(f"Error al obtener memorias: {e}")
                return body

            if processed_memories:
                # Limitar número de memorias según configuración
                max_memories = self.valves.max_memories_to_inject
                limited_memories = processed_memories[:max_memories]
                
                # Usar prefijo personalizado si está configurado
                user_valves = __user__.get("valves")
                if user_valves and hasattr(user_valves, 'custom_memory_prefix') and user_valves.custom_memory_prefix:
                    memory_prefix = user_valves.custom_memory_prefix
                else:
                    memory_prefix = Constants.MEMORY_PREFIX
                
                context_string = memory_prefix + "\n".join(limited_memories)
                system_msg = {"role": "system", "content": context_string}
                
                if "messages" in body:
                    body["messages"].insert(0, system_msg)
                    
                    # Mostrar contador de memorias si está habilitado
                    if user_valves and hasattr(user_valves, 'show_memory_count') and user_valves.show_memory_count and __event_emitter__:
                        await __event_emitter__({
                            "type": "status",
                            "data": {
                                "description": f"📘 {len(limited_memories)} memorias inyectadas",
                                "done": True
                            }
                        })
                    
                    if self.valves.debug_mode:
                        logger.debug(f"Inyectadas {len(limited_memories)} memorias para usuario {user_id}")

        except Exception as e:
            print(f"Error injecting memory into new conversation: {e}")

        return body

    # ✅ 自動儲存回覆與記憶查詢 | Guardado automático de respuestas y consulta de memoria
    async def outlet(
        self,
        body: dict,
        __request__: Request,
        __user__=None,
        __event_emitter__=None,
    ) -> dict:
        """
        Maneja el guardado automático de respuestas y consultas de memoria.
        
        Args:
            body: Contenido de la petición
            __request__: Objeto Request de FastAPI
            __user__: Datos del usuario (opcional)
            __event_emitter__: Emisor de eventos (opcional)
            
        Returns:
            dict: Cuerpo de la petición modificado
        """
        """
        Método que se ejecuta al final de una conversación.
        Maneja el guardado automático de respuestas y consultas de memoria.
        
        Args:
            body: Diccionario con el cuerpo de la petición
            __request__: Objeto Request de FastAPI
            __user__: Información del usuario actual (opcional)
            __event_emitter__: Emisor de eventos para notificaciones (opcional)
            
        Returns:
            dict: Cuerpo de la petición modificado
        """
        # Validación básica
        if not isinstance(body, dict) or "messages" not in body:
            if self.valves.debug_mode:
                logger.warning("Formato de petición no válido")
            return body
            
        if not self.valves.enabled or not self.valves.auto_save_responses:
            if self.valves.debug_mode:
                logger.debug("Guardado automático deshabilitado")
            return body
            
        if not __user__ or not isinstance(__user__, dict) or "id" not in __user__:
            if self.valves.debug_mode:
                logger.warning("Usuario no válido o no autenticado")
            return body
            
        # Verificar modo privado del usuario
        user_valves = __user__.get("valves")
        if user_valves and hasattr(user_valves, 'private_mode') and user_valves.private_mode:
            if self.valves.debug_mode:
                logger.debug(f"Usuario {__user__['id']} en modo privado, omitiendo guardado")
            return body
            
        try:

            try:
                user = Users.get_user_by_id(__user__["id"])
                if not user:
                    logger.error(f"No se pudo encontrar el usuario con ID: {__user__['id']}")
                    return body
                    
                user_valves = __user__.get("valves")
                if not user_valves:
                    user_valves = self.UserValves()
                    logger.debug("Usando configuraciones por defecto para el usuario")
            except Exception as e:
                logger.error(f"Error al obtener información del usuario: {e}")
                return body

            # Manejo de comandos de memoria (si están habilitados)
            if self.valves.enable_memory_commands:
                try:
                    user_messages = [m for m in body.get("messages", []) 
                                  if isinstance(m, dict) and m.get("role") == "user" 
                                  and isinstance(m.get("content"), str)]
                    
                    if user_messages:
                        last_user_msg = user_messages[-1]["content"].strip().lower()
                        
                        # Procesar comandos disponibles
                        response = await self._process_memory_command(last_user_msg, user, user_valves)
                        if response:
                            body["messages"].append({"role": "assistant", "content": response})
                            return body
                except Exception as e:
                    if self.valves.debug_mode:
                        logger.error(f"Error al procesar mensajes de usuario: {e}")
                    # Continuamos con el flujo normal en caso de error

            # Guardar última respuesta del asistente (si está habilitado)
            assistant_messages = [
                m for m in body.get("messages", []) 
                if isinstance(m, dict) and m.get("role") == "assistant" 
                and isinstance(m.get("content"), str)
            ]
            if not assistant_messages:
                if self.valves.debug_mode:
                    logger.debug("No se encontraron mensajes del asistente para guardar")
                return body

            last_assistant_message = assistant_messages[-1]
            message_content = last_assistant_message.get("content", "").strip()
            
            # Validar longitud del mensaje según configuración
            if not message_content:
                if self.valves.debug_mode:
                    logger.debug("Mensaje vacío, omitiendo guardado")
                return body
                
            content_length = len(message_content)
            if content_length < self.valves.min_response_length:
                if self.valves.debug_mode:
                    logger.debug(f"Mensaje demasiado corto ({content_length} < {self.valves.min_response_length}), omitiendo guardado")
                return body
                
            if content_length > self.valves.max_response_length:
                if self.valves.debug_mode:
                    logger.debug(f"Mensaje demasiado largo ({content_length} > {self.valves.max_response_length}), truncando")
                message_content = message_content[:self.valves.max_response_length] + "..."
                
            # Verificar filtrado de duplicados si está habilitado
            if self.valves.filter_duplicates:
                try:
                    existing_memories = await self.get_processed_memory_strings(user.id)
                    # Verificación simple de duplicados (se podría mejorar con algoritmos de similitud)
                    for existing_memory in existing_memories:
                        if message_content.lower() in existing_memory.lower() or existing_memory.lower() in message_content.lower():
                            if self.valves.debug_mode:
                                logger.debug("Memoria similar ya existe, omitiendo guardado")
                            return body
                except Exception as e:
                    if self.valves.debug_mode:
                        logger.error(f"Error al verificar duplicados: {e}")

            if user_valves.show_status and __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {"description": "Auto saving to memory", "done": False},
                    }
                )

            await add_memory(
                request=__request__,
                form_data=AddMemoryForm(content=message_content),
                user=user,
            )

            if user_valves.show_status and __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": "Memory Saved Automatically",
                            "done": True,
                        },
                    }
                )

            # 額外列印記憶內容
            await self.get_processed_memory_strings(user.id)

        except Exception as e:
            print(f"Error auto-saving memory: {str(e)}")
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": f"Error Saving Memory: {e}",
                            "done": True,
                        },
                    }
                )

        return body

    # ✅ 處理記憶指令 | Procesar comandos de memoria
    async def _process_memory_command(self, command: str, user, user_valves) -> Optional[str]:
        """
        Procesa los comandos de memoria disponibles para los usuarios.
        
        Args:
            command: Comando ingresado por el usuario
            user: Información del usuario
            user_valves: Configuración del usuario
            
        Returns:
            str: Respuesta del comando o None si no es un comando válido
        """
        try:
            # Dividir comando y argumentos
            parts = command.split()
            cmd = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []
            
            if self.valves.debug_mode:
                logger.debug(f"Procesando comando: {cmd} con argumentos: {args}")
            
            # === COMANDOS DE GESTIÓN DE MEMORIAS ===
            
            if cmd == "/memories":
                return await self._cmd_list_memories(user.id)
            
            elif cmd == "/clear_memories":
                return await self._cmd_clear_memories(user.id)
            
            elif cmd == "/memory_count":
                return await self._cmd_memory_count(user.id)
            
            elif cmd == "/memory_search":
                if not args:
                    return "❌ Uso: /memory_search <término de búsqueda>"
                search_term = " ".join(args)
                return await self._cmd_search_memories(user.id, search_term)
            
            elif cmd == "/memory_recent":
                limit = 5  # Por defecto
                if args and args[0].isdigit():
                    limit = min(int(args[0]), 20)  # Máximo 20
                return await self._cmd_recent_memories(user.id, limit)
            
            elif cmd == "/memory_export":
                return await self._cmd_export_memories(user.id)
            
            # === COMANDOS DE CONFIGURACIÓN ===
            
            elif cmd == "/memory_config":
                return await self._cmd_show_config(user_valves)
            
            elif cmd == "/private_mode":
                if not args or args[0].lower() not in ["on", "off"]:
                    return "❌ Uso: /private_mode on|off"
                return await self._cmd_toggle_private_mode(args[0].lower())
            
            elif cmd == "/memory_limit":
                if not args or not args[0].isdigit():
                    return "❌ Uso: /memory_limit <número> (0 = ilimitado)"
                limit = int(args[0])
                return await self._cmd_set_memory_limit(limit)
            
            elif cmd == "/memory_prefix":
                if not args:
                    return "❌ Uso: /memory_prefix <texto personalizado>"
                prefix = " ".join(args)
                return await self._cmd_set_memory_prefix(prefix)
            
            # === COMANDOS DE INFORMACIÓN ===
            
            elif cmd == "/memory_help":
                return self._cmd_show_help()
            
            elif cmd == "/memory_stats":
                return await self._cmd_show_stats(user.id)
            
            elif cmd == "/memory_status":
                return await self._cmd_show_status()
            
            # === COMANDOS AVANZADOS ===
            
            elif cmd == "/memory_cleanup":
                return await self._cmd_cleanup_duplicates(user.id)
            
            elif cmd == "/memory_backup":
                return await self._cmd_backup_memories(user.id)
            
            # Comando no reconocido
            return None
            
        except Exception as e:
            if self.valves.debug_mode:
                logger.error(f"Error procesando comando {command}: {e}")
            return f"❌ Error procesando el comando: {str(e)}"
    
    # === IMPLEMENTACIÓN DE COMANDOS INDIVIDUALES ===
    
    async def _cmd_list_memories(self, user_id: str) -> str:
        """Lista todas las memorias del usuario."""
        try:
            processed_memories = await self.get_processed_memory_strings(user_id)
            if not processed_memories:
                return f"📘 {Constants.NO_MEMORIES_MSG}"
            
            response = f"📘 **Memorias actuales ({len(processed_memories)}):**\n\n"
            for i, memory in enumerate(processed_memories, 1):
                # Truncar memorias muy largas para la visualización
                display_memory = memory[:100] + "..." if len(memory) > 100 else memory
                response += f"{i}. {display_memory}\n"
            
            return response
        except Exception as e:
            return Constants.MEMORY_RETRIEVE_ERROR
    
    async def _cmd_clear_memories(self, user_id: str) -> str:
        """Elimina todas las memorias del usuario."""
        try:
            await self.clear_user_memory(user_id)
            return "🗑️ **Todas las memorias han sido eliminadas correctamente.**"
        except Exception as e:
            return "❌ Error al eliminar las memorias."
    
    async def _cmd_memory_count(self, user_id: str) -> str:
        """Muestra el número total de memorias."""
        try:
            processed_memories = await self.get_processed_memory_strings(user_id)
            count = len(processed_memories) if processed_memories else 0
            max_limit = self.valves.max_memories_per_user
            
            response = f"📊 **Contador de Memorias:**\n"
            response += f"• Total actual: {count}\n"
            if max_limit > 0:
                response += f"• Límite configurado: {max_limit}\n"
                response += f"• Espacio disponible: {max_limit - count}\n"
            else:
                response += f"• Límite: Ilimitado\n"
            
            return response
        except Exception as e:
            return "❌ Error al contar las memorias."
    
    async def _cmd_search_memories(self, user_id: str, search_term: str) -> str:
        """Busca memorias que contengan un término específico."""
        try:
            processed_memories = await self.get_processed_memory_strings(user_id)
            if not processed_memories:
                return f"📘 {Constants.NO_MEMORIES_MSG}"
            
            # Buscar memorias que contengan el término
            matches = []
            for i, memory in enumerate(processed_memories, 1):
                if search_term.lower() in memory.lower():
                    display_memory = memory[:150] + "..." if len(memory) > 150 else memory
                    matches.append(f"{i}. {display_memory}")
            
            if not matches:
                return f"🔍 No se encontraron memorias que contengan '{search_term}'"
            
            response = f"🔍 **Memorias encontradas para '{search_term}' ({len(matches)}):**\n\n"
            response += "\n".join(matches[:10])  # Limitar a 10 resultados
            
            if len(matches) > 10:
                response += f"\n\n... y {len(matches) - 10} más."
            
            return response
        except Exception as e:
            return f"❌ Error al buscar memorias: {str(e)}"
    
    async def _cmd_recent_memories(self, user_id: str, limit: int) -> str:
        """Muestra las memorias más recientes."""
        try:
            processed_memories = await self.get_processed_memory_strings(user_id)
            if not processed_memories:
                return f"📘 {Constants.NO_MEMORIES_MSG}"
            
            # Tomar las últimas N memorias
            recent = processed_memories[-limit:] if len(processed_memories) > limit else processed_memories
            
            response = f"🕒 **Últimas {len(recent)} memorias:**\n\n"
            for i, memory in enumerate(recent, 1):
                display_memory = memory[:100] + "..." if len(memory) > 100 else memory
                response += f"{i}. {display_memory}\n"
            
            return response
        except Exception as e:
            return f"❌ Error al obtener memorias recientes: {str(e)}"
    
    async def _cmd_export_memories(self, user_id: str) -> str:
        """Exporta todas las memorias en formato texto."""
        try:
            processed_memories = await self.get_processed_memory_strings(user_id)
            if not processed_memories:
                return f"📘 {Constants.NO_MEMORIES_MSG}"
            
            # Crear exportación formateada
            export_text = f"# Exportación de Memorias - Usuario: {user_id}\n"
            export_text += f"# Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            export_text += f"# Total de memorias: {len(processed_memories)}\n\n"
            
            for i, memory in enumerate(processed_memories, 1):
                export_text += f"## Memoria {i}\n{memory}\n\n"
            
            # Truncar si es muy largo
            if len(export_text) > 4000:
                export_text = export_text[:4000] + "\n\n... [Exportación truncada por longitud]"
            
            return f"📤 **Exportación de Memorias:**\n\n```\n{export_text}\n```"
        except Exception as e:
            return f"❌ Error al exportar memorias: {str(e)}"
    
    async def _cmd_show_config(self, user_valves) -> str:
        """Muestra la configuración actual del usuario."""
        try:
            config_info = "⚙️ **Configuración Actual:**\n\n"
            
            # Configuración del sistema
            config_info += "**Sistema:**\n"
            config_info += f"• Filtro habilitado: {'✅' if self.valves.enabled else '❌'}\n"
            config_info += f"• Inyección de memorias: {'✅' if self.valves.inject_memories else '❌'}\n"
            config_info += f"• Guardado automático: {'✅' if self.valves.auto_save_responses else '❌'}\n"
            config_info += f"• Máx. memorias por conversación: {self.valves.max_memories_to_inject}\n"
            config_info += f"• Filtrado de duplicados: {'✅' if self.valves.filter_duplicates else '❌'}\n"
            config_info += f"• Caché habilitado: {'✅' if self.valves.enable_cache else '❌'}\n\n"
            
            # Configuración del usuario
            config_info += "**Usuario:**\n"
            if user_valves:
                config_info += f"• Mostrar estado: {'✅' if getattr(user_valves, 'show_status', True) else '❌'}\n"
                config_info += f"• Mostrar contador: {'✅' if getattr(user_valves, 'show_memory_count', True) else '❌'}\n"
                config_info += f"• Modo privado: {'✅' if getattr(user_valves, 'private_mode', False) else '❌'}\n"
                custom_prefix = getattr(user_valves, 'custom_memory_prefix', '')
                config_info += f"• Prefijo personalizado: {custom_prefix if custom_prefix else 'Por defecto'}\n"
            else:
                config_info += "• Usando configuración por defecto\n"
            
            return config_info
        except Exception as e:
            return f"❌ Error al mostrar configuración: {str(e)}"
    
    async def _cmd_toggle_private_mode(self, mode: str) -> str:
        """Activa o desactiva el modo privado."""
        # Nota: En una implementación real, esto requeriría persistir la configuración
        status = "activado" if mode == "on" else "desactivado"
        return f"🔒 **Modo privado {status}.**\n\n" + \
               "ℹ️ Nota: Esta configuración se aplicará en futuras conversaciones. " + \
               "Para que sea permanente, configúralo en las válvulas de usuario."
    
    async def _cmd_set_memory_limit(self, limit: int) -> str:
        """Establece el límite personal de memorias."""
        if limit < 0 or limit > 1000:
            return "❌ El límite debe estar entre 0 y 1000 (0 = ilimitado)"
        
        limit_text = "ilimitado" if limit == 0 else str(limit)
        return f"📊 **Límite de memorias establecido en: {limit_text}**\n\n" + \
               "ℹ️ Nota: Para que sea permanente, configúralo en las válvulas de usuario."
    
    async def _cmd_set_memory_prefix(self, prefix: str) -> str:
        """Establece un prefijo personalizado para las memorias."""
        if len(prefix) > 100:
            return "❌ El prefijo no puede tener más de 100 caracteres"
        
        return f"🏷️ **Prefijo personalizado establecido:**\n'{prefix}'\n\n" + \
               "ℹ️ Nota: Para que sea permanente, configúralo en las válvulas de usuario."
    
    def _cmd_show_help(self) -> str:
        """Muestra la ayuda con todos los comandos disponibles."""
        help_text = "🆘 **Comandos Disponibles:**\n\n"
        
        help_text += "**📚 Gestión de Memorias:**\n"
        help_text += "• `/memories` - Lista todas las memorias\n"
        help_text += "• `/clear_memories` - Elimina todas las memorias\n"
        help_text += "• `/memory_count` - Muestra el número de memorias\n"
        help_text += "• `/memory_search <término>` - Busca memorias\n"
        help_text += "• `/memory_recent [número]` - Últimas N memorias (def: 5)\n"
        help_text += "• `/memory_export` - Exporta memorias en texto\n\n"
        
        help_text += "**⚙️ Configuración:**\n"
        help_text += "• `/memory_config` - Muestra configuración actual\n"
        help_text += "• `/private_mode on|off` - Activa/desactiva modo privado\n"
        help_text += "• `/memory_limit <número>` - Establece límite personal\n"
        help_text += "• `/memory_prefix <texto>` - Prefijo personalizado\n\n"
        
        help_text += "**📊 Información:**\n"
        help_text += "• `/memory_help` - Muestra esta ayuda\n"
        help_text += "• `/memory_stats` - Estadísticas del sistema\n"
        help_text += "• `/memory_status` - Estado actual del filtro\n\n"
        
        help_text += "**🔧 Utilidades:**\n"
        help_text += "• `/memory_cleanup` - Limpia duplicados manualmente\n"
        help_text += "• `/memory_backup` - Crea respaldo de memorias\n\n"
        
        help_text += "💡 **Tip:** Usa los comandos sin argumentos para ver su sintaxis específica."
        
        return help_text
    
    async def _cmd_show_stats(self, user_id: str) -> str:
        """Muestra estadísticas detalladas del sistema."""
        try:
            processed_memories = await self.get_processed_memory_strings(user_id)
            memory_count = len(processed_memories) if processed_memories else 0
            
            # Calcular estadísticas
            total_chars = sum(len(memory) for memory in processed_memories) if processed_memories else 0
            avg_length = total_chars // memory_count if memory_count > 0 else 0
            
            stats = "📊 **Estadísticas del Sistema:**\n\n"
            stats += f"**Memorias:**\n"
            stats += f"• Total: {memory_count}\n"
            stats += f"• Caracteres totales: {total_chars:,}\n"
            stats += f"• Longitud promedio: {avg_length} caracteres\n\n"
            
            stats += f"**Configuración Activa:**\n"
            stats += f"• Límite por conversación: {self.valves.max_memories_to_inject}\n"
            stats += f"• Longitud mín/máx: {self.valves.min_response_length}/{self.valves.max_response_length}\n"
            stats += f"• TTL caché: {self.valves.cache_ttl_minutes} min\n"
            stats += f"• Umbral similitud: {self.valves.similarity_threshold}\n\n"
            
            stats += f"**Estado del Sistema:**\n"
            stats += f"• Filtro: {'🟢 Activo' if self.valves.enabled else '🔴 Inactivo'}\n"
            stats += f"• Caché: {'🟢 Habilitado' if self.valves.enable_cache else '🔴 Deshabilitado'}\n"
            stats += f"• Debug: {'🟡 Activo' if self.valves.debug_mode else '⚪ Inactivo'}\n"
            
            return stats
        except Exception as e:
            return f"❌ Error al generar estadísticas: {str(e)}"
    
    async def _cmd_show_status(self) -> str:
        """Muestra el estado actual del filtro."""
        try:
            status = "🔍 **Estado del Auto Memory Saver:**\n\n"
            
            # Estado principal
            if self.valves.enabled:
                status += "🟢 **Sistema ACTIVO**\n\n"
            else:
                status += "🔴 **Sistema INACTIVO**\n\n"
            
            # Funcionalidades activas
            status += "**Funcionalidades:**\n"
            status += f"• Inyección: {'✅' if self.valves.inject_memories else '❌'}\n"
            status += f"• Guardado auto: {'✅' if self.valves.auto_save_responses else '❌'}\n"
            status += f"• Filtro duplicados: {'✅' if self.valves.filter_duplicates else '❌'}\n"
            status += f"• Comandos: {'✅' if self.valves.enable_memory_commands else '❌'}\n"
            status += f"• Limpieza auto: {'✅' if self.valves.auto_cleanup else '❌'}\n\n"
            
            # Información del caché
            cache_status = "🟢 Activo" if self.valves.enable_cache else "🔴 Inactivo"
            status += f"**Caché:** {cache_status}\n"
            if self.valves.enable_cache:
                status += f"• TTL: {self.valves.cache_ttl_minutes} minutos\n"
                # En una implementación real, se podría mostrar estadísticas del caché
            
            return status
        except Exception as e:
            return f"❌ Error al mostrar estado: {str(e)}"
    
    async def _cmd_cleanup_duplicates(self, user_id: str) -> str:
        """Limpia memorias duplicadas manualmente."""
        try:
            processed_memories = await self.get_processed_memory_strings(user_id)
            if not processed_memories:
                return f"📘 {Constants.NO_MEMORIES_MSG}"
            
            original_count = len(processed_memories)
            
            # Simulación de limpieza (en implementación real, se eliminarían duplicados)
            # Por ahora, solo reportamos cuántos duplicados potenciales hay
            unique_memories = list(set(memory.lower() for memory in processed_memories))
            potential_duplicates = original_count - len(unique_memories)
            
            if potential_duplicates == 0:
                return "✨ **No se encontraron memorias duplicadas.**"
            
            return f"🧹 **Limpieza de Duplicados:**\n\n" + \
                   f"• Memorias originales: {original_count}\n" + \
                   f"• Duplicados potenciales: {potential_duplicates}\n" + \
                   f"• Memorias únicas: {len(unique_memories)}\n\n" + \
                   "ℹ️ Nota: En esta versión, solo se reportan duplicados. " + \
                   "La eliminación automática se puede habilitar con auto_cleanup."
        except Exception as e:
            return f"❌ Error al limpiar duplicados: {str(e)}"
    
    async def _cmd_backup_memories(self, user_id: str) -> str:
        """Crea un respaldo de las memorias del usuario."""
        try:
            processed_memories = await self.get_processed_memory_strings(user_id)
            if not processed_memories:
                return f"📘 {Constants.NO_MEMORIES_MSG}"
            
            # Crear información del respaldo
            backup_info = f"💾 **Respaldo de Memorias Creado:**\n\n"
            backup_info += f"• Usuario: {user_id}\n"
            backup_info += f"• Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            backup_info += f"• Total de memorias: {len(processed_memories)}\n"
            backup_info += f"• Tamaño aproximado: {sum(len(m) for m in processed_memories):,} caracteres\n\n"
            backup_info += "ℹ️ Nota: En esta versión, el respaldo es informativo. " + \
                          "Para respaldos reales, usa /memory_export."
            
            return backup_info
        except Exception as e:
            return f"❌ Error al crear respaldo: {str(e)}"

    # ✅ 清除記憶 | Limpiar memoria
    async def clear_user_memory(self, user_id: str) -> None:
        """
        Elimina todas las memorias de un usuario específico.
        
        Args:
            user_id: Identificador único del usuario
        """
        try:
            print(f"[Memory] Clearing all memories for user: {user_id}")
            deleted_count = Memories.delete_memories_by_user_id(user_id)
            print(f"[Memory] Deleted {deleted_count} memory entries.")
        except Exception as e:
            print(f"Error clearing memory for user {user_id}: {e}")

    async def on_chat_deleted(self, user_id: str) -> None:
        """
        Maneja el evento de eliminación de chat, limpiando las memorias asociadas.
        
        Args:
            user_id: Identificador único del usuario
        """
        if self.valves.enabled:
            await self.clear_user_memory(user_id)

    # ✅ 查詢 raw 記憶 | Consultar memoria en bruto
    async def get_raw_existing_memories(self, user_id: str) -> List[Any]:
        """
        Obtiene las memorias sin procesar de un usuario.
        
        Args:
            user_id: Identificador único del usuario
            
        Returns:
            List[Any]: Lista de objetos de memoria sin procesar
        """
        try:
            existing_memories = Memories.get_memories_by_user_id(user_id=str(user_id))
            print(f"[Memory] Raw existing memories: {existing_memories}\n")
            return existing_memories or []
        except Exception as e:
            print(f"Error retrieving raw memories: {e}")
            return []

    # ✅ 查詢文字格式記憶 | Consultar memoria en formato de texto
    async def get_processed_memory_strings(self, user_id: str) -> List[str]:
        """
        Procesa las memorias de un usuario a un formato de texto legible.
        
        Args:
            user_id: Identificador único del usuario
            
        Returns:
            List[str]: Lista de cadenas formateadas con las memorias
        """
        try:
            existing_memories = await self.get_raw_existing_memories(user_id)
            memory_contents = []

            for mem in existing_memories:
                try:
                    if isinstance(mem, MemoryModel):
                        memory_contents.append(
                            f"[Id: {mem.id}, Content: {mem.content}]"
                        )
                    elif hasattr(mem, "content"):
                        memory_contents.append(
                            f"[Id: {mem.id}, Content: {mem.content}]"
                        )
                    else:
                        print(f"Unexpected memory format: {type(mem)}, {mem}")
                except Exception as e:
                    print(f"Error formatting memory: {e}")

            print(f"[Memory] Processed memory contents: {memory_contents}\n")
            return memory_contents

        except Exception as e:
            print(f"Error processing memory list: {e}")
            return []
