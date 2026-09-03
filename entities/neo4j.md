---
title: Neo4j
category: entities
tags:
  - neo4j
  - graph-db
  - cypher
  - knowledge-graph
  - graph-rag
sources:
  - "[[_sources/Study/AI-Lectures/편한AI/20260903/Headroom_심층분석_및_Group_2nd_Brain_연계.md]]"
created: "2026-09-03"
updated: "2026-09-03"
summary: 노드와 엣지 기반의 그래프 데이터베이스이자, 다중 홉(Multi-hop) 지식 탐색 및 엔터프라이즈 Graph RAG(KG-MCP)의 핵심 백본 엔진.
base_confidence: 0.95
lifecycle: reviewed
tier: core
relationships:
  - target: "[[concepts/graph-rag]]"
    type: enables
---

# Neo4j

## 📌 개요
**Neo4j**는 가장 널리 사용되는 선도적인 오픈소스 및 엔터프라이즈 그래프 데이터베이스(Graph Database)입니다. 데이터를 테이블이나 단순 벡터 대신 **노드(Node: 개체)**, **엣지(Edge/Relationship: 관계)**, **속성(Property)**으로 모델링하며, 전용 질의어인 **Cypher**를 사용해 복잡한 네트워크를 초고속으로 탐색합니다.

---

## 🛠️ Graph RAG 및 Group 2nd Brain에서의 역할
1. **Multi-hop 관계 탐색의 백본:**
   - Vector DB가 해결하지 못하는 "문서 A ➡️ 도메인 룰 B ➡️ 검증 대상 C"와 같은 다단계 인과 관계 및 영향도 쿼리를 밀리초(ms) 단위로 탐색.
2. **KG-MCP (Knowledge Graph MCP):**
   - 에이전트가 Cypher 도구를 통해 그래프 DB의 서브그래프를 조회하는 프로토콜 환경에서, 단순 키워드/유사도 기반 MCP 대비 **정답률 50%p 이상 향상**을 달성하는 토대.
3. **자가 진화(Self-Evolving) 지식 저장소:**
   - 에이전트의 실행 성공/실패 로그와 해결 패턴을 그래프 관계(예: `(:Issue)-[:RESOLVED_BY]->(:Solution)`)로 누적 저장하여 시간이 갈수록 지식망이 스스로 진화하도록 지원.

---

## 🔗 연관 지식
- 개념: [[concepts/graph-rag|Graph RAG]], [[concepts/context-compression|Context Compression]]
- 연계 도구: [[entities/headroom|Headroom]]
