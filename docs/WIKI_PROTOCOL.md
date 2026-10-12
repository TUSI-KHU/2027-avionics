---
title: "Karpathy LLM Wiki 큐레이터 프로토콜"
type: guideline
status: active
tags:
  - protocol
  - llm-wiki
  - obsidian
  - guidelines
aliases:
  - WIKI_PROTOCOL
  - WikiProtocol
created: 2026-10-12
updated: 2026-10-12
---

# 🤖 Karpathy LLM Wiki 큐레이터 프로토콜

> **"Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."**  
> — Andrej Karpathy

본 문서는 NURA Avionics 프로젝트의 지식 베이스를 유지·관리할 때 팀원과 AI 에이전트(LLM)가 준수해야 하는 운영 계약(Contract)입니다.

---

## 1. 2계층 지식 아키텍처 (Two-Layer Architecture)

지식 베이스는 명확하게 두 개의 레이어로 분리됩니다:

```
[불변의 원시 입력]              [지속적인 정제/컴파일]
docs/raw/ (Raw Stream)  --->  docs/wiki/ (Living Knowledge)
 - 회의록 (meetings/)           - 서브시스템 (systems/)
 - 기술조사 (research/)         - 인터페이스 (interfaces/)
 - 작업일지 (logs/)             - 의사결정 (decisions/)
                               - 검증 매트릭스 (verification/)
```

### Layer 1: Raw Stream (`docs/raw/`)
- **불변성**: 사람이 회의하거나 작업하면서 남긴 날것의 기록(Raw input)입니다. 한 번 작성된 후에는 사실 왜곡을 방지하기 위해 임의로 삭제하거나 대폭 변형하지 않습니다.
- **역할**: LLM과 팀원이 진실의 근거(Provenance)를 추적할 수 있는 핑거프린트입니다.

### Layer 2: Living Wiki (`docs/wiki/`)
- **컴파일된 지식**: Raw Stream에서 추출된 사실, 사양, 아키텍처, 의사결정이 유기적으로 정리된 영구 지식(Evergreen notes)입니다.
- **단일 원본 (SSOT)**: 시스템의 현재 사양과 최신 합의는 항상 `docs/wiki/`의 해당 엔티티 노트가 유일한 원본입니다.

---

## 2. LLM 에이전트 큐레이션 파이프라인 (Compilation Workflow)

새로운 회의록이나 리서치가 `docs/raw/`에 추가되었을 때, LLM 에이전트는 아래 5단계 파이프라인에 따라 위키를 컴파일합니다:

```text
[새 Raw 문서 입력]
       |
       v
1. 사실 및 변경점 추출 (Fact Extraction)
       |
       v
2. 위키 엔티티 갱신 (Entity Update in docs/wiki/)
       |
       v
3. 상호 위키링크 연결 (Dense Interlinking via [[...]])
       |
       v
4. 의사결정 및 사양 추적 (ADR & Verification Sync)
       |
       v
5. 인덱스(Index.md / MOC) 반영 및 상태 보고
```

### 단계별 상세 행동 지침

1. **사실 및 변경점 추출**:
   - 새 회의록이나 리서치에서 서브시스템 사양(MCU, 센서, 통신 주기 등), 상태 머신 전이 조건, 핀 할당 등의 변경점을 식별합니다.
2. **위키 엔티티 갱신**:
   - 관련 엔티티 문서(`[[docs/wiki/systems/flight-state-machine]]`, `[[docs/wiki/interfaces/pinout-matrix]]` 등)를 찾아 업데이트합니다.
   - 확정되지 않은 사양은 임의로 단정하지 않고 `(미확정 - 팀원 논의 필요)` 상태로 명시합니다.
3. **상호 위키링크 연결**:
   - 관련된 문서끼리 반드시 양방향 또는 적절한 단방향 위키링크(`[[노트명]]`)를 삽입하여 Obsidian 그래프 뷰(Graph View)가 풍부하게 연결되도록 합니다.
4. **의사결정 및 검증 추적**:
   - 아키텍처 선택이나 부품 변경이 수반되는 경우 `[[docs/wiki/decisions/]]`에 새 ADR 초안을 제안합니다.
   - 시험 결과가 추가되면 `[[docs/wiki/verification/matrix]]`의 상태를 갱신합니다.
5. **Index(MOC) 갱신**:
   - 새 엔티티나 중요한 ADR이 추가된 경우 `[[docs/Index|docs/Index.md]]`에 링크를 등록합니다.

---

## 3. Obsidian 최적화 작성 규칙

### 3.1 YAML Frontmatter (Obsidian Properties) 필수
모든 Markdown 문서의 맨 앞에는 아래의 속성(Properties)을 포함해야 합니다:

```yaml
---
title: "문서 제목"
type: moc | system | interface | adr | procedure | result | report | raw-meeting | raw-research | raw-log | guideline
status: draft | active | accepted | deprecated | in-progress
tags:
  - domain/avionics
  - system/... # 필요 시
aliases:
  - 문서별칭1
  - 문서별칭2
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

### 3.2 위키링크(Wikilinks) 표기
- Obsidian 내부 링크는 표준 Wikilink 문법을 사용합니다:
  - 동일 폴더 또는 유니크한 파일명: `[[flight-state-machine]]` 또는 `[[flight-state-machine|비행 상태 머신]]`
  - 명확한 경로 표기: `[[docs/wiki/systems/flight-state-machine|비행 상태 머신]]`
- GitHub 렌더링 호환성도 고려하여 상대 경로가 포함된 위키링크 또는 유효한 파일명을 유지합니다.

### 3.3 Obsidian 콜아웃(Callouts) 적극 활용
문서의 가독성과 위험 요소 강조를 위해 Obsidian 콜아웃을 사용합니다:

```markdown
> [!NOTE]
> 설계 배경 및 참고 사항

> [!IMPORTANT]
> 안전 필수 요건 및 필수 준수 사항

> [!WARNING]
> 오작동 위험 및 하드웨어 파손 주의

> [!TIP]
> 디버깅 팁 및 개발 권장 사항
```

### 3.4 상태 전이 및 약어 표기
- 상태 머신 전이 표기는 ASCII `->`를 사용합니다 (`[ARMED] -> [BOOST]`).
- 모듈 및 신호 명칭은 한국어와 영문을 일관성 있게 병기합니다.
