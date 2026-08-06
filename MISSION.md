# E1-3 Mini NPU 시뮬레이터 미션

## 1. 미션 목적

2차원 숫자 배열로 표현한 패턴과 필터 사이의 MAC(Multiply-Accumulate) 점수를 반복문으로 계산하고, 점수 비교를 통해 패턴을 판정하는 Python 콘솔 애플리케이션을 구현한다.

사용자 입력 3×3 모드와 `data.json` 일괄 분석 모드를 지원하고, 3×3·5×5·13×13·25×25 크기의 연산 시간을 측정하여 O(N²) 시간 복잡도를 설명할 수 있어야 한다.

## 2. 필수 제출물

- `main.py`: 메인 실행 파일
- `README.md`: 실행 방법, 구현 요약, 실제 결과 리포트
- `data.json`: 평가용 데이터가 제공되거나 사용자가 전달한 경우 저장소 루트에 배치
- 정상 동작하는 Python 콘솔 애플리케이션

현재 저장소 루트에는 실제 평가용 `data.json`이 있으며, 문서와 실행 결과는 해당 파일을 기준으로 한다.

## 3. 필수 기능

### 사용자 입력 모드

- 3×3 필터 A 입력
- 3×3 필터 B 입력
- 3×3 패턴 입력
- 행·열 개수와 숫자 형식 검증
- 오류가 있는 행 재입력
- 두 MAC 점수 출력
- epsilon 기반 A/B/판정 불가 판정
- 최소 10회 반복한 3×3 평균 MAC 시간 출력

### data.json 분석 모드

- `filters.size_5`, `filters.size_13`, `filters.size_25` 로드
- `patterns.size_{N}_{idx}` 형태의 케이스 처리
- 키에서 N을 추출해 대응 필터 선택
- 필터와 패턴의 정사각형 크기 검증
- 스키마·크기 오류가 있어도 전체 프로그램을 중단하지 않고 케이스 단위 FAIL 처리
- 라벨 정규화
  - expected `+` → `Cross`
  - expected `x` → `X`
  - filter key `cross` → `Cross`
  - filter key `x` → `X`
- Cross/X 점수, 판정, expected, PASS/FAIL 출력
- 총 테스트·통과·실패 수와 실패 케이스 사유 출력

### MAC 및 판정

- NumPy 등 외부 라이브러리 금지
- 이중 반복문으로 같은 위치의 값을 곱하고 누적
- 실수 점수 허용
- `abs(score_cross - score_x) < epsilon`이면 `UNDECIDED`
- 내부 표준 라벨은 `Cross`, `X`
- `UNDECIDED`는 expected가 Cross/X인 경우 불일치이므로 FAIL 처리

### 성능 분석

- 크기별 최소 10회 반복 측정
- 3×3, 5×5, 13×13, 25×25 포함
- 파일 읽기·입력·출력 시간을 제외하고 MAC 함수 호출 구간 측정
- 크기, 평균 시간(ms), 연산 횟수 N² 출력
- 실제 측정값을 근거로 O(N²) 설명

## 4. 기술 및 품질 제약

- Python 3.8 이상
- 표준 라이브러리만 사용
- UTF-8과 LF 사용
- 개인 PC 절대 경로 금지
- 숫자 파싱·파일 읽기·JSON 디코딩·스키마 오류를 적절히 처리
- 실제 실행 결과와 측정값만 문서화
- 보너스는 필수 기능 완료 후 별도 진행

## 5. 현재 프로젝트 구조

소스 파일 증가와 역할 분리를 고려해 실행 진입점은 루트에 두고 구현 모듈은 `src/` 패키지로 관리한다.

```text
.
├── main.py
├── src/
│   ├── __init__.py
│   ├── menu.py
│   ├── mini_npu.py
│   ├── manual_mode.py
│   ├── data_loader.py
│   ├── json_mode.py
│   ├── performance.py
│   └── report.py
├── data.json
├── docs/
│   ├── requirements.md
│   ├── progress.md
│   ├── worklog.md
│   └── troubleshooting.md
├── evidence/
├── AGENTS.md
├── MISSION.md
├── README.md
├── .gitignore
└── .gitattributes
```

- `main.py`: 프로그램 실행 진입점
- `src/menu.py`: 메뉴 출력과 모드 선택 흐름
- `src/mini_npu.py`: MAC, epsilon 비교, 판정과 단일 MAC 성능 측정
- `src/manual_mode.py`: 3×3 사용자 입력 흐름
- `src/data_loader.py`: JSON 읽기, 키 해석, 라벨 정규화와 스키마 검증
- `src/json_mode.py`: JSON 케이스별 판정 흐름
- `src/performance.py`: 필수 네 크기의 성능 측정 입력과 결과 구성
- `src/report.py`: 케이스 결과, 전체 요약과 성능 표 출력

작은 미션이므로 불필요한 패키지 계층이나 과도한 클래스 구조는 만들지 않는다.

## 6. 구현 단계

### 단계 1. 핵심 데이터와 MAC 연산

- 요구사항: TECH-001, FUNC-001, FUNC-002, FUNC-003
- 구현: 정사각형 행렬 검증, 반복문 MAC, epsilon 판정
- 정상 기준: Cross/X 예시 점수가 각각 5와 1로 계산되고 동점 정책이 동작
- 권장 커밋: `Feat: MAC 연산과 판정 로직 구현`

### 단계 2. 사용자 입력 3×3 모드

- 요구사항: FUNC-004~FUNC-007
- 구현: 행별 입력, 재입력, A/B 점수와 판정, 3×3 성능 측정
- 정상 기준: 잘못된 열 수와 숫자 입력 후 같은 행을 다시 입력할 수 있음
- 권장 커밋: `Feat: 3x3 사용자 입력 모드 구현`

### 단계 3. JSON 로드와 정규화

- 요구사항: DATA-001~DATA-006, FUNC-008~FUNC-010
- 구현: 파일·JSON 예외 처리, size 키 추출, 필터 선택, 라벨 정규화
- 정상 기준: 실제 `data.json` 구조를 읽고 케이스별 오류를 분리
- 권장 커밋: `Feat: JSON 데이터 로드와 스키마 검증 구현`

### 단계 4. 일괄 판정과 결과 요약

- 요구사항: FUNC-011~FUNC-014
- 구현: Cross/X 점수, expected 비교, PASS/FAIL, 실패 목록
- 정상 기준: 오류 케이스가 있어도 다음 케이스까지 실행하고 합계가 맞음
- 권장 커밋: `Feat: JSON 일괄 판정과 결과 요약 구현`

### 단계 5. 크기별 성능 분석

- 요구사항: PERF-001~PERF-004
- 구현: 3·5·13·25 크기 최소 10회 측정, 평균과 N² 표
- 정상 기준: I/O를 제외한 측정값이 표로 출력
- 권장 커밋: `Feat: 크기별 MAC 성능 분석 구현`

### 단계 6. 수동 검증·증거·README

- 요구사항: TEST-003~TEST-004, EVID-001~EVID-005, DOC-001~DOC-004
- 구현: 사용자 수동 콘솔 검증, 증거 저장, README 결과 리포트와 문서 최종 동기화
- 정상 기준: 필수 재현 시나리오가 macOS에서 성공하고 문서와 일치
- 유닛 테스트: 사용자 작업 방침에 따라 작성하거나 실행하지 않음
- 권장 커밋: `Docs: 수동 검증 결과와 문서 동기화`

## 7. Git 작업 방침

commit, push와 merge는 사용자가 직접 수행한다. Codex는 구현이 끝난 뒤 변경 범위에 맞는 권장 커밋 메시지만 안내한다.

## 8. 증거 수집 계획

실제 실행 후에만 저장한다.

- `evidence/manual-mode-success.md`
  - 3×3 Cross/X 필터와 X 판정 실행 결과
- `evidence/invalid-input.md`
  - 열 개수 오류와 숫자 파싱 오류 후 같은 행 재입력 로그
- `evidence/json-load.md`
  - 실제 필터·패턴 구조, 키 해석과 라벨 정규화 결과
- `evidence/size-mismatch.md`
  - 크기 불일치 케이스가 FAIL 처리되고 다음 케이스가 계속된 결과
- `evidence/json-analysis.md`
  - 전체 테스트·통과·실패와 실패 목록
- `evidence/performance.md`
  - 3×3·5×5·13×13·25×25 성능 표
- 유닛 테스트 증거는 사용자 작업 방침에 따라 생성하지 않음

텍스트 로그로 충분한 결과는 스크린샷을 강제하지 않는다.

## 9. 확정된 구현 결정과 남은 조건

1. 실제 `data.json`은 `filters.size_N` 아래 `cross`, `x` 필터를 두며 내부에서 `Cross`, `X`로 정규화한다.
2. 패턴 키는 실제 데이터의 `size_{N}_{idx}` 형식을 해석하고 N에 맞는 필터를 연결한다.
3. expected `+`, `cross`는 `Cross`, `x`는 `X`로 정규화하며 공백과 대소문자 차이를 허용한다.
4. 성능 시간은 패턴과 Cross 필터의 `calculate_mac()` 한 번에 대한 반복 평균으로 정의한다.
5. `data.json`에 없는 3×3 성능 입력은 코드 내부 기준 행렬을 사용한다.
6. JSON 파일 자체가 없거나 최상위 구조가 손상된 경우 모드 오류로 안내하고 안전 종료한다. 이 오류 시나리오는 실행 검증 전이다.
7. 실제 성능 수치는 실행 환경에 따라 달라지므로 실행일의 측정 결과와 조건을 함께 기록한다.

## 10. 제출을 막을 수 있는 조건

- `data.json` 구조를 잘못 추측해 실제 파일을 읽지 못함
- MAC 계산에 NumPy 등 외부 라이브러리 사용
- 라벨을 `+`, `x`, `cross` 상태로 직접 비교하여 PASS/FAIL 오류 발생
- `==`로 실수 점수를 비교해 거의 같은 점수를 동점 처리하지 못함
- 크기 불일치 한 건 때문에 프로그램 전체가 종료됨
- 성능 측정에 `input`, `print`, 파일 읽기 시간이 포함됨
- 최소 10회 반복을 하지 않음
- JSON 모드 성능 표에서 3×3 누락
- 실패 목록 또는 전체 합계 누락
- README 결과 리포트가 10줄 미만이거나 실제 측정 결과와 불일치
- 실행 명령이 `python`/`python3` 중 실제 환경과 맞지 않음
- 실행하지 않은 PASS/FAIL 결과나 측정값을 README에 작성
