---
title: Evidence-driven Engineering
category: concepts
tags: [concept, verification, agentic-engineering, testing]
sources: ["_source/Projects/HW Change List E2E implementation loop/handoff.md"]
created: "2026-08-10"
updated: "2026-08-10"
summary: A verification philosophy prioritizing complete evidence chains over 100% simulation coverage.
base_confidence: 0.9
lifecycle: draft
lifecycle_changed: "2026-08-10"
tier: core
provenance:
  extracted: 0.9
  inferred: 0.1
  ambiguous: 0.0
---

# Evidence-driven Engineering

**Evidence-driven Engineering** is a paradigm shift away from traditional "Coverage-driven Verification" (which aims for 100% test coverage) toward building a complete "evidence chain" for every change ^[extracted].

## Core Philosophy
The core philosophy is that it is impossible or highly inefficient to achieve 100% simulation coverage for complex hardware behaviors, such as Modem HW behaviors in a Virtual Platform (VP) ^[extracted]. Instead of blindly increasing test cases, the focus is on ensuring that **every hardware change has at least one independent piece of evidence** verifying its correctness.

## Evidence Sources
Evidence can be assembled from multiple risk-based sources ^[extracted]:
- Static Analysis & Code Graph checks
- [[concepts/hw-change-contract|HW Change Contract]] Consistency
- Automated Code Review
- Unit Tests (UT)
- Focused Virtual Platform (VP) simulation
- Focused Hybrid Zebu simulation
- Silicon Evidence

By classifying the risk of a change (e.g., Low, Medium, High, Critical), engineers and AI agents can select the minimum required evidence chain to ensure quality without wasting resources on unnecessary full-coverage simulations ^[inferred].
