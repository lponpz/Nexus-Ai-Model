# Your AI roadmap

This is a staged plan. Checkboxes indicate implemented work only; partial work is described separately.

## Milestone 1 — Foundation
- [x] FastAPI app and health route
- [x] SQLite project creation/listing
- [x] Cloud/local provider adapter (cloud key takes priority; otherwise Ollama is attempted)
- [x] Responsive browser dashboard
- [x] Automated unit tests and GitHub Actions CI
- [x] Persistent conversation history and recent-context loading
- [ ] Settings UI

## Verified partial implementation
- Paper plugin starter generator creates a ZIP containing a Maven project, JavaPlugin class and plugin.yml. It does **not** compile a JAR, install to a server or run an integration test.
- Four unit tests cover ZIP contents and invalid package/version inputs. The latest observed GitHub Actions run completed successfully, including the unit-test step.

## Milestone 2 — Core assistant
- [ ] Model selector and provider diagnostics
- [x] Basic persistent conversation history and recent context
- [ ] Conversation export and deletion controls
- [ ] User-controlled memory and offline knowledge vault
- [ ] Hindi, Urdu, Roman Urdu and English UI/content support
- [ ] Explicit consent before any future cloud sync
- [ ] Basic offline chat validation on a device with no internet
- [ ] Separate lightweight and advanced local-model profiles

## Milestone 3 — Minecraft Creator Studio
- [ ] Complete Paper/Purpur plugin builder with actual compilation and build-log reporting
- [ ] Fabric/Forge/NeoForge mod project templates
- [ ] Resource-pack and datapack tools
- [ ] Compatibility checks, build logs and test fixtures
- [ ] Schematic/model tools and farm design guides
- [ ] Export ZIP/JAR only after actual build validation

## Milestone 4 — Full AI Developer Mode
- [ ] Workspace-scoped project file read/write/create operations
- [ ] User approval before every file change or deletion
- [ ] Backup and rollback before major changes
- [ ] Test generation and execution in a sandbox
- [ ] Debugging and proposed bug fixes with review before applying
- [ ] Terminal integration with explicit approval for each command
- [ ] Dangerous-command blocklist and safe working-directory restrictions
- [ ] GitHub integration with least-privilege permissions and approval before writes
- [ ] VS Code integration
- [ ] Audit log and emergency stop for agent actions

## Milestone 5 — Voice, image and creative studios
- [ ] Voice input and output, with user-controlled microphone permissions
- [ ] Image understanding and image generation integrations
- [ ] Image/design, video/animation, voice/audio and 3D workflows
- [ ] Integrate suitable local or cloud models
- [ ] Report unsupported operations rather than pretending to render/export

## Milestone 6 — Agents, memory and security
- [ ] Multi-agent task planning with a visible action queue
- [ ] User-controlled long-term memory and memory review/deletion
- [ ] Offline knowledge vault
- [ ] Approval Center and audit log
- [ ] Stop button and rollback/backup workflow
- [ ] No background system changes or unrestricted shell access
- [ ] Security tools operate only on user-selected files and scopes

## Cross-platform and hybrid requirements
- [ ] Android app/package and Windows desktop package
- [ ] Cloud AI engine
- [ ] Lightweight local model for low-resource devices
- [ ] Optional advanced local model for stronger hardware
- [ ] Basic chat works offline when a compatible local model is installed
- [ ] Offline conversations sync only after explicit user permission
- [ ] No automatic cloud upload of offline conversations

## Definition of done
A feature is complete only when source code, tests, documented configuration and a verified run/build exist. UI placeholders and roadmap entries do not count as working features.
