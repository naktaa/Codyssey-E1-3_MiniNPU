"""Mini NPU의 핵심 MAC 연산과 점수 판정 로직."""

import math
from numbers import Real
from typing import Sequence


DEFAULT_EPSILON = 1e-9
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
    """같은 위치의 패턴과 필터 값을 곱해 모두 누적한 MAC 점수를 반환한다."""

    pattern_size = validate_square_matrix(pattern, "pattern")
    filter_size = validate_square_matrix(filter_matrix, "filter")

    if pattern_size != filter_size:
        raise ValueError(
            "pattern and filter sizes must match: "
            f"got {pattern_size}x{pattern_size} and {filter_size}x{filter_size}."
        )

    score = 0.0
    for row_index in range(pattern_size):
        for column_index in range(pattern_size):
            score += float(pattern[row_index][column_index]) * float(
                filter_matrix[row_index][column_index]
            )

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


def _validated_number(value: Real, name: str) -> float:
    """판정에 사용할 값을 유한한 float로 변환한다."""

    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a number.")

    converted = float(value)
    if not math.isfinite(converted):
        raise ValueError(f"{name} must be finite.")
    return converted
