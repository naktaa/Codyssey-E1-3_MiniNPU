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

## 2026-08-06 — 단계 2 사용자 입력 모드 구현

### 변경 파일

- `AGENTS.md`
- `main.py`
- `mini_npu.py` 삭제 후 `src/mini_npu.py`로 이동
- `src/__init__.py`
- `src/manual_mode.py`
- `README.md`
- `docs/requirements.md`
- `docs/progress.md`
- `docs/worklog.md`

### 수행 내용

- 향후 소스 증가를 고려해 핵심 모듈을 `src/` 패키지로 분리
- 루트 `main.py`에 실행 메뉴와 종료 처리 구현
- 3×3 필터 A(Cross), 필터 B(X), 패턴 입력 구현
- 열 개수, 숫자 형식, NaN과 무한대 오류 시 해당 행만 재입력하도록 구현
- 기존 MAC과 epsilon 판정을 사용자 입력 흐름에 연결
- Cross/X 점수와 사용자용 판정 결과 출력 구현
- `perf_counter_ns()`로 `calculate_mac()` 1회를 1,000회 반복한 평균 시간 계산 구현
- 측정 대상과 실제 반복 횟수를 콘솔 출력에 명시
- 필요한 로그와 캡처를 구현 후 안내하고 임시 Python 검증 예시는 생략하도록 작업 지침 갱신

### 실행 명령과 실제 결과

- 코드 실행 없음
- 유닛 테스트 작성 및 실행 없음
- 성능 측정 결과 없음
- PASS/FAIL 결과 없음

### 다음 작업

사용자가 `python3 main.py`로 사용자 입력 모드를 직접 검증한다. 결과가 확인되면 단계 3 JSON 로드와 라벨 정규화의 구현 방향을 설명하고 승인을 받는다.

## 2026-08-06 — 사용자 실행 결과 반영과 메뉴 분리

### 사용자 제공 실행 결과

- 실행 명령: `py`
- Cross 점수: `3.000000`
- X 점수: `6.000000`
- 판정: `X`
- 3×3 평균 MAC 시간: `0.018066 ms`
- 측정 대상: 패턴과 필터 A의 `calculate_mac()` 1회
- 반복 횟수: 1,000회

입력값을 위치별로 계산한 Cross 점수 3과 X 점수 6이 실제 출력과 일치했다. 오류 입력 재시도는 이 실행에서 확인하지 않았다.

### 변경 파일

- `main.py`
- `src/menu.py`
- `src/manual_mode.py`
- `AGENTS.md`
- `MISSION.md`
- `evidence/FUNC-008-manual-mode-x.md`
- `README.md`
- `docs/requirements.md`
- `docs/progress.md`
- `docs/worklog.md`
- `docs/troubleshooting.md`

### 수행 내용

- `main.py`에서 메뉴 출력과 선택 처리를 제거해 실행 진입점만 유지
- 메뉴 흐름을 `src/menu.py`로 분리
- 실제 사용자 로그에 맞춰 종료 메뉴 번호를 3으로 통일
- `패턴를 입력하세요` 문구를 `패턴 행렬을 입력하세요`로 수정
- 실행 로그를 개인정보가 없는 Markdown 증거로 정리
- 정상 입력, 점수, X 판정과 3×3 성능 결과를 요구사항과 README에 반영

### Codex 실행 여부

- 코드 실행 없음
- 유닛 테스트 작성 및 실행 없음
- Git 명령 실행 없음

### 다음 작업

사용자가 오류 입력 후 같은 행을 다시 요청하는지 확인한다. 결과를 받은 뒤 단계 3 JSON 로드와 라벨 정규화의 구현 방향을 설명한다.

## 2026-08-06 — 사용자 입력 오류 재시도 결과 반영

### 사용자 제공 실행 결과

- 필터 A 2행에 숫자 4개 입력 후 열 개수 오류 메시지 확인
- 오류 뒤 필터 A 2행을 다시 요청하는 동작 확인
- 필터 A 3행에 문자 `q` 입력 후 숫자 형식 오류 메시지 확인
- 오류 뒤 필터 A 3행을 다시 요청하는 동작 확인
- 정상적으로 입력한 이전 행은 다시 요청하지 않음

### 변경 파일

- `evidence/FUNC-007-invalid-input.md`
- `README.md`
- `docs/requirements.md`
- `docs/progress.md`
- `docs/worklog.md`

### 실제 결과

- `FUNC-007`: 필수 열 개수·숫자 형식 오류의 행 단위 재입력 확인
- `EVID-002`: Markdown 실행 로그 확보
- NaN과 무한대 입력 재시도는 실행하지 않음

### Codex 실행 여부

- 코드 실행 없음
- 유닛 테스트 작성 및 실행 없음
- Git 명령 실행 없음

### 다음 작업

단계 3 JSON 로드와 라벨 정규화의 구현 방향을 설명하고 사용자 승인을 받는다.
