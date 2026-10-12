---
title: "NURA Avionics 지식 베이스 안내"
type: moc
status: active
tags:
  - domain/avionics
  - documentation
created: 2026-10-12
updated: 2026-10-12
---

# 🚀 NURA Avionics 지식 베이스 (Obsidian & LLM Wiki)

NURA 400m 소형 로켓 Avionics 프로젝트의 모든 시스템 설계, 인터페이스, 의사결정 및 시험 문서를 관리하는 지식 베이스입니다.

> [!TIP]
> 본 저장소는 **Obsidian** 환경에 최적화되어 있으며, **Andrej Karpathy의 LLM Wiki** 패러다임을 따릅니다.
> 전체 지식 그래프를 탐색하려면 최상위 허브인 **[[docs/Index|docs/Index.md (MOC)]]**를 열어보세요.

---

## 🏛️ 지식 베이스 구조 (Karpathy 2-Tier Architecture)

```
docs/
├── Index.md                     # [MOC] Obsidian 그래프의 중심 허브이자 전체 지식 맵
├── WIKI_PROTOCOL.md             # LLM Wiki 큐레이터 운영 규약 및 컴파일 지침
├── README.md                    # 본 문서 (지식 베이스 안내)
│
├── raw/                         # [Layer 1: Raw Stream] 불변의 원시 입력 기록
│   ├── meetings/                # 날짜별 회의록 (불변 기록)
│   ├── research/                # 기술 조사 및 칩셋/수식 분석 원본
│   └── logs/                    # 일일 작업 및 디버깅 일지
│
├── wiki/                        # [Layer 2: Living Knowledge] 지속적으로 정제되는 영구 지식
│   ├── systems/                 # 서브시스템 엔티티 위키 (FSM, HW, Recovery, RF 등)
│   ├── interfaces/              # 하드웨어 핀맵 및 통신 패킷 프로토콜 명세
│   ├── decisions/               # 기술 의사결정 기록 (ADR)
│   ├── verification/            # 요구사항 검증 매트릭스 및 시험 절차/결과
│   └── reports/                 # PDR, CDR 등 공식 발표 및 분석 보고서
│
└── templates/                   # Obsidian 네이티브 템플릿 (Properties 포함)
```

---

## 🗺️ 주요 바로가기

| 구분 | 주요 문서 | 설명 |
|---|---|---|
| **중심 허브 (MOC)** | [[docs/Index\|Index.md]] | 전체 시스템, 인터페이스, 의사결정, 검증 종합 대시보드 |
| **운영 규약** | [[docs/WIKI_PROTOCOL\|WIKI_PROTOCOL.md]] | Karpathy LLM Wiki 큐레이터 프로토콜 및 컴파일 워크플로 |
| **시스템 종합** | [[docs/wiki/systems/system-overview\|system-overview.md]] | 400m 미션 목표, 비행 모드(FSM), 핵심 아키텍처 |
| **비행 상태 머신** | [[docs/wiki/systems/flight-state-machine\|flight-state-machine.md]] | 6단계 비행 FSM 및 결함 격리 로직 |
| **인터페이스** | [[docs/wiki/interfaces/README\|interfaces/]] | [[docs/wiki/interfaces/pinout-matrix\|MCU 핀맵]], [[docs/wiki/interfaces/packet-specs\|패킷 프로토콜]] |
| **의사결정 (ADR)** | [[docs/wiki/decisions/README\|decisions/]] | [[docs/wiki/decisions/ADR-001-mcu-selection\|ADR-001: ESP32-S3 및 ESP-IDF/FreeRTOS 선정]] |
| **검증 매트릭스** | [[docs/wiki/verification/matrix\|verification/matrix.md]] | 시스템 핵심 요구사항(REQ-SYS-001~005) 추적 |
| **원시 회의록** | [[docs/raw/meetings/README\|raw/meetings/]] | [[docs/raw/meetings/2026-10-12-kickoff\|2026-10-12 킥오프 회의록]] |

---

## ✍️ 문서 작성 및 AI 에이전트 활용 요령

1. **새로운 회의나 리서치 진행 시**:
   - `docs/raw/meetings/` 또는 `docs/raw/research/`에 원시 기록을 작성합니다.
   - Obsidian 템플릿(`Ctrl+T` or `Cmd+T`)을 사용하면 Frontmatter가 자동 완성됩니다.
2. **AI 에이전트에게 위키 컴파일 요청 시**:
   - `"방금 작성한 회의록을 Living Wiki에 반영해줘"`라고 요청하면, 에이전트가 [[docs/WIKI_PROTOCOL|큐레이터 프로토콜]]에 따라 자동으로 엔티티 갱신, ADR 등록, 검증 매트릭스 연동, 양방향 `[[wikilink]]` 연결을 수행합니다.
3. **사양 단정 금지 원칙**:
   - 아직 확정되지 않은 핀 할당이나 임계값은 임의로 단정하지 않고 `(미확정 - 팀원 논의 필요)` 상태로 명시합니다.
