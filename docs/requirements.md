# 요구사항 추적표

## 상태 기준

- `예정`: 아직 구현하지 않음
- `구현 중`: 현재 수정 중
- `구현 완료`: 코드 작성 완료, 실행 검증 전
- `실행 검증 완료`: 실제 실행으로 정상 동작 확인
- `증거 확보 완료`: 필요한 로그 또는 스크린샷 저장
- `문서 반영 완료`: README와 관련 문서까지 실제 결과 반영

필수 기능과 두 보너스의 구현을 완료했다. 사용자가 모드 1 직접 입력과 모드 2 JSON 판정, 기존 필터 기반 2차원·1차원 MAC 10회 성능을 최신 코드로 확인했다. 개별·묶음 10·100·1,000회 추가 실험과 새 7×7 생성 크기의 성능 분석 재사용도 확인했다. JSON과 같은 생성 크기의 중복 제거는 최종 재검증 전이다.

## 추적표

| ID | 요구사항 | 필수 여부 | 구현 위치 | 검증 방법 | 필요한 증거 | 구현 단계 | 권장 커밋 | 현재 상태 |
|---|---|---:|---|---|---|---:|---|---|
| FUNC-001 | n×n 2차원 패턴·필터 저장 및 위치별 값 접근 | 필수 | `src/mini_npu.py` | 3·5·13·25 크기 실행 결과 확인 | `evidence/json-analysis.md`, `evidence/performance.md` | 1 | `Feat: MAC 연산과 판정 로직 구현` | 증거 확보 완료 |
| FUNC-002 | 반복문으로 위치별 곱셈과 누적 MAC 점수 계산 | 필수 | `src/mini_npu.py` | 사용자 입력과 JSON의 실제 MAC 점수 확인 | `evidence/manual-mode-success.md`, `evidence/json-analysis.md` | 1 | 동일 | 증거 확보 완료 |
| FUNC-003 | 실수 입력과 실수 점수 처리 | 필수 | `src/mini_npu.py` | 소수 데이터 MAC 결과 확인 | `evidence/json-analysis.md` | 1 | 동일 | 증거 확보 완료 |
| FUNC-004 | 실행 시 사용자 입력/JSON 분석 모드 선택 | 필수 | `src/menu.py` | 메뉴 1, 2 각각 진입 | `evidence/manual-mode-success.md`, `evidence/json-load.md` | 2, 4 | `Feat: 3x3 사용자 입력 모드 구현` | 실행 검증 완료 |
| FUNC-005 | 3×3 필터 A와 B를 행 단위 공백 구분으로 입력 | 필수 | `src/manual_mode.py` | 각 필터 3줄 저장 확인 | `evidence/manual-mode-success.md` | 2 | 동일 | 실행 검증 완료 |
| FUNC-006 | 3×3 패턴을 같은 방식으로 입력 | 필수 | `src/manual_mode.py` | 패턴 3줄 저장 확인 | `evidence/manual-mode-success.md` | 2 | 동일 | 실행 검증 완료 |
| FUNC-007 | 행/열 불일치와 숫자 파싱 오류 시 안내 후 재입력 | 필수 | `src/manual_mode.py` | 잘못된 열 개수, 문자 입력 후 정상 재입력 | `evidence/invalid-input.md` | 2 | 동일 | 증거 확보 완료 |
| FUNC-008 | 사용자 모드 A/B 점수와 판정 출력 | 필수 | `src/manual_mode.py`, `src/mini_npu.py` | X 패턴 입력 시 B 판정 | `evidence/manual-mode-success.md` | 2 | 동일 | 증거 확보 완료 |
| FUNC-009 | 사용자 모드 3×3 평균 MAC 시간 출력 | 필수 | `src/mini_npu.py`, `src/manual_mode.py`, `src/report.py` | 워밍업 후 순수 MAC 10회 독립 측정 결과가 공통 `MAC 성능` 표로 출력되는지 확인 | `evidence/simplified-final-run.md` | 2 | `Feat: 3x3 사용자 입력 모드 구현` | 증거 확보 완료 |
| FUNC-010 | epsilon 기반 점수 비교 | 필수 | `src/mini_npu.py` | 실제 동점 케이스와 epsilon 출력 확인 | `evidence/json-analysis.md` | 1 | `Feat: MAC 연산과 판정 로직 구현` | 증거 확보 완료 |
| FUNC-011 | 동점 시 사용자 모드 판정 불가, JSON 모드 UNDECIDED | 필수 | `src/mini_npu.py`, `src/report.py` | 실제 동점 케이스로 확인 | `evidence/json-analysis.md` | 1, 4 | 동일 | 증거 확보 완료 |
| FUNC-012 | JSON 케이스별 Cross/X 점수·판정·expected·PASS/FAIL 출력 | 필수 | `src/json_mode.py`, `src/report.py` | 실제 data.json 전체 실행 | `evidence/json-analysis.md` | 4 | `Feat: JSON 일괄 판정과 결과 요약 구현` | 증거 확보 완료 |
| FUNC-013 | 전체 테스트/통과/실패 수 출력 | 필수 | `src/report.py` | 케이스 결과 집계와 수기 대조 | `evidence/json-analysis.md` | 4 | 동일 | 증거 확보 완료 |
| FUNC-014 | 실패 케이스 식별자와 사유 목록 출력 | 필수 | `src/report.py` | 실제 실패 케이스 포함 실행 | `evidence/json-analysis.md` | 4 | 동일 | 증거 확보 완료 |
| DATA-001 | 저장소 루트의 `data.json` 읽기 | 필수 | `src/data_loader.py` | 정상 파일 로드 | `evidence/json-load.md` | 3 | `Feat: JSON 데이터 로드와 스키마 검증 구현` | 증거 확보 완료 |
| DATA-002 | JSON 파일 없음·읽기·UTF-8 디코딩·JSON 문법 오류 처리 | 필수 | `src/data_loader.py`, `src/json_mode.py` | 예외 처리 흐름 코드 확인 | 별도 실행 증거 생략 | 3, 6 | `Fix: JSON 파일 인코딩 오류 처리 보완` | 구현 완료 (사용자 결정으로 실행 생략) |
| DATA-003 | `filters.size_5`, `size_13`, `size_25` 해석 | 필수 | `src/data_loader.py` | 각 크기 필터 두 개 로드 | `evidence/json-load.md` | 3 | 동일 | 증거 확보 완료 |
| DATA-004 | `patterns.size_{N}_{idx}` 키에서 N 추출 | 필수 | `src/data_loader.py` | 5·13·25 키 파싱 수동 확인 | `evidence/json-load.md` | 3 | 동일 | 증거 확보 완료 |
| DATA-005 | 키의 N에 맞는 `size_N` 필터 선택 | 필수 | `src/data_loader.py` | 각 케이스의 선택 필터 확인 | `evidence/json-load.md` | 3 | 동일 | 증거 확보 완료 |
| DATA-006 | 필터와 패턴 크기 일치 검증 | 필수 | `src/data_loader.py` | 행렬·키 크기 검증 코드 확인 | 별도 실행 증거 생략 | 3, 4 | 동일 | 구현 완료 (사용자 결정으로 실행 생략) |
| DATA-007 | 크기/스키마 불일치를 케이스 단위 FAIL 처리하고 계속 실행 | 필수 | `src/data_loader.py`, `src/json_mode.py`, `src/report.py` | 케이스 오류의 FAIL 변환과 `continue` 확인 | 별도 실행 증거 생략 | 4 | `Feat: JSON 일괄 판정과 결과 요약 구현` | 구현 완료 (사용자 결정으로 실행 생략) |
| DATA-008 | expected `+`를 `Cross`, `x`를 `X`로 정규화 | 필수 | `src/data_loader.py` | 라벨 변환 수동 확인 | `evidence/json-load.md` | 3 | `Feat: JSON 데이터 로드와 스키마 검증 구현` | 증거 확보 완료 |
| DATA-009 | filter key `cross`를 `Cross`, `x`를 `X`로 정규화 | 필수 | `src/data_loader.py` | 라벨 변환 수동 확인 | `evidence/json-load.md` | 3 | 동일 | 증거 확보 완료 |
| DATA-010 | 내부 비교와 출력에 표준 라벨 Cross/X 사용 | 필수 | 전체 | 원본 라벨이 결과 비교에 남지 않는지 확인 | `evidence/json-analysis.md` | 3, 4 | 동일 | 증거 확보 완료 |
| PERF-001 | MAC 함수 호출 구간 중심으로 시간 측정 | 필수 | `src/mini_npu.py`, `src/performance.py` | 입력 검증·워밍업이 타이머 전에 있고 순수 MAC만 측정하는지 확인 | `evidence/simplified-final-run.md` | 5 | `Feat: 크기별 MAC 성능 분석 구현` | 증거 확보 완료 |
| PERF-002 | 크기별 최소 10회 반복 후 평균 계산 | 필수 | `src/mini_npu.py`, `src/performance.py`, `src/manual_mode.py` | 모드 1·2가 공통 반복 횟수로 평균·표준편차를 출력하는지 확인 | `evidence/simplified-final-run.md` | 5 | 동일 | 증거 확보 완료 |
| PERF-003 | 3×3·5×5·13×13·25×25 성능 분석 | 필수 | `src/performance.py`, `src/report.py` | 기존 Cross/X 필터의 네 크기 행 확인 | `evidence/simplified-final-run.md` | 5 | 동일 | 증거 확보 완료 |
| PERF-004 | 크기/평균 ms/표준편차/CV/N² 연산 횟수 표 출력 | 필수 | `src/report.py` | 정렬된 한글 열과 9·25·169·625 확인 | `evidence/simplified-final-run.md` | 5 | 동일 | 증거 확보 완료 |
| TECH-001 | Python 3.8 이상에서 실행 | 필수 | 전체 | Python 3.12.13 환경과 사용자 실행 확인 | `docs/worklog.md`, 사용자 실행 로그 | 6 | `Docs: 수동 검증 결과와 문서 동기화` | 실행 검증 완료 |
| TECH-002 | 외부 라이브러리 없이 표준 라이브러리만 사용 | 필수 | 전체 | import 목록과 의존성 파일 정적 확인 | 코드 리뷰 | 6 | 동일 | 구현 완료 |
| TECH-003 | MAC에 벡터화 라이브러리 사용 금지, 반복문 직접 구현 | 필수 | `src/mini_npu.py` | 코드 리뷰와 사용자 수동 검증 | 코드 리뷰 | 1 | `Feat: MAC 연산과 판정 로직 구현` | 구현 완료 |
| TECH-004 | 오류 하나로 프로그램 전체 비정상 종료 방지 | 필수 | `src/menu.py`, `src/data_loader.py`, `src/json_mode.py` | 사용자 입력 재시도 증거와 JSON 예외 흐름 코드 확인 | `evidence/invalid-input.md`, 코드 리뷰 | 2~4 | 관련 기능 커밋 | 구현 완료 |
| TEST-003 | 모드 1 재현 시나리오 수동 검증 | 필수 | 실행 결과 | 예시 필터·패턴 입력 | `evidence/simplified-final-run.md` | 6 | `Test: 필수 시나리오 검증` | 증거 확보 완료 |
| TEST-004 | 모드 2 총합과 개별 PASS/FAIL 수동 검증 | 필수 | 실행 결과 | 실제 data.json 결과 대조 | `evidence/simplified-final-run.md` | 6 | 동일 | 증거 확보 완료 |
| DOC-001 | README 실행 방법 작성 | 필수 | `README.md` | 단순화 후 `python3 main.py` 최종 재현 | `evidence/simplified-final-run.md` | 6 | `Docs: 실행 방법과 결과 리포트 작성` | 문서 반영 완료 |
| DOC-002 | README 라벨 정규화·MAC·epsilon 구현 요약 | 필수 | `README.md` | 실제 코드와 대조 | README | 6 | 동일 | 문서 반영 완료 |
| DOC-003 | README 결과 리포트 10줄 이상 작성 | 필수 | `README.md` | 줄 수와 실제 결과 확인 | README | 6 | 동일 | 문서 반영 완료 |
| DOC-004 | README 실패 원인과 O(N²) 분석 작성 | 필수 | `README.md` | 새 측정값·실패 로그와 대조 | README | 6 | 동일 | 문서 반영 완료 |
| EVID-001 | 사용자 모드 정상 실행 결과 확보 | 권장 | `evidence/` | 실제 실행 로그 저장 | `evidence/simplified-final-run.md` | 6 | `Test: 필수 시나리오 검증` | 증거 확보 완료 |
| EVID-002 | 잘못된 사용자 입력 재입력 증거 확보 | 권장 | `evidence/` | 실제 입력과 재시도 흐름 기록 | Markdown 로그 | 6 | 동일 | 증거 확보 완료 |
| EVID-003 | JSON 크기 불일치 케이스 FAIL 증거 확보 | 권장 | 해당 없음 | 사용자 결정으로 생성하지 않음 | 해당 없음 | 6 | 해당 없음 | 제외 (사용자 결정) |
| EVID-004 | JSON 전체 결과 요약 증거 확보 | 권장 | `evidence/` | 실제 분석 로그 저장 | `evidence/simplified-final-run.md` | 6 | 동일 | 증거 확보 완료 |
| EVID-005 | 성능 표 증거 확보 | 권장 | `evidence/` | 네 필수 크기의 순수 MAC 성능표 저장 | `evidence/simplified-final-run.md` | 6 | 동일 | 증거 확보 완료 |
| ENV-001 | 최종 결과를 macOS zsh에서 재현하고 환경 기록 | 필수 | 전체 | 단순화 후 메뉴 1·2 실행과 운영체제·CPU 확인 | `evidence/mac-status.png`, 새 최종 로그 | 6 | `Test: macOS 최종 재현 검증` | 환경 증거 확보 / 최신 코드 재검증 전 |
| BONUS-001 | 2차원 배열을 1차원으로 변환한 최적화 비교 | 선택 | `src/mini_npu.py`, `src/performance.py`, `src/report.py` | 네 크기의 10회 1차원 평균·표준편차와 2차원 결과 비교 | `evidence/simplified-final-run.md`, `evidence/performance-repetition-experiments.md` | 7 | `Feat: 1차원 MAC 최적화 비교 추가` | 증거 확보 완료 |
| BONUS-002 | 3 이상의 홀수 N×N Cross/X 패턴 생성 후 모드 1·성능 분석 재사용 | 선택 | `src/pattern_generator.py`, `src/menu.py`, `src/manual_mode.py`, `src/performance.py` | 자동 생성·교체·재사용과 생성 크기의 중복 없는 필터 기반 성능표 확인 | `evidence/manual-nxn-filter-flow.md`, `evidence/generated-filter-merge.md` | 필수 완료 후 | `Feat: N×N 필터 생성과 성능 재사용 추가` | 새 크기 재사용 증거 확보 / JSON 동일 크기 중복 재검증 전 |
| BENCH-001 | 묶음 MAC 측정으로 타이머 오버헤드 영향 비교 | 선택 | `benchmark_batch.py` | 위치 인자 10·100·1000의 묶음 2차원·1차원 결과 확인 | `evidence/performance-repetition-experiments.md` | 필수 결과와 분리 | `Feat: 묶음 MAC 벤치마크 분리` | 최신 증거 확보 완료 |

## 별도 실행을 생략한 항목

- 필터·패턴 크기 불일치 케이스 단위 FAIL과 다음 케이스 계속 처리
- `data.json` 파일 없음, UTF-8 인코딩 오류와 손상 JSON의 모드 오류 처리

두 항목은 필수 처리 코드가 구현되어 있으나 별도 실행 증거는 사용자 결정으로 생성하지 않는다.

보너스 확장 항목인 짝수·3 미만 크기 재입력은 별도 실행하지 않았다. 필터 생성과 모드 1 자동 생성·저장 필터 선택은 이전 구조에서 실제 실행으로 확인했고, 새 7×7 생성 필터의 모드 2 재사용은 최신 구조에서 확인했다. JSON과 같은 생성 크기의 중복 제거는 재검증해야 한다.

## 확인된 data.json 구조

- 필터: `filters.size_5`, `filters.size_13`, `filters.size_25`
- 각 필터 라벨: `cross`, `x`
- 패턴: `size_5_1`부터 `size_25_2`까지 총 6개
- expected: `+` 3개, `x` 3개
- 3×3 데이터는 포함되어 있지 않음
