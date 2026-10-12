---
title: "GitHub 저장소 및 브랜치 보호 설정 가이드"
type: guideline
status: active
tags:
  - domain/avionics
  - guideline/settings
  - github
aliases:
  - RepositorySettings
  - 저장소설정
created: 2026-10-12
updated: 2026-10-12
---

# ⚙️ GitHub 저장소 및 브랜치 보호 설정 가이드

> [!NOTE]
> NURA Avionics 저장소 관리자와 팀원을 위한 GitHub 권장 설정 기준입니다.
> 전체 지식 맵은 [[docs/Index|Index (MOC)]]를 참조하십시오.

---

## 1. 일반 설정 (General Repository Settings)

- **Default branch**: `main`
- **Pull Requests**:
  - `Allow squash merging` 활성화 (커밋 히스토리를 깔끔하게 유지하기 위해 Squash merge 권장)
  - `Automatically delete head branches` 활성화 (머지 완료된 feature 브랜치 자동 정리)
- **Features**:
  - `Issues` 활성화
  - `Projects` 활성화

---

## 2. 브랜치 보호 규칙 (`main` Branch Protection)

> [!IMPORTANT]
> `main` 브랜치는 항상 동작 가능한 릴리스 형상을 유지해야 하므로 직접 푸시(Direct Push)를 금지합니다.

- `Require a pull request before merging` 체크
- `Require approvals`: 1명 이상 승인 권장
- `Dismiss stale pull request approvals when new commits are pushed` 체크
- `Do not allow bypassing the above settings` 체크 (관리자도 PR을 통해 머지)

---

## 3. 연관 문서
- [[docs/wiki/guidelines/project-workflow|GitHub Projects 칸반 및 협업 가이드]]
- [[CONTRIBUTING|기여 가이드 (CONTRIBUTING.md)]]
