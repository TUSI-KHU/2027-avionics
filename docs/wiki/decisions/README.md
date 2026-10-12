---
title: "Architecture Decision Records (ADR) 레지스트리"
type: moc
status: active
tags:
  - domain/avionics
  - adr/hub
aliases:
  - Decisions
  - ADR
  - 의사결정기록
created: 2026-10-12
updated: 2026-10-12
---

# 🏛️ Architecture Decision Records (ADR)

> [!NOTE]
> 이 디렉터리는 주요 기술 선택, 아키텍처 결정, 부품 선정 및 규격 변경 결정을 기록하는 공간입니다.
> 전체 지식 맵은 [[docs/Index|Index (MOC)]]를 참조하십시오.

---

## 📋 ADR 등록 목록

| 번호 | 결정 제목 | 상태 | 결정일 | 관련 서브시스템 |
|---|---|---|---|---|
| [[docs/wiki/decisions/ADR-001-mcu-selection\|ADR-001]] | 주 비행 컴퓨터 MCU 및 펌웨어 플랫폼으로 ESP32-S3-WROOM-1-N16R8 (ESP-IDF + FreeRTOS) 선정 | `accepted` | 2026-10-12 | [[docs/wiki/systems/flight-computer\|Flight Computer]] |

---

## ✍️ 새 ADR 작성 절차

1. [[docs/wiki/decisions/_template|docs/wiki/decisions/_template.md]] (또는 [[docs/templates/template-adr|Obsidian 템플릿]])를 복사하여 `ADR-NNN-<주제-slug>.md`로 저장합니다.
2. YAML Frontmatter의 `status`를 `proposed`로 설정하고 배경, 대안 비교, 결정 내용, 영향을 작성합니다.
3. GitHub Pull Request를 통해 기술 검토 후 합의되면 `accepted`로 병합합니다.
