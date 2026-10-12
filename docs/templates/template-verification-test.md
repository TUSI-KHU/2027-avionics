---
title: "TEST: {{title}}"
type: procedure
status: draft
tags:
  - domain/avionics
  - verification/test
aliases:
  - TEST-{{title}}
created: {{date}}
updated: {{date}}
---

# TEST: {{title}}

- **시험 ID**: TEST-{{date}}
- **작성일**: {{date}}
- **작성자**: 
- **대상 서브시스템**: HW / FW / GNC / GS
- **연관 요구사항**: [[docs/wiki/verification/matrix|REQ-SYS-NNN]]

---

## 1. 시험 목적 및 요구사항
- 무엇을 검증하기 위한 시험인지 기술합니다.

## 2. 시험 환경 및 준비물
- 시험 장비, 하드웨어 보드 버전, 펌웨어 빌드 커밋:

## 3. 안전 점검 (Safety Checklist)
- [ ] 전원 극성 및 과전류 리밋 확인
- [ ] 물리적 안전 핀 체결 확인

## 4. 절차 및 수행 결과

| 단계 | 수행 절차 | 예상 결과 | 실제 결과 | 판정 (P/F) |
|---|---|---|---|---|
| 1 | 전원 인가 및 부팅 | 정상 LED 점등 | | |
| 2 | 센서 입력 자극 | 고도/가속도 변화 감지 | | |
| 3 | 사출 신호 계측 | 1.0초 이내 펄스 출력 | | |

---

## 5. 결론 및 조치사항
- 시험 성공 여부 및 특이사항:

---

## 6. 연관 문서
- [[docs/wiki/verification/matrix|요구사항 검증 매트릭스]]
