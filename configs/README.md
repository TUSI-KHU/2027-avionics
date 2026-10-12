# Flight Configurations

비행 컴퓨터 파라미터 및 비행 형상 설정 파일(센서 샘플링 주기, 정점 감지 임계값, 사출 타이머 등)과 센서 캘리브레이션 데이터를 관리하는 공간입니다.

---

## 🗂️ 디렉터리 구조

```text
configs/
├── flight-01-270415.yaml        # 플라이트별 비행 설정 파일 ({id}-{yymmdd}.yaml)
├── default.yaml                 # 개발 및 기본 파라미터 템플릿
└── calibration/                 # 보드별 센서 캘리브레이션 데이터
    └── calib-board01-270315.yaml
```

---

## 🏷️ 파일 명명 규칙

### 1. 플라이트별 설정 파일 (`configs/`)
- **형식**: `{id}-{yymmdd}.yaml`
- **규칙**:
  - `{id}`: 비행 또는 시험 식별자 (예: `flight-01`, `FLT-01`, `ground-test-01`)
  - `{yymmdd}`: 시험 또는 발사 예정 일자 (년월일 6자리, 예: 2027년 4월 15일 -> `270415`)
- **예시**:
  - `flight-01-270415.yaml`
  - `FLT-02-270520.yaml`

### 2. 센서 캘리브레이션 파일 (`configs/calibration/`)
- **형식**: `calib-{board_id}-{yymmdd}.yaml`
- **예시**: `calib-board01-270315.yaml`
- 상세 지침은 [calibration/README.md](calibration/README.md)를 참조하십시오.

---

## 💡 관리 지침

- **이력 불변성**: 실제 비행이나 시험에 적용된 설정 파일은 사후 분석 및 추적성을 위해 절대 덮어쓰지 않고, 변경 시 새 파일(또는 일자 갱신)로 관리합니다.
- **매니페스트 연동**: 비행 시험 전 작성하는 탑재 형상 매니페스트([flight-manifests](../docs/wiki/verification/flight-manifests/))에 적용할 설정 파일과 캘리브레이션 파일의 정확한 경로를 명시합니다.
