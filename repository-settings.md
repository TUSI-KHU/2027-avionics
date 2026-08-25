# 관리자용: 저장소의 실제 설정과 제한 사항

Repository: [TUSI-KHU/2027-avionics](https://github.com/TUSI-KHU/2027-avionics)

이 문서는 GitHub API로 확인한 **실제 적용 상태**를 기록한다. 희망 설정을 적용된 것처럼 표기하지 않는다.

## 적용 설정

- Visibility: Private
- Default branch: `main`
- Issues: 활성화
- Discussions, Wiki: 비활성화
- Merge 방식: squash만 허용
- Merge된 head branch 자동 삭제: 활성화
- License file: MIT
- PR template: `.github/pull_request_template.md`
- Issue form: `.github/ISSUE_TEMPLATE/task.yml`
- CI check job: `repository-contract`

## `main` 보호 상태

현재 branch protection/ruleset은 **미적용**이다. GitHub API가 이 private repository에 대해 다음 제한을 반환한다.

> Upgrade to GitHub Pro or make this repository public to enable this feature.

따라서 아래 정책은 현재 자동 강제되지 않으며 팀 운영 규칙으로만 적용한다.

- merge 전 Pull Request 사용
- 일반 변경은 독립 reviewer 1명 승인
- 비행 중요 변경은 Technical Lead와 독립 reviewer를 포함해 최소 2명 승인
- 새 commit 후 재검토
- 모든 review conversation 해결
- `repository-contract` check 통과
- `main` force push와 삭제 금지

지원 plan으로 변경하거나 repository를 public으로 전환한 뒤 ruleset을 생성하고 위 항목을 required rule로 설정해야 한다. 그 전까지 administrator도 같은 review 절차를 따른다.

## CODEOWNERS

실제 GitHub 계정 또는 존재하는 team이 확정되지 않아 `.github/CODEOWNERS`는 만들지 않는다. 역할 확정 후 실제 handle로 추가하고 그때 Code Owner review를 ruleset에 연결한다.

## 검증

```bash
uv venv .venv
uv pip install --python .venv/bin/python --require-hashes -r requirements-dev.txt
make validate PYTHON=.venv/bin/python
```

GitHub Actions의 `repository-contract` job도 같은 명령을 실행한다. 이 check가 존재하는 것과 merge 조건으로 강제되는 것은 별개이며, 현재는 plan 제한 때문에 required check로 지정할 수 없다.
