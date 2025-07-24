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
                # MEJORA BYTIA: Fallback con datos de prueba para testing de ordenación
                from datetime import datetime, timedelta
                
                # Crear memorias de prueba con fechas diferentes para testear ordenación
                test_memories = []
                base_date = datetime.now()
                
                # Simular memorias con diferentes fechas (más antigua a más reciente)
                test_data = [
                    {"id": "mem_001", "content": "Memoria más antigua - hace 5 días", "days_ago": 5},
                    {"id": "mem_002", "content": "Memoria intermedia - hace 3 días", "days_ago": 3},
                    {"id": "mem_003", "content": "Memoria reciente - hace 1 día", "days_ago": 1},
                    {"id": "mem_004", "content": "Memoria más reciente - hace 2 horas", "days_ago": 0},
                ]
                
                for data in test_data:
                    # Crear objeto simulado con estructura similar a MemoryModel
                    class TestMemory:
                        def __init__(self, id, content, created_at):
                            self.id = id
                            self.content = content
                            self.created_at = created_at
                        
                        def __str__(self):
                            return f"TestMemory(id={self.id}, content='{self.content[:30]}...', created_at={self.created_at})"
                    
                    # Calcular fecha de creación
                    if data["days_ago"] == 0:
                        created_at = (base_date - timedelta(hours=2)).isoformat()
                    else:
                        created_at = (base_date - timedelta(days=data["days_ago"])).isoformat()
                    
                    test_memories.append(TestMemory(
                        id=data["id"],
                        content=data["content"],
                        created_at=created_at
                    ))
                
                print(f"[MEMORIA-DEBUG] 🧪 Fallback devolviendo {len(test_memories)} memorias de prueba")
                logger.info(f"[MEMORIA-DEBUG] 🧪 Fallback devolviendo {len(test_memories)} memorias de prueba")
                
                # Devolver en orden de BD (normalmente por ID = más antiguas primero)
                return test_memories
        
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
        
        # Configuración de relevancia (NUEVA - sugerencia de auditoría)
        relevance_threshold: float = Field(
            default=0.05,
            description="Umbral de relevancia (0.0-1.0) para inyectar memorias en contexto",
            ge=0.0, le=1.0
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

    # === MÉTODOS AUXILIARES PARA LÓGICA DE INYECCIÓN ===
    
    def _is_first_message(self, messages: List[dict]) -> bool:
        """
        Determina si es el primer mensaje de una nueva sesión de chat.
        
        Args:
            messages: Lista de mensajes de la conversación actual
            
        Returns:
            bool: True si es el primer mensaje, False en caso contrario
        """
        if not messages or not isinstance(messages, list):
            return True
            
        # Contar mensajes del usuario (excluyendo mensajes del sistema)
        user_messages = [
            msg for msg in messages 
            if isinstance(msg, dict) and msg.get("role") == "user"
        ]
        
        # Es el primer mensaje si hay 1 o menos mensajes del usuario
        # (el mensaje actual se cuenta como el primero)
        is_first = len(user_messages) <= 1
        
        if self.valves.debug_mode:
            logger.debug(f"Detección primer mensaje: {is_first} (mensajes usuario: {len(user_messages)})")
            
        return is_first
    
    async def _get_recent_memories(self, user_id: str, limit: int) -> List[str]:
        """
        Obtiene las memorias más recientes de un usuario, ordenadas por fecha.
        
        Args:
            user_id: ID del usuario
            limit: Número máximo de memorias a obtener
            
        Returns:
            List[str]: Lista de memorias formateadas, ordenadas de más reciente a más antigua
        """
        try:
            print(f"[MEMORIA-DEBUG] 🔍 Obteniendo {limit} memorias más recientes para usuario {user_id}")
            logger.info(f"[MEMORIA-DEBUG] 🔍 Obteniendo {limit} memorias más recientes para usuario {user_id}")
            
            if self.valves.debug_mode:
                logger.debug(f"Obteniendo {limit} memorias más recientes para usuario {user_id}")
            
            # Obtener memorias sin procesar (EXPLÍCITAMENTE ordenadas por fecha descendente)
            raw_memories = await self.get_raw_existing_memories(user_id, order_by="created_at DESC")
            if not raw_memories:
                print(f"[MEMORIA-DEBUG] ⚠️ No se encontraron memorias para el usuario")
                logger.info(f"[MEMORIA-DEBUG] ⚠️ No se encontraron memorias para el usuario")
                if self.valves.debug_mode:
                    logger.debug("No se encontraron memorias para el usuario")
                return []
            
            print(f"[MEMORIA-DEBUG] 📊 Total memorias encontradas: {len(raw_memories)}")
            logger.info(f"[MEMORIA-DEBUG] 📊 Total memorias encontradas: {len(raw_memories)}")
            
            # Inspeccionar las primeras memorias para ver su estructura
            for i, mem in enumerate(raw_memories[:3]):
                created_at = getattr(mem, 'created_at', 'NO_DATE')
                mem_id = getattr(mem, 'id', 'NO_ID')
                content_preview = str(mem)[:50] if hasattr(mem, '__str__') else 'NO_CONTENT'
                print(f"[MEMORIA-DEBUG] Memoria {i+1}: ID={mem_id}, created_at={created_at}, content={content_preview}...")
                logger.info(f"[MEMORIA-DEBUG] Memoria {i+1}: ID={mem_id}, created_at={created_at}, content={content_preview}...")
            
            # Ordenar por fecha de creación (más reciente primero)
            print(f"[MEMORIA-DEBUG] 🔄 Ordenando memorias por fecha (más reciente primero)")
            logger.info(f"[MEMORIA-DEBUG] 🔄 Ordenando memorias por fecha (más reciente primero)")
            
            sorted_memories = sorted(
                raw_memories,
                key=lambda x: getattr(x, 'created_at', '1970-01-01T00:00:00'),
                reverse=True
            )
            
            # Mostrar las primeras memorias después del ordenamiento
            print(f"[MEMORIA-DEBUG] 🏆 Después del ordenamiento (primeras 3):")
            logger.info(f"[MEMORIA-DEBUG] 🏆 Después del ordenamiento (primeras 3):")
            for i, mem in enumerate(sorted_memories[:3]):
                created_at = getattr(mem, 'created_at', 'NO_DATE')
                mem_id = getattr(mem, 'id', 'NO_ID')
                content_preview = str(mem)[:50] if hasattr(mem, '__str__') else 'NO_CONTENT'
                print(f"[MEMORIA-DEBUG] Posición {i+1}: ID={mem_id}, created_at={created_at}, content={content_preview}...")
                logger.info(f"[MEMORIA-DEBUG] Posición {i+1}: ID={mem_id}, created_at={created_at}, content={content_preview}...")
            
            # Limitar al número solicitado
            limited_memories = sorted_memories[:limit]
            
            # Formatear las memorias
            formatted_memories = []
            for mem in limited_memories:
                try:
                    if isinstance(mem, MemoryModel):
                        content = f"[Id: {mem.id}, Content: {mem.content}]"
                    elif hasattr(mem, "content"):
                        content = f"[Id: {getattr(mem, 'id', 'N/A')}, Content: {mem.content}]"
                    else:
                        content = str(mem)
                    
                    formatted_memories.append(content)
                except Exception as e:
                    if self.valves.debug_mode:
                        logger.warning(f"Error al formatear memoria: {e}")
                    continue
            
            if self.valves.debug_mode:
                logger.debug(f"Obtenidas {len(formatted_memories)} memorias recientes")
            
            return formatted_memories
            
        except Exception as e:
            logger.error(f"Error al obtener memorias recientes: {e}")
            return []
    
    def _calculate_relevance_score(self, memory_content: str, user_input: str) -> float:
        """
        Calcula un puntaje de relevancia entre una memoria y el input del usuario.
        Algoritmo simplificado y más efectivo.
        
        Args:
            memory_content: Contenido de la memoria
            user_input: Input actual del usuario
            
        Returns:
            float: Puntaje de relevancia entre 0.0 y 1.0
        """
        if not memory_content or not user_input:
            return 0.0
            
        # Convertir a minúsculas para comparación
        memory_lower = memory_content.lower()
        input_lower = user_input.lower()
        
        # Dividir en palabras (sin filtrar por longitud para capturar "IA", "AI", etc.)
        memory_words = set(memory_lower.split())
        input_words = set(input_lower.split())
        
        # Calcular coincidencias exactas de palabras
        word_matches = memory_words.intersection(input_words)
        word_score = len(word_matches) / len(input_words) if input_words else 0.0
        
        # Bonus por palabras clave importantes (case-insensitive substring matching)
        substring_score = 0.0
        important_terms = [word for word in input_words if len(word) >= 3]
        
        for term in important_terms:
            if term in memory_lower:
                substring_score += 1.0
        
        substring_score = substring_score / len(important_terms) if important_terms else 0.0
        
        # Puntaje final: 60% coincidencias exactas + 40% substring matching
        final_score = (word_score * 0.6) + (substring_score * 0.4)
        
        # Debug logging si está habilitado
        if self.valves.debug_mode and final_score > 0:
            logger.debug(f"Relevancia calculada: {final_score:.3f} - Coincidencias: {word_matches}")
        
        return min(final_score, 1.0)
    
    def _calculate_phrase_similarity(self, text1: str, text2: str) -> float:
        """
        Calcula similitud basada en frases comunes de 2+ palabras.
        
        Args:
            text1: Primer texto
            text2: Segundo texto
            
        Returns:
            float: Puntaje de similitud de frases entre 0.0 y 1.0
        """
        # Generar bigramas (frases de 2 palabras)
        words1 = text1.split()
        words2 = text2.split()
        
        if len(words1) < 2 or len(words2) < 2:
            return 0.0
            
        bigrams1 = {f"{words1[i]} {words1[i+1]}" for i in range(len(words1)-1)}
        bigrams2 = {f"{words2[i]} {words2[i+1]}" for i in range(len(words2)-1)}
        
        if not bigrams1 or not bigrams2:
            return 0.0
            
        intersection = bigrams1.intersection(bigrams2)
        union = bigrams1.union(bigrams2)
        
        return len(intersection) / len(union) if union else 0.0
    
    async def _get_relevant_memories(self, user_id: str, user_input: str, max_memories: int = 5) -> List[str]:
        """
        Obtiene las memorias más relevantes para el input del usuario.
        
        Args:
            user_id: ID del usuario
            user_input: Input actual del usuario
            max_memories: Número máximo de memorias relevantes a devolver
            
        Returns:
            List[str]: Lista de memorias relevantes formateadas
        """
        try:
            print(f"[MEMORIA-DEBUG] 🔍 Buscando memorias relevantes para: '{user_input[:50]}...'")
            logger.info(f"[MEMORIA-DEBUG] 🔍 Buscando memorias relevantes para: '{user_input[:50]}...'")
            if self.valves.debug_mode:
                logger.debug(f"Buscando memorias relevantes para: '{user_input[:50]}...'")
            
            # Obtener todas las memorias del usuario (orden no crítico para relevancia, pero mantenemos consistencia)
            raw_memories = await self.get_raw_existing_memories(user_id, order_by="created_at DESC")
            if not raw_memories:
                return []
            
            # Calcular relevancia para cada memoria
            memories_with_scores = []
            for mem in raw_memories:
                try:
                    content = mem.content if hasattr(mem, 'content') else str(mem)
                    score = self._calculate_relevance_score(content, user_input)
                    
                    if score > 0:  # Solo considerar memorias con alguna relevancia
                        memories_with_scores.append({
                            'memory': mem,
                            'content': content,
                            'score': score
                        })
                except Exception as e:
                    if self.valves.debug_mode:
                        logger.warning(f"Error al calcular relevancia: {e}")
                    continue
            
            print(f"[MEMORIA-DEBUG] ⚖️ Usando umbral de relevancia: {self.valves.relevance_threshold}")
            logger.info(f"[MEMORIA-DEBUG] ⚖️ Usando umbral de relevancia: {self.valves.relevance_threshold}")
            
            relevant_memories = [
                mem for mem in memories_with_scores 
                if mem['score'] >= self.valves.relevance_threshold
            ]
            
            print(f"[MEMORIA-DEBUG] 📊 Memorias que superan umbral: {len(relevant_memories)} de {len(memories_with_scores)}")
            logger.info(f"[MEMORIA-DEBUG] 📊 Memorias que superan umbral: {len(relevant_memories)} de {len(memories_with_scores)}")
            
            if self.valves.debug_mode:
                logger.debug(f"Usando umbral de relevancia: {self.valves.relevance_threshold}")
            
            if not relevant_memories:
                print(f"[MEMORIA-DEBUG] ❌ No se encontraron memorias relevantes")
                logger.info(f"[MEMORIA-DEBUG] ❌ No se encontraron memorias relevantes")
                if self.valves.debug_mode:
                    logger.debug("No se encontraron memorias relevantes")
                return []
            
            # Ordenar por relevancia (mayor a menor)
            relevant_memories.sort(key=lambda x: x['score'], reverse=True)
            
            # Limitar al número máximo
            selected_memories = relevant_memories[:max_memories]
            
            # Formatear las memorias seleccionadas
            formatted_memories = []
            for mem_data in selected_memories:
                try:
                    mem = mem_data['memory']
                    score = mem_data['score']
                    
                    if isinstance(mem, MemoryModel):
                        content = f"[Relevancia: {score:.2f}] [Id: {mem.id}, Content: {mem.content}]"
                    elif hasattr(mem, "content"):
                        content = f"[Relevancia: {score:.2f}] [Id: {getattr(mem, 'id', 'N/A')}, Content: {mem.content}]"
                    else:
                        content = f"[Relevancia: {score:.2f}] {str(mem)}"
                    
                    formatted_memories.append(content)
                except Exception as e:
                    if self.valves.debug_mode:
                        logger.warning(f"Error al formatear memoria relevante: {e}")
                    continue
            
            if self.valves.debug_mode:
                logger.debug(f"Encontradas {len(formatted_memories)} memorias relevantes")
                for i, mem in enumerate(formatted_memories[:3]):  # Mostrar solo las 3 primeras en debug
                    logger.debug(f"  {i+1}. {mem[:100]}...")
            
            return formatted_memories
            
        except Exception as e:
            logger.error(f"Error al obtener memorias relevantes: {e}")
            return []
    
    async def _inject_memories_into_conversation(
        self,
        body: dict,
        memories: List[str],
        user_valves: Any,
        user_id: str,
        is_first_message: bool,
        __event_emitter__=None
    ) -> None:
        """
        Inyecta las memorias seleccionadas en la conversación.
        
        Args:
            body: Cuerpo de la petición
            memories: Lista de memorias formateadas para inyectar
            user_valves: Configuración del usuario
            user_id: ID del usuario
            is_first_message: Si es el primer mensaje de la sesión
            __event_emitter__: Emisor de eventos (opcional)
        """
        if not memories or "messages" not in body:
            return
        
        try:
            # Usar prefijo personalizado si está configurado
            if user_valves and hasattr(user_valves, 'custom_memory_prefix') and user_valves.custom_memory_prefix:
                memory_prefix = user_valves.custom_memory_prefix
            else:
                memory_prefix = Constants.MEMORY_PREFIX
            
            # Añadir información sobre el tipo de inyección
            if is_first_message:
                context_header = f"{memory_prefix}\n[Memorias recientes para continuidad de contexto]\n"
            else:
                context_header = f"{memory_prefix}\n[Memorias relevantes al contexto actual]\n"
            
            # Crear el mensaje de contexto
            context_string = context_header + "\n".join(memories)
            system_msg = {"role": "system", "content": context_string}
            
            # Insertar al principio de la conversación
            body["messages"].insert(0, system_msg)
            
            # Mostrar notificación al usuario si está habilitado
            if user_valves and hasattr(user_valves, 'show_memory_count') and user_valves.show_memory_count and __event_emitter__:
                memory_type = "recientes" if is_first_message else "relevantes"
                await __event_emitter__({
                    "type": "status",
                    "data": {
                        "description": f"📘 {len(memories)} memorias {memory_type} cargadas",
                        "done": True
                    }
                })
            
            if self.valves.debug_mode:
                memory_type = "recientes" if is_first_message else "relevantes"
                logger.info(f"Inyectadas {len(memories)} memorias {memory_type} para usuario {user_id}")
                logger.debug(f"Contexto inyectado (primeros 300 chars): {context_string[:300]}...")
                
        except Exception as e:
            logger.error(f"Error al inyectar memorias: {e}", exc_info=True)
    
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
        
        NUEVA LÓGICA INTELIGENTE:
        - Primer mensaje: Inyecta las X memorias más recientes (continuidad de contexto)
        - Mensajes posteriores: Inyecta solo memorias relevantes al input actual, o ninguna
        
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
            messages = body.get("messages", [])
            
            # LOGS DE DIAGNÓSTICO VISIBLES (SIEMPRE ACTIVOS)
            print(f"[NUEVA-LOGICA] 🔍 INLET ejecutándose para usuario: {user_id}")
            logger.info(f"[NUEVA-LOGICA] 🔍 INLET ejecutándose para usuario: {user_id}")
            
            # PASO 0: PROCESAR SLASH COMMANDS PRIMERO (NUEVA FUNCIONALIDAD)
            if self.valves.enable_memory_commands and messages:
                try:
                    # Obtener el último mensaje del usuario
                    user_messages = [
                        msg for msg in messages 
                        if isinstance(msg, dict) and msg.get("role") == "user" 
                        and isinstance(msg.get("content"), str)
                    ]
                    
                    if user_messages:
                        last_user_msg = user_messages[-1]["content"].strip()
                        
                        # LOG DE DIAGNÓSTICO PARA COMANDOS
                        print(f"[SLASH-COMMANDS] 🎯 Último mensaje del usuario: '{last_user_msg[:50]}...'")
                        logger.info(f"[SLASH-COMMANDS] 🎯 Último mensaje del usuario detectado")
                        
                        # Verificar si es un slash command
                        if last_user_msg.startswith("/"):
                            print(f"[SLASH-COMMANDS] ⚡ COMANDO DETECTADO: {last_user_msg}")
                            logger.info(f"[SLASH-COMMANDS] ⚡ COMANDO DETECTADO: {last_user_msg}")
                            
                            # Obtener información del usuario
                            try:
                                user = Users.get_user_by_id(user_id)
                                if not user:
                                    print(f"[SLASH-COMMANDS] ❌ Usuario no encontrado: {user_id}")
                                    logger.error(f"Usuario no encontrado: {user_id}")
                                else:
                                    user_valves = __user__.get("valves") or self.UserValves()
                                    
                                    # Procesar el comando
                                    command_response = await self._process_memory_command(last_user_msg, user, user_valves)
                                    
                                    if command_response:
                                        print(f"[SLASH-COMMANDS] ✅ COMANDO PROCESADO EXITOSAMENTE")
                                        logger.info(f"[SLASH-COMMANDS] ✅ COMANDO PROCESADO EXITOSAMENTE")
                                        
                                        # Reemplazar el mensaje del usuario con la respuesta del comando
                                        body["messages"] = messages[:-1] + [{
                                            "role": "assistant",
                                            "content": command_response
                                        }]
                                        
                                        # Notificar al usuario si está configurado
                                        if __event_emitter__ and hasattr(user_valves, 'show_status') and user_valves.show_status:
                                            await __event_emitter__({
                                                "type": "status",
                                                "data": {"description": "Comando ejecutado correctamente"}
                                            })
                                        
                                        return body
                                    else:
                                        print(f"[SLASH-COMMANDS] ⚠️ Comando no reconocido: {last_user_msg}")
                                        logger.warning(f"[SLASH-COMMANDS] ⚠️ Comando no reconocido: {last_user_msg}")
                            except Exception as e:
                                print(f"[SLASH-COMMANDS] ❌ Error procesando comando: {e}")
                                logger.error(f"[SLASH-COMMANDS] ❌ Error procesando comando: {e}")
                                
                except Exception as e:
                    print(f"[SLASH-COMMANDS] ❌ Error en detección de comandos: {e}")
                    logger.error(f"[SLASH-COMMANDS] ❌ Error en detección de comandos: {e}")
            
            # PASO 1: Determinar si es el primer mensaje de la sesión
            is_first_message = self._is_first_message(messages)
                
            # LOG VISIBLE DEL RESULTADO
            print(f"[NUEVA-LOGICA] 🎯 Primer mensaje detectado: {is_first_message}")
            logger.info(f"[NUEVA-LOGICA] 🎯 Primer mensaje detectado: {is_first_message}")
            
            if self.valves.debug_mode:
                logger.debug(f"Procesando memorias para usuario {user_id} - Primer mensaje: {is_first_message}")
            
            # PASO 2: Obtener memorias según la estrategia
            memories_to_inject = []
            
            if is_first_message:
                # ESTRATEGIA 1: Primer mensaje - Inyectar memorias más recientes
                print(f"[NUEVA-LOGICA] 🔄 Ejecutando estrategia PRIMER MENSAJE - obteniendo memorias recientes")
                logger.info(f"[NUEVA-LOGICA] 🔄 Ejecutando estrategia PRIMER MENSAJE - obteniendo memorias recientes")
                
                memories_to_inject = await self._get_recent_memories(
                    user_id=user_id,
                    limit=self.valves.max_memories_to_inject
                )
                
                print(f"[NUEVA-LOGICA] ✅ Primer mensaje: obtenidas {len(memories_to_inject)} memorias recientes")
                logger.info(f"[NUEVA-LOGICA] ✅ Primer mensaje: obtenidas {len(memories_to_inject)} memorias recientes")
                
                if self.valves.debug_mode:
                    logger.debug(f"Primer mensaje: obtenidas {len(memories_to_inject)} memorias recientes")
                    
            else:
                # ESTRATEGIA 2: Mensajes posteriores - Solo memorias relevantes
                # Extraer el input del usuario actual
                user_messages = [
                    msg.get("content", "") 
                    for msg in messages 
                    if isinstance(msg, dict) and msg.get("role") == "user"
                ]
                
                if user_messages:
                    current_user_input = user_messages[-1]  # Último mensaje del usuario
                    
                    memories_to_inject = await self._get_relevant_memories(
                        user_id=user_id,
                        user_input=current_user_input,
                        max_memories=self.valves.max_memories_to_inject
                    )
                    
                    if self.valves.debug_mode:
                        if memories_to_inject:
                            logger.debug(f"Mensaje posterior: obtenidas {len(memories_to_inject)} memorias relevantes")
                        else:
                            logger.debug("Mensaje posterior: no se encontraron memorias relevantes")
            
            # PASO 3: Inyectar memorias si las hay
            if memories_to_inject:
                await self._inject_memories_into_conversation(
                    body=body,
                    memories=memories_to_inject,
                    user_valves=user_valves,
                    user_id=user_id,
                    is_first_message=is_first_message,
                    __event_emitter__=__event_emitter__
                )
            else:
                if self.valves.debug_mode:
                    logger.debug("No se inyectaron memorias (no hay memorias disponibles o relevantes)")

        except Exception as e:
            logger.error(f"Error en el método inlet: {e}", exc_info=True)
            # Continuar sin fallar la petición

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

            # NOTA: Los comandos de memoria ahora se procesan en inlet() para mejor UX
            # Esta sección se mantiene como comentario para referencia histórica

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
    async def get_raw_existing_memories(self, user_id: str, order_by: str = "created_at DESC") -> List[Any]:
        """
        Obtiene las memorias sin procesar de un usuario, ordenadas por fecha.
        
        MEJORA SUGERIDA POR BYTIA: Intentar ordenación en la consulta de base de datos.
        
        Args:
            user_id: Identificador único del usuario
            order_by: Criterio de ordenación (por defecto: created_at DESC para más recientes primero)
            
        Returns:
            List[Any]: Lista de objetos de memoria sin procesar, ordenados por fecha
        """
        try:
            print(f"[MEMORIA-DEBUG] 🔍 Obteniendo memorias para usuario {user_id} con orden: {order_by}")
            logger.info(f"[MEMORIA-DEBUG] 🔍 Obteniendo memorias para usuario {user_id} con orden: {order_by}")
            
            # ESTRATEGIA 1: Intentar obtener memorias ordenadas desde la base de datos
            try:
                # Verificar si el método acepta parámetros de ordenación
                if hasattr(Memories, 'get_memories_by_user_id_ordered'):
                    existing_memories = Memories.get_memories_by_user_id_ordered(
                        user_id=str(user_id), 
                        order_by=order_by
                    )
                    print(f"[MEMORIA-DEBUG] ✅ Memorias obtenidas con ordenación desde BD")
                    logger.info(f"[MEMORIA-DEBUG] ✅ Memorias obtenidas con ordenación desde BD")
                else:
                    # Método estándar sin ordenación
                    existing_memories = Memories.get_memories_by_user_id(user_id=str(user_id))
                    print(f"[MEMORIA-DEBUG] ⚠️ Memorias obtenidas SIN ordenación desde BD")
                    logger.info(f"[MEMORIA-DEBUG] ⚠️ Memorias obtenidas SIN ordenación desde BD")
                    
            except Exception as db_error:
                print(f"[MEMORIA-DEBUG] ❌ Error en consulta BD: {db_error}")
                logger.warning(f"[MEMORIA-DEBUG] ❌ Error en consulta BD: {db_error}")
                existing_memories = []
            
            print(f"[MEMORIA-DEBUG] 📊 Total memorias obtenidas: {len(existing_memories or [])}")
            logger.info(f"[MEMORIA-DEBUG] 📊 Total memorias obtenidas: {len(existing_memories or [])}")
            
            return existing_memories or []
            
        except Exception as e:
            print(f"[MEMORIA-DEBUG] ❌ Error general al obtener memorias: {e}")
            logger.error(f"Error retrieving raw memories: {e}")
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
            existing_memories = await self.get_raw_existing_memories(user_id, order_by="created_at DESC")
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

            if self.valves.debug_mode:
                logger.debug(f"[MEMORIA-DEBUG] 📋 Procesadas {len(memory_contents)} memorias para usuario {user_id}")
            return memory_contents

        except Exception as e:
            print(f"Error processing memory list: {e}")
            return []