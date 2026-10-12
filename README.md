# 2027 NURA Avionics

NURA 400m 소형 로켓의 비행 컴퓨터(Flight Computer), 펌웨어, GNC, RF 통신 및 지상국 저장소입니다.

## 📚 주요 안내
- [협업 및 기여 가이드 (CONTRIBUTING.md)](CONTRIBUTING.md): **(필독)** 팀 작업 사이클, 칸반 보드 및 Antigravity 자연어 협업 방법
- [시스템 종합 설계서 (docs/system-design.md)](docs/system-design.md): 400m 미션 목표, 비행 모드(FSM), 핵심 아키텍처 요약
- [지식 베이스 대시보드 (docs/Index.md)](docs/Index.md): 서브시스템 엔티티, 인터페이스(핀맵/패킷), ADR 및 검증 매트릭스 전체 맵 (Obsidian MOC)

---

## 🗂️ 저장소 구조

| 경로 | 책임 범위 |
|---|---|
| `firmware/` | 온보드 비행 컴퓨터 펌웨어 (PlatformIO 표준 프로젝트: `platformio.ini`, `src/`, `include/`, `lib/`, `test/`) |
| `docs/` | 시스템 종합 설계, 의사결정(ADR), 인터페이스, 시험/검증, 보고서 등 전체 문서 |
| `hardware/` | KiCad 회로도, PCB 아트워크, 심볼/풋프린트 라이브러리 |
| `ground-station/` | 지상국 수신, 명령 전송 및 실시간 모니터링 소프트웨어 |
| `simulation/` | 비행 동역학 시뮬레이션 모델, 환경 시나리오 및 파라미터 |
| `configs/` | 비행 형상 설정 파일(`{id}-{yymmdd}.yaml`) 및 센서 캘리브레이션 데이터(`configs/calibration/`) |

---

## License

[MIT](LICENSE)
