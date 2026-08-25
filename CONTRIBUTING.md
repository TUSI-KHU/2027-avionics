# 협업 흐름

이 저장소의 Task 단위는 GitHub Issue이며 상태와 우선순위의 기준은 [2027 Avionics Project](https://github.com/orgs/TUSI-KHU/projects/1)의 **실제 설정**이다. 문서와 Project가 다르면 Project를 먼저 따르고 같은 PR에서 문서를 갱신한다.

## 1. Task 시작

1. Issue form으로 Task를 만들거나 Project의 Draft Item을 repository Issue로 전환한다.
2. Project에서 `Priority`, `유형`, `Subsystem`, `Gate`를 지정한다.
3. 착수 전에 Accountable owner 한 명, 완료 조건과 검증 방법을 확인한다.
4. 주요 `In Progress` Task는 팀원별 하나만 유지한다.
5. 준비가 끝나면 Status를 `Backlog`에서 `In Progress`로 옮긴다.

## 2. Branch와 commit

- 최신 `main`에서 작업 branch를 만든다.
- 이름은 `<type>/<issue-number>-<short-description>` 형식을 사용한다.
- type 예: `feat`, `fix`, `docs`, `test`, `chore`.
- commit은 한 가지 논리 변경을 담고 Conventional Commit 형식을 권장한다.

```bash
git switch main
git pull --ff-only
git switch -c docs/12-update-interface-contract
```

## 3. 검증과 Pull Request

1. PR 전에 `make validate PYTHON=.venv/bin/python`을 실행한다.
2. PR 본문에 `Refs #<issue>`를 넣어 원 Task와 연결하되 merge만으로 Issue를 자동 종료하지 않는다.
3. 영향분석, 검증 결과, evidence와 미검증 항목을 사실대로 기록한다.
4. 검토 가능한 상태가 되면 Project Status를 `Review`로 옮긴다.
5. 같은 Task의 PR을 Project card로 별도 추가하지 않는다.

일반 변경은 구현자와 다른 reviewer 1명이 승인한다. 비행 중요 변경은 Technical Lead와 독립 reviewer를 포함해 최소 2명이 검토한다. 실제 계정 또는 team이 확정되기 전에는 CODEOWNERS를 사용하지 않는다.

## 4. Merge와 종료

- merge 방식은 squash만 사용한다.
- review conversation을 모두 해결하고 CI를 통과한 뒤 merge한다.
- merge 후 Issue의 검증 조건까지 확인한 다음 Issue를 수동으로 닫는다. 활성화된 `Item closed` workflow가 Status를 `Done`으로 바꾼다.
- 취소할 때는 근거와 영향을 남기고 Issue를 닫은 뒤, 자동 `Done` 전이가 끝나면 Status를 `Canceled`로 명시적으로 바꾼다.
- 막힌 Task는 현재 Status를 유지하고 원인, 해제 조건과 다음 action을 기록한다.

## 5. Evidence와 보안

- P0, 안전, subsystem interface 변경은 관련 requirement/interface/hazard ID를 남긴다.
- 시험 evidence에는 가능한 경우 HW revision/serial, source commit, configuration/calibration과 URI/hash를 포함한다.
- secret, credential, private data, 대형 raw data와 생성 binary는 Git에 commit하지 않는다.
