---
title: "[시험 결과 보고서 제목]"
type: result
status: draft
tags:
  - domain/avionics
  - verification/result
aliases:
  - TEST-RES-NNN
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# [시험 결과 보고서 제목]

- **시험 ID**: TEST-RES-NNN (관련 절차서: [[docs/wiki/verification/procedures/_template|절차서 링크]])
- **수행 일시**: YYYY-MM-DD HH:MM
- **시험 수행자**: 
- **시험 결과**: ✅ 통과(Passed) / ❌ 실패(Failed) / ⚠️ 조건부 통과
- **연관 요구사항**: [[docs/wiki/verification/matrix|REQ-SYS-NNN]]

---

## 1. 시험 환경 및 형상
- **하드웨어**: FC Main Board Rev 1.0 (보드 번호: #1)
- **펌웨어 Git Commit**: `main` (커밋 해시)
- **설정 파일**: `configs/default.yaml`

## 2. 시험 결과 요약

| 시험 항목 | 판정 기준 | 측정/확인 결과 | 합격 여부 |
|---|---|---|---|
| 정점 감지 반응 시간 | 1.0초 이내 | 0.42초 | Pass |
| 사출 신호 펄스 폭 | 1.0초 이상 | 1.20초 | Pass |

## 3. 관찰 사항 및 발견된 문제점

> [!NOTE]
> 실패하거나 이상 징후가 발견된 기록도 삭제하지 않고 개선 추적용으로 보존합니다.

- 시험 중 특이사항, 이상 동작이나 발견된 버그를 기록합니다.
- (예: 고속 샘플링 시 플래시 쓰기 지연 2ms 발생 -> 버퍼 크기 확장 검토 필요)

## 4. 관련 데이터 및 증빙
- 측정 원본 데이터, 오실로스코프 캡처, 테스트 영상 링크 (Google Drive 등):
- [Google Drive 데이터 폴더 링크](https://drive.google.com/...)

---

## 5. 연관 문서
- [[docs/wiki/verification/matrix|요구사항 검증 매트릭스]]
