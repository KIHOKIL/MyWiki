---
title: HW Change List E2E implementation loop
category: projects
tags: [project, agentic-engineering, phy-sw, mobile-modem]
sources: ["_source/Projects/HW Change List E2E implementation loop/handoff.md"]
created: "2026-08-10"
updated: "2026-08-10"
summary: A project to transform PHY SW Group's HW Change List response process into an AI-driven, E2E Agentic Engineering workflow.
base_confidence: 0.9
lifecycle: draft
lifecycle_changed: "2026-08-10"
tier: core
provenance:
  extracted: 0.8
  inferred: 0.2
  ambiguous: 0.0
relationships:
  - target: "[[concepts/evidence-driven-engineering]]"
    type: uses
  - target: "[[concepts/hw-change-contract]]"
    type: uses
  - target: "[[concepts/historical-hw-change-reconstruction]]"
    type: uses
  - target: "[[concepts/commit-linked-knowledge]]"
    type: uses
  - target: "[[concepts/e2e-agentic-engineering-workflow]]"
    type: uses
---

# HW Change List E2E implementation loop

This project aims to transform the Mobile Modem PHY SW Group's response to HW Change Lists from a manual, error-prone process into an AI-driven **E2E Agentic Engineering** workflow.

## Background & Objectives
In new chipset bring-up, HW changes are a constant (300-400 per chip). PHY SW must implement these changes and verify them. The current AS-IS process is highly manual, and misunderstandings of HW intent early on cause massive costs downstream in commercialization. The goal is to move from **Coverage-driven Verification** to **Evidence-driven Engineering** ^[extracted].

## Target AI Agent Architecture
The project does not seek a fully autonomous agent out of the gate. Instead, a multi-agent system with phased responsibility ^[extracted]:
1. **Change Analyst Agent**: Analyzes HW changes, impacts, risks, and history.
2. **Implementation Agent**: Implements low-risk changes, builds, and unit tests.
3. **Review Agent**: Provides evidence-based cross-checks of code against design guides and registers.
4. **Verification Agent**: Recommends risk-based verification (Static, UT, VP, Hybrid Zebu).
5. **Knowledge Agent**: Keeps the engineering knowledge base updated dynamically with code changes.

## Engineering Knowledge Base
To empower these agents, a static RAG is insufficient. The knowledge base must connect ^[inferred]:
- **Architecture**: Domains, state machines, messages.
- **Code Graph**: Call graphs, references, register accesses.
- **HW Knowledge**: Registers, bit fields, reset values.
- **Design Guide**: Interfaces, constraints, intents.

## Roadmap
- **Phase 0 (Foundation)**: Define contracts, schemas, and historical data.
- **Phase 1 (AI Review)**: AI analyzes impact and risks to improve human review.
- **Phase 2 (Low-risk AI Implementation)**: Automate patching for low-risk changes.
- **Phase 3 (Risk-based Verification)**: AI directs verification effort efficiently.
- **Phase 4 (E2E Agentic Engineering)**: Full integration from HW change to commercialization with knowledge feedback.

## Strategic Principles
- **Do not** just adopt an AI coding tool (Copilot/Claude).
- **Do not** rely solely on expanding Virtual Platform (VP) coverage.
- **Do not** build static RAG wikis.
- **Do not** jump to fully autonomous agents initially.
- **Do** standardize HW ↔ SW handoffs via Contracts.
- **Do** build traceablity in JIRA.
- **Do** establish feedback loops from Silicon/Commercial issues back to the knowledge base.
