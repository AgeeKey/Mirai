# 🌸 MIRAI Autonomous Agent - Vision & Scope Document

**Version:** 1.0  
**Date:** October 2025  
**Status:** Phase 0 - Discovery  
**Owner:** MIRAI Development Team

---

## 🎯 Executive Summary

MIRAI is a locally/cloud-deployable, autonomous, and secure AI agent designed to revolutionize task automation and software development. The system integrates task planning, browser/software automation (RPA), code execution, data collection/processing, memory storage/retrieval (RAG), and workflow execution capabilities - all while maintaining manageability, testability, and production scalability.

**Vision Statement:**
> Build an intelligent, autonomous agent that can think, learn, act, and evolve - transforming how humans interact with software systems while maintaining security, reliability, and ethical boundaries.

---

## 🏗️ Project Scope

### In Scope

#### Core Capabilities
- **Autonomous Task Planning** - AI-driven task decomposition and execution planning
- **Browser & Software Automation (RPA)** - Playwright/CDP integration for web automation
- **Multi-Language Code Execution** - Python, JavaScript, TypeScript, C, C++, Go, Rust, Bash
- **Memory & Context Management** - Long-term memory with RAG for intelligent retrieval
- **Workflow Orchestration** - Multi-step business process automation
- **Security & Safety Controls** - Policy engine, sandboxing, approval workflows
- **Monitoring & Observability** - Production-grade logging, metrics, tracing

#### Integration Points
- OpenAI GPT-4o/GPT-4o-mini for intelligence
- GitHub for CI/CD monitoring and code management
- Multiple database backends (SQLite, PostgreSQL, MongoDB, Redis)
- Web dashboard for monitoring and control
- Terminal UI for interactive operations

### Out of Scope (Current Version)
- Physical robotics/hardware control
- Real-time voice conversation (future phase)
- Video generation/editing (future phase)
- Blockchain/cryptocurrency operations
- Medical diagnosis or legal advice
- Military or surveillance applications

---

## 🎪 Business Value

### Target Users
1. **Solo Developers** - Automate repetitive coding tasks, testing, documentation
2. **Small Teams** - DevOps automation, CI/CD monitoring, code reviews
3. **Enterprise** - Large-scale RPA, workflow automation, compliance monitoring
4. **Researchers** - Data collection, analysis automation, experiment tracking

### Key Benefits
- **Time Savings**: 60-80% reduction in repetitive task time
- **Quality Improvement**: Consistent execution, reduced human error
- **Cost Efficiency**: One agent replaces multiple manual processes
- **24/7 Operation**: Autonomous monitoring and response
- **Continuous Learning**: Agent improves from experience

### Success Metrics
- Task success rate: **≥80%** for prioritized workflows
- Mean task latency: **<30s** for search→read→summary flow
- Cost per automated task: **<$0.05**
- Time to onboard new macro: **<2 hours**
- System uptime: **≥99.5%**

---

## 🔐 Security & Compliance

### Security Requirements
- **Policy Engine**: YAML-driven rules for allowed/prohibited actions
- **Sandboxed Execution**: Docker-based isolation for code execution
- **Token Authentication**: Secure API access with rotation
- **Audit Logging**: Complete action history for forensic analysis
- **Panic Stop**: Emergency shutdown mechanism
- **Secret Management**: Vault integration, no secrets in code

### Compliance Considerations
- **Data Retention Policy**: Configurable memory persistence duration
- **User Consent**: Opt-in for data collection, opt-out available
- **Privacy Controls**: No external data transmission without approval
- **Regular Security Audits**: Quarterly pen tests and vulnerability assessments
- **GDPR/CCPA Ready**: Data export and deletion capabilities

---

## 📊 Technical Constraints

### Resource Requirements
- **Compute**: 2-4 CPU cores, 4-8GB RAM for local deployment
- **Storage**: 10GB minimum (databases, logs, knowledge base)
- **Network**: Stable internet for AI API calls (optional offline mode)
- **OS Support**: Linux (primary), macOS (supported), Windows (experimental)

### Technology Stack
- **Backend**: Python 3.10+, FastAPI, asyncio
- **AI/ML**: OpenAI API, sentence-transformers (embeddings)
- **Automation**: Playwright (browser), pyautogui (desktop)
- **Storage**: SQLite (default), PostgreSQL (production)
- **Monitoring**: Prometheus, Grafana (optional)
- **Orchestration**: Kubernetes (enterprise deployment)

### Limitations
- AI model dependency (external API or local model required)
- Browser automation limited by anti-bot measures (captchas)
- Code execution risks require sandboxing
- Token costs for cloud AI models
- DOM changes can break RPA selectors

---

## 🚀 High-Level Approach

### Development Methodology
- **Agile/Scrum**: 2-week sprints with demos
- **Quarterly Roadmaps**: Strategic planning and review
- **Definition of Done**: Code + Tests + Docs + Infra + Runbook
- **Guilds**: Cross-team collaboration (Architecture, Security, RPA)

### Risk Management Strategy
- **Unpredictable agent actions**: Policy engine + manual approval + sandbox
- **Website blocking/captchas**: API fallbacks + human-in-the-loop
- **Secret leaks**: Vault + audit logs + key rotation
- **Rising LLM costs**: Cost guards + model tiering + local fallback
- **DOM changes breaking RPA**: Selector maps + ML-based visual selectors + monitoring

### Quality Assurance
- **Unit Tests**: Critical module coverage
- **Integration Tests**: End-to-end workflow validation
- **Load Testing**: Concurrent task handling
- **Security Testing**: Penetration tests, fuzzing
- **Human Evaluation**: Annotation interface for output quality

---

## 📅 Timeline Overview

### Phase 0: Pre-start (2-4 weeks)
- Vision & Scope documentation ✓
- Critical Use Cases definition
- Architectural design
- PoC: Browser search + simple actions
- Team hiring plan

### Phase 1: MVP (8-12 weeks)
- Agent Core + Orchestration
- Operator (Playwright integration)
- Task Queue (SQLite → Redis)
- Basic Memory (conversation history)
- Web UI (task submission + logs)

### Phase 2: Hardening & Safety (8-12 weeks)
- Vector DB + RAG
- Policy Engine
- Sandboxed code execution
- Retry/DLQ logic
- Observability stack

### Phase 3: RPA Professional (12-16 weeks)
- DSL for operator commands
- Site maps & selector libraries
- Macro library (50+ workflows)
- Human-in-the-loop approvals

### Phase 4: Scale & Enterprise (12-20 weeks)
- Kubernetes deployment
- Multi-tenant isolation
- Cost control & billing
- Integration marketplace

### Phase 5: Continuous Evolution (Ongoing)
- Fine-tuning & RLHF
- Auto-repair flows
- Offline LLM support
- Plugin marketplace

**Total Time to Production:** 9-16 months (with 100-person team at full scale)

---

## 👥 Team & Resources

### Initial Team (Month 1-2)
1. **Product Lead** - Vision and prioritization
2. **Tech Lead / Architect** - Technical direction
3. **2x Backend Engineers** - Core orchestration
4. **2x ML/LLM Engineers** - AI integration
5. **1x RPA Engineer** - Playwright automation
6. **1x Security Engineer** - Policy and safety
7. **1x DevOps/SRE** - Infrastructure
8. **1x QA Engineer** - Testing strategy

### Scale-up Plan (Months 3-12)
- Grow to 30 people by Month 3 (MVP)
- Grow to 45 people by Month 6 (Hardening)
- Grow to 75 people by Month 9 (RPA Pro)
- Grow to 100 people by Month 12 (Enterprise-ready)

---

## ✅ Acceptance Criteria (Phase 0)

This phase is complete when:

- ✅ Vision & Scope document approved by stakeholders
- ✅ 10-20 prioritized Use Cases documented
- ✅ Logical architecture diagram created
- ✅ PoC demonstrates: search → open URL → read → screenshot
- ✅ Initial hiring plan defined
- ✅ Risk assessment completed
- ✅ Initial budget estimate prepared

---

## 📖 Related Documents

- [Use Cases](./USE_CASES.md) - Detailed user scenarios
- [Architecture](./ARCHITECTURE.md) - Logical architecture design
- [Roadmap](./DEVELOPMENT_ROADMAP.md) - Phased development plan
- [Risk Matrix](./RISK_MATRIX.md) - Risk assessment and mitigation
- [Hiring Plan](./HIRING_PLAN.md) - Team structure and roles

---

**Document Version History:**
- v1.0 (2025-10) - Initial Vision & Scope document
