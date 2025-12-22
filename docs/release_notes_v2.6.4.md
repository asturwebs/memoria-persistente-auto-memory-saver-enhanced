# Release Notes v2.6.4 - Hotfix: Token Explosion Guardrails

**Release Date**: 2025-12-22  
**Type**: Patch Release (Critical Hotfix)

## Overview

Version **2.6.4** is a **critical production hotfix** to stop excessive prompt growth and runaway token usage (reported as "hundreds of memories" injected into the prompt, e.g. "700 memories loaded"), especially noticeable with **Gemini** API billing.

This release adds **hard caps** and a **failsafe sanitizer** that strips known external memory-dump `system` messages before the request reaches the model.

## What Changed

### ✅ Hard Limits for Injection (Always Enforced)

- **Max injected memories** remains controlled by:
  - `max_memories_to_inject` (default: `5`)

- **New: hard cap for injected size**:
  - `max_injection_chars` (default: `3500`)
  - Enforced even if memory retrieval returns many items.

- **New: hard cap for DB scan**:
  - `max_memories_to_scan` (default: `300`)
  - Prevents scanning thousands of memories just to compute relevance.

### ✅ Skip Injection for Casual Turns

- **New**:
  - `skip_injection_for_casual` (default: `True`)
- Skips memory injection for short greetings / casual turns (e.g. "Hola Socia").

### 🚨 Critical Failsafe: Strip External Memory Dumps

Even if OpenWebUI (or another filter) injects a huge memory dump as a `system` message, v2.6.4 strips it before sending the prompt to the model.

Removed when detected:
- `Retrieving stored memories`
- `\d+ memories loaded`
- Very large `system` messages containing `memory/memories` (size heuristic)

## New/Updated Valves

```python
max_injection_chars: int = 3500
max_memories_to_scan: int = 300
skip_injection_for_casual: bool = True
```

## Deployment Notes (OpenWebUI)

- Replace the function code with `src/memoria_persistente_auto_memory_saver_enhanced.py` from this release.
- Restart OpenWebUI container if you suspect caching.
- Validate status messages show `AMSE v2.6.4`.

## Verification Checklist

- Send: `Hola Socia`
- Expected:
  - No "Retrieving stored memories" in the prompt.
  - No massive memory dump / no "700 memories loaded".
  - If memories are injected, it should be **0-5** and limited by `max_injection_chars`.

## Files Changed

- `src/memoria_persistente_auto_memory_saver_enhanced.py`
- `README.md`
- `docs/CHANGELOG.md`
- `docs/release_notes_v2.6.4.md`
