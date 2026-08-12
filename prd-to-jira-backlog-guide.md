# PRD → Jira Backlog — Cursor Agent Guide

**Audience:** Product, TPM, and Engineering leads using Cursor + Atlassian MCP to turn Confluence PRDs into Jira backlogs.

**Last updated:** August 2026

**Related WBD docs:**
- [Product — PRDs and Jira Best Practices](https://wbdstreaming.atlassian.net/wiki/spaces/C360/pages/1310330550/Product+-+PRDs+and+Jira+Best+Practices)
- [Jira Field Standards — Required Fields by Level](https://wbdstreaming.atlassian.net/wiki/spaces/~6400e33a4307e46ad144cce5/pages/3806757531/Jira+Field+Standards+Required+Fields+by+Level)
- [Connect Atlassian to Cursor — Step-by-Step Guide](https://wbdstreaming.atlassian.net/wiki/spaces/~6400e33a4307e46ad144cce5/pages/3807610331/Connect+Atlassian+to+Cursor+Step-by-Step+Guide)

---

## What this guide does

When you share a **Product Requirements Document (PRD)** from Confluence, the Cursor agent will:

1. Read and analyze the PRD
2. Propose a **Feature → Capability → Epic → Story** breakdown aligned with WBD hierarchy
3. Wait for your approval
4. Create the approved issues in Jira **top-down** (parents before children)
5. Return links to everything created

**Ownership model (WBD standard):**
- **Product** creates Features and Capabilities (the *what* and *why*)
- **Engineering** typically creates Epics and Stories (the *how*)
- The agent can create all levels when asked, but **Stories are optional** — many teams stop at Epic and let eng refine

---

## Prerequisites

| Requirement | Details |
|---|---|
| Cursor + Atlassian MCP | Follow [Connect Atlassian to Cursor](https://wbdstreaming.atlassian.net/wiki/spaces/~6400e33a4307e46ad144cce5/pages/3807610331/Connect+Atlassian+to+Cursor+Step-by-Step+Guide) |
| Jira create permissions | You need `write:jira-work` on the target project |
| PRD in Confluence | A published PRD page with problem, opportunity, requirements, and success metrics |
| Project key | e.g. `MLG`, `CD`, `WBD` — know which Jira project to use |

### Optional: add the Cursor rule to your repo

Copy `.cursor/rules/prd-to-jira.mdc` from this guide's source repo into your project so the agent always follows WBD hierarchy rules when you ask about PRDs or Jira backlogs.

---

## Jira hierarchy (WBD standard)

```
Initiative
  └── Feature          ← 1 PRD ≈ 1 Feature
        └── Capability ← quarterly deliverable / KR chunk
              └── Epic ← execution container (eng-owned)
                    └── Story / Task / Bug / Spike
```

| Level | Purpose | Typical owner | Created from PRD? |
|---|---|---|---|
| **Initiative** | Strategic program, multi-quarter | Product / Leadership | Link existing only (usually) |
| **Feature** | Large releasable outcome | Product | **Yes** — maps 1:1 to PRD |
| **Capability** | Business-value chunk, often quarterly | Product | **Yes** — from requirements / KRs |
| **Epic** | Execution work package | Engineering Lead | **Yes, if requested** |
| **Story** | Team-level implementation | Engineering | **Only if requested** |

---

## Agent workflow (mandatory sequence)

The agent **must** follow this order:

### Step 1 — Fetch the PRD

Provide one of:
- Confluence URL: `https://wbdstreaming.atlassian.net/wiki/spaces/SPACE/pages/PAGE_ID/...`
- Page title (agent will search Confluence)

The agent calls `getConfluencePage` with `contentFormat: markdown`.

### Step 2 — Gather context

Before creating anything, the agent asks for:

| Input | Required? | Example |
|---|---|---|
| **Jira project key** | Yes | `MLG` |
| **Parent Initiative key** | If Feature needs one | `WBD-292` |
| **Depth to create** | Yes | `Feature + Capabilities only` or `through Epics` or `through Stories` |
| **Tracking label** | Recommended | `prd-backlog-v1` |
| **Group / Labels** | If project-specific | C360: Group = `MLG C360 Consumer 360`, Label = `mlg_c360_portfolio` |

If the user is unsure about projects, the agent lists available projects via `getVisibleJiraProjects`.

### Step 3 — Analyze the PRD (no Jira writes yet)

The agent extracts:

**For the Feature:**
- Summary = PRD title or objective (no domain tags in title — use Labels/Components)
- Description = PRD link + Problem, Opportunity, Impact, Use Cases (3–5 line synced summary, not link-only)
- Success metrics / KPIs from PRD Key Results

**For each Capability (target 3–7, not more unless PRD warrants it):**
- One stakeholder-facing deliverable per Capability
- Align with quarterly KRs where possible
- Acceptance criteria derived from PRD requirements
- Requirements that support the KR, copied/summarized from PRD

**For each Epic (if requested):**
- Execution container under a Capability
- Written for Engineering Lead ownership
- Definition of Ready checklist in description
- Acceptance criteria

**For each Story (if requested):**
- Independently deliverable, 1–5 day scope
- Testable acceptance criteria
- Parent = Epic

### Step 4 — Present breakdown for approval

The agent shows a tree **before creating anything**:

```
Proposed backlog for MLG (from PRD: "User Consent Management v2"):

Initiative: WBD-145 (existing, linked)

Feature: User Consent Management v2
├── Capability 1: GDPR consent capture & storage (Q4'26)
│   ├── Epic: Backend consent API
│   └── Epic: Web consent UI
├── Capability 2: Preference center self-service (Q1'27)
│   └── Epic: Preference center MVP
└── Capability 3: Audit & compliance reporting (Q1'27)
    └── Epic: Consent audit pipeline

Stories: 12 proposed (hold until Epic approval?)

Shall I create Feature + 3 Capabilities + 5 Epics in MLG?
```

**Wait for explicit confirmation.** If the user requests changes, re-present.

### Step 5 — Create issues top-down

**CRITICAL: Create parents before children.**

```
1. Feature        (parent = Initiative if provided)
2. Capabilities   (parent = Feature)
3. Epics          (parent = Capability)
4. Stories        (parent = Epic)
```

For each issue, the agent:
1. Calls `getJiraProjectIssueTypesMetadata` to confirm issue type names
2. Calls `getJiraIssueTypeMetaWithFields` if creation fails (required custom fields)
3. Calls `createJiraIssue` with `parent` set to the parent's key
4. Saves each created key for linking children

### Step 6 — Summary

Return all created keys with browse links and the source PRD URL.

---

## Required fields by level

Use [Jira Field Standards](https://wbdstreaming.atlassian.net/wiki/spaces/~6400e33a4307e46ad144cce5/pages/3806757531/Jira+Field+Standards+Required+Fields+by+Level) as source of truth. Minimum for agent-created issues:

### Feature

```markdown
## Overview
[1–2 sentences: what this Feature delivers]

## Source
PRD: [Confluence link]

## Problem
[From PRD]

## Opportunity
[From PRD]

## Impact
[From PRD — business/financial]

## Use Cases
- [Use case 1]
- [Use case 2]

## Success Metrics
- [KPI 1]
- [KPI 2]
```

**Fields:** Summary, Description, Owner (Product), Parent Initiative, Priority, Group, Planning Interval, Quarters, Labels

### Capability

```markdown
## Overview
[Deliverable this Capability ships]

## Source
PRD: [Confluence link]

## Quarterly KR
[Specific KR this Capability closes]

## Requirements
- [Requirement from PRD]
- [Requirement from PRD]

## Acceptance Criteria
- [ ] [Testable criterion]
- [ ] [Testable criterion]

## Out of Scope
- [Explicit exclusions]
```

**Fields:** Summary, Description, Owner (Product), Parent Feature, Priority, Target timeframe/PI, Estimate, Acceptance criteria

### Epic

```markdown
## Context
[Why this Epic exists under its Capability]

## Requirements
- [Requirement 1]
- [Requirement 2]

## Acceptance Criteria
- [ ] [Testable criterion]
- [ ] [Testable criterion]

## Definition of Ready
- [ ] Owner assigned (Engineering Lead)
- [ ] Acceptance criteria defined
- [ ] Dependencies identified
- [ ] Estimate provided

## Related
- PRD: [link]
- Capability: [parent key]
```

**Fields:** Summary, Description, Owner (Eng Lead), Parent Capability, Estimate, Acceptance criteria, Definition of Ready

### Story (when created)

```markdown
## User Story
As a [persona], I want [goal] so that [benefit].

## Context
[Brief context from PRD/Epic]

## Acceptance Criteria
- [ ] [Testable criterion]
- [ ] [Testable criterion]

## Related
- Epic: [parent key]
- PRD: [link]
```

---

## Breakdown principles

### Feature
- **One PRD → one Feature** (C360 standard)
- Exception: if another team owns the Feature, link PRD to Capability only

### Capabilities
- Limit to **deliverables that make business sense**, not one per requirement
- Align with **quarterly KRs** — Capabilities should close within a quarter when possible
- Order by **who they unblock**, not what's easiest to build
- Typical count: **3–7** per Feature

### Epics
- Group by **execution domain**: platform, backend, frontend, data, infra
- One Epic per platform team when work splits that way (see [Jira Epic Playbook](https://wbdstreaming.atlassian.net/wiki/spaces/GCX/pages/73335907/Jira+Epic+Playbook))
- Typical count: **1–3 Epics per Capability**

### Stories
- Only create when user explicitly requests or PRD has implementation-ready detail
- Size: independently completable in a sprint
- Include testable acceptance criteria
- Hold **Sub-tasks** until after Story review (create in a second pass)

---

## Prompt templates for team members

### Standard — Feature + Capabilities (Product)

```
Read this PRD and create Jira Feature + Capabilities following our PRD-to-Jira guide:
[Confluence PRD URL]

Project: MLG
Parent Initiative: WBD-145
Group: MLG C360 Consumer 360
Label: mlg_c360_portfolio
Do NOT create Epics or Stories yet — present the breakdown first.
```

### Full stack — through Epics

```
Convert this PRD to Jira through Epics (no Stories yet):
[Confluence PRD URL]

Project: CD
Parent Initiative: WBD-292
Tracking label: my-feature-v1
Present the full tree for approval before creating anything.
```

### Full backlog — through Stories

```
Create the full backlog from this PRD through Stories:
[Confluence PRD URL]

Project: MLG
Depth: Feature → Capabilities → Epics → Stories
Cap at 15 Stories for first pass; hold Sub-tasks.
Ask me about any required custom fields before creating.
```

### Add to existing Feature

```
This PRD adds scope to existing Feature MLG-1234.
Read: [Confluence PRD URL]
Propose new Capabilities (+ Epics if needed) under MLG-1234 only.
Do not recreate the Feature.
```

---

## Edge cases

| Scenario | Agent behavior |
|---|---|
| PRD spans multiple Features | Ask user: one Feature or split? Propose split with rationale |
| Existing Feature/Capability | Skip that level; link new children to existing keys |
| Required custom fields fail creation | Fetch field metadata; ask user for values; retry |
| 15+ Stories would be created | Present full plan; ask to cap first pass or split by Capability |
| Light / incomplete PRD | Create broader tickets; note "needs refinement" in descriptions |
| Another team owns the Feature | Link PRD to Capability only; skip Feature creation |
| Architecture impact | Flag Capability for ARCH-* review in description |

---

## Quality checklist (agent self-review before presenting)

- [ ] Feature summary has no domain tags (use Labels instead)
- [ ] Every issue has a self-contained description (not link-only)
- [ ] PRD link + 3–5 line synced summary on Feature and Capabilities
- [ ] Capabilities have acceptance criteria
- [ ] Parent chain is valid: Initiative → Feature → Capability → Epic → Story
- [ ] Ownership matches level (Product for Feature/Capability, Eng for Epic/Story)
- [ ] Tracking label applied to all created issues (if requested)
- [ ] User confirmed before any Jira writes

---

## Non-negotiables

1. **Never create Jira issues without user approval** of the proposed breakdown
2. **Always create top-down** — Feature before Capability before Epic before Story
3. **Respect ownership** — Product levels vs Engineering levels
4. **PRD is source of truth** — do not invent requirements not in the PRD; flag gaps instead
5. **Directory identities only** for assignees — correct casing, no duplicate names

---

## Example output

```
✅ Backlog created successfully!

Source PRD: https://wbdstreaming.atlassian.net/wiki/spaces/C360/pages/...

Feature: MLG-5678 — User Consent Management v2
https://wbdstreaming.atlassian.net/browse/MLG-5678

Capabilities:
1. MLG-5679 — GDPR consent capture & storage (Q4'26)
2. MLG-5680 — Preference center self-service (Q1'27)
3. MLG-5681 — Audit & compliance reporting (Q1'27)

Epics:
1. MLG-5682 — Backend consent API (under MLG-5679)
2. MLG-5683 — Web consent UI (under MLG-5679)
3. MLG-5684 — Preference center MVP (under MLG-5680)
4. MLG-5685 — Consent audit pipeline (under MLG-5681)

Label applied: prd-backlog-v1

Next steps:
- Assign owners (Product → Capabilities, Eng Lead → Epics)
- Fill project-specific fields (Regions, Products, Group)
- Engineering to break Epics into Stories during refinement
- Link Feature in PRD Summary section
```
