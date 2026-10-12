---
title: "서브시스템 인터페이스 총괄 (Interfaces)"
type: moc
status: active
tags:
  - domain/avionics
  - interface/hub
aliases:
  - Interfaces
  - 인터페이스
created: 2026-10-12
updated: 2026-10-12
---

# 🔌 서브시스템 인터페이스 정의 (Interfaces)

> [!NOTE]
> 하드웨어 핀맵, 통신 프로토콜 및 서브시스템 간(HW - FW - 지상국) 연동 규격을 관리하는 공간입니다.
> 전체 지식 맵은 [[docs/Index|Index (MOC)]]를 참조하십시오.

---

## 📌 관리 대상 문서

1. **[[docs/wiki/interfaces/pinout-matrix|하드웨어 핀맵 매트릭스 (Pinout)]]**:
   - MCU 핀 할당 (SPI1~3, I2C1, USART1~2, PWM, GPIO)
   - 전원 레일(3.3V, VBAT) 및 사출 화약 구동/Arming 핀
2. **[[docs/wiki/interfaces/packet-specs|통신 패킷 프로토콜 명세 (Packet Specs)]]**:
   - 비행 컴퓨터 -> 지상국 다운링크 텔레메트리 바이너리 패킷 구조체 (42 Bytes, 5 Hz)
   - 지상국 -> 비행 컴퓨터 업링크 명령/점검 패킷 구조체 (8 Bytes)
   - 센서 데이터 정수형 스케일 단위 및 체크섬 알고리즘

---

## 💡 변경 및 작성 지침

> [!WARNING]
> 핀맵이나 패킷 구조가 변경될 때는 하드웨어, 펌웨어, 지상국 담당 팀원과 상의 후 이 문서를 함께 갱신합니다.

- 인터페이스를 변경할 경우 관련 팀원에게 GitHub Issue 또는 PR을 통해 즉시 공유합니다.
- 패킷 구조는 C 언어 구조체(`#pragma pack(push, 1)`) 및 표 형태로 누구나 오차 없이 구현할 수 있도록 관리합니다.
