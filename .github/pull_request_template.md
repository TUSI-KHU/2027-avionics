## 변경 목적

Refs #

PR merge만으로 Issue를 닫지 않는다. merge 후 Issue의 검증 조건까지 확인한 다음 Issue를 수동으로 닫는다.

## 변경한 artifact

## 영향분석

- 관련 Interface / Requirement / Hazard ID: 해당 시 기입, 아니면 `N/A`
- 일정 영향: 없음 / 있음 — 설명
- 변경 등급: 일반 / 비행 중요
- 독립 reviewer: 원 Task C / 별도 review Task A/R
- 관련 owner 검토: 계정 또는 team

## 검증

- 명령 또는 Test ID:
- HW revision/serial: 해당 시 기입, 아니면 `N/A`
- Source commit / firmware: 해당 시 기입, 아니면 `N/A`
- Configuration / calibration: 해당 시 기입, 아니면 `N/A`
- 결과 및 evidence URI/hash:

## 미검증, 후속 항목

없으면 `없음`으로 명시한다.

## Rollback 또는 P1/P2 비활성화 방법

## Checklist

- [ ] 연결 Issue의 완료 조건과 검증 방법을 충족했다.
- [ ] 해당하면 requirement, interface, hazard, ADR와 verification matrix를 갱신했다.
- [ ] 실패, 제한, anomaly를 숨기거나 덮어쓰지 않았다.
- [ ] Secret, private data, 대형 raw data와 생성 binary를 포함하지 않았다.
- [ ] `make validate PYTHON=.venv/bin/python` 또는 동등한 환경의 `make validate`를 통과했다.
