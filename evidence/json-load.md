# JSON 로드와 정규화 실행 로그

## 실행 정보

- 실행일: 2026-08-06
- 실행 주체: 사용자
- 실행 명령: `py`
- 실행 목적: `data.json`의 필터·패턴 구조, 키 해석, 라벨 정규화와 필터 연결 확인
- 개인정보 보호: 터미널 프롬프트의 계정명과 장치명은 기록에서 제거함

## 실제 출력

```text
=== Mini NPU Simulator ===
1. 3x3 사용자 입력 모드
2. data.json 로드 및 정규화
3. 종료
모드를 선택하세요: 2

[data.json 로드 및 정규화]
필터 크기: 5, 13, 25
패턴 수: 6

[패턴 구조 확인]
- size_5_1: 5x5, expected=X, filters=Cross/X
- size_5_2: 5x5, expected=Cross, filters=Cross/X
- size_13_1: 13x13, expected=X, filters=Cross/X
- size_13_2: 13x13, expected=Cross, filters=Cross/X
- size_25_1: 25x25, expected=X, filters=Cross/X
- size_25_2: 25x25, expected=Cross, filters=Cross/X

[로드 요약]
정상 케이스: 6
구조 오류 케이스: 0
MAC 점수와 PASS/FAIL 분석은 다음 단계에서 구현합니다.
```

## 확인 결과

| 확인 항목 | 실제 결과 | 상태 |
|---|---|---|
| JSON 모드 진입 | 메뉴 2 선택 후 로드 모드 진입 | 확인 |
| 필터 크기 | 5, 13, 25 | 확인 |
| 패턴 수 | 6 | 확인 |
| 패턴 키 크기 해석 | 5×5, 13×13, 25×25 각각 2건 | 확인 |
| expected `x` 정규화 | `X` | 확인 |
| expected `+` 정규화 | `Cross` | 확인 |
| 대응 필터 선택 | 모든 케이스에서 Cross/X 연결 | 확인 |
| 정상 케이스 | 6 | 확인 |
| 구조 오류 케이스 | 0 | 확인 |

## 결론

실제 `data.json`의 필터 3개 그룹과 패턴 6건을 모두 정상적으로 읽었다. 각 패턴 키에서 크기를 추출해 같은 크기의 Cross/X 필터를 선택했고, 외부 expected 라벨을 내부 표준 `Cross`와 `X`로 정규화했다.

## 이 실행 당시 확인하지 않은 항목

- JSON 파일 없음·권한·문법 오류 처리
- 개별 케이스의 잘못된 키나 크기 불일치 처리
- Cross/X MAC 점수 계산
- expected와 판정의 PASS/FAIL 비교
- 전체 통과·실패 수 집계

MAC 점수, PASS/FAIL과 전체 집계는 이후 [JSON 일괄 판정](json-analysis.md)에서 확인했다. 파일 오류와 개별 케이스 크기 불일치는 아직 실행하지 않았다.
