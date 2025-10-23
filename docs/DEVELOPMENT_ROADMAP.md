# 🗺️ MIRAI - Development Roadmap

**Version:** 1.0  
**Date:** October 2025  
**Status:** Phase 0 - Discovery

---

## 📅 Timeline Overview

```
Phase 0: Discovery          ████████ (2-4 weeks)     ✓ Current
Phase 1: MVP               ████████████ (8-12 weeks) → Next
Phase 2: Hardening         ████████████ (8-12 weeks)
Phase 3: RPA Professional  ████████████████ (12-16 weeks)
Phase 4: Scale & Enterprise████████████████████ (12-20 weeks)
Phase 5: Evolution         ████████████████████████ (Ongoing)
─────────────────────────────────────────────────────────────
Total to Production:       9-16 months (with full team)
```

---

## 🎯 Phase 0: Pre-start / Discovery (2-4 weeks)

**Goal:** Align vision, requirements, risks; assemble core team; build PoC

### Team Size: 8-10 people
- 1 Product Lead
- 1 Tech Lead / Architect
- 2 Backend Engineers
- 2 ML/LLM Engineers
- 1 RPA Engineer
- 1 Security Engineer
- 1 DevOps/SRE

### Week 1-2: Documentation & Planning

**Deliverables:**
- ✅ Vision & Scope document (1-2 pages)
- ✅ Critical Use Cases (10-20 scenarios with priority)
- ✅ Logical Architecture sketch
- ✅ Initial risk assessment
- ✅ Budget estimate

**Activities:**
- Product workshop (2 days) - Define product, business value, success metrics
- Security & Legal workshop - Data privacy, compliance requirements
- Architecture design sessions - Component breakdown, tech stack decisions
- Team structure planning - Define roles, responsibilities, hiring needs

### Week 3-4: Technical PoC

**Goal:** Prove technical feasibility

**PoC Scope:**
1. Open browser via Playwright with CDP
2. Perform Google search for "Python 3.12 features"
3. Open top 3 search results
4. Extract text content from pages
5. Take screenshots
6. Generate summary using GPT-4o-mini
7. Display results in terminal

**Success Criteria:**
- ✅ PoC executes 3 key scenarios successfully
- ✅ Browser automation works reliably
- ✅ LLM integration functional
- ✅ No major technical blockers identified

**Acceptance Criteria:**
- PoC demonstrates search → read → screenshot on local machine
- Document lists 10 prioritized features for MVP scope
- Team of 10 hired or committed

---

## 🚀 Phase 1: MVP - Core Agent (8-12 weeks)

**Goal:** Ship working MIRAI MVP - brain + operator, basic memory, API, basic UI

### Team Size: ~30 people
- 1 Product Lead, 2 PMs
- 6 Backend Engineers (API, orchestration, queue)
- 6 ML/LLM Engineers (prompts, model infra)
- 4 Operator/RPA Engineers (Playwright, automation)
- 4 SRE/Infra (K8s, CI/CD, monitoring)
- 4 QA/Automation Engineers
- 2 UX/UI, 1 Designer
- 1 Security/DevSecOps
- 1 Data Engineer
- 1 Tech Writer

### Sprint Plan (2-week sprints, 5-6 total)

#### Sprint 1: Foundation (Weeks 1-2)
**Focus:** Core infrastructure and scaffolding

**Deliverables:**
- API scaffolding (FastAPI)
  - `/ask` - Submit query
  - `/tasks` - List tasks
  - `/status` - Task status
  - `/health` - Health check
- Authentication (JWT tokens)
- Task queue skeleton (SQLite)
- Operator API stub (Playwright integration)
- CI/CD pipeline setup (GitHub Actions)
- Development environment setup

**Acceptance:**
- API responds to requests
- Auth protects endpoints
- CI pipeline runs tests

#### Sprint 2: Browser Automation (Weeks 3-4)
**Focus:** Operator with Playwright CDP

**Deliverables:**
- Playwright CDP connector
- Browser commands:
  - `open_url(url)` - Navigate to URL
  - `click(selector)` - Click element
  - `type_text(selector, text)` - Type into input
  - `read_page()` - Extract page content
  - `screenshot()` - Capture screenshot
- Session management (persistent browser contexts)
- Simple command executor

**Acceptance:**
- Browser opens and navigates successfully
- Commands execute reliably (≥90% success rate)
- Screenshots captured correctly

#### Sprint 3: LLM Integration (Weeks 5-6)
**Focus:** AI intelligence and tool calling

**Deliverables:**
- OpenAI API integration
  - GPT-4o-mini as main model
  - GPT-3.5-turbo as fallback
- Tool calling framework
  - `web_search(query)`
  - `open_url(url)`
  - `read_page()`
  - `execute_python(code)`
- Prompt templates for common tasks
- Token usage tracking
- Error handling and retries

**Acceptance:**
- LLM responds to queries
- Tool calls execute correctly
- Token usage logged

#### Sprint 4: Memory & UI (Weeks 7-8)
**Focus:** Persistence and user interface

**Deliverables:**
- Memory database (SQLite)
  - Sessions table
  - Messages table
  - User preferences table
  - Tasks history table
- Memory manager API
  - Save/retrieve conversations
  - User preference storage
  - Session management
- Web UI (Flask)
  - Submit task form
  - Task list view
  - Logs viewer
  - Basic styling
- Terminal UI improvements (Rich)

**Acceptance:**
- Conversations persist across restarts
- UI allows task submission and monitoring
- Memory retrieves context correctly

#### Sprint 5: Testing & QA Hardening (Weeks 9-10)
**Focus:** Quality and reliability

**Deliverables:**
- Unit tests for core modules
  - Agent core
  - Memory manager
  - Operator
  - API endpoints
- Integration tests
  - End-to-end task execution
  - Browser automation flows
  - API workflows
- Performance tests
  - Load testing (10 concurrent tasks)
  - Latency measurements
- Bug fixing
- Documentation updates

**Acceptance:**
- Test coverage ≥70% for core modules
- E2E smoke tests pass
- Performance meets SLOs (< 30s median latency)

#### Sprint 6: Security & Release Prep (Weeks 11-12)
**Focus:** Security hardening and deployment

**Deliverables:**
- Security checklist
  - Input validation
  - SQL injection prevention
  - XSS prevention
  - CSRF tokens
- Panic stop mechanism (emergency shutdown)
- Audit logging
- Deployment scripts
- User documentation
- Release notes

**Acceptance:**
- Security audit passes
- Deployment runbook complete
- MVP ready for beta users

### MVP Deliverables Summary

**Core Features:**
1. ✅ Agent Core - Orchestration, LLM integration, tool calling
2. ✅ Operator - Playwright CDP, basic commands
3. ✅ Task Queue - SQLite-based reliable queue
4. ✅ Memory - Conversation history, user preferences
5. ✅ Basic UI - Web interface for task management
6. ✅ Monitoring - Logs, basic metrics
7. ✅ Security - Token auth, panic stop

**Success Criteria:**
- End-to-end: user → agent → operator → result (≥80% reliability)
- Median task completion < 30s for search→read→summary
- Basic security: token auth, panic stop, logs
- Test coverage: unit tests + E2E smoke tests
- KPIs tracked: success rate, latency, crashes, token spend

---

## 🛡️ Phase 2: Hardening, Safety & Memory (8-12 weeks)

**Goal:** Production-grade reliability, security, and learning

### Team Size: ~45 people
- Existing 30 + additions:
- +6 ML Engineers (eval, embeddings, retrieval)
- +4 Data Annotators / Evaluators
- +3 Security Engineers
- +2 Product Ops / Release Managers

### What We Build

#### Vector DB + RAG (Weeks 1-3)
**Components:**
- Embeddings pipeline (text-embedding-3-large)
- Vector database (FAISS or Chroma)
- Document ingestion
- Semantic search API
- RAG integration with LLM

**Success Metrics:**
- Retrieval accuracy ≥85%
- Query latency < 2s
- Supports 10k+ documents

#### Policy Engine (Weeks 2-4)
**Components:**
- YAML-driven rule engine
- Risk scoring algorithm
- Approval workflow UI
- Domain blacklist/whitelist
- Command whitelisting
- Audit log integration

**Example Policy:**
```yaml
rules:
  - name: "file_deletion"
    pattern: "delete|rm|remove"
    requires_approval: true
    risk_level: high
    
  - name: "web_browsing"
    action: "open_url"
    domain_blacklist:
      - "*.onion"
      - "malicious-site.com"
```

**Success Metrics:**
- Policy evaluation < 50ms
- 100% enforcement (zero bypasses)
- All decisions logged

#### Sandboxed Code Execution (Weeks 3-6)
**Components:**
- Docker-based sandbox
- Resource limits (CPU, memory, disk)
- Network isolation
- Timeout enforcement
- Language runtimes (Python, Node, Go, Rust, C/C++, Bash)

**Success Metrics:**
- Execution isolated (zero escapes)
- Timeout enforcement reliable
- Supports 8 languages

#### Robust Operator (Weeks 4-8)
**Components:**
- Retry logic with exponential backoff
- Dead Letter Queue (DLQ) for failed tasks
- Window focus handling
- Captcha detection + human fallback
- Selector fallbacks (multiple strategies)
- Error classification

**Success Metrics:**
- Retry success rate ≥70%
- Captcha detection accuracy ≥90%
- Graceful degradation on failures

#### Observability (Weeks 5-10)
**Components:**
- Distributed tracing (OpenTelemetry)
- Metrics dashboards (Grafana)
- Alerting rules (PagerDuty)
- Cost tracking dashboard
- Performance profiling
- Log aggregation (ELK or equivalent)

**Dashboards:**
- System health overview
- Task success/failure rates
- LLM token usage and costs
- Browser automation metrics
- Database performance

#### Evaluation Framework (Weeks 6-12)
**Components:**
- Automated evaluation suite
- Factuality checks
- Safety checks
- Hallucination detection
- Human review UI
- A/B testing framework

**Metrics:**
- Hallucination rate target: ≤5%
- Safety violation rate: 0%
- Human review efficiency

### Acceptance Criteria (Phase 2)

- ✅ Vector DB + RAG: ≤5% hallucination on benchmark tasks
- ✅ Policy engine: No high-risk commands execute without approval
- ✅ Sandbox: Zero escape attempts succeed
- ✅ Load test: 50 concurrent tasks with SLOs met
- ✅ Observability: All key metrics tracked and dashboarded
- ✅ Canary deployment flow operational

---

## 🤖 Phase 3: Operator Pro & RPA at Scale (12-16 weeks)

**Goal:** Full RPA - complex website flows, multi-step transactions, macro library

### Team Size: ~65 people
- Existing 45 + additions:
- +8 RPA Engineers (domain mappers, selector engineers)
- +4 Automation QA
- +4 SRE (scale & infrastructure)
- +4 Integrations (APIs: Google, Slack, Calendar, etc.)

### What We Build

#### DSL for Operator (Weeks 1-4)
**Domain-Specific Language for RPA:**

```python
# Example DSL
workflow = {
    "name": "Login and Extract Data",
    "steps": [
        {"action": "OPEN", "url": "https://example.com/login"},
        {"action": "WAIT", "selector": "#username"},
        {"action": "TYPE", "selector": "#username", "text": "user@example.com"},
        {"action": "TYPE", "selector": "#password", "text": "{{SECRET}}"},
        {"action": "CLICK", "selector": "#login-button"},
        {"action": "WAIT", "selector": ".dashboard"},
        {"action": "SCRAPE", "selector": ".data-table", "output": "data"},
    ]
}
```

**Components:**
- DSL parser
- Step executor
- Variable interpolation
- Error handling per step
- Step-level rollback

#### Site Maps & Selector Libraries (Weeks 2-8)
**Curated selectors for popular sites:**

```yaml
sites:
  - domain: "linkedin.com"
    actions:
      login:
        username_field: "#username"
        password_field: "#password"
        submit_button: ".btn-primary"
      search:
        search_box: ".search-global-typeahead input"
        results_list: ".search-results-list"
```

**Priority Domains:**
- LinkedIn (professional networking)
- YouTube (content management)
- Gmail (email automation)
- GitHub (repository management)
- Notion (documentation)
- Slack (messaging)
- Google Calendar (scheduling)
- +40 more

**Success Metrics:**
- 50+ domain site maps
- Selector accuracy ≥95%
- Fallback strategies for DOM changes

#### Stateful Sessions (Weeks 4-10)
**Components:**
- Persistent browser profiles
- Cookie/localStorage management
- Session vault (encrypted credentials)
- Multi-account support
- Session expiry handling

**Use Cases:**
- Stay logged into services
- Reuse authentication
- Manage multiple accounts safely

#### Macro Library (Weeks 5-12)
**Prebuilt workflows:**

1. **Login + Extract** - Authenticate and scrape data
2. **Price Watch** - Monitor product prices
3. **Form Filler** - Auto-fill repetitive forms
4. **Report Generator** - Collect data, generate report
5. **Social Media Post** - Publish to multiple platforms
6. **Email Parser** - Extract structured data from emails
7. **Calendar Sync** - Sync events across calendars
8. **File Upload** - Bulk upload to services
9. **Screenshot Capture** - Automated visual testing
10. **Data Export** - Export from web apps
... 40+ more macros

**Macro Format:**
```yaml
macro:
  name: "LinkedIn Profile Scraper"
  version: "1.0"
  description: "Extract profile data from LinkedIn"
  inputs:
    - profile_url
  outputs:
    - name
    - title
    - company
    - skills
  steps:
    - action: open_url
      url: "{{profile_url}}"
    - action: scrape
      selectors:
        name: "h1.text-heading-xlarge"
        title: ".text-body-medium"
        # ... more selectors
```

#### Operator Monitoring (Weeks 8-14)
**Components:**
- Step-by-step execution viewer
- Visual replay (screenshot per step)
- Step abort/resume
- Manual intervention mode
- Error diagnostics

**UI Features:**
- Real-time step progress
- Screenshot history
- Selector highlighting
- Error details with suggestions

#### Human-in-the-Loop (Weeks 10-16)
**Components:**
- Risk-based intervention
- Step approval UI
- Manual correction mode
- Training data collection
- Feedback loop to improve automation

**Approval Triggers:**
- High-risk actions (delete, purchase)
- Unknown domain
- Captcha detected
- Confidence < threshold

### Acceptance Criteria (Phase 3)

- ✅ DSL + editor: Non-technical users can create workflows
- ✅ 50+ domain macros: Library covers top use cases
- ✅ Operator reliability: ≥95% on curated flows
- ✅ End-to-end: 10 core workflows execute without manual intervention
- ✅ Robustness: Selector fallbacks handle common DOM changes

---

## 📈 Phase 4: Scale, Multi-instance & Orchestration (12-20 weeks)

**Goal:** Enterprise-ready - scale, multi-tenancy, marketplace

### Team Size: ~100 people
- Existing 65 + additions:
- +10 Backend & Infra SRE
- +8 Distributed Systems Engineers
- +6 QA Automation
- +4 Customer Success / Onboarding
- +4 Legal & Compliance
- +3 Data Privacy / Security Ops

### What We Build

#### Kubernetes Deployment (Weeks 1-6)
**Components:**
- Helm charts for all services
- Canary deployments
- Blue/green deployments
- Autoscaling (HPA, VPA)
- Multi-region support
- Disaster recovery plan

**Infrastructure:**
```yaml
# Kubernetes resources
- Agent Core: Deployment (3+ replicas)
- Operator: StatefulSet (browser pool)
- API Gateway: Deployment (autoscale 2-10)
- Task Queue: Redis Cluster
- Database: PostgreSQL (primary + replicas)
- Monitoring: Prometheus + Grafana
```

#### Distributed Queue (Weeks 2-8)
**Components:**
- Redis Cluster (HA)
- Worker pool management
- Priority queue implementation
- Fair scheduling
- Queue health monitoring

**Features:**
- Handles 1000+ tasks/minute
- No single point of failure
- Fair distribution across workers

#### Multi-Tenant Isolation (Weeks 4-10)
**Components:**
- Tenant database (per-tenant schemas)
- Resource quotas (CPU, memory, tokens)
- Billing system integration
- Tenant-specific policies
- Data isolation guarantees

**Isolation Strategy:**
- Database: Schema per tenant
- Queue: Namespace per tenant
- Browser: Separate profiles per tenant
- Storage: S3 bucket per tenant

#### Cost Control & Budget Guard (Weeks 6-12)
**Components:**
- Token budget per tenant/team
- Alert thresholds
- Auto-pause on budget exceeded
- Cost optimization recommendations
- Detailed billing reports

**Budget Policy:**
```yaml
tenant:
  monthly_budget: 1000  # USD
  alert_at: 800         # 80% threshold
  pause_at: 1000        # Hard limit
```

#### Integration Framework (Weeks 8-16)
**Connectors Marketplace:**
1. **Google Workspace** - Gmail, Calendar, Drive, Docs
2. **Slack** - Messaging, channels, notifications
3. **Notion** - Pages, databases, blocks
4. **GitHub** - Repos, PRs, Issues, Actions
5. **Jira** - Projects, tickets, sprints
6. **Jenkins** - CI/CD pipelines
7. **AWS** - S3, Lambda, CloudWatch
8. **Stripe** - Payments, invoices
9. **Salesforce** - CRM operations
10. **Zoom** - Meetings, recordings
... 20+ more connectors

**Connector API:**
```python
class Connector(ABC):
    @abstractmethod
    def authenticate(self, credentials: Dict):
        pass
        
    @abstractmethod
    def execute_action(self, action: str, params: Dict):
        pass
```

#### Customer Onboarding (Weeks 10-18)
**Deliverables:**
- Onboarding wizard (UI)
- Video tutorials (10+ videos)
- Documentation site (100+ pages)
- Sample workflows (30+ examples)
- Training materials
- Certification program

**Onboarding Flow:**
1. Sign up + verify email
2. Create first workspace
3. Configure integrations (optional)
4. Run "Hello World" workflow
5. Try sample macros
6. Create custom workflow
7. Invite team members

### Acceptance Criteria (Phase 4)

- ✅ Kubernetes: Sustains X concurrent users (business-defined) with SLOs
- ✅ Recovery: RTO < 15 minutes for critical failures
- ✅ Multi-tenancy: Complete data isolation verified
- ✅ Cost control: Budget enforcement 100% effective
- ✅ Integrations: 20+ connectors available and tested
- ✅ Onboarding: ≤30 minutes for new user to first workflow

---

## 🧬 Phase 5: Enterprise Features, ML Research, Continuous Improvement (Ongoing)

**Goal:** Cutting-edge capabilities, continuous evolution

### Focus Areas

#### Fine-tuning & Domain Adaptation
- Fine-tune GPT models for specific domains
- Retrieval-augmented tuning
- Domain-specific prompt optimization
- Specialized models (code, legal, medical - with proper licensing)

#### Advanced Evaluation
- RLHF loops (human feedback)
- Synthetic data generation for testing
- Adversarial testing
- Continuous quality monitoring

#### Auto-Repair Flows
**Intelligent error recovery:**
```python
def handle_failure(task, error):
    # Analyze error
    root_cause = analyze_error(error)
    
    # Generate alternative approach
    alternative = generate_alternative_strategy(task, root_cause)
    
    # Retry with new strategy
    retry_with_strategy(task, alternative)
```

#### Offline LLM Support
- Local model deployment (Ollama, LLaMA)
- On-premise installations
- Air-gapped environments
- Privacy-first deployments

#### Marketplace Evolution
- User-created macros
- Third-party plugins
- Revenue sharing model
- Certification program
- Community ratings/reviews

---

## 📊 Resource Planning

### Budget Estimates (Annual, USD)

| Phase | Team Size | Salaries ($150k avg) | Infrastructure | LLM API | Total |
|-------|-----------|---------------------|----------------|---------|-------|
| Phase 0 | 10 | $250k (2 months) | $5k | $1k | $256k |
| Phase 1 | 30 | $900k (3 months) | $20k | $5k | $925k |
| Phase 2 | 45 | $1.4M (3 months) | $40k | $10k | $1.45M |
| Phase 3 | 65 | $2.0M (4 months) | $80k | $20k | $2.1M |
| Phase 4 | 100 | $3.1M (5 months) | $150k | $30k | $3.28M |
| **Total Year 1** | **100** | **$7.65M** | **$295k** | **$66k** | **~$8M** |

*Note: Estimates are rough and vary by location, seniority, market conditions*

### Infrastructure Scaling

| Phase | Compute | Storage | Network | LLM Tokens/mo | Est. Cost/mo |
|-------|---------|---------|---------|---------------|--------------|
| MVP | 4 vCPU, 8GB | 100GB | <1TB | 1M | $500 |
| Phase 2 | 16 vCPU, 32GB | 500GB | <5TB | 10M | $2k |
| Phase 3 | 64 vCPU, 128GB | 2TB | <20TB | 50M | $8k |
| Phase 4 | 256+ vCPU, 512GB+ | 10TB+ | <100TB | 200M+ | $30k+ |

---

## 🎯 Success Metrics by Phase

### Phase 1 (MVP)
- **Task Success Rate:** ≥80%
- **Latency:** < 30s median
- **Uptime:** ≥95%
- **Test Coverage:** ≥70%

### Phase 2 (Hardening)
- **Task Success Rate:** ≥85%
- **Latency:** < 25s median
- **Uptime:** ≥99%
- **Hallucination Rate:** ≤5%

### Phase 3 (RPA Pro)
- **Workflow Success:** ≥95% on curated macros
- **Latency:** < 20s median
- **Macro Library:** 50+ workflows
- **Uptime:** ≥99.5%

### Phase 4 (Enterprise)
- **Scale:** Support 1000+ concurrent tasks
- **Multi-tenancy:** 100% data isolation
- **RTO:** < 15 minutes
- **Customer Satisfaction:** ≥4.5/5

### Phase 5 (Evolution)
- **Continuous improvement:** 10%+ efficiency gain per quarter
- **Community plugins:** 50+ available
- **Auto-repair:** 70%+ failures auto-resolved

---

## 🚧 Risk Management

### Critical Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Unpredictable agent actions | Medium | High | Policy engine, manual approvals, sandboxing |
| Captcha/bot detection | High | Medium | Fallback APIs, human-in-loop, stealth mode |
| Secret leakage | Low | Critical | Vault, audit logs, no secrets in code |
| LLM cost explosion | High | High | Budget guards, model tiering, local fallback |
| DOM changes breaking RPA | High | Medium | Selector maps, ML visual selectors, monitoring |
| Team scaling challenges | Medium | High | Experienced hires, clear processes, mentorship |
| Technical debt accumulation | Medium | High | Regular refactoring, code reviews, 20% time |

---

## ✅ Acceptance Criteria Summary

### Phase 0 Complete When:
- ✅ Vision & Scope approved
- ✅ 10-20 Use Cases defined
- ✅ Architecture designed
- ✅ PoC demonstrates browser search + actions
- ✅ Core team hired

### Phase 1 Complete When:
- ✅ E2E: user → agent → operator → result (≥80%)
- ✅ Latency: < 30s median
- ✅ Security: auth, panic stop, logs
- ✅ Tests: unit + E2E coverage

### Phase 2 Complete When:
- ✅ RAG: ≤5% hallucination
- ✅ Policy: 100% enforcement
- ✅ Load: 50 concurrent tasks
- ✅ Observability: full dashboards

### Phase 3 Complete When:
- ✅ 50+ macros
- ✅ ≥95% reliability on curated workflows
- ✅ DSL + editor functional
- ✅ 10 core workflows execute autonomously

### Phase 4 Complete When:
- ✅ Kubernetes deployed
- ✅ Multi-tenant isolation verified
- ✅ RTO < 15 min
- ✅ 20+ integrations live

---

**Document Version History:**
- v1.0 (2025-10) - Initial comprehensive roadmap
