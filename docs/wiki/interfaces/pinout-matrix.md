---
title: "하드웨어 핀맵 매트릭스 (Pinout Matrix)"
type: interface
status: active
tags:
  - domain/avionics
  - interface/pinout
  - hw
  - esp32s3
aliases:
  - PinoutMatrix
  - 핀맵
  - PinAssignment
created: 2026-10-12
updated: 2026-10-12
---

# 🔌 하드웨어 핀맵 매트릭스 (Pinout Matrix)

> [!NOTE]
> [[docs/wiki/decisions/ADR-001-mcu-selection|ADR-001]]에 따라 주 비행 컴퓨터가 **Espressif ESP32-S3-WROOM-1-N16R8**로 선정되었습니다.
> 본 문서는 비행 컴퓨터의 주변장치 버스 및 GPIO 핀 할당의 단일 원본(SSOT)입니다.
> 현재 ESP32-S3 모듈의 하드웨어 특성(Octal PSRAM 예약 핀, Strapping 핀 등)을 반영하여 세부 핀 할당을 HW/FW 팀 간 조율 중이며, 미확정 사양은 `(미확정 - 팀원 논의 필요)`로 관리합니다.

---

## 1. 통신 버스 및 센서 인터페이스

| 버스 / 기능 | 후보 핀 번호 (GPIO) | 신호명 | 연결 장치 | 상태 | 비고 |
|---|---|---|---|---|---|
| **SPI (FSPI)** | (미확정 - 팀원 논의 필요) | SCK, MISO, MOSI, CS_IMU | 고속 IMU (ICM-42688-P) | 검토 중 | 10 MHz 고속 센서 통신 (Core 0 전담) |
| **SPI (FSPI / 공유 또는 전용)** | (미확정 - 팀원 논의 필요) | SCK, MISO, MOSI, CS_FLASH | 온보드 Flash (W25Q128) | 검토 중 | 고속 비행 데이터 바이너리 로깅 |
| **SPI (FSPI / 공유 또는 전용)** | (미확정 - 팀원 논의 필요) | SCK, MISO, MOSI, CS_LORA, RST, BUSY, DIO1 | LoRa 무선 모듈 (SX1262) | 검토 중 | 텔레메트리 트랜시버 (Core 1 전담) |
| **I2C0** | (미확정 - 팀원 논의 필요) | SCL, SDA | 고정밀 기압계 (BMP390) | 검토 중 | 400 kHz Fast Mode, 풀업 4.7k |
| **UART1** | (미확정 - 팀원 논의 필요) | TX, RX | GPS 모듈 (MAX-M10S) | 검토 중 | 115200 bps, 10 Hz NMEA/UBX |
| **USB/UART (디버그)** | GPIO 19, GPIO 20 (USB_D-, USB_D+) 또는 UART0 | D-, D+ / TX, RX | USB-JTAG 디버그 콘솔 | 검토 중 | ESP32-S3 내장 USB 직결 또는 외부 UART |

---

## 2. GPIO 제어 및 액추에이터 핀

| 기능 | 후보 핀 번호 (GPIO) | 입출력 | 극성 / 기본값 | 연결 회로 | 상태 |
|---|---|---|---|---|---|
| **사출 화약 채널 1 (Main)** | (미확정 - 팀원 논의 필요) | Output | Active HIGH (Low) | N-MOSFET 게이트 드라이버 | 검토 중 |
| **사출 화약 채널 2 (Drogue/Backup)** | (미확정 - 팀원 논의 필요) | Output | Active HIGH (Low) | N-MOSFET 게이트 드라이버 | 검토 중 |
| **사출 회로 Arming 스위치** | (미확정 - 팀원 논의 필요) | Output | Active HIGH (Low) | 전원 차단 하이측 P-MOSFET | 검토 중 |
| **화약 도통 확인 (Continuity)** | (미확정 - 팀원 논의 필요) | Input | ADC Analog / High | 분압 저항 측정 회로 | 검토 중 |
| **상태 표시 LED (RGB)** | (미확정 - 팀원 논의 필요) | Output | Active LOW 또는 WS2812 | 시스템 상태 LED | 검토 중 |
| **부저 (Buzzer)** | (미확정 - 팀원 논의 필요) | Output (LEDC/PWM) | Active HIGH (Low) | 착륙 후 비콘 알림음 | 검토 중 |
| **RBF 안전 핀 감지** | (미확정 - 팀원 논의 필요) | Input | Pull-UP (GND 단선 감지) | Remove-Before-Flight 핀 | 검토 중 |

---

## 3. ESP32-S3-WROOM-1-N16R8 핀 설계 필수 고려사항

> [!WARNING]
> ESP32-S3-WROOM-1-N16R8은 8 MB Octal PSRAM 및 16 MB Flash를 내장하고 있으므로 다음 GPIO는 보드 설계 시 절대 외부 용도로 사용해서는 안 됩니다:
> 1. **내부 Flash/PSRAM 점유 핀 (사용 불가)**:
>    - `GPIO 33, 34, 35, 36, 37` (Octal PSRAM 클럭 및 데이터 신호용)
>    - `GPIO 26, 27, 28, 29, 30, 31, 32` (SPI Flash용)
> 2. **Strapping Pins (부팅 시 전압 주의)**:
>    - `GPIO 0`, `GPIO 3`, `GPIO 45`, `GPIO 46`: 부팅 시 로직 레벨에 따라 칩의 부팅 모드, ROM 메시지 출력, Flash 전압이 결정되므로 사출 드라이버 등 민감한 출력 회로에 연결을 금지합니다.
> 3. **사출 구동 핀 안전 조치**:
>    - 사출 화약 구동 핀(MOSFET 게이트)은 부팅 시 MCU 핀 플로팅 및 초기화 지연으로 인한 오발을 방지하기 위해 **10kΩ 하드웨어 풀다운 저항**을 반드시 실장해야 합니다.

---

## 4. 연관 문서

- [[docs/wiki/decisions/ADR-001-mcu-selection|ADR-001: 주 비행 컴퓨터 MCU 및 펌웨어 플랫폼 선정]]
- [[docs/wiki/systems/flight-computer|비행 컴퓨터 하드웨어]]
- [[docs/wiki/systems/recovery-system|복구 및 사출 시스템]]
- [[docs/wiki/interfaces/packet-specs|통신 패킷 프로토콜 명세]]
