# Hardware

NURA 로켓 비행 컴퓨터 및 전장 하드웨어(회로도, PCB 아트워크, 테스트 치구)를 관리하는 디렉터리입니다.

## 🗂️ 디렉터리 구성
- `flight-computer/`: KiCad 회로도, PCB 아트워크, 심볼/풋프린트 라이브러리 및 발주 체크리스트(`release-manifest/`)
- `test-fixtures/`: 센서 및 비행 컴퓨터 점검용 테스트 지그/치구

## 💡 작업 지침
- **회로 및 부품 변경**: 주요 부품이나 핀맵이 변경될 때는 GitHub Issue로 팀원에게 공유하고, 검토를 거쳐 반영합니다.
- **제조 발주 파일**: PCB 제작용 거버(Gerber) 파일 등 대용량 산출물은 Git에 직접 올리지 않고 GitHub Release 또는 공유 드라이브 링크로 관리합니다.

