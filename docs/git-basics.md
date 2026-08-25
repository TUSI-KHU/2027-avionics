# 선택 문서: 이 저장소에서 필요한 Git 기초

Git이 익숙하지 않을 때만 읽으면 됩니다. Git의 모든 기능을 설명하지 않습니다. 이 저장소에서 Issue 하나를 맡아 branch에서 작업하고 PR을 올리는 데 필요한 내용만 다룹니다.

현재 팀 workflow는 다음과 같습니다.

```text
Issue 만들기 → In Progress로 옮기기 → branch 만들기 → commit → push → PR → review → merge
```

## 1. Git과 GitHub의 차이

- Git은 내 컴퓨터에서 파일의 변경 이력을 관리하는 도구입니다.
- GitHub는 Git repository를 팀원과 공유하고 Issue와 PR을 관리하는 서비스입니다.

인터넷이 없어도 파일 수정과 commit은 할 수 있습니다. `pull`과 `push`, PR 작성에는 GitHub 연결이 필요합니다.

## 2. 꼭 알아야 할 용어

| 용어 | 이 저장소에서의 뜻 |
|---|---|
| repository | 파일과 변경 이력을 함께 보관하는 작업 공간 |
| local | 내 컴퓨터에 있는 repository |
| remote | GitHub에 있는 repository |
| `origin` | 이 local repository가 연결된 기본 remote 이름 |
| `main` | 팀이 기준으로 삼는 branch |
| branch | `main`에 바로 손대지 않고 내 변경을 만드는 공간 |
| `HEAD` | 지금 내가 작업하고 있는 branch 또는 commit |
| commit | 관련된 변경을 하나의 단위로 저장한 것 |
| staged | 다음 commit에 넣기로 고른 변경 |
| `pull` | remote의 새 변경을 local로 가져오는 것 |
| `push` | local commit을 remote로 올리는 것 |
| PR | 내 branch를 `main`에 merge해 달라고 요청하는 곳 |
| merge | 한 branch의 변경을 다른 branch에 합치는 것 |

## 3. 처음 한 번만 준비하기

### repository 내려받기

아직 repository가 없다면 다음 명령을 실행합니다.

```bash
git clone https://github.com/TUSI-KHU/2027-avionics.git
cd 2027-avionics
```

private repository라서 GitHub 접근 권한과 로그인이 필요합니다.

### 이름과 이메일 설정하기

commit에는 작성자 정보가 들어갑니다. 아래 값은 자신의 GitHub 이름과 이메일로 바꿉니다.

```bash
git config --global user.name "이름"
git config --global user.email "GitHub 이메일"
```

설정값은 다음 명령으로 확인합니다.

```bash
git config --global user.name
git config --global user.email
```

공용 컴퓨터에서는 `--global`을 쓰지 말고 담당자에게 먼저 문의합니다.

## 4. 작업을 시작하는 순서

예시에서는 Issue 번호가 `12`, 작업 내용이 센서 목록 문서라고 가정합니다.

### 1) 현재 상태 확인

```bash
git status
```

먼저 다음을 확인합니다.

- 현재 branch가 무엇인지
- 아직 commit하지 않은 변경이 있는지
- Git이 추적하지 않는 새 파일이 있는지

내가 만들지 않은 변경이 보이면 삭제하거나 덮어쓰지 말고 먼저 팀원에게 확인합니다.

### 2) 최신 `main` 받기

```bash
git switch main
git pull --ff-only
```

- `git switch main`: 현재 branch를 `main`으로 바꿉니다.
- `git pull --ff-only`: GitHub의 최신 `main`을 가져옵니다. 이력 모양을 임의로 바꿔야 하는 상황이면 명령이 멈춥니다.

명령이 실패하면 억지로 진행하지 말고 오류를 Issue에 붙여 넣어 도움을 요청합니다.

### 3) 내 branch 만들기

```bash
git switch -c docs/12-sensor-list
```

`-c`는 새 branch를 만들고 바로 그 branch로 이동한다는 뜻입니다.

branch 이름은 다음 형식을 사용합니다.

```text
종류/Issue번호-짧은-설명
```

자주 쓰는 종류:

- `feat`: 새 기능
- `fix`: 잘못된 동작 수정
- `docs`: 문서 변경
- `test`: 시험 또는 검사 추가
- `chore`: 설정이나 정리

현재 branch는 다음 명령으로 확인합니다.

```bash
git branch --show-current
```

## 5. 파일을 바꾼 뒤 확인하기

### 어떤 파일이 바뀌었는지 확인

```bash
git status --short
```

대표적인 표시:

- `M`: 기존 파일을 수정함
- `??`: 아직 Git이 추적하지 않는 새 파일
- `D`: 파일을 삭제함

예상하지 못한 `D`가 보이면 commit하지 말고 먼저 확인합니다.

### 실제 변경 내용 확인

```bash
git diff
```

새 파일은 `git diff`에 내용이 나오지 않을 수 있습니다. `git status --short`도 함께 봅니다.

## 6. commit 만들기

### 1) commit에 넣을 파일 고르기

```bash
git add docs/sensor-list.md
```

가능하면 `git add .` 대신 파일 이름을 적습니다. 그래야 비밀번호 파일이나 관계없는 변경이 실수로 들어가는 것을 줄일 수 있습니다.

여러 파일을 함께 넣을 수도 있습니다.

```bash
git add README.md docs/sensor-list.md
```

### 2) 고른 변경 확인

```bash
git diff --staged
```

이 명령에 나오는 내용이 다음 commit에 들어갑니다.

확인할 것:

- 내가 의도한 파일만 들어갔는가
- 비밀번호나 인증 정보가 없는가
- 큰 원본 자료나 자동 생성 파일이 없는가
- 임시 메모와 디버그 출력이 없는가

### 3) commit 저장

```bash
git commit -m "docs: 센서 목록 작성 방법 추가"
```

commit 메시지는 무엇을 바꿨는지 한 문장으로 적습니다.

좋은 예:

```text
docs: 센서 목록 작성 방법 추가
fix: 패킷 길이 검사 오류 수정
test: 전원 차단 시험 절차 추가
```

피할 예:

```text
수정함
최종
여러 가지 변경
```

commit 뒤 상태를 다시 확인합니다.

```bash
git status
```

## 7. PR 전에 검사하기

처음 한 번만 검사 환경을 만듭니다.

```bash
uv venv .venv
uv pip install --python .venv/bin/python --require-hashes -r requirements-dev.txt
```

PR을 올리기 전에는 다음 명령을 실행합니다.

```bash
make validate PYTHON=.venv/bin/python
```

실패하면 출력된 `ERROR`부터 해결합니다. 해결하기 어렵다면 오류를 Issue에 그대로 붙여 넣습니다.

## 8. branch를 GitHub에 push하기

```bash
git push -u origin HEAD
```

각 부분의 뜻:

- `push`: local commit을 remote에 올림
- `-u`: 다음부터 같은 branch에 `git push`만 써도 되도록 연결함
- `origin`: 기본 remote
- `HEAD`: 현재 branch

첫 push 뒤에는 보통 다음 명령만 사용해도 됩니다.

```bash
git push
```

## 9. PR 만들기

GitHub에서 내 branch의 PR을 만듭니다. 자동으로 나온 양식을 채우고 다음처럼 Issue를 연결합니다.

```text
Refs #12
```

`Closes #12`는 사용하지 않습니다. PR을 merge한 뒤 별도의 확인이 남아 있을 수 있기 때문입니다.

PR을 올린 뒤 Issue 상태를 `Review`로 바꿉니다. review 의견을 반영할 때는 같은 branch에서 수정하고 새 commit을 만든 뒤 다시 push합니다.

```bash
git add 바꾼-파일
git commit -m "docs: review 의견 반영"
git push
```

기존 PR에 새 commit이 자동으로 추가됩니다. PR을 새로 만들 필요가 없습니다.

## 10. merge 뒤 정리하기

PR이 merge되고 Issue의 완료 조건까지 확인한 뒤 Issue를 닫습니다.

local `main`은 다음처럼 최신 상태로 맞춥니다.

```bash
git switch main
git pull --ff-only
git fetch --prune
```

- `git fetch --prune`: GitHub에서 이미 삭제된 remote branch의 오래된 표시를 local에서 정리합니다.
- remote branch는 repository 설정에 따라 merge 뒤 자동으로 삭제됩니다.

squash merge 뒤에는 Git이 local branch를 "merge 완료"로 판단하지 못할 수 있습니다. local branch 삭제는 작업에 꼭 필요하지 않으므로 이 문서에서는 다루지 않습니다.

## 11. 자주 생기는 상황

### branch를 만들기 전에 파일을 수정했다

아직 commit하지 않았다면 보통 다음 명령으로 새 branch를 만든 뒤 계속할 수 있습니다.

```bash
git switch -c docs/12-sensor-list
```

그다음 `git status`와 `git diff`로 변경이 그대로 있는지 확인합니다.

### `push`가 거부됐다

다음 명령을 바로 사용하지 않습니다.

```text
git push --force
```

remote에 내가 모르는 변경이 있을 수 있습니다. 오류 전체와 `git status` 결과를 Issue에 붙여 넣고 도움을 요청합니다.

### 충돌(conflict)이 발생했다

Git이 같은 부분을 자동으로 합치지 못한 상태입니다. 먼저 다음 명령을 실행합니다.

```bash
git status
```

충돌한 파일을 확인한 뒤 담당자나 reviewer와 해결합니다. 내용을 모른 채 충돌 표시를 지우거나 한쪽 변경을 전부 선택하지 않습니다.

### 잘못된 파일을 `git add`했다

아직 commit하지 않았다면 다음 명령으로 staged 상태만 해제할 수 있습니다. 파일 수정 내용은 남습니다.

```bash
git restore --staged 잘못-고른-파일
```

## 12. 초심자가 피해야 할 명령

다음 명령은 변경이나 이력을 크게 지울 수 있습니다. 이 문서의 workflow에는 필요하지 않습니다.

```text
git reset --hard
git clean -fd
git push --force
git branch -D
```

필요해 보이더라도 혼자 실행하지 말고 먼저 도움을 요청합니다.

## 시작 전 확인

```text
[ ] 작업할 Issue가 있다.
[ ] Issue에 담당자, 완료 조건, 확인 방법이 있다.
[ ] Issue 상태가 In Progress다.
[ ] git status로 기존 변경을 확인했다.
[ ] 최신 main에서 새 branch를 만들었다.
```

## PR 전 확인

```text
[ ] git status로 바뀐 파일을 확인했다.
[ ] git diff와 git diff --staged를 확인했다.
[ ] 비밀번호, 인증 정보, 큰 원본 자료가 없다.
[ ] commit 메시지가 변경 내용을 설명한다.
[ ] make validate가 통과했다.
[ ] branch를 push했다.
[ ] PR에 Refs #Issue번호를 적었다.
```
