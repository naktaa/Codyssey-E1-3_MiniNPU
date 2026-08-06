# JSON 일괄 판정 실행 로그

## 실행 정보

- 실행일: 2026-08-06
- 실행 주체: 사용자
- 실행 명령: `py`
- 실행 목적: 실제 `data.json` 6개 케이스의 MAC 점수, 판정, PASS/FAIL과 전체 합계 확인
- 개인정보 보호: 터미널 프롬프트의 계정명과 장치명은 기록에서 제거함

## 실제 출력

```text
=== Mini NPU Simulator ===
1. 3x3 사용자 입력 모드
2. data.json 일괄 분석
3. 종료
모드를 선택하세요: 2

[data.json 일괄 분석]
필터 크기: 5, 13, 25
분석 대상 패턴: 6

[케이스별 결과]

[size_5_1]
Cross 점수: 0.900000
X 점수: 0.900000
판정: UNDECIDED
expected: X
결과: FAIL
사유: expected=X, actual=UNDECIDED

[size_5_2]
Cross 점수: 8.900000
X 점수: 0.100000
판정: Cross
expected: Cross
결과: PASS

[size_13_1]
Cross 점수: 0.300000
X 점수: 14.700000
판정: X
expected: X
결과: PASS

[size_13_2]
Cross 점수: 7.500000
X 점수: 7.500000
판정: UNDECIDED
expected: Cross
결과: FAIL
사유: expected=Cross, actual=UNDECIDED

[size_25_1]
Cross 점수: 4.900000
X 점수: 4.900000
판정: UNDECIDED
expected: X
결과: FAIL
사유: expected=X, actual=UNDECIDED

[size_25_2]
Cross 점수: 52.900000
X 점수: 0.100000
판정: Cross
expected: Cross
결과: PASS

[전체 결과]
전체 케이스: 6
통과: 3
실패: 3
판정 epsilon: 1e-09

[실패 케이스]
- size_5_1: expected=X, actual=UNDECIDED
- size_13_2: expected=Cross, actual=UNDECIDED
- size_25_1: expected=X, actual=UNDECIDED
```

## 케이스별 결과

| 케이스 | Cross 점수 | X 점수 | 판정 | expected | 결과 |
|---|---:|---:|---|---|---|
| `size_5_1` | 0.900000 | 0.900000 | UNDECIDED | X | FAIL |
| `size_5_2` | 8.900000 | 0.100000 | Cross | Cross | PASS |
| `size_13_1` | 0.300000 | 14.700000 | X | X | PASS |
| `size_13_2` | 7.500000 | 7.500000 | UNDECIDED | Cross | FAIL |
| `size_25_1` | 4.900000 | 4.900000 | UNDECIDED | X | FAIL |
| `size_25_2` | 52.900000 | 0.100000 | Cross | Cross | PASS |

## 합계 확인

| 항목 | 실제 결과 |
|---|---:|
| 전체 | 6 |
| 통과 | 3 |
| 실패 | 3 |
| 통과 + 실패 | 6 |

## 실패 원인 분석

세 실패 케이스 모두 Cross 점수와 X 점수가 같아 epsilon `1e-9` 기준으로 `UNDECIDED`가 됐다. expected는 `Cross` 또는 `X`이므로 `UNDECIDED`와 일치하지 않아 FAIL 처리됐다.

- `size_5_1`: 0.9 대 0.9, expected X
- `size_13_2`: 7.5 대 7.5, expected Cross
- `size_25_1`: 4.9 대 4.9, expected X

이는 요구사항의 동점 정책과 일치하며 JSON 구조나 라벨 정규화 오류로 발생한 실패가 아니다.

## 미검증 항목

- 구조 또는 크기가 잘못된 케이스 뒤 다음 케이스 계속 처리
- 파일 없음과 손상 JSON 처리
- 크기별 성능 분석
