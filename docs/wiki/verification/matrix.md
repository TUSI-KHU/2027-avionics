---
title: "시스템 요구사항 검증 매트릭스 (Verification Matrix)"
type: verification
status: active
tags:
  - domain/avionics
  - verification/matrix
aliases:
  - VerificationMatrix
  - 검증매트릭스
created: 2026-10-12
updated: 2026-10-12
---

# 📊 시스템 요구사항 검증 매트릭스 (Verification Matrix)

> [!NOTE]
> [[docs/wiki/systems/system-overview|시스템 종합 개요]]에 정의된 시스템 핵심 요구사항(P0/P1)의 시험 절차서, 결과 보고서 및 검증 현황을 실시간으로 추적하는 단일 원본(SSOT) 매트릭스입니다.

---

## 📈 검증 상태 범례
- `✅ 완료(Passed)`: 시험 수행 완료 및 판정 기준 통과
- `⏳ 진행중(In Progress)`: 시험 절차서 작성 중 또는 시험 진행 중
- `⚪ 대기(Pending)`: 시험 계획 수립 대기

---

## 📋 요구사항별 검증 현황

| 요구사항 ID | 요구사항 내용 | 대상 서브시스템 | 우선순위 | 연관 위키 엔티티 | 시험 절차서 | 시험 결과 보고서 | 검증 상태 |
|---|---|---|---|---|---|---|---|
| **REQ-SYS-001** | 목표 고도 400 m 비행 환경에서 기구적/전기적 무결성 유지 | SYS, HW | P0 | [[docs/wiki/systems/flight-computer\|Flight Computer]] | [[docs/wiki/verification/procedures/README\|절차서]] | - | ⚪ 대기 |
| **REQ-SYS-002** | 정점 판정 후 1.0초 이내 사출 장치 격발 신호 인가 | FSW, HW | P0 | [[docs/wiki/systems/recovery-system\|Recovery System]] | [[docs/wiki/verification/procedures/README\|절차서]] | - | ⚪ 대기 |
| **REQ-SYS-003** | 비행 중 기압 및 9축 IMU 데이터 100 Hz 이상 로깅 | FSW | P0 | [[docs/wiki/systems/flight-computer\|Flight Computer]] | [[docs/wiki/verification/procedures/README\|절차서]] | - | ⚪ 대기 |
| **REQ-SYS-004** | 무선 통신 두절 시에도 사출 및 로깅 독자 완수 | FSW, SYS | P0 | [[docs/wiki/systems/flight-state-machine\|FSM]], [[docs/wiki/systems/recovery-system\|Recovery]] | [[docs/wiki/verification/procedures/README\|절차서]] | - | ⚪ 대기 |
| **REQ-SYS-005** | 비행 중 주요 상태 및 GPS 좌표 5 Hz 이상 지상국 전송 | RF, GS | P1 | [[docs/wiki/systems/telemetry-protocol\|Telemetry & RF]] | [[docs/wiki/verification/procedures/README\|절차서]] | - | ⚪ 대기 |

---

## 🤖 Karpathy LLM Wiki 큐레이터 동기화 지침
- 새로운 시험 결과 보고서([[docs/wiki/verification/results/]])가 작성되면, LLM 에이전트는 본 매트릭스의 연관 요구사항 `시험 결과 보고서` 링크와 `검증 상태`를 즉시 동기화합니다.
- 지침 전문은 [[docs/WIKI_PROTOCOL|LLM Wiki 큐레이터 프로토콜]]을 참조하십시오.
