# 2027 Avionics

NURA 발사대회급 400m 로켓의 전자 장비를 개발하는 저장소입니다.

## 처음 참여한다면

[처음 참여하는 사람을 위한 작업 방법](CONTRIBUTING.md)을 먼저 읽어 주세요. 작업 카드 작성 예시부터 검토 요청을 합친 뒤 마무리하는 방법까지 순서대로 적혀 있습니다.

작업은 아래 순서로 진행합니다.

```text
작업 카드 만들기 → 내 작업으로 옮기기 → 작업 가지 만들기 → 검토 요청 올리기 → 확인 후 합치기
```

## 처음 한 번만 준비하기

```bash
uv venv .venv
uv pip install --python .venv/bin/python --require-hashes -r requirements-dev.txt
```

변경을 올리기 전에는 다음 검사를 실행합니다.

```bash
make validate PYTHON=.venv/bin/python
```

## 바로가기

- [작업판](https://github.com/orgs/TUSI-KHU/projects/1)
- [새 작업 카드 만들기](https://github.com/TUSI-KHU/2027-avionics/issues/new/choose)
- [작업 방법과 작성 예시](CONTRIBUTING.md)
- [관리자용 작업판 설정 기록](project-configuration.md)
- [관리자용 저장소 설정 기록](repository-settings.md)
