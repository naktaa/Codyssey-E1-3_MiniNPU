# Mini NPU 시험 핵심 개념과 Python 기본 문법

이 문서는 시험 직전 복습을 위한 자료다. Mini NPU 미션에 실제로 사용된 문법을 중심으로 정리했으며, 우선순위는 다음과 같다.

1. 이중 반복문과 2차원 리스트
2. 함수, 조건문과 점수 판정
3. 리스트·딕셔너리 처리
4. 문자열 입력과 예외 처리
5. JSON, 시간 복잡도와 성능 측정
6. 보너스 개념과 Python 부가 문법

시험 직전 시간이 부족하다면 1~7장과 20장의 예상 문제부터 본다.

## 1. 반드시 알아야 할 전체 흐름

Mini NPU의 핵심은 다음 여섯 단계다.

```text
행렬 입력
→ 입력 검증
→ 같은 위치의 값끼리 곱함
→ 모든 곱을 더해 MAC 점수 계산
→ Cross/X 점수를 epsilon으로 비교
→ Cross, X 또는 UNDECIDED 판정
```

JSON 모드는 판정 뒤에 한 단계가 더 있다.

```text
실제 판정과 expected 비교
→ 같으면 PASS
→ 다르면 FAIL
```

성능 분석은 다음과 같다.

```text
입력 검증과 워밍업
→ 타이머 시작
→ MAC 한 번 계산
→ 타이머 종료
→ 10개 시간의 평균·표준편차 계산
```

## 2. 변수와 기본 자료형

### 변수

변수는 값을 가리키는 이름이다.

```python
size = 3
score = 0.0
label = "Cross"
passed = True
```

Python은 변수 선언 시 자료형을 별도로 적지 않아도 된다.

### 주요 자료형

| 자료형 | 예시 | 의미 |
|---|---|---|
| `int` | `3`, `25` | 정수 |
| `float` | `0.9`, `1.0` | 실수 |
| `str` | `"Cross"` | 문자열 |
| `bool` | `True`, `False` | 참·거짓 |
| `list` | `[1, 2, 3]` | 순서가 있고 변경 가능한 모음 |
| `tuple` | `(1, 2, 3)` | 순서가 있고 보통 변경하지 않는 모음 |
| `dict` | `{"Cross": matrix}` | 키와 값을 연결하는 자료구조 |
| `None` | `None` | 값이 없음을 나타내는 특별한 값 |

### 형 변환

사용자 입력은 항상 문자열이므로 계산하려면 숫자로 변환해야 한다.

```python
raw = "3"
size = int(raw)

raw_score = "0.9"
score = float(raw_score)
```

변환할 수 없는 문자열은 `ValueError`를 발생시킨다.

```python
int("abc")    # ValueError
float("x")    # ValueError
```

## 3. 리스트와 2차원 리스트

### 1차원 리스트

```python
numbers = [10, 20, 30]

print(numbers[0])   # 10
print(numbers[2])   # 30
```

인덱스는 0부터 시작한다.

```text
값:       10  20  30
인덱스:    0   1   2
```

리스트 끝에 값을 추가하려면 `append()`를 사용한다.

```python
numbers = []
numbers.append(10)
numbers.append(20)

# [10, 20]
```

### 2차원 리스트

행렬은 리스트 안에 행 리스트를 넣어 표현한다.

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
```

특정 값은 `matrix[행][열]`로 접근한다.

```python
matrix[0][0]   # 1
matrix[1][2]   # 6
matrix[2][1]   # 8
```

### 행과 열의 의미

```text
matrix[row][column]
       행     열
```

3×3 행렬은 행이 3개이고 각 행의 값도 3개다.

```python
size = len(matrix)        # 행 개수: 3
row_size = len(matrix[0]) # 첫 행의 열 개수: 3
```

### 정사각형 행렬 검사

정사각형 행렬은 행의 수와 모든 행의 열 수가 같다.

```python
size = len(matrix)

for row in matrix:
    if len(row) != size:
        print("정사각형이 아닙니다.")
```

다음 행렬은 행이 2개인데 첫 행의 열이 3개이므로 정사각형이 아니다.

```python
matrix = [
    [1, 2, 3],
    [4, 5],
]
```

## 4. `for`, `range()`와 이중 반복문

### 기본 `for` 반복문

```python
for number in [1, 2, 3]:
    print(number)
```

출력:

```text
1
2
3
```

### `range()`

`range(stop)`은 0부터 `stop - 1`까지 만든다.

```python
for index in range(3):
    print(index)
```

출력:

```text
0
1
2
```

중요한 형태는 다음과 같다.

```python
range(3)        # 0, 1, 2
range(1, 4)     # 1, 2, 3
range(0, 6, 2)  # 0, 2, 4
```

끝값은 포함하지 않는다.

### 이중 반복문

반복문 안에 다른 반복문이 들어간 형태다.

```python
for row in range(3):
    for column in range(3):
        print(row, column)
```

실행 순서:

```text
(0, 0) (0, 1) (0, 2)
(1, 0) (1, 1) (1, 2)
(2, 0) (2, 1) (2, 2)
```

바깥 반복문이 행 하나를 선택하면 안쪽 반복문이 그 행의 모든 열을 돈다.

### 반복 횟수 계산

```python
for row in range(N):       # N번
    for column in range(N): # 각 행마다 N번
        work()
```

전체 `work()` 실행 횟수는 다음과 같다.

```text
N × N = N²
```

| N | 안쪽 작업 횟수 |
|---:|---:|
| 3 | 9 |
| 5 | 25 |
| 13 | 169 |
| 25 | 625 |

### 크기가 다른 반복문

```python
for row in range(N):
    for column in range(M):
        work()
```

전체 횟수는 `N × M`이고 시간 복잡도는 O(NM)이다. 두 크기가 모두 N일 때 O(N²)이 된다.

### 반복문으로 행렬 출력

```python
for row in matrix:
    for value in row:
        print(value, end=" ")
    print()
```

### 자주 틀리는 부분

```python
for row in range(len(matrix)):
    for column in range(len(matrix[row])):
        print(matrix[row][column])
```

- `matrix[row]`는 한 행이다.
- `matrix[row][column]`이 실제 숫자 하나다.
- `range(len(matrix))`의 마지막 인덱스는 `len(matrix) - 1`이다.
- 들여쓰기가 잘못되면 반복 범위와 실행 결과가 달라진다.

## 5. MAC 연산

### MAC의 뜻

MAC은 Multiply-Accumulate의 약자다.

```text
Multiply: 같은 위치의 값을 곱함
Accumulate: 곱한 결과를 누적해서 더함
```

### 계산식

패턴 P와 필터 F가 N×N일 때:

```text
score = Σ P[row][column] × F[row][column]
```

### 이중 반복문 구현

```python
def calculate_mac(pattern, filter_matrix):
    score = 0.0
    size = len(pattern)

    for row in range(size):
        for column in range(size):
            score += pattern[row][column] * filter_matrix[row][column]

    return score
```

`score += value`는 다음과 같다.

```python
score = score + value
```

### 손으로 계산하기

```python
pattern = [
    [1, 0],
    [1, 1],
]

filter_matrix = [
    [1, 1],
    [0, 1],
]
```

계산:

```text
(1×1) + (0×1) + (1×0) + (1×1)
= 1 + 0 + 0 + 1
= 2
```

### 왜 O(N²)인가

N×N의 모든 위치를 정확히 한 번씩 방문한다. 입력 한 변의 길이를 N이라고 할 때 방문 횟수가 N²이므로 O(N²)이다.

MAC 안에서 곱셈과 덧셈을 모두 한다고 해서 O(2N²)이라고 쓰지 않는다. 빅오 표기에서는 상수 2를 제거하므로 O(N²)이다.

## 6. 조건문과 논리 연산자

### `if`, `elif`, `else`

```python
if score_cross > score_x:
    result = "Cross"
elif score_cross < score_x:
    result = "X"
else:
    result = "UNDECIDED"
```

조건은 위에서부터 검사하며, 처음 참인 블록 하나만 실행한다.

### 비교 연산자

| 연산자 | 뜻 |
|---|---|
| `==` | 값이 같다 |
| `!=` | 값이 다르다 |
| `>` | 크다 |
| `<` | 작다 |
| `>=` | 크거나 같다 |
| `<=` | 작거나 같다 |

대입에는 `=`, 값 비교에는 `==`를 사용한다.

```python
result = "Cross"          # 대입
result == "Cross"         # 비교
```

### 논리 연산자

```python
if size >= 3 and size % 2 == 1:
    print("3 이상의 홀수")

if label == "+" or label == "cross":
    print("Cross")

if size not in generated_store:
    print("저장된 필터 없음")
```

| 연산자 | 뜻 |
|---|---|
| `and` | 두 조건이 모두 참 |
| `or` | 하나 이상 참 |
| `not` | 참·거짓을 반대로 바꿈 |
| `in` | 값이 모음에 포함됨 |
| `not in` | 값이 모음에 포함되지 않음 |

### 나머지 연산자 `%`

```python
size % 2 == 0  # 짝수
size % 2 == 1  # 홀수
```

현재 생성기는 다음 조건으로 잘못된 크기를 거부한다.

```python
if size < 3 or size % 2 == 0:
    raise ValueError("필터 크기는 3 이상의 홀수여야 합니다.")
```

## 7. 부동소수점과 epsilon

### 부동소수점 오차

컴퓨터는 많은 십진 실수를 이진수로 정확히 표현하지 못한다.

```python
0.1 + 0.2 == 0.3  # 일반적으로 False
```

따라서 계산된 실수 두 개가 수학적으로 같아야 해도 아주 조금 다를 수 있다.

### epsilon 비교

```python
epsilon = 1e-9

if abs(score_cross - score_x) < epsilon:
    result = "UNDECIDED"
```

`1e-9`는 다음 값이다.

```text
0.000000001
```

`abs()`는 절댓값을 반환한다.

```python
abs(3)     # 3
abs(-3)    # 3
```

점수 차이가 양수인지 음수인지와 관계없이 차이의 크기만 보기 위해 사용한다.

### 경계 조건

현재 조건은 `< epsilon`이다.

```text
차이 < 1e-9  → 동점
차이 = 1e-9  → 동점 아님
```

`<`와 `<=`의 차이는 시험에서 자주 묻는다.

### epsilon의 의미

epsilon은 오차를 없애는 값이 아니다. 어느 정도 차이까지 같은 값으로 볼지 정하는 비교 정책이다.

## 8. 함수

### 함수 정의와 호출

```python
def add(a, b):
    return a + b

result = add(2, 3)
```

- `def`: 함수 정의
- `a`, `b`: 매개변수
- `2`, `3`: 전달 인자
- `return`: 호출한 곳으로 결과 반환

### 반환과 출력의 차이

```python
def add_and_print(a, b):
    print(a + b)

def add_and_return(a, b):
    return a + b
```

`print()`는 화면에 보여줄 뿐이고, `return`은 결과를 다른 계산에서 사용할 수 있게 돌려준다.

```python
value = add_and_print(2, 3)   # 화면에는 5, value는 None
value = add_and_return(2, 3)  # value는 5
```

### 기본 매개변수

```python
def classify(score_a, score_b, epsilon=1e-9):
    ...
```

호출할 때 epsilon을 생략하면 `1e-9`가 사용된다.

```python
classify(3.0, 2.0)
classify(3.0, 2.0, 1e-6)
```

### 여러 값 반환

```python
def get_scores():
    return 3.0, 6.0

cross, x_score = get_scores()
```

실제로는 튜플 `(3.0, 6.0)`이 반환되고 두 변수에 나누어 저장된다.

### 지역 변수

함수 안에서 만든 변수는 기본적으로 함수 밖에서 직접 사용할 수 없다.

```python
def calculate():
    score = 10
    return score
```

`score`는 지역 변수다. 필요한 값은 `return`으로 반환한다.

### 함수를 나누는 기준

이 미션에서는 역할을 기준으로 나눈다.

```text
validate_square_matrix() → 입력 검증
calculate_mac()          → 순수 계산
classify_scores()        → 점수 판정
load_data()              → JSON 파일 로드
print_summary()          → 결과 출력
```

## 9. `while`, `break`, `continue`, `return`

### `while`

조건이 참인 동안 반복한다.

```python
while True:
    choice = input("선택: ")
    if choice == "1":
        break
```

`while True`는 직접 종료하지 않으면 계속 반복된다.

### `break`

현재 반복문 하나를 즉시 끝낸다.

```python
while True:
    value = input("숫자: ")
    if value.isdigit():
        break
```

### `continue`

현재 반복의 남은 코드를 건너뛰고 다음 반복으로 간다.

```python
for number in range(5):
    if number == 2:
        continue
    print(number)
```

출력:

```text
0
1
3
4
```

### `return`

함수 전체를 즉시 끝낸다. 반복문 안에 있어도 반복문뿐 아니라 함수에서 빠져나간다.

```python
def find_negative(numbers):
    for number in numbers:
        if number < 0:
            return number
    return None
```

### 차이 정리

| 문법 | 영향 범위 |
|---|---|
| `continue` | 현재 반복만 건너뜀 |
| `break` | 현재 반복문 하나를 종료 |
| `return` | 현재 함수 전체를 종료 |

## 10. 문자열 입력 처리

### `input()`

```python
raw = input("값을 입력하세요: ")
```

`input()`의 결과는 항상 문자열이다.

### `strip()`

문자열 양끝의 공백과 줄바꿈을 제거한다.

```python
"  Cross  ".strip()  # "Cross"
```

### `split()`

공백을 기준으로 문자열을 나눈다.

```python
raw = "1 2 3"
values = raw.split()

# ["1", "2", "3"]
```

### 숫자 행 입력

```python
raw_row = input("행 입력: ").strip()
values = raw_row.split()

if len(values) != 3:
    print("숫자 3개가 필요합니다.")
else:
    row = [float(value) for value in values]
```

### 리스트 컴프리헨션

```python
row = [float(value) for value in values]
```

다음 반복문을 짧게 쓴 것이다.

```python
row = []
for value in values:
    row.append(float(value))
```

시험에서 컴프리헨션이 어렵다면 먼저 일반 반복문으로 풀어 생각한다.

### f-string

문자열 안에 변수나 계산 결과를 넣는다.

```python
size = 3
print(f"크기: {size}x{size}")
```

실수 출력 자릿수도 지정할 수 있다.

```python
score = 3.141592
print(f"{score:.2f}")  # 3.14
print(f"{score:.6f}")  # 3.141592
```

## 11. 예외 처리

### `try`와 `except`

오류가 발생할 수 있는 코드를 `try`에 넣고, 예상한 오류를 `except`에서 처리한다.

```python
try:
    size = int(input("크기: "))
except ValueError:
    print("정수를 입력하세요.")
```

이렇게 하면 잘못된 입력 때문에 프로그램 전체가 바로 종료되는 것을 막을 수 있다.

### `raise`

문제가 발견됐을 때 직접 예외를 발생시킨다.

```python
if size < 3:
    raise ValueError("크기는 3 이상이어야 합니다.")
```

### 예외를 다시 바꾸어 전달

```python
try:
    validate_square_matrix(value)
except ValueError as error:
    raise DataValidationError(str(error)) from error
```

행렬 검증의 `ValueError`를 JSON 데이터 문제라는 의미의 `DataValidationError`로 바꾼다.

### 파일 전체 오류와 케이스 오류

```text
파일을 읽을 수 없음
→ JSON 분석 모드 종료

패턴 한 건의 구조가 잘못됨
→ 해당 케이스만 FAIL
→ 다음 케이스 계속 분석
```

이 둘을 구분해야 한 건의 잘못된 패턴 때문에 나머지 정상 패턴까지 처리하지 못하는 일을 막을 수 있다.

## 12. 딕셔너리

### 기본 사용

딕셔너리는 키로 값을 찾는다.

```python
filters = {
    "Cross": [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
    "X": [[1, 0, 1], [0, 1, 0], [1, 0, 1]],
}

cross_filter = filters["Cross"]
```

### 키 존재 확인

```python
if "Cross" in filters:
    print("Cross 필터가 있습니다.")

if size not in generated_store:
    print("해당 크기가 없습니다.")
```

### 값 추가와 교체

```python
generated_store[7] = filters
```

7이라는 키가 없으면 추가되고, 이미 있으면 기존 값이 교체된다.

### 반복

```python
for key in filters:
    print(key)

for key, value in filters.items():
    print(key, value)
```

### `update()`

```python
result = {3: filters_3}
result.update(json_filters)
```

같은 키가 있으면 뒤에서 전달한 값으로 교체된다.

### 중복 없는 크기 합치기

현재 성능 입력은 JSON 필터를 우선하고, 없는 생성 크기만 추가한다.

```python
filter_pairs = {3: baseline_filters}
filter_pairs.update(json_filters)

for size, filters in generated_filters.items():
    if size not in filter_pairs:
        filter_pairs[size] = filters
```

이 구조에서 생성 5×5와 JSON 5×5가 모두 있다면 JSON 5×5만 남는다.

## 13. JSON과 파일 처리

### JSON과 Python 자료형

| JSON | Python |
|---|---|
| object | `dict` |
| array | `list` |
| string | `str` |
| number | `int` 또는 `float` |
| true/false | `True`/`False` |
| null | `None` |

### 파일 열기

```python
with open("data.json", "r", encoding="utf-8") as file:
    document = json.load(file)
```

`with` 블록이 끝나면 파일을 자동으로 닫는다.

### `json.load()`와 `json.loads()`

```python
json.load(file)          # 열린 파일에서 JSON 읽기
json.loads(json_string)  # 문자열에서 JSON 읽기
```

두 함수 이름을 혼동하지 않는다.

### 키 규칙

```text
filters.size_5
patterns.size_5_1
```

`size_5_1`에서 필요한 크기 5를 꺼내 `size_5` 필터를 선택한다.

현재 코드는 정규식을 사용하지만 기본 원리는 문자열을 정해진 규칙으로 해석하는 것이다.

```python
parts = "size_5_1".split("_")
size = int(parts[1])
```

정규식은 형식 전체가 올바른지도 함께 검사하기 위해 사용한다.

## 14. 라벨 정규화

### 정규화가 필요한 이유

외부 데이터에는 같은 의미가 여러 문자열로 표현될 수 있다.

```text
"+"       → Cross
"cross"   → Cross
"Cross"   → Cross
"x"       → X
```

표현을 그대로 비교하면 `"+" == "Cross"`가 거짓이므로 정상 데이터도 FAIL이 될 수 있다.

### `strip()`과 `casefold()`

```python
normalized = value.strip().casefold()
```

- `strip()`: 양끝 공백 제거
- `casefold()`: 대소문자 차이를 줄여 비교하기 좋은 문자열로 변환

```python
if normalized in ("+", "cross"):
    return "Cross"
if normalized == "x":
    return "X"
```

정규화의 핵심은 외부 표현을 내부 표준 하나로 바꾸는 것이다.

## 15. 시간 복잡도와 공간 복잡도

### 빅오 표기

빅오 표기는 입력 크기가 커질 때 작업량이 어떻게 증가하는지를 나타낸다.

| 형태 | 이름 | 예시 |
|---|---|---|
| O(1) | 상수 시간 | 딕셔너리에서 키 하나 조회 |
| O(N) | 선형 시간 | 리스트 한 번 순회 |
| O(N²) | 제곱 시간 | N×N 행렬 전체 순회 |

### 상수 제거

```text
2N² + 3N + 10 → O(N²)
```

입력이 매우 커질 때 가장 빠르게 증가하는 항만 남기고 상수는 제거한다.

### 연속된 반복문

```python
for i in range(N):
    work()

for j in range(N):
    work()
```

전체는 `N + N = 2N`이므로 O(N)이다. 반복문이 두 개 있다고 무조건 O(N²)은 아니다.

### 중첩된 반복문

```python
for i in range(N):
    for j in range(N):
        work()
```

전체는 `N × N = N²`이므로 O(N²)이다.

### 2차원과 1차원 MAC

2차원 방식:

```python
for row in range(N):
    for column in range(N):
        work()
```

1차원 방식:

```python
for index in range(N * N):
    work()
```

두 방식 모두 N²개 값을 처리하므로 O(N²)이다. 반복문이 한 겹이라고 O(N)이 되는 것이 아니다. 1차원 리스트의 길이 자체가 N²이기 때문이다.

### 공간 복잡도

MAC 계산 중 추가로 만드는 값이 `score`와 인덱스 정도라면 추가 공간은 O(1)이다.

2차원 행렬을 새 1차원 리스트로 펼치면 N²개 값을 새로 저장하므로 변환 결과의 추가 공간은 O(N²)이다.

## 16. 성능 측정 기초

### 올바른 측정 구간

```python
start = time.perf_counter_ns()
calculate_mac(pattern, filter_matrix)
elapsed = time.perf_counter_ns() - start
```

타이머 안에는 MAC 계산만 들어간다.

다음은 타이머 밖에서 처리한다.

- `input()`
- `print()`
- JSON 파일 읽기
- 행렬 검증
- 1차원 변환
- 워밍업

### 단위 변환

```text
1초 = 1,000밀리초(ms)
1밀리초 = 1,000,000나노초(ns)
```

```python
elapsed_ms = elapsed_ns / 1_000_000.0
```

### 평균

```text
평균 = 측정값의 합 ÷ 측정 개수
```

```python
average = sum(times) / len(times)
```

현재 코드는 `statistics.fmean()`을 사용한다.

### 표준편차

측정값들이 평균 주변에서 얼마나 퍼져 있는지를 나타낸다.

- 작으면 측정값들이 평균 가까이에 모여 있음
- 크면 측정값의 변동이 큼

현재 실행의 10개 값을 전체 모집단으로 보고 `statistics.pstdev()`를 사용한다.

### CV

```text
CV(%) = 표준편차 ÷ 평균 × 100
```

평균에 비해 표준편차가 얼마나 큰지 나타낸다. 평균이 매우 작은 경우 작은 절대 변화도 큰 CV로 나타날 수 있으므로 절대적인 점수처럼 해석하지 않는다.

### 워밍업

측정 전에 같은 계산을 몇 번 미리 실행하는 것이다.

```python
for _ in range(10):
    calculate_mac(pattern, filter_matrix)
```

첫 실행의 인터프리터·캐시 상태 영향을 줄이기 위한 준비이며 측정 결과에는 넣지 않는다.

`_`는 반복 변수의 값을 실제로 사용하지 않겠다는 관례적인 이름이다.

## 17. 필터 생성기의 조건식

### Cross 필터

N이 홀수이면 가운데 인덱스는 다음과 같다.

```python
center = size // 2
```

`//`는 몫을 구하는 정수 나눗셈이다.

```python
7 // 2  # 3
5 // 2  # 2
```

가운데 행 또는 가운데 열이면 Cross의 1이다.

```python
is_cross = row == center or column == center
```

### X 필터

왼쪽 위에서 오른쪽 아래 대각선:

```python
row == column
```

오른쪽 위에서 왼쪽 아래 대각선:

```python
row + column == size - 1
```

둘 중 하나면 X의 1이다.

```python
is_x = row == column or row + column == size - 1
```

### 조건식으로 값 선택

```python
value = 1.0 if is_cross else 0.0
```

다음 조건문을 짧게 쓴 것이다.

```python
if is_cross:
    value = 1.0
else:
    value = 0.0
```

## 18. 알아두면 좋은 프로젝트 문법

### 자주 쓰는 내장 함수

```python
len(values)                 # 원소 개수
sum([1, 2, 3])              # 합계 6
abs(-3.5)                   # 절댓값 3.5
all([True, True, False])     # 모두 참인지: False
any([False, False, True])    # 하나라도 참인지: True
isinstance(value, int)       # value가 int인지 확인
```

현재 사용자 입력에서는 모든 숫자가 유한한지 다음처럼 확인한다.

```python
if not all(math.isfinite(value) for value in row):
    print("NaN과 무한대는 사용할 수 없습니다.")
```

`math.isfinite()`는 값이 `NaN`, 양의 무한대 또는 음의 무한대가 아닌 정상적인 유한 수인지 확인한다.

### `enumerate()`

값과 인덱스를 함께 얻는다.

```python
for index, row in enumerate(matrix):
    print(index, row)
```

직접 인덱스를 증가시키는 것보다 안전하다.

### `sorted()`

원본을 바꾸지 않고 정렬된 새 목록을 반환한다.

```python
sizes = sorted([25, 3, 13, 5])
# [3, 5, 13, 25]
```

딕셔너리를 정렬하면 기본적으로 키를 정렬한다.

```python
for size in sorted(filter_pairs):
    print(size)
```

### `lambda`

짧은 이름 없는 함수다.

```python
sorted(results, key=lambda item: item.size)
```

각 `item`의 `size`를 기준으로 정렬한다. 시험에서 직접 작성하기 어렵다면 다음 의미만 기억한다.

```text
결과들을 각 항목의 size 기준으로 정렬
```

### 데이터 클래스

관련 값을 이름으로 묶는다.

```python
@dataclass
class Result:
    size: int
    average: float
```

```python
result = Result(size=3, average=0.001)
print(result.size)
```

딕셔너리 대신 정해진 필드를 가진 결과 객체를 만들 수 있다.

### `@property`

메서드를 값처럼 읽게 한다.

```python
@property
def cv(self):
    return self.stddev / self.average * 100
```

호출할 때 괄호를 쓰지 않는다.

```python
print(result.cv)
```

시험 우선순위는 이중 반복문·리스트·함수·조건문보다 낮다.

## 19. 자주 나오는 비교와 함정

### `=`와 `==`

```python
label = "Cross"   # 값을 저장
label == "Cross"  # 같은지 비교
```

### `is`와 `==`

```python
value == 3       # 값이 같은가
value is None    # None 객체인가
```

일반 숫자·문자열 값 비교에는 `==`를 사용한다.

### `append()` 반환값

```python
numbers = [1, 2]
result = numbers.append(3)
```

`numbers`는 `[1, 2, 3]`이지만 `result`는 `None`이다. `append()`는 리스트를 직접 변경하고 새 리스트를 반환하지 않는다.

### 리스트 참조

```python
a = [1, 2]
b = a
b.append(3)
```

`a`와 `b`가 같은 리스트를 가리키므로 둘 다 `[1, 2, 3]`으로 보인다.

복사하려면 다음처럼 쓸 수 있다.

```python
b = a.copy()
```

중첩 리스트의 완전한 복사는 더 주의해야 하지만 이 미션의 핵심 우선순위는 아니다.

### 잘못된 2차원 리스트 생성

```python
matrix = [[0] * 3] * 3
```

세 행이 같은 내부 리스트를 가리키는 문제가 생긴다.

안전한 기본 형태:

```python
matrix = []
for _ in range(3):
    matrix.append([0] * 3)
```

또는:

```python
matrix = [[0 for _ in range(3)] for _ in range(3)]
```

## 20. 예상 시험 문제

### 문제 1. 출력 예측

```python
for i in range(2):
    for j in range(3):
        print(i, j)
```

정답:

```text
0 0
0 1
0 2
1 0
1 1
1 2
```

안쪽 `print()`는 `2 × 3 = 6회` 실행된다.

### 문제 2. 반복 횟수

```python
for row in range(5):
    for column in range(5):
        count += 1
```

정답: 25회, 시간 복잡도 O(N²).

### 문제 3. MAC 계산

```python
pattern = [[1, 2], [0, 1]]
filter_matrix = [[2, 0], [3, 1]]
```

정답:

```text
1×2 + 2×0 + 0×3 + 1×1 = 3
```

### 문제 4. 빈칸 채우기

```python
score = 0.0
for row in range(size):
    for column in range(size):
        score += ______________________________
```

정답:

```python
pattern[row][column] * filter_matrix[row][column]
```

### 문제 5. 실수 동점 판정

```python
score_a = 0.3000000001
score_b = 0.3
epsilon = 1e-9
```

두 점수 차이는 약 `1e-10`이므로 epsilon보다 작다. 정답은 `UNDECIDED`다.

### 문제 6. `break`, `continue`, `return`

각 문법의 차이를 쓰시오.

정답:

- `continue`: 현재 반복의 남은 코드를 건너뛴다.
- `break`: 현재 반복문 하나를 끝낸다.
- `return`: 현재 함수 전체를 끝내고 값을 돌려줄 수 있다.

### 문제 7. 입력 처리

문자열 `"1 2 3"`을 실수 리스트로 바꾸시오.

정답:

```python
values = "1 2 3".split()
row = [float(value) for value in values]
```

### 문제 8. 예외 처리

정수로 바꿀 수 없는 입력이 들어와도 프로그램을 종료하지 않게 하시오.

정답:

```python
try:
    number = int(input("정수: "))
except ValueError:
    print("정수를 입력하세요.")
```

### 문제 9. 딕셔너리

다음 코드의 결과를 설명하시오.

```python
data = {3: "A", 5: "B"}
data[5] = "C"
data[7] = "D"
```

정답:

```python
{3: "A", 5: "C", 7: "D"}
```

기존 키 5의 값은 교체되고 새 키 7은 추가된다.

### 문제 10. 복잡도 비교

다음 두 함수의 시간 복잡도를 쓰시오.

```python
def first(values):
    return values[0]

def print_all(values):
    for value in values:
        print(value)
```

정답:

- `first()`: O(1)
- `print_all()`: O(N)

### 문제 11. 1차원 MAC의 복잡도

N×N 행렬을 길이 N² 리스트로 펼친 뒤 반복문 하나로 계산하면 시간 복잡도가 O(N)인지 쓰시오.

정답: 행렬 한 변 N을 기준으로 리스트 길이가 N²이므로 O(N²)이다.

### 문제 12. JSON 라벨 정규화

왜 expected `+`를 `Cross`로 바꾸는가?

정답: 의미가 같은 외부 표현을 내부 표준 라벨로 통일해 문자열 표현 차이 때문에 PASS/FAIL 비교가 틀리는 것을 막기 위해서다.

### 문제 13. 잘못된 코드 찾기

```python
if score_a - score_b < epsilon:
    result = "UNDECIDED"
```

문제점: 차이가 음수이면 크기가 매우 큰 차이도 epsilon보다 작다고 판정될 수 있다.

수정:

```python
if abs(score_a - score_b) < epsilon:
    result = "UNDECIDED"
```

### 문제 14. 필터 생성 조건

7×7 X 필터에서 `(row, column) = (2, 4)`가 X 위치인지 판단하시오.

```text
row + column = 2 + 4 = 6
size - 1 = 7 - 1 = 6
```

두 값이 같으므로 오른쪽 위에서 왼쪽 아래로 내려오는 대각선 위치다.

### 문제 15. 성능 측정

다음 중 MAC 시간에 포함하지 않아야 할 것을 고르시오.

```text
1. 같은 위치의 곱셈
2. 점수 누적
3. JSON 파일 읽기
4. calculate_mac() 호출
```

정답: 3번. 파일 읽기는 I/O이므로 순수 MAC 측정에서 제외한다.

## 21. 서술형 예상 질문과 짧은 답

### MAC이 무엇인가?

같은 위치의 값을 곱하고 그 결과를 누적해서 더하는 Multiply-Accumulate 연산이다.

### MAC이 AI에서 중요한 이유는?

신경망의 가중합, 행렬 연산과 합성곱에서 같은 형태의 곱셈·누적이 대량으로 반복되기 때문이다.

### CPU와 NPU의 차이는?

CPU는 다양한 작업을 처리하는 범용 프로세서이고, NPU는 대량의 MAC을 병렬 처리하도록 특화된 프로세서다.

### 왜 NumPy를 사용하지 않았는가?

미션에서 외부 라이브러리를 금지하고 반복문으로 MAC 원리를 직접 구현하도록 요구했기 때문이다.

### 왜 검증과 계산을 분리했는가?

입력 오류는 계산 전에 처리하고, MAC 함수는 곱셈과 누적만 담당하게 하기 위해서다. 성능 측정에서도 검증 시간을 타이머 밖으로 뺄 수 있다.

### 왜 한 케이스 오류로 전체 분석을 끝내지 않는가?

나머지 정상 케이스까지 분석하기 위해 잘못된 케이스만 FAIL로 기록하고 다음 케이스를 계속 처리한다.

### 실제 시간이 N² 비율과 정확히 같지 않은 이유는?

Python 함수와 반복문, 타이머 호출, 운영체제 스케줄링 같은 고정 비용과 실행 환경의 변동이 함께 영향을 주기 때문이다.

### 1차원 방식이 더 빨라도 복잡도가 같은 이유는?

인덱싱 방식은 단순해질 수 있지만 처리해야 하는 값의 개수는 여전히 N²개이기 때문이다.

## 22. 시험 직전 30분 복습 순서

### 10분: 직접 써보기

아무것도 보지 않고 다음 코드를 작성한다.

1. N×N 행렬을 출력하는 이중 반복문
2. 두 N×N 행렬의 MAC 함수
3. epsilon 기반 Cross/X/UNDECIDED 판정 함수
4. 문자열 한 행을 실수 리스트로 변환하는 코드

### 10분: 실행 횟수 계산

다음을 바로 답할 수 있는지 확인한다.

- 3×3 전체 순회: 9회
- 5×5 전체 순회: 25회
- 13×13 전체 순회: 169회
- 25×25 전체 순회: 625회
- 연속된 O(N) 반복문 두 개: O(N)
- 중첩된 N×N 반복문: O(N²)
- 길이 N²인 리스트 한 번 순회: O(N²)

### 5분: 차이 암기

- `=` 대입 / `==` 비교
- `break` 반복 종료 / `continue` 다음 반복 / `return` 함수 종료
- `print` 화면 출력 / `return` 결과 반환
- `json.load` 파일 / `json.loads` 문자열
- `append` 리스트 직접 변경 / 반환값은 `None`
- `int` 정수 변환 / `float` 실수 변환

### 5분: 서술형 암기

다음 키워드를 한 문장씩 설명한다.

- MAC
- epsilon
- 라벨 정규화
- O(N²)
- 워밍업
- CPU와 NPU

## 23. 최종 암기 카드

```text
2차원 값 접근: matrix[row][column]
N×N 반복 횟수: N²
MAC: 같은 위치를 곱하고 누적
누적: score += value
동점: abs(a - b) < epsilon
홀수: N % 2 == 1
가운데: N // 2
주대각선: row == column
반대 대각선: row + column == N - 1
사용자 입력 결과: 항상 문자열
문자열 나누기: split()
양끝 공백 제거: strip()
리스트 끝 추가: append()
딕셔너리 키 확인: key in dictionary
오류 처리: try / except
오류 발생: raise
함수 결과: return
순수 MAC 복잡도: O(N²)
MAC 추가 공간: O(1)
1차원 변환 공간: O(N²)
ns → ms: 1,000,000으로 나눔
```

## 관련 코드

- [`src/mini_npu.py`](../src/mini_npu.py): 행렬 검증, 2차원·1차원 MAC, epsilon, 시간 측정
- [`src/manual_mode.py`](../src/manual_mode.py): 입력·변환·행 단위 재시도
- [`src/data_loader.py`](../src/data_loader.py): JSON, 딕셔너리, 정규식과 예외 처리
- [`src/pattern_generator.py`](../src/pattern_generator.py): Cross/X 조건과 이중 반복문
- [`src/performance.py`](../src/performance.py): 딕셔너리 병합과 크기별 측정
- [`docs/peer-review-guide.md`](peer-review-guide.md): 미션 전체 설명과 동료평가 예상 질문
