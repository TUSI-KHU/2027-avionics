---
title: "텔레메트리 및 통신 시스템 (Telemetry & RF)"
type: system
status: active
tags:
  - domain/avionics
  - system/rf
  - system/telemetry
aliases:
  - TelemetryProtocol
  - 통신프로토콜
  - LoRaTelemetry
created: 2026-10-12
updated: 2026-10-12
---

# 📡 텔레메트리 및 통신 시스템 (Telemetry & RF)

> [!NOTE]
> 본 문서는 로켓 온보드 컴퓨터와 지상국(Ground Station) 간의 무선 링크(RF/LoRa) 사양 및 텔레메트리 운용 개념을 다룹니다.
> 구체적인 패킷 바이너리 구조체는 [[docs/wiki/interfaces/packet-specs|통신 패킷 프로토콜 명세]]를 참조하십시오.

---

## 1. 무선 통신 링크 개요

- **주파수 대역**: 433 MHz / 915 MHz ISM 대역 (국내 전파법 준수 대역 적용: `(미확정 - 팀원 논의 필요)`)
- **변조 방식**: LoRa (Long Range) Chirp Spread Spectrum
- **트랜시버 칩셋**: Semtech SX1262 (또는 SX1276)
- **전송 출력**: 최대 20 dBm (100 mW)
- **안테나**: 온보드 1/4 파장 모노폴 또는 플렉서블 PCB 안테나

---

## 2. 다운링크 텔레메트리 (Downlink)

`REQ-SYS-005` 요구사항에 따라 비행 중 핵심 상태 및 GPS 좌표를 **최소 5 Hz 이상** 지상국으로 전송합니다.

- **프레임 주기**: 5 Hz (200 ms 간격)
- **포함 데이터**:
  - 패킷 시퀀스 번호 및 온보드 타임스탬프 (ms)
  - 현재 비행 상태 (FSM State: `[PAD_IDLE]`, `[BOOST]`, `[APOGEE]` 등)
  - 기압 고도 ($m$) 및 수직 속도 ($m/s$)
  - 3축 가속도 ($g$) 및 3축 각속도 ($deg/s$)
  - GPS 위도, 경도, GPS 고도, 수신 위성 수
  - 배터리 전압 ($V$) 및 온보드 온도 ($^\circ C$)
  - 사출 회로 연속성(Continuity) 상태

---

## 3. 업링크 명령 (Uplink Command)

발사 전 지상 점검 및 비상 상황 시 지상국에서 탑재 컴퓨터로 명령을 전송합니다.

> [!CAUTION]
> 비행 중(`[BOOST]`, `[COAST]`) 오동작을 유발할 수 있는 파괴적 명령(Disarm, Reboot 등)은 펌웨어 상태 머신 레벨에서 수신 무시(Inhibit) 처리됩니다.

- **지원 명령**:
  1. `CMD_PING`: 통신 링크 상태 확인
  2. `CMD_CALIBRATE_IMU`: 발사대 수평 상태에서 IMU 바이어스 영점 조절
  3. `CMD_ARM`: 발사 준비 승인 (`[PAD_IDLE] -> [ARMED]`)
  4. `CMD_DISARM`: 발사 취소 및 대기 복귀 (`[ARMED] -> [PAD_IDLE]`)
  5. `CMD_FORCE_EJECT`: 지상 점검 시 수동 사출 테스트 (지상 모드 전용)

---

## 4. 연관 문서
- [[docs/wiki/systems/flight-state-machine|비행 상태 머신]]
- [[docs/wiki/interfaces/packet-specs|통신 패킷 프로토콜 명세]]
- [[docs/wiki/interfaces/pinout-matrix|하드웨어 핀맵 매트릭스]]
- [[docs/wiki/verification/matrix|요구사항 검증 매트릭스 (REQ-SYS-005)]]
