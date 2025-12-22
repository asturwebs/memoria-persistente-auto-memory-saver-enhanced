# Release Notes v2.6.5

## 🧹 Maintenance & UX Improvements

**Version:** v2.6.5
**Date:** 2025-12-22
**Priority:** Low (Maintenance) / Medium (UX)

This release polishes the user experience by preventing trivial casual conversations from cluttering the memory database and includes version synchronization.

### 🚀 Key Changes

#### 1. Casual Conversation Guardrails (Save Logic)
- **What Changed:** The `skip_injection_for_casual` logic is now applied to the **auto-save** mechanism (`outlet`) as well.
- **Why:** Previously, if a user said "Hola Socia", the system wouldn't inject memories (good) but *would* save the interaction "User: Hola Socia | Assistant: Hola..." as a new memory (bad). This led to "dirty" databases filled with trivial greetings.
- **Result:** Greetings, simple acknowledgments ("ok", "gracias"), and short casual interactions are now **ignored** by the auto-saver, keeping your memory database clean and focused on relevant facts.

#### 2. Security & Stability
- **External Memory Stripping:** Retained and refined the failsafe mechanism that strips massive external memory dumps (like those from the "Memory" tool by CookSleep) from the prompt, ensuring AMSE remains the sole authority on memory injection.

### 📦 Deployment Instructions

1. **Update the file**: Replace `memoria_persistente_auto_memory_saver_enhanced.py` with the v2.6.5 version.
2. **Restart OpenWebUI**: Required to apply the code changes.
3. **Verify**: Check that the status message now says `(AMSE v2.6.5)`.

### ✅ Verification Checklist

- [ ] Send a simple "Hola" or "Hello" to the bot.
- [ ] Ensure NO "Memory saved" status message appears (it should be skipped).
- [ ] Send a factual statement like "My favorite color is green".
- [ ] Ensure "✅ Memory saved (AMSE v2.6.5)" appears.
