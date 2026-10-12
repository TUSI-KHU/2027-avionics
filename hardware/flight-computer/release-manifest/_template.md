# [비행 컴퓨터 PCB 제작/발주 체크리스트] (예: FC Rev 1.0)

- **보드 명칭**: FC Main Board
- **하드웨어 리비전**: Rev 1.0
- **작성일**: YYYY-MM-DD
- **작성자**: 
- **Git Commit**: `abcdef`

---

## 1. 설계 검증 체크리스트

> 발주 전 회로 및 아트워크 검증을 완료하고 체크박스를 표시합니다.

- [ ] **KiCad ERC**: 전기 규칙 검사 오류(Error) 0건 통과
- [ ] **KiCad DRC**: 디자인 규칙 검사 클리어런스 오류 0건 통과
- [ ] **인터페이스 일치**: 펌웨어 담당자와 핀맵([docs/wiki/interfaces/pinout-matrix.md](file:///home/changsu/Workspace/2027-nura-avionics/docs/wiki/interfaces/pinout-matrix.md)) 일치 확인
- [ ] **기구 치수 검증**: 로켓 기체 내부 장착 치수 및 마운팅 홀 직경/간격 확인

---

## 2. 발주 및 제조 사양

| 사양 항목 | 설정값 | 비고 |
|---|---|---|
| **제조사** | JLCPCB / PCBWay | |
| **레이어 수** | 4 Layers | |
| **PCB 두께** | 1.6 mm (또는 1.0 mm) | |
| **동박 두께** | 1 oz Outer / 0.5 oz Inner | |
| **표면 처리** | HASL Lead-Free (또는 ENIG) | 센서 납땜 패드 평탄도 고려 |
| **솔더마스크 색상** | Black / Green / Blue | |

---

## 3. 제조 산출물 링크

- **거버(Gerber) 압축 파일**: [Google Drive 링크](https://drive.google.com/...)
- **BOM(부품 목록) 파일**: [BOM 링크](https://drive.google.com/...) 또는 KiCad 생성 부품 목록 링크
- **SMT/CPL 좌표 파일**: 필요 시 링크 첨부

---

## 4. 특이사항 및 개정 이력 메모

- (예: 3.3V LDO 발열 대비를 위해 GND 비아 추가 배치)
- (예: IMU 센서 라인 노이즈 저감을 위해 바이패스 커패시터 위치 수정)
