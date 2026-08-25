# 2027 Avionics

NURA 발사대회급 400m 로켓 Avionics 개발 저장소입니다.

## 협업 시작점

- [협업 흐름](CONTRIBUTING.md)
- [GitHub Project 실설정 기준선](project-configuration.md)
- [저장소 설정과 제한 사항](repository-settings.md)
- [2027 Avionics Project](https://github.com/orgs/TUSI-KHU/projects/1)

```bash
uv venv .venv
uv pip install --python .venv/bin/python --require-hashes -r requirements-dev.txt
make validate PYTHON=.venv/bin/python
```

Task는 Issue로 관리하고, 구현은 branch와 Pull Request를 거쳐 squash merge합니다. 상태와 우선순위는 GitHub Project의 현재 설정을 기준으로 합니다.
