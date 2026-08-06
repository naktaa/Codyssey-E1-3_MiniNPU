# Mini NPU Simulator

E1-3 미션용 Python 콘솔 애플리케이션 저장소입니다.

> 현재 상태: 초기 문서 구성 완료 / 기능 미구현 / 실행 미검증

## 실행 환경

- Python 3.8 이상
- 기본 검증 환경: macOS, zsh
- 외부 라이브러리 사용 금지
- 표준 라이브러리만 사용

## 예정된 실행 방법

구현 완료 후 저장소 루트에서 실행합니다.

```zsh
python3 main.py
```

프로그램은 다음 두 모드를 제공해야 합니다.

1. 사용자 입력(3×3)
2. `data.json` 분석

`data.json`은 저장소 루트에 두는 것을 기본으로 합니다.

## 구현 요약

아직 구현 전이며, 다음 원칙으로 개발할 예정입니다.

- 2차원 리스트로 n×n 패턴과 필터를 저장합니다.
- 같은 위치의 값을 이중 반복문으로 곱하고 누적하여 MAC 점수를 구합니다.
- 내부 표준 라벨은 `Cross`, `X`를 사용합니다.
- expected `+`와 filter key `cross`는 `Cross`로 정규화합니다.
- expected `x`와 filter key `x`는 `X`로 정규화합니다.
- 두 점수 차가 epsilon보다 작으면 `UNDECIDED`로 판정합니다.
- JSON 케이스 오류는 가능한 한 해당 케이스만 FAIL 처리합니다.
- 성능 측정은 I/O를 제외한 MAC 함수 호출 구간만 측정합니다.

## 프로젝트 구조

```text
.
├── main.py                 # 구현 예정
├── mini_npu.py             # 구현 예정
├── data_loader.py          # 구현 예정
├── report.py               # 구현 예정
├── data.json               # 원본 제공 후 배치
├── tests/                  # 구현 예정
├── docs/
├── evidence/
├── AGENTS.md
├── MISSION.md
├── README.md
├── .gitignore
└── .gitattributes
```

## 결과 리포트

아래 내용은 최종 구현과 macOS 실행 검증 후 실제 결과로 교체해야 합니다.

1. 전체 JSON 테스트 수: TODO
2. 통과 수: TODO
3. 실패 수: TODO
4. 실패 케이스 목록과 직접 원인: TODO
5. 데이터·스키마 문제 여부: TODO
6. MAC 또는 판정 로직 문제 여부: TODO
7. 부동소수점 비교 문제 여부: TODO
8. 라벨 정규화가 PASS/FAIL에 미친 영향: TODO
9. epsilon 값과 동점 처리 근거: TODO
10. 3×3 평균 MAC 시간과 반복 횟수: TODO
11. 5×5 평균 MAC 시간과 반복 횟수: TODO
12. 13×13 평균 MAC 시간과 반복 횟수: TODO
13. 25×25 평균 MAC 시간과 반복 횟수: TODO
14. N² 연산 횟수와 측정 시간 증가 관계: TODO
15. O(N²) 시간 복잡도 결론과 측정 오차 해석: TODO

실패가 0개라면 단순히 “모두 통과했다”고 끝내지 않고, 라벨 정규화와 epsilon 정책으로 비교 기준을 일관되게 만든 이유를 설명해야 합니다.

## 검증 예정 항목

- 3×3 Cross/X 예시 점수 확인
- A/B 판정과 epsilon 동점 판정 확인
- 행 개수·열 개수·숫자 파싱 오류 후 재입력 확인
- 실제 `data.json` 모든 케이스 분석
- 필터·패턴 크기 불일치 케이스 단위 FAIL 확인
- 총 테스트·통과·실패 합계 확인
- 3×3·5×5·13×13·25×25 성능 표 확인
- 자동 테스트와 수동 실행 결과 일치 확인

## 문서

- [미션 요약](MISSION.md)
- [요구사항 추적표](docs/requirements.md)
- [현재 진행 상태](docs/progress.md)
- [작업 기록](docs/worklog.md)
- [트러블슈팅](docs/troubleshooting.md)
