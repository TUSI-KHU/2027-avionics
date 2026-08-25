# GitHub Project 실설정 기준선

Project: [2027 Avionics](https://github.com/orgs/TUSI-KHU/projects/1)

이 문서는 Project API로 조회한 **현재 실설정**을 기록한다. 문서와 Project가 다르면 Project를 기준으로 운영하고 문서를 갱신한다.

## Field

Project에는 built-in field 12개와 custom field 6개, 총 18개가 있다.

### Custom field

| Field | 형식 | 현재 값 |
|---|---|---|
| Status | Single select | Backlog, In Progress, Review, Done, Canceled |
| Priority | Single select | P0, P1, P2 |
| 유형 | Single select | Feature, Change, Defect, Research, Test, Risk, Anomaly |
| Subsystem | Single select | SYS, HW, FSW, GNC, RF, GS, TEST |
| Gate | Single select | G0, G1, G2, G3, Post-flight |
| Target date | Date | 기한이 있는 항목에 입력 |

`Target date`를 포함하면 custom field는 여섯 종류지만 API의 총 field 18개에는 built-in field 12개와 함께 계산된다. GitHub가 `Type` 이름을 사용하므로 custom field 이름은 `유형`이다.

### Built-in field

`Title`, `Assignees`, `Labels`, `Linked pull requests`, `Milestone`, `Repository`, `Reviewers`, `Parent issue`, `Sub-issues progress`, `Created`, `Updated`, `Closed`가 활성화되어 있다.

### Status

| 값 | Color | 현재 description |
|---|---|---|
| Backlog | Gray | 해야 할 Task |
| In Progress | Yellow | 수행하고 있는 Task |
| Review | Purple | PR 혹은 재현 가능한 결과가 도출된 Task |
| Done | Green | Merge와 검증을 모두 완료한 Task |
| Canceled | Pink | 취소 근거와 영향을 기록한 결정 보관용 Task |

### Priority

| 값 | Color | 현재 description |
|---|---|---|
| P0 | Red | 필수 기능 |
| P1 | Orange | 목표 기능 |
| P2 | Blue | 상황에 따라 제외 가능한 기능 |

### 유형

| 값 | Color | 현재 description |
|---|---|---|
| Feature | Blue | 새 capability |
| Change | Purple | 승인된 설계 또는 interface 변경 |
| Defect | Red | 기대 결과와 실제 결과의 불일치 |
| Research | Green | 설계 결정을 위한 조사 또는 계산 |
| Test | Yellow | 시험 절차 작성 또는 실행 |
| Risk | Orange | 일정, 기술 또는 조달 위험 |
| Anomaly | Pink | 시험 또는 비행 중 예기치 않은 현상 |

### Subsystem

| 값 | Color | 현재 description |
|---|---|---|
| SYS | Purple | 시스템 요구사항, architecture와 안전 |
| HW | Orange | 비행 컴퓨터, 전원과 hardware 통합 |
| FSW | Blue | 비행 firmware와 장치 제어 |
| GNC | Green | 상태 추정, guidance와 자세 제어 |
| RF | Pink | 무선 link와 protocol |
| GS | Yellow | 지상국 software와 운용 도구 |
| TEST | Red | 시험, 검증과 evidence 관리 |

### Gate

| 값 | Color | 현재 description |
|---|---|---|
| G0 | Gray | 임무, 역할과 scope 확정 |
| G1 | Blue | 요구사항, 설계와 interface 기준선 |
| G2 | Green | prototype, 설계 동결과 통합 검증 |
| G3 | Yellow | P0 검증, manifest와 비행 준비 승인 |
| Post-flight | Pink | 비행 data, anomaly와 개선 Task 검토 |

## View

| View | Layout | 현재 filter |
|---|---|---|
| Board | Board | `-status:Done,Canceled` |
| All Tasks | Table | 없음 |
| P0 Progress | Table | `priority:P0 -status:Done,Canceled` |
| My Tasks | Board | `assignee:@me -status:Done,Canceled` |
| My Review | Table | `status:Review` |
| Backlog | Table | 없음 |

`Backlog` 뷰 이름과 달리 현재 filter는 비어 있다. 이 문서에서는 의도를 추정해 보정하지 않고 실설정을 그대로 기록한다.

## Workflow

현재 활성화된 built-in workflow는 두 개다.

- `Item added to project`: 추가된 item의 Status를 `Backlog`로 설정
- `Item closed`: 닫힌 Issue의 Status를 `Done`으로 설정

`Item closed`는 검증 여부나 취소 사유를 구분하지 않는 실설정이다. 따라서 PR에는 `Refs #`를 사용하고, merge 후 완료 조건과 검증을 확인한 다음 Issue를 수동으로 닫아 `Done` 전이를 발생시킨다. 취소하는 Issue는 근거와 영향을 기록하고 닫은 뒤 자동 전이가 끝나면 Status를 `Canceled`로 다시 지정한다. 다시 열린 Issue도 수동으로 상태를 조정한다. 같은 Task의 Issue와 PR을 별도 card로 중복 관리하지 않는다.

## 현재 Item

현재 9개 item이 있다.

| 형태 | 상태 | 제목 |
|---|---|---|
| Issue #1 | Backlog | `[G0] 역할 분배 확정` |
| Draft Item | Backlog | `[G0] 일정 및 타임라인, 주간 가용 시간 확정` |
| Draft Item | Backlog | `[G0] Avionics 부품, airframe interface 요구사항 확정` |
| Draft Item | Backlog | `[G0] 시험 장비, 장소, RF, 안전 제약 확정` |
| Draft Item | Backlog | `[G0] Raw flight data archive, backup 책임 확정` |
| Draft Item | Backlog | `[G0] 개발 toolchain과 version pinning 정책 확정` |
| Draft Item | Backlog | `[협업] 최초 baseline 검토, push 후 main ruleset 적용` |
| Draft Item | Backlog | `[협업] 팀원별 Issue->branch->PR dry run` |
| Issue #2 | In Progress | `[협업] Discord 서버와 GitHub 자동화 기준선 설정` |

착수할 Draft Item은 repository Issue로 전환하고 owner, 완료 조건과 검증 방법을 확인한 뒤 `In Progress`로 이동한다.

## 운영 규칙

```text
Backlog -> In Progress -> Review -> Done
Backlog/In Progress/Review -> Canceled
```

- 팀원별 주요 `In Progress` Task는 하나로 제한한다.
- `In Progress` 전에 owner, 완료 조건과 검증 방법을 정한다.
- `Review`에는 PR 또는 재현 가능한 실험 결과가 있어야 한다.
- `Done`은 merge와 검증 완료를 모두 요구한다.
- 독립 reviewer는 구현 Task의 A/R과 같을 수 없다.
- 관련 ID와 상세 traceability는 P0, 안전 또는 subsystem interface 관련 Task에 필수다.
- 막힌 Task에는 원인, 해제 조건과 다음 action을 기록한다.
- 일정 지연은 P2, P1 순으로 scope를 축소하고 P0은 축소하지 않는다.
