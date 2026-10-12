---
title: "[시험 절차서 제목]"
type: procedure
status: draft
tags:
  - domain/avionics
  - verification/procedure
aliases:
  - TEST-PROC-NNN
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# [시험 절차서 제목]

- **시험 ID**: TEST-PROC-NNN
- **작성일**: YYYY-MM-DD
- **작성자**: 
- **관련 Issue**: #
- **대상 서브시스템**: HW / FW / GNC / GS
- **연관 요구사항**: [[docs/wiki/verification/matrix|REQ-SYS-NNN]]

---

## 1. 시험 목적
- 이 시험을 통해 무엇을 확인하고 검증하는지 작성합니다.
- (예: 비행 컴퓨터 정점(Apogee) 판정 및 낙하산 사출 신호 인가 동작 검증)

## 2. 준비물 및 시험 환경
- 필요 장비: 전원공급기, 멀티미터/오실로스코프, 비행 컴퓨터 타깃 보드, PC 등
- 안전 장비: 보안경 (화약/서보 작동 시험 시 필수)

## 3. 안전 수칙 및 사전 점검

> [!WARNING]
> 화약/서보 구동 시험 시에는 반드시 물리적 안전 장치를 체결하고 진행하십시오.

- [ ] 전원 전압(3.3V / 배터리) 및 극성 확인
- [ ] 사출 화약/구동기 물리적 안전 핀(Safety Pin) 체결 확인 (오발 방지)

## 4. 상세 시험 절차
1. 보드에 전원을 인가하고 정상 부팅(LED 점등)을 확인한다.
2. 센서 모의 신호 또는 압력 챔버를 통해 기압을 감소시킨다.
3. 사출 핀의 출력 전압 및 지속 시간을 오실로스코프로 측정한다.

## 5. 성공 판정 기준 (Pass Criteria)
- 조건 1: 정점 감지 후 1.0초 이내에 사출 신호가 인가되는가?
- 조건 2: 신호 인가 시간이 1.0초 이상 유지되는가?

---

## 6. 연관 문서
- [[docs/wiki/verification/matrix|요구사항 검증 매트릭스]]
- [[docs/wiki/verification/results/README|시험 결과 보고서]]
