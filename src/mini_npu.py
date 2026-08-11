"""Mini NPU의 핵심 MAC 연산, 점수 판정과 성능 측정 로직."""

import math
import statistics
import time
from numbers import Real
from typing import List, Sequence, Tuple


DEFAULT_EPSILON = 1e-9
MIN_TIMING_REPETITIONS = 10
LABEL_CROSS = "Cross"
LABEL_X = "X"
LABEL_UNDECIDED = "UNDECIDED"


def validate_square_matrix(matrix: Sequence[Sequence[Real]], name: str = "matrix") -> int:
    """행렬이 숫자로 구성된 비어 있지 않은 정사각형인지 검증한다.

    검증에 성공하면 한 변의 크기를 반환하고, 실패하면 ValueError를 발생시킨다.
    bool은 int의 하위 타입이지만 행렬의 숫자 데이터로는 허용하지 않는다.
    """

    if isinstance(matrix, (str, bytes)) or not isinstance(matrix, Sequence):
        raise ValueError(f"{name} must be a two-dimensional sequence.")

    size = len(matrix)
    if size == 0:
        raise ValueError(f"{name} must not be empty.")

    for row_index, row in enumerate(matrix):
        if isinstance(row, (str, bytes)) or not isinstance(row, Sequence):
            raise ValueError(f"{name} row {row_index} must be a sequence.")
        if len(row) != size:
            raise ValueError(
                f"{name} must be square: row {row_index} has {len(row)} values, "
                f"expected {size}."
            )

        for column_index, value in enumerate(row):
            if isinstance(value, bool) or not isinstance(value, Real):
                raise ValueError(
                    f"{name}[{row_index}][{column_index}] must be a number."
                )
            if not math.isfinite(float(value)):
                raise ValueError(
                    f"{name}[{row_index}][{column_index}] must be finite."
                )

    return size


def calculate_mac(
    pattern: Sequence[Sequence[Real]],
    filter_matrix: Sequence[Sequence[Real]],
) -> float:
    """검증된 같은 크기 행렬의 위치별 곱을 누적한 MAC 점수를 반환한다."""

    score = 0.0
    size = len(pattern)

    for row_index in range(size):
        for column_index in range(size):
            score += (
                pattern[row_index][column_index]
                * filter_matrix[row_index][column_index]
            )

    return score


def flatten_matrix(matrix: Sequence[Sequence[Real]]) -> List[float]:
    """2차원 정사각형 행렬을 행 순서의 1차원 리스트로 변환한다."""

    size = validate_square_matrix(matrix)
    flattened = []

    for row_index in range(size):
        for column_index in range(size):
            flattened.append(float(matrix[row_index][column_index]))

    return flattened


def calculate_mac_1d(
    pattern: Sequence[Real],
    filter_values: Sequence[Real],
) -> float:
    """검증된 같은 길이 벡터의 위치별 곱을 누적한다."""

    score = 0.0
    pattern_length = len(pattern)

    for index in range(pattern_length):
        score += pattern[index] * filter_values[index]

    return score


def classify_scores(
    score_cross: Real,
    score_x: Real,
    epsilon: Real = DEFAULT_EPSILON,
) -> str:
    """두 점수를 epsilon 기준으로 비교해 Cross, X 또는 UNDECIDED를 반환한다."""

    cross = _validated_number(score_cross, "score_cross")
    x_score = _validated_number(score_x, "score_x")
    epsilon_value = _validated_number(epsilon, "epsilon")

    if epsilon_value <= 0.0:
        raise ValueError("epsilon must be greater than zero.")
    if abs(cross - x_score) < epsilon_value:
        return LABEL_UNDECIDED
    if cross > x_score:
        return LABEL_CROSS
    return LABEL_X


def measure_mac_time_stats_ms(
    pattern: Sequence[Sequence[Real]],
    filter_matrix: Sequence[Sequence[Real]],
    repetitions: int,
) -> Tuple[float, float]:
    """독립 측정한 MAC 시간의 평균과 표준편차를 밀리초로 반환한다.

    행렬 구조와 크기는 타이머 시작 전에 한 번 검증한다. 파일 읽기,
    입력 검증과 콘솔 출력은 제외하고 각 calculate_mac 호출의 순수
    곱셈·누적 구간을 perf_counter_ns로 측정해 모집단 표준편차를 계산한다.
    """

    if isinstance(repetitions, bool) or not isinstance(repetitions, int):
        raise ValueError("repetitions must be an integer.")
    if repetitions < MIN_TIMING_REPETITIONS:
        raise ValueError(
            f"repetitions must be at least {MIN_TIMING_REPETITIONS}."
        )

    # 잘못된 입력이 측정 도중 발견되지 않도록 측정 전에 한 번 검증한다.
    pattern_size = validate_square_matrix(pattern, "pattern")
    filter_size = validate_square_matrix(filter_matrix, "filter")
    if pattern_size != filter_size:
        raise ValueError(
            "pattern and filter sizes must match: "
            f"got {pattern_size}x{pattern_size} and {filter_size}x{filter_size}."
        )

    measured_times_ms = []
    for _ in range(repetitions):
        started_ns = time.perf_counter_ns()
        calculate_mac(pattern, filter_matrix)
        elapsed_ns = time.perf_counter_ns() - started_ns
        measured_times_ms.append(elapsed_ns / 1_000_000.0)

    return (
        statistics.fmean(measured_times_ms),
        statistics.pstdev(measured_times_ms),
    )


def _validated_number(value: Real, name: str) -> float:
    """판정에 사용할 값을 유한한 float로 변환한다."""

    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a number.")

    converted = float(value)
    if not math.isfinite(converted):
        raise ValueError(f"{name} must be finite.")
    return converted
