# 작업 기록

실제로 수행한 작업, 명령과 결과만 기록한다. 예상 명령과 가상의 결과는 작성하지 않는다.

## 2026-08-05 — 초기 문서 구성

### 환경

- 문서 생성 단계
- 실제 저장소 경로: 확인 필요
- 실제 브랜치: 확인 필요
- Python 버전: 미확인
- 운영체제 실행 검증: 미실행

### 변경 파일

- `AGENTS.md`
- `MISSION.md`
- `README.md`
- `.gitignore`
- `.gitattributes`
- `docs/requirements.md`
- `docs/progress.md`
- `docs/worklog.md`
- `docs/troubleshooting.md`
- `evidence/.gitkeep`

### 수행 내용

- 미션 원문을 필수 기능, 데이터, 성능, 문서와 제약으로 분류
- 요구사항 추적표 작성
- 단계별 구현 순서와 권장 커밋 계획 작성
- 실제 결과가 없는 항목을 모두 `예정`, `TODO`, `미검증`으로 표시
- `data.json` 상세 구조가 미확정임을 기록

### 실행 명령

없음.

### 실제 결과

- 코드 실행 없음
- 테스트 실행 없음
- 성능 측정 없음
- PASS/FAIL 결과 없음
- 증거 파일 없음

### 다음 작업

`mini_npu.py`에 MAC 연산과 epsilon 판정 로직을 구현하고 예시 데이터로 검증한다.

## 2026-08-06 — 단계 1 핵심 MAC과 판정 로직 구현

### 작업 시작 상태

- 브랜치: `main`
- 작업 트리: 변경사항 없음
- 최근 커밋: `e25d9d8 Chore: 프로젝트 초기 파일 구성`
- Python 버전: 3.12.13

### 변경 파일

- `AGENTS.md`
- `mini_npu.py`
- `README.md`
- `docs/requirements.md`
- `docs/progress.md`
- `docs/worklog.md`

### 수행 내용

- 사용자 승인 후 단계 1 범위만 구현
- 숫자로 구성된 정사각형 행렬 검증 구현
- 패턴과 필터 크기 일치 검증 구현
- 외부 라이브러리 없이 이중 반복문 MAC 계산 구현
- 기본 epsilon `1e-9` 기반 Cross/X/UNDECIDED 판정 구현
- NaN, 무한대, bool과 숫자가 아닌 값의 오류 처리 구현
- 구현과 동시에 요구사항, 진행 상태와 README 갱신
- Codex가 유닛 테스트를 작성·실행하지 않는 작업 방침을 `AGENTS.md`에 반영

### 실행 명령과 실제 결과

- 코드 실행 없음
- 유닛 테스트 작성 및 실행 없음
- 성능 측정 없음
- PASS/FAIL 결과 없음

### 다음 작업

사용자가 단계 1 핵심 로직을 직접 검증한다. 검증 결과가 확인되면 단계 2 사용자 입력 모드의 구현 방향을 설명하고 승인을 받는다.
