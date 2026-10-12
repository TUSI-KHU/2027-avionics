# NURA Flight Computer Firmware

NURA 400m 로켓 온보드 주 비행 컴퓨터(Flight Computer)의 임베디드 펌웨어 프로젝트입니다.  
본 디렉터리는 [[docs/wiki/decisions/ADR-001-mcu-selection|ADR-001]]에 따라 **Espressif ESP32-S3-WROOM-1-N16R8** 및 **ESP-IDF + FreeRTOS** 기반의 **표준 PlatformIO 프로젝트 구조**를 따릅니다.

---

## ⚙️ 타깃 환경 사양
- **MCU 모듈**: Espressif ESP32-S3-WROOM-1-N16R8
  - CPU: Xtensa® Dual-core 32-bit LX7 @ 240 MHz (벡터 명령어 가속)
  - Memory: 16 MB Quad SPI Flash, 8 MB Octal PSRAM, 512 KB 내부 SRAM
- **프레임워크**: ESP-IDF + FreeRTOS (SMP 멀티코어 실시간 스케줄링)
- **빌드 시스템**: PlatformIO ([platformio.ini](file:///home/changsu/Workspace/2027-nura-avionics/firmware/platformio.ini))

---

## 🗂️ 표준 PlatformIO 디렉터리 구조
```text
firmware/
├── platformio.ini          # PlatformIO 프로젝트 빌드 설정
├── src/                    # 펌웨어 메인 소스 코드
│   ├── main.c              # FreeRTOS app_main() 진입점
│   ├── bsp/                # 센서/통신 하드웨어 드라이버 (SPI, I2C, UART)
│   ├── flight/             # 비행 상태 머신(FSM), 사출, 데이터 로깅
│   ├── gnc/                # 칼만 필터(EKF), 자세/고도 추정 알고리즘
│   └── common/             # 공용 데이터 구조체, 패킷 프로토콜 정의
├── include/                # 공용 C/C++ 프로젝트 헤더 (.h)
├── lib/                    # 프로젝트 전용 프라이빗 라이브러리
└── test/                   # 단위 테스트 (Unity / Native host test)
```

---

## 🔨 빌드 및 실행 가이드

`firmware/` 디렉터리 내에서 PlatformIO CLI(`pio`)를 사용하거나, 루트 디렉터리에서 `-d firmware` 옵션으로 실행할 수 있습니다.

```bash
# firmware 디렉터리 내부에서 실행 시
cd firmware
pio run -e esp32s3_flight_computer                   # 펌웨어 빌드
pio run -e esp32s3_flight_computer -t upload -t monitor # 플래싱 및 모니터링
pio test -e native_test                              # 로컬 단위 테스트

# 저장소 루트에서 직접 실행 시
pio run -d firmware -e esp32s3_flight_computer
pio test -d firmware -e native_test
```

---

## 💡 작업 지침
- **인터페이스 준수**: 하드웨어 핀맵 및 통신 패킷 구조는 `docs/wiki/interfaces/`에 정의된 규격([[docs/wiki/interfaces/pinout-matrix|핀맵 매트릭스]], [[docs/wiki/interfaces/packet-specs|패킷 명세]])을 기준으로 구현합니다.
- **실시간 태스크 격리**: Core 0은 고주파수 센서 수집 및 GNC/EKF 연산, Core 1은 통신(LoRa), 데이터 로깅 및 사출 FSM을 전담하도록 설계합니다.
- **동작 검증**: 코드를 커밋하기 전 로컬 빌드 및 타깃 보드(또는 테스트 지그) 동작을 확인하고 PR에 결과를 첨부합니다.
