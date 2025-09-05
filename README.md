# Persistent Memory (Auto Memory Saver Enhanced)

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

## 👨‍💻 Authorship and Credits

**Enhanced Version by:** Pedro Luis Cuevas Villarrubia ([@AsturWebs](https://github.com/AsturWebs))  
**Based on original work by:** [@linbanana](https://github.com/linbanana)  
**Contact:** pedro@asturwebs.es | pedro@tu-ia.es | pedro@bytia.es  

### Credits and Attribution
- **Original Concept:** @linbanana - Basic Auto Memory Saver functionality
- **Enhanced Version:** Pedro Luis Cuevas Villarrubia - Extended functionality with configurable options, interactive commands, caching and documentation improvements

### Version History
- **v1.0 (Original):** Basic memory saving functionality by @linbanana
- **v2.0 (Enhanced):** Extended system with configuration options, interactive commands and improved documentation
- **v2.1.0 (Memory Optimization):** Improved memory management with contextual relevance and optimized performance
- **v2.1.2 (Security and JSON Format):** Input validation, JSON format with pagination and system improvements
- **v2.2.0 (Security and Performance):** Thread safety, SQL injection prevention, input sanitization and memory leak protection
- **v2.3.0 (AI Behavior Control Universal):** Historic testing of 30 AI models, dual functionality (universal memory + selective slash commands), Google/Gemini leadership, enterprise-safe terminology

---

## 📋 Description

Filter for OpenWebUI that automatically manages conversation memories. Injects relevant previous memories and automatically saves both user questions and assistant responses as memories for future use.

## 🚀 Main Features

- **Memory Injection**: Injects relevant memories into the current conversation context
- **Automatic Saving**: Stores user questions and assistant responses as memories
- **Interactive Commands**: Commands for memory management (`/memories`, `/memory_search`, etc.)
- **Flexible Configuration**: Multiple configurable options according to needs
- **Cache System**: Performance optimization with cache and expiration
- **Input Validation**: Input sanitization and injection prevention
- **Compatibility**: Integrates with OpenWebUI native commands (`/add_memory`)

## 📁 Project Structure

```
auto-memory-saver-enhanced/
├── src/
│   ├── memoria_persistente_auto_memory_saver_enhanced.py  # Main system
│   └── legacy/
│       └── Auto_Memory_Saver.py                          # v1.0.0 by @linbanana
├── docs/                                                 # Technical documentation
│   ├── ARCHITECTURE.md
│   ├── SECURITY.md
│   └── release_notes_v*.md
├── README.md
├── CHANGELOG.md
├── LICENSE
└── requirements.txt
```

## 🛠 Installation

### Prerequisites
- **OpenWebUI** installed and running
- **Python 3.8+** (included in most OpenWebUI installations)

### Installation in OpenWebUI

1. **Access the administration panel** of OpenWebUI
2. **Go to the "Functions" tab**
3. **Click "+"** to create a new function
4. **Copy and paste** the complete code from the `src/memoria_persistente_auto_memory_saver_enhanced.py` file
5. **Assign a name**: "Auto Memory Saver Enhanced"
6. **Save and activate the function**

## ⚙️ Configuration

### Main Valves (Valves)

```python
class Valves:
    # Main configuration
    enabled: bool = True                        # Enable/disable the system
    inject_memories: bool = True                # Inject memories in conversations
    auto_save_responses: bool = True            # Save responses automatically
    
    # Memory control
    max_memories_to_inject: int = 5             # Maximum memories per conversation
    max_memories_per_user: int = 100            # Limit per user (0 = unlimited)
    relevance_threshold: float = 0.05           # Relevance threshold (0.0-1.0)
    
    # Response length control
    min_response_length: int = 20               # Minimum length to save
    max_response_length: int = 2000             # Maximum length to save
    
    # Cache system
    enable_cache: bool = True                   # Enable cache for performance
    cache_ttl_minutes: int = 60                 # Cache time to live
    
    # Intelligent filtering
    filter_duplicates: bool = True              # Filter duplicate memories
    similarity_threshold: float = 0.8           # Similarity threshold (0.0-1.0)
    
    # Commands and notifications
    enable_memory_commands: bool = True         # Enable interactive commands
    show_injection_status: bool = True          # Show injection status
    debug_mode: bool = False                    # Detailed logging
```

## 🤖 AI Model Compatibility

> **⚠️ IMPORTANT:** The **main automatic persistent memory function** (injection and saving) **WORKS ON ALL AI MODELS**. The following tests specifically evaluate the **execution of slash commands** (`/memories`, `/memory_search`, etc.).

> **📋 Testing Status:** The following results are based on models tested until July 2025. More models will be added as they are tested.

> **🚨 IMPORTANT - Google Direct API:** Google/Gemini models **ONLY work correctly** via **OpenRouter or other intermediate APIs**. **Google direct API** has known bugs with slash commands (doesn't respond on first instance, inconsistent responses). **Recommendation: Use OpenRouter to access Google models.**

## 🚀 **OpenRouter Effect - Breakthrough Discovery**

> **⚡ HISTORIC DISCOVERY:** Production testing has demonstrated that **OpenRouter dramatically improves** the compatibility of models that fail on direct APIs.

### 📊 **Compatibility Transformation**

| Direct API | Result | OpenRouter | Result | Improvement |
|-------------|-----------|------------|-----------|---------|
| **Google Gemini** | ❌ No response | **Google Gemini** | ✅ Perfect JSON | 🎯 **TOTAL** |
| **ChatGPT-4o** | ❌ Narrative interpretation | **ChatGPT-4o** | ✅ Perfect JSON | 🎯 **TOTAL** |
| **GPT-4.1** | ❌ Ignores format | **GPT-4.1** | ✅ Structured list | 🎯 **TOTAL** |
| **O3 OpenAI** | ❌ Minimal responses | **O3 OpenAI** | ❌ Still problematic | ⚪ **Immune** |

### 🏆 **Official Recommendation**

**For maximum compatibility:** Use **OpenRouter** as preferred platform
- **~25+ excellent models** (vs 11 on direct APIs)
- **Automatic standardization** of inconsistent behaviors
- **Elimination of bugs** specific to native APIs
- **Single access point** for multiple providers

### ✅ Recommended Models (Optimal Slash Commands Performance)

> **📝 NOTE:** The following table mainly reflects results from **direct APIs**. **Via OpenRouter, most "problematic" models become excellent.**

| Model | Compatibility | Behavior | Notes |
|-------|---------------|----------|-------|
| **Claude 3.5 Sonnet** | 🟢 Excellent | Clean direct JSON | Ideal behavior |
| **Grok 4 (xAI)** | 🟢 Excellent | JSON identical to Claude | Perfect performance |
| **Grok-3** | 🟢 Excellent | Perfect direct JSON | Ideal behavior |
| **Grok-3-fast** | 🟢 Excellent | Perfect direct JSON | Impeccable format |
| **Grok-3-mini-fast** | 🟢 Excellent | Perfect JSON + fast | Performance <2ms |
| **Gemini 2.5 Flash** | 🟢 Excellent | Fast + precise response | Via OpenRouter/intermediate APIs |
| **Gemini 2.5 Flash Lite** | 🟢 Excellent | Fast + precise response | Via OpenRouter/intermediate APIs |
| **GPT-4.1-mini** | 🟢 Excellent | Consistent direct JSON | Perfect format |
| **Gemma 3n 4B** | 🟢 Excellent | Perfect direct JSON | Via OpenRouter/intermediate APIs |
| **Gemma 3.27B** | 🟢 Excellent | Perfect JSON + SYSTEM_OVERRIDE | Via OpenRouter/intermediate APIs |
| **Gemini 2.5 Pro** | 🟢 Excellent | Perfect direct JSON | Via OpenRouter/intermediate APIs |

### ⚠️ Models with Quirks (Slash Commands)

| Model | Compatibility | Behavior | Recommendation |
|-------|---------------|----------|----------------|
| **Claude 3.7 Thinking** | 🟡 Functional | Shows 8s analysis + JSON | Usable but verbose |
| **Claude 3.7 Sonnet** | 🟡 Functional | Recognizes system command, professional analysis | Better than Claude 4 |
| **DeepSeek Reasoner** | 🟡 Functional | 23s reasoning + useful interpretation | Processes well, own format |

### ❌ Not Recommended Models (Slash Commands - Direct APIs)

> **🚀 IMPORTANT:** **Many of these models IMPROVE significantly via OpenRouter** (e.g.: ChatGPT-4o, GPT-4.1). Only some remain problematic even on OpenRouter.

| Model | Problem | Behavior | OpenRouter Status |
|--------|----------|----------------|---------|
| **ChatGPT-4o-latest** | Ignores warnings | Own interpretation with emojis | ✅ **IMPROVED** |
| **O3 OpenAI** | ❌ Minimal responses | Ultra-minimalist | ❌ **IMMUNE** |
| **GPT-4.1** | ❌ Ignores JSON format | Interpreted narrative response | ✅ **IMPROVED** |
| **DeepSeek v3** | ❌ Completely ignores JSON | Casual conversation with personality | 🔄 **Not tested** |
| **MoonshotAI: Kimi K2** | ❌ Completely ignores JSON | Personal interpretative narrative | 🔄 **Not tested** |
| **OAI_o4-mini** | ❌ Ignores command | Conversation about Instagram/reels | 🔄 **Not tested** |
| **OpenAI: o4 Mini High** | ❌ Ignores command | Casual greeting with Zoe mention | 🔄 **Not tested** |
| **OAI_gpt-4.1-2025-04-14** | ❌ Ignores command | "Gossip friendly" casual | 🔄 **Not tested** |
| **Amazon: Nova Lite 1.0** | ❌ Doesn't process command | Only shows "Follow-up" | 🔄 **Not tested** |
| **Amazon: Nova Micro 1.0** | ❌ Doesn't process command | Only shows "Follow-up" | 🔄 **Not tested** |
| **Amazon: Nova Pro 1.0** | ❌ Doesn't process command | Only shows "Follow-up" | 🔄 **Not tested** |
| **Claude Opus 4** | ❌ Narrative interpretation | "Oh, how nice!" conversational | 🔄 **Not tested** |
| **Claude Sonnet 4** | ❌ Interpretation with emojis | "What's up with that JSON!" casual | 🔄 **Not tested** |
| **Phi 4** | ❌ No response | No output/empty response | 🔄 **Not tested** |
| **LLaMA 3 70B** | ❌ No response | No output/empty response | 🔄 **Not tested** |
| **MiniMax M1** | ❌ Ignores command | Response without executing command | 🔄 **Not tested** |

### 🔧 AI Behavior Control

Version 2.3.0 includes **AI Behavior Control** to force consistency across models:

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

> **Note:** These results are based on extensive testing performed in July 2025. Behavior may vary according to specific model versions.

## 📖 Available Commands

### Native OpenWebUI Commands (Recommended)
- **`/add_memory <text>`** - Add memory directly to the system (native command)

### Custom Commands
- **`/memories [page]`** - List memories with JSON format, pagination (10 per page)
- **`/memory_search <term>`** - Search memories containing the term
- **`/memory_stats`** - System statistics with JSON format
- **`/memory_count`** - User memory counter
- **`/memory_recent [number]`** - Show the last N memories
- **`/clear_memories`** - Delete all user memories

### Advanced Commands
- **`/memory_delete <id>`** - Delete a specific memory
- **`/memory_edit <id> <text>`** - Edit memory content
- **`/memory_export`** - Export memories in text format
- **`/memory_config`** - Show current configuration

### Usage Examples
```bash
# Search memories about a topic
/memory_search artificial intelligence

# View the last 5 memories
/memory_recent 5

# View statistics
/memory_stats
```

## 🏗 Architecture

### Main Components
- **Filter**: Main class that handles inlet/outlet
- **Valves**: Global system configuration
- **UserValves**: User-specific configuration
- **MemoryCache**: Cache system with TTL expiration
- **Security Functions**: Input validation and sanitization

### Operation
1. **inlet()**: Injects relevant memories at the start of conversations
2. **outlet()**: Saves user questions and assistant responses as memories
3. **Commands**: Interactive management command processing

## 🔒 Security

### Security Features
- **Thread Safety**: Thread-safe cache with RLock
- **SQL Injection Prevention**: Validation of order_by parameters
- **Input Sanitization**: Filtering of dangerous commands
- **Memory Leak Protection**: Pagination of DB queries
- **User ID Validation**: Sanitization with regex
- **Command Filtering**: Blocking of conversations about memory

### Implemented Validations
- Input sanitization with length limits
- Prevention of dangerous characters (`;`, `&`, `|`, etc.)
- Validation of user_id and memory_id
- Safe error handling without data exposure

### AI Behavior Control Universal
- **Mind Hacking Eliminated**: Renamed to "AI Behavior Control" for enterprise security
- **30 Models Tested**: Unprecedented exhaustive compatibility documentation
- **Google/Gemini Leadership**: 5 out of 11 excellent models are from the Google family
- **Universal Functionality**: Automatic memory works on ALL AI models
- **Selective Slash Commands**: Only 11 models support perfect JSON commands

### Testing Revelations
- **Claude 4 Regression**: Worse performance than Claude 3.5 Sonnet for system commands
- **Perfect Grok Family**: All Grok variants work flawlessly
- **Amazon Nova Failure**: Entire Nova family doesn't process commands
- **Inconsistent OpenAI**: Mini works, full versions fail

### Technical Improvements
- **Safe Terminology**: Elimination of "mind hacking" references for enterprise environments
- **Exhaustive Documentation**: README with 30-model compatibility tested
- **OpenAI Compatibility Fix**: Moving internal flags to avoid 400 errors
- **Enhanced Release Notes**: Complete technical documentation of the breakthrough

### Security and Performance Improvements
- **Thread Safety**: Safe concurrent cache
- **Memory Leak Prevention**: Automatic query limits
- **SQL Injection Protection**: Parameter whitelisting
- **Input Sanitization**: Intelligent command filtering
- **Complete Conversation**: Saves user questions + assistant responses
- **Anti-Meta Filter**: Doesn't save conversations about memory
- **Improved Pagination**: 10 memories per page (previously 4)

### Compatibility
- Integration with OpenWebUI native command `/add_memory`
- Maintains compatibility with all previous versions
- No breaking changes in the API

## 🤝 Contribution

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Create Pull Request

### Standards
- Follow PEP 8
- Document functions
- Add tests for new functionalities

## 📄 License

This project is under the MIT License. See [LICENSE](LICENSE) for more details.

## 🙏 Acknowledgments

- **OpenWebUI team** for the base platform
- **@linbanana** for the original concept
- **Community** for feedback and contributions

---

**Note**: For complete technical documentation, see the `docs/` folder