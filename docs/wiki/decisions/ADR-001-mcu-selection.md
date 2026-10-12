---
title: "ADR-001: 주 비행 컴퓨터 MCU 및 펌웨어 플랫폼으로 ESP32-S3-WROOM-1-N16R8 (ESP-IDF + FreeRTOS) 선정"
type: adr
status: accepted
tags:
  - domain/avionics
  - adr
  - hw
  - mcu
  - fsw
  - platformio
aliases:
  - ADR-001
  - MCU선정
  - ESP32-S3선정
created: 2026-10-12
updated: 2026-10-12
---

# ADR-001: 주 비행 컴퓨터 MCU 및 펌웨어 플랫폼으로 ESP32-S3-WROOM-1-N16R8 (ESP-IDF + FreeRTOS) 선정

- **상태**: 승인됨 (Accepted)
- **결정일**: 2026-10-12
- **결정자**: NURA Avionics 팀 (HW/FSW)

---

## 1. 배경 및 문제 상황

NURA 400m 로켓의 비행 컴퓨터(Flight Computer)는 다음과 같은 엄격한 시스템 요구사항을 충족해야 합니다:
1. **고속 센서 융합 및 실시간성**: 100 Hz 이상의 9축 센서(IMU) 및 기압계 데이터 수집, 확장 칼만 필터(EKF) 자세 추정 연산 ([[docs/wiki/verification/matrix#REQ-SYS-003|REQ-SYS-003]]).
2. **신뢰성 높은 멀티태스킹**: 센서 수집/자세 제어 루프와 통신(LoRa/지상국 송수신), 플래시 로깅, 사출 판단 FSM이 상호 간섭(지연) 없이 독립적으로 병렬 수행되어야 함.
3. **충분한 온보드 메모리**: 센서 원시 데이터 및 비행 이벤트 바이너리 로깅을 위한 고속 버퍼링 메모리 필요.
4. **팀 개발 효율성 및 빌드 단일화**: 펌웨어 개발 환경이 여러 툴체인으로 분편화되지 않고, 단일 PlatformIO 프로젝트 환경(`platformio.ini`)에서 의존성, 컴파일러 플래그, 파티션 테이블, 단위 테스트를 일원화 관리할 수 있어야 함.

이전 검토 대상이었던 STM32F405RGT6(단일 코어, 외부 RAM 부재, IDE 종속성 등) 및 RP2040을 재검토하고, **Espressif ESP32-S3-WROOM-1-N16R8** 모듈을 주 비행 컴퓨터 칩셋으로, **ESP-IDF + FreeRTOS**를 단일 **PlatformIO** 프로젝트 아키텍처로 도입하기로 결정하였습니다.

---

## 2. 검토한 대안 비교

| 비교 항목 | Espressif ESP32-S3-WROOM-1-N16R8 (채택) | STM32F405RGT6 (기존 검토안) | RP2040 (Raspberry Pi) |
|---|---|---|---|
| **CPU 아키텍처** | Xtensa® Dual-core 32-bit LX7 @ 최대 240 MHz (벡터 명령어/DSP 가속 지원) | ARM Cortex-M4 @ 168 MHz (하드웨어 단정밀도 FPU) | Dual ARM Cortex-M0+ @ 133 MHz (소프트웨어 부동소수점) |
| **코어 구성 및 병렬성** | **듀얼 코어** (코어별 태스크 분리 및 하드웨어 인터럽트 격리 가능) | 단일 코어 (태스크 전환 오버헤드 및 I/O 블로킹 위험) | 듀얼 코어 (하드웨어 FPU 미지원으로 센서 융합 시 클럭 지연 발생) |
| **내장 메모리** | **16 MB Quad SPI Flash** + **8 MB Octal PSRAM** + 512 KB SRAM | 1 MB Flash + 192 KB SRAM (외부 RAM 미지원 시 버퍼 한계) | 외부 2~16 MB Flash + 264 KB SRAM |
| **운영체제 및 프레임워크** | **ESP-IDF + FreeRTOS** (네이티브 SMP 멀티스레딩 최적화) | FreeRTOS 또는 베어메탈 (수동 포팅 및 HAL 설정 필요) | FreeRTOS / Pico SDK |
| **프로젝트 및 빌드 환경** | **Single PlatformIO 프로젝트** (`platformio.ini` 일원화, 라이브러리 및 CI 자동화) | STM32CubeIDE / Keil 종속 또는 Make/CMake 분산 | PlatformIO / CMake |
| **주변장치 및 버스 유연성** | SPI 4개, I2C 2개, UART 3개, TWAI(CAN) 1개, **GPIO Matrix (핀 매핑 자유도 극대화)** | SPI 3개, USART 6개, I2C 3개 (고정 핀 멀티플렉싱 제한) | SPI 2개, UART 2개, I2C 2개 (PIO 커스텀 필요) |
| **추가 무선/디버그 기능** | 2.4 GHz Wi-Fi 및 BLE 5 지원 (발사대 점검, 착륙 후 무선 데이터 다운로드 및 필드 무선 설정 가능) | 무선 기능 없음 (외부 모듈 필수) | 무선 기능 없음 (Pico W 별도) |

---

## 3. 결정 내용

주 비행 컴퓨터의 주 MCU로 **Espressif ESP32-S3-WROOM-1-N16R8**을 채택하고, 펌웨어는 **ESP-IDF + FreeRTOS** 기반의 **단일 PlatformIO (Single PlatformIO) 프로젝트**로 구축하기로 최종 결정하였습니다.

### 주요 사유:

1. **듀얼 코어(240 MHz) 기반의 결정론적 실시간 처리 (Dual-Core Determinism)**:
   - **Core 0 (센서 & GNC)**: 100 Hz 이상의 IMU/기압계 센서 고속 인터럽트 폴링, 확장 칼만 필터(EKF), 자세/고도 추정 연산 전담.
   - **Core 1 (통신 & 로깅 & 사출 FSM)**: SX1262 LoRa 텔레메트리 송수신, W25Q128/PSRAM 고속 바이너리 로깅, 비행 상태 머신(FSM) 전이 및 사출 화약 격발 로직 전담.
   - 통신 및 외부 플래시 I/O 블로킹이 센서 융합 루프에 미치는 지연을 물리적으로 원천 차단.

2. **8 MB Octal PSRAM + 16 MB Flash 대용량 메모리 마진**:
   - 8 MB의 고속 PSRAM을 활용하여 비행 중 순간적인 플래시 쓰기 지연(Flash Write Latency) 발생 시에도 초당 수백 회의 센서 원시 패킷을 손실 없이 링 버퍼에 안전하게 보관.
   - 비행 종료 후 16 MB 온보드 플래시 및 PSRAM 데이터를 지상국으로 완벽하게 덤프 가능.

3. **ESP-IDF + FreeRTOS 네이티브 안정성**:
   - 검증된 FreeRTOS SMP(대칭형 다중 처리) 커널을 기반으로 우선순위 기반 선점형 스케줄링(Preemptive Scheduling), 태스크 간 세마포어, 큐(Queue), 이벤트 그룹을 표준 방식으로 운용.
   - SPI Master, I2C, UART, 고분해능 타이머(ESP Timer) 등 핵심 하드웨어 인터페이스를 ESP-IDF 드라이버 레이어로 견고하게 지원.

4. **단일 PlatformIO 프로젝트 (`platformio.ini`) 표준화**:
   - 복잡한 툴체인 수동 설치 없이 PlatformIO 생태계를 통해 `framework = espidf`, `board = esp32-s3-devkitc-1` (또는 커스텀 보드 json), 빌드 플래그, 파티션 테이블(`partitions.csv`)을 단일 설정 파일로 통합 관리.
   - 단위 테스트(`pio test`) 및 팀원 협업 시 동일한 빌드 환경과 재현성 보장.

5. **GPIO 매트릭스에 따른 PCB 라우팅 및 핀 할당 유연성**:
   - ESP32-S3의 GPIO 매트릭스를 통해 대부분의 디지털 주변장치(SPI, I2C, UART, PWM)를 최적의 PCB 경로에 자유롭게 매핑 가능.

---

## 4. 영향 및 향후 과제

- **긍정적 영향**:
  - 단일 코어의 연산 부하 병목 해소 및 8 MB PSRAM을 통한 무손실 텔레메트리/로깅 버퍼링 확보.
  - PlatformIO 기반으로 모든 팀원이 동일한 개발 환경에서 원클릭 빌드/업로드/테스트 가능.
  - Wi-Fi/BLE 인터페이스를 활용하여 발사대 대기 상태(Pad Standby) 점검 및 회수 후 지상 무선 로그 다운로드 확장성 확보.

- **후속 과제**:
  - `firmware/` 디렉터리에 표준 PlatformIO 프로젝트 환경 (`platformio.ini`, `src/`, `include/`, `lib/`, `test/`) 구성 및 관리.
  - FreeRTOS 코어 고정(`xTaskCreatePinnedToCore`) 및 태스크 우선순위 맵 작성.
  - 하드웨어 팀과 협의하여 ESP32-S3 핀맵([[docs/wiki/interfaces/pinout-matrix|하드웨어 핀맵 매트릭스]])을 확정하고, 미확정 핀은 `(미확정 - 팀원 논의 필요)` 상태로 관리.
  - 사출 구동 핀 부팅 글리치(Strapping Pin 및 부팅 시 초기 GPIO 레벨) 분석 및 안전 풀다운 회로 검증.

---

## 5. 연관 문서

- [[docs/wiki/systems/flight-computer|비행 컴퓨터 하드웨어 및 MCU]]
- [[docs/wiki/interfaces/pinout-matrix|하드웨어 핀맵 매트릭스]]
- [[docs/wiki/decisions/README|ADR 레지스트리]]
- [[docs/system-design|시스템 종합 설계서]]
