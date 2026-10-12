---
title: "[비행 매니페스트 제목]"
type: procedure
status: draft
tags:
  - domain/avionics
  - verification/manifest
aliases:
  - FLT-MANIFEST-NNN
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# [비행 매니페스트 제목] (예: FLT-2027-01 1차 시험 비행)

- **비행 ID**: FLT-2027-01
- **발사 일시**: YYYY-MM-DD HH:MM
- **발사 장소**: 
- **점검 책임자**: 발사 책임자(         ), 에비오닉스 오퍼레이터(         )

---

## 1. 탑재 형상 요약

| 구분 | 항목 | 적용 형상 / 버전 | 비고 |
|---|---|---|---|
| **하드웨어** | 비행 컴퓨터 보드 | FC Rev 1.0 (Board #1) | 배터리 무부하 전압: 8.2V |
| | 복구 장치 (사출) | 서보 모터 / 사출 화약 | 장전 확인 완료 |
| **소프트웨어** | 온보드 펌웨어 | `v1.0.0` (Git 커밋: `abcdef`) | [[docs/wiki/systems/flight-state-machine\|FSM 탑재]] |
| | 지상국 소프트웨어 | `v1.0.0` | 모니터링 UI 연동 |
| **설정** | 설정 파일 | `configs/flight-01-270415.yaml` | |
| | 캘리브레이션 | `configs/calibration/calib-board01-270315.yaml` | IMU 및 기압계 보정 |

---

## 2. 발사대 최종 체크리스트 (Pre-flight Checklist)

> [!IMPORTANT]
> 현장 점검 완료 후 체크박스를 클릭(터치)하여 완료 표시합니다.

- [ ] **센서 무결성**: IMU 3축 및 기압 센서 데이터 정상 수신 확인
- [ ] **무선 링크**: 지상국 텔레메트리 패킷 수신 및 RSSI 감도 정상 확인
- [ ] **온보드 로깅**: Flash 메모리 마운트 및 로깅 대기 상태(Armed) 진입
- [ ] **물리 안전 핀 제거**: 발사 직전 안전 핀(Remove-Before-Flight) 제거 완료

---

## 3. 현장 특이사항 및 관찰 메모

- (예: 1차 점검 시 기압 센서 노이즈가 튀어 지상 재부팅 1회 수행 후 정상화됨)
- (예: 현장 기온 28도, 풍속 2m/s 서풍)

---

## 4. 연관 문서
- [[docs/wiki/systems/flight-computer|비행 컴퓨터 하드웨어]]
- [[docs/wiki/systems/flight-state-machine|비행 상태 머신]]
- [[docs/wiki/verification/matrix|요구사항 검증 매트릭스]]
