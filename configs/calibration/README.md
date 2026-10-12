# Sensor Calibration

보드별 센서 캘리브레이션 데이터(IMU 바이어스/오프셋, 지자기 보정 파라미터 등)를 관리하는 공간입니다.

## 📁 파일 명명 규칙
- 형식: `calib-{board_id}-{yymmdd}.yaml`
- 예시: `calib-board01-270315.yaml`

## 💡 관리 지침
- 보드 식별자(Board ID) 및 측정 날짜(YYMMDD)를 파일명에 명시하여 구분합니다.
- 센서 재측정 시 기존 데이터를 덮어쓰지 않고 새 파일로 저장하여 비행 데이터 사후 분석 시 정확한 형상을 추적할 수 있도록 합니다.
- 특정 비행에 사용된 캘리브레이션 파일은 해당 비행의 매니페스트 문서([flight-manifests](../../docs/wiki/verification/flight-manifests/))에 기록합니다.
