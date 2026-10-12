---
title: "통신 패킷 프로토콜 명세 (Packet Specs)"
type: interface
status: active
tags:
  - domain/avionics
  - interface/packet
  - fsw
  - ground-station
aliases:
  - PacketSpecs
  - 패킷프로토콜
  - TelemetryPacket
created: 2026-10-12
updated: 2026-10-12
---

# 📦 통신 패킷 프로토콜 명세 (Packet Specs)

> [!NOTE]
> 본 문서는 비행 컴퓨터(FSW)와 지상국(GS) 간 LoRa 무선 링크로 송수신되는 바이너리 패킷 포맷의 단일 원본(SSOT)입니다.
> 모든 데이터는 **Little-Endian** 바이트 순서를 따릅니다.

---

## 1. 다운링크 텔레메트리 패킷 (`TelemetryFrame`)

- **전송 주기**: 5 Hz (200 ms 간격)
- **전체 길이**: 42 Bytes
- **동기화 헤더**: `0xAA 0x55`

### 1.1 구조체 정의 (C 언어)

```c
#pragma pack(push, 1)
typedef struct {
    uint8_t  header[2];       // 0xAA, 0x55 (Sync Word)
    uint32_t timestamp_ms;    // 부팅 후 경과 시간 (ms)
    uint16_t packet_seq;      // 패킷 시퀀스 번호 (0 ~ 65535)
    uint8_t  flight_mode;     // 비행 모드 (0: INIT, 1: PAD_IDLE, 2: ARMED, 3: BOOST, 4: COAST, 5: APOGEE, 6: DESCENT, 7: LANDED)
    
    // 센서 데이터 (스케일 적용 정수형)
    int32_t  pressure_pa;     // 기압 (Pa, 101325 = 1 atm)
    int16_t  altitude_m;      // 해면 기준 고도 (0.1 m 단위, 예: 4000 = 400.0 m)
    int16_t  velocity_z_cms;  // 수직 속도 (cm/s, 예: 1520 = 15.2 m/s)
    
    int16_t  accel_x_mg;      // X축 가속도 (mG 단위)
    int16_t  accel_y_mg;      // Y축 가속도 (mG 단위)
    int16_t  accel_z_mg;      // Z축 가속도 (mG 단위, 중력 포함)
    
    int16_t  gyro_x_dps;      // X축 각속도 (0.1 deg/s)
    int16_t  gyro_y_dps;      // Y축 각속도 (0.1 deg/s)
    int16_t  gyro_z_dps;      // Z축 각속도 (0.1 deg/s)
    
    // GPS 데이터
    int32_t  gps_lat_e7;      // 위도 (1e-7 deg)
    int32_t  gps_lon_e7;      // 경도 (1e-7 deg)
    uint8_t  gps_sats;        // 유효 위성 수 (SIV)
    
    // 시스템 상태
    uint16_t vbat_mv;         // 배터리 전압 (mV, 예: 7400 = 7.4 V)
    uint8_t  pyro_continuity; // 사출 채널 도통 상태 (Bit 0: Main, Bit 1: Drogue)
    uint8_t  checksum;        // XOR 체크섬 (헤더 제외 전 바이트)
} TelemetryFrame_t;
#pragma pack(pop)
```

---

## 2. 지상국 업링크 명령 패킷 (`CommandFrame`)

- **전송 방식**: 지상국 이벤트 발생 시 송신 (ACK 응답 대기)
- **전체 길이**: 8 Bytes
- **동기화 헤더**: `0x55 0xAA`

### 2.1 구조체 정의 (C 언어)

```c
#pragma pack(push, 1)
typedef struct {
    uint8_t  header[2];       // 0x55, 0xAA (Command Sync)
    uint16_t cmd_seq;         // 명령 일련번호
    uint8_t  cmd_id;          // 명령 코드 (아래 표 참조)
    uint16_t cmd_param;       // 명령 보조 파라미터
    uint8_t  checksum;        // XOR 체크섬
} CommandFrame_t;
#pragma pack(pop)
```

### 2.2 지원 명령 코드 (Command IDs)

| `cmd_id` | 명령 명칭 | 설명 | 파라미터 (`cmd_param`) |
|---|---|---|---|
| `0x01` | `CMD_PING` | 링크 핑 점검 | 예약 (`0x0000`) |
| `0x02` | `CMD_CALIBRATE` | 센서 바이어스 0점 조절 | 대상 센서 비트마스크 |
| `0x10` | `CMD_ARM` | 발사 준비 승인 (`[ARMED]`) | 보안 키값 (`0xCAFE`) |
| `0x11` | `CMD_DISARM` | 대기 모드 복귀 (`[PAD_IDLE]`) | 보안 키값 (`0xDEAD`) |
| `0xF0` | `CMD_EJECT_TEST` | 지상 점검 수동 격발 | 채널 번호 (1 or 2) |

> [!CAUTION]
> 보안 키값이 일치하지 않는 `CMD_ARM` 또는 `CMD_EJECT_TEST` 명령은 MCU에서 즉시 거부(Drop)됩니다.

---

## 3. 연관 문서
- [[docs/wiki/systems/telemetry-protocol|텔레메트리 및 통신 시스템]]
- [[docs/wiki/systems/flight-state-machine|비행 상태 머신]]
- [[docs/wiki/interfaces/pinout-matrix|하드웨어 핀맵 매트릭스]]
- [[docs/wiki/verification/matrix|요구사항 검증 매트릭스 (REQ-SYS-005)]]
