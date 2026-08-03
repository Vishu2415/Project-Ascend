```mermaid
graph TD

User --> Frontend
Frontend --> Backend
Backend --> AIOrchestrator

AIOrchestrator --> LLM
AIOrchestrator --> Memory
AIOrchestrator --> Tools

Memory --> Database
Tools --> GitHub
Tools --> Gmail
Tools --> Calendar
```