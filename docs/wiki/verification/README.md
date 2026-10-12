---
title: "시험 및 검증 체계 (Verification)"
type: moc
status: active
tags:
  - domain/avionics
  - verification/hub
aliases:
  - Verification
  - 시험검증
created: 2026-10-12
updated: 2026-10-12
---

# 🧪 시험 및 검증 (Verification)

> [!NOTE]
> 비행 컴퓨터 및 서브시스템의 기능 동작, 안전 사양 충족 여부를 확인하는 시험 절차서, 결과 보고서 및 비행 형상 기록을 관리합니다.
> 전체 지식 맵은 [[docs/Index|Index (MOC)]]를 참조하십시오.

---

## 🗂️ 디렉터리 구성 및 문서 링크

- **[[docs/wiki/verification/matrix|요구사항 검증 매트릭스 (matrix.md)]]**: 핵심 요구사항별 시험 진행 상태 종합
- **`procedures/`**: 시험 절차서 모음 ([[docs/wiki/verification/procedures/_template|_template.md]])
- **`results/`**: 시험 수행 결과 기록 ([[docs/wiki/verification/results/_template|_template.md]])
- **`flight-manifests/`**: 실제 발사 탑재 HW/FW 형상 매니페스트 ([[docs/wiki/verification/flight-manifests/_template|_template.md]])

---

## 💡 기본 원칙

> [!IMPORTANT]
> 실패한 시험 결과나 오류 로그도 삭제하지 않고 그대로 기록하여 원인을 분석하고 개선합니다.

- 하드웨어 점검 및 안전 시험은 절차서(`procedures/`)를 미리 작성하여 순서대로 진행합니다.
- 시험 원본 로그(CSV, 고해상도 시험 영상)는 Git 대신 Google Drive 링크로 첨부합니다.
