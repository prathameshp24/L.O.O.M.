# 🧵 L.O.O.M. (Layered Orchestration and Operational Mind)

**An autonomous, ambient, and deterministic desktop orchestrator designed natively for the Linux Wayland ecosystem.**

L.O.O.M. represents a paradigm shift in desktop automation. Moving beyond reactive chat interfaces and brittle GUI-scraping scripts, L.O.O.M. is designed to be a continuous, unmonitored background daemon—a true "Jarvis-like" entity for your local machine. It seamlessly integrates with your operating system to execute complex, multi-step workflows autonomously.

---

## 🏛️ Core Architectural Philosophy

L.O.O.M. operates on a strict hierarchy of interaction, prioritizing speed, reliability, and security over heuristic guessing:

1. **Deterministic Inter-Process Communication (IPC):** Uses D-Bus (System & Session) to execute hardware and app commands instantly and invisibly without stealing window focus.
2. **Semantic Accessibility Trees:** Uses AT-SPI2 to traverse native GTK/Qt applications programmatically, achieving 100% accuracy in UI element location.
3. **Semantic Visual Grounding:** When native APIs fail (e.g., complex Electron apps or web canvases), relies on local Vision-Language Models (like Florence-2/OmniParser) to map the screen into structured data, completely replacing legacy computer vision (OpenCV) heuristics.
4. **Event-Driven Execution:** Built on Python's `asyncio` framework to react to system state changes dynamically, completely eliminating arbitrary `time.sleep()` bottlenecks.
5. **Stateful Multi-Agent Routing:** Utilizes a LangGraph-inspired state machine to route tasks between specialized agents (Desktop, Research, Coding) while maintaining robust, interruptible context.

---

## 📂 System Architecture & Directory Structure

L.O.O.M. is built for massive scalability. It decouples the "Brain" (Orchestrator) from the "Hands" (Tools) and the "Personas" (Agents).

```text
loom/
├── main.py                     # Systemd daemon entry point
├── .env                        # API keys and system paths
├── requirements.txt            # Python dependencies
│
├── core/                       # The Brain
│   ├── orchestrator.py         # Graph-based routing (LangGraph logic)
│   ├── state.py                # Shared state/context across agents
│   └── memory_manager.py       # Qdrant (vectors) and SQLite (checkpoints) integration
│
├── agents/                     # The Workers
│   ├── base_agent.py           # Abstract Base Class for agent standard IO
│   ├── desktop_agent/          # Core Wayland OS interaction agent
│   ├── research_agent/         # (Future) Web search and deep research
│   └── coding_agent/           # (Future) Codebase manipulation
│
├── tools/                      # The Hands (Physical execution)
│   ├── registry.py             # Maps natural language to tool execution
│   ├── system/                 # D-Bus IPC (Volume, Brightness, Wi-Fi, Spotify/MPRIS)
│   ├── fs/                     # File system operations (Watchdog, I/O)
│   ├── vision/                 # UI Fallbacks (AT-SPI2, Florence-2 local VLM)
│   └── macros.py               # Complex chained skills (e.g., "Deep Work Mode")
│
└── interfaces/                 # Human Interaction Layer
    ├── cli.py                  # Standard terminal execution
    ├── hitl.py                 # Human-In-The-Loop desktop notifications (Approve/Deny)
    └── voice/                  # (Future) Local Wake-word, Whisper STT, Piper TTS

🗺️ Development Roadmap
Phase 1: The Deterministic Foundation (Current)
Objective: Replace brittle simulated keystrokes with direct Linux native IPC.

[ ] Implement tools/system/dbus_hardware.py (Volume, Brightness, Network).

[ ] Implement tools/system/dbus_media.py (Spotify/MPRIS Play, Pause, Next, Metadata).

[ ] Refactor core execution loop to use asyncio instead of synchronous polling.

Phase 2: System Navigation & Semantic Fallback
Objective: Enable flawless application interaction without blind X/Y coordinate clicking.

[ ] Integrate pyatspi2 to read GTK/Qt application accessibility trees.

[ ] Deploy local VLM (Florence-2) for structured JSON mapping of opaque applications.

[ ] Remove all dependencies on OpenCV Canny edge detection.

Phase 3: Multi-Agent Orchestration & Memory
Objective: Give L.O.O.M. continuous context, fault tolerance, and specialized routing.

[ ] Implement core/state.py for interruptible execution graphs.

[ ] Integrate Qdrant vector database for local, long-term Episodic and Procedural memory.

[ ] Implement local SQLite checkpointing to recover gracefully from mid-task crashes.

Phase 4: Ambient Operation & Security
Objective: Make L.O.O.M. pervasive, voice-activated, and completely safe to run unmonitored.

[ ] Wrap all LLM-generated script execution in Bubblewrap zero-trust sandboxes.

[ ] Build GNOME Gio.Notification Human-in-the-Loop (HITL) prompt for destructive actions.

[ ] Daemonize the process using systemd user services.

[ ] Integrate local audio pipeline (faster-whisper + Piper).

