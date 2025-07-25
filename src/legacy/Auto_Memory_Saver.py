"""
Auto Memory Saver - Versión 1.0.0
================================

Función para OpenWebUI que guarda automáticamente los mensajes del asistente en la memoria del usuario.

Autor original: @linbanana (https://github.com/linbanana)
Basado en: https://github.com/linbanana/auto-memory-saver

Esta es la versión original 1.0.0 conservada con fines de referencia.
La versión mejorada y actualizada está disponible en Auto_Memory_Saver_Enhanced.py
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Any

from fastapi.requests import Request
from open_webui.routers.users import Users
from open_webui.routers.memories import (
    add_memory,
    AddMemoryForm,
    Memories,
    MemoryModel,
)


class Filter:
    class Valves(BaseModel):
        enabled: bool = Field(
            default=True, description="Enable/disable auto memory save"
        )

    class UserValves(BaseModel):
        show_status: bool = Field(
            default=True, description="Show status while saving to memory"
        )

    def __init__(self):
        self.valves = self.Valves()

    # ✅ Inject memories into new conversations
    async def inlet(
        self,
        body: dict,
        __request__: Request,
        __user__=None,
        __event_emitter__=None,
    ) -> dict:
        if not self.valves.enabled or not __user__:
            return body

        try:
            user_id = __user__["id"]
            processed_memories = await self.get_processed_memory_strings(user_id)

            if processed_memories:
                context_string = "📘 Prior Memory:\n" + "\n".join(processed_memories)
                system_msg = {"role": "system", "content": context_string}
                if "messages" in body:
                    body["messages"].insert(0, system_msg)

        except Exception as e:
            print(f"Error injecting memory into new conversation: {e}")

        return body

    # ✅ Auto-save replies and handle memory queries
    async def outlet(
        self,
        body: dict,
        __request__: Request,
        __user__=None,
        __event_emitter__=None,
    ) -> dict:
        try:
            if not self.valves.enabled or not __user__:
                return body

            user = Users.get_user_by_id(__user__["id"])
            user_valves = __user__.get("valves", self.UserValves())

            # Handle /memories command
            user_messages = [m for m in body.get("messages", []) if m["role"] == "user"]
            if user_messages:
                last_user_msg = user_messages[-1]["content"].strip().lower()
                if last_user_msg == "/memories":
                    processed_memories = await self.get_processed_memory_strings(
                        user.id
                    )
                    response = "📘 Current Memories:\n" + "\n".join(
                        processed_memories or ["(no memory found)"]
                    )
                    body["messages"].append({"role": "assistant", "content": response})
                    return body

            # Save last assistant message
            assistant_messages = [
                m for m in body.get("messages", []) if m["role"] == "assistant"
            ]
            if not assistant_messages:
                return body

            last_assistant_message = assistant_messages[-1]
            message_content = last_assistant_message.get("content", "").strip()
            if not message_content:
                return body

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

            # Extra memory logging
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

    # ✅ Clear user memories
    async def clear_user_memory(self, user_id: str) -> None:
        try:
            print(f"[Memory] Clearing all memories for user: {user_id}")
            deleted_count = Memories.delete_memories_by_user_id(user_id)
            print(f"[Memory] Deleted {deleted_count} memory entries.")
        except Exception as e:
            print(f"Error clearing memory for user {user_id}: {e}")

    async def on_chat_deleted(self, user_id: str) -> None:
        if self.valves.enabled:
            await self.clear_user_memory(user_id)

    # ✅ Get raw memories
    async def get_raw_existing_memories(self, user_id: str) -> List[Any]:
        try:
            existing_memories = Memories.get_memories_by_user_id(user_id=str(user_id))
            print(f"[Memory] Raw existing memories: {existing_memories}\n")
            return existing_memories or []
        except Exception as e:
            print(f"Error retrieving raw memories: {e}")
            return []

    # ✅ Get formatted memory strings
    async def get_processed_memory_strings(self, user_id: str) -> List[str]:
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
