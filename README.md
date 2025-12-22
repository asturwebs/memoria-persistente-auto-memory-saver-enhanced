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

## Available Commands

| Command | Description |
|---------|-------------|
| `/memories [page]` | List memories (paginated) |
| `/memory_search <term>` | Search memories |
| `/memory_recent [n]` | Last N memories |
| `/memory_count` | Memory count |
| `/memory_stats` | Statistics |
| `/memory_export` | Export memories |
| `/clear_memories` | Delete all |
| `/memory_help` | Show all commands |

> **Tip**: Use OpenWebUI native `/add_memory <text>` to add memories manually.

## Configuration

Key settings in Valves:

```python
enabled: bool = True                    # Enable/disable system
inject_memories: bool = True            # Inject memories in conversations
auto_save_responses: bool = True        # Auto-save conversations
max_memories_to_inject: int = 5         # Max memories per conversation
max_injection_chars: int = 3500         # Hard cap total injected chars
max_memories_to_scan: int = 300         # Hard cap scanned memories from DB
skip_injection_for_casual: bool = True  # Skip injection for greetings/casual
max_memories_per_user: int = 100        # User limit (0 = unlimited)
enable_cache: bool = True               # Cache for performance
debug_mode: bool = False                # Detailed logging
```

## AI Compatibility

- **Automatic memory** (injection/saving): Works on **all AI models**
- **Slash commands**: Best results with Claude, Grok, Gemini (via OpenRouter), GPT-4.1-mini

## Project Structure

```text
├── src/
│   └── memoria_persistente_auto_memory_saver_enhanced.py
├── docs/
│   ├── CHANGELOG.md
│   ├── ARCHITECTURE.md
│   └── release_notes_v*.md
├── README.md
└── requirements.txt

## Credits


- **Enhanced by**: Pedro Luis Cuevas Villarrubia ([@AsturWebs](https://github.com/AsturWebs))
- **Original concept**: [@linbanana](https://github.com/linbanana)

## License

MIT License - See [LICENSE](LICENSE)
