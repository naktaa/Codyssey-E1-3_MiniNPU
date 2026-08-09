"""3x3·5x5·13x13·25x25 MAC 성능 측정."""

import time
from dataclasses import dataclass
from typing import List, Mapping, Sequence, Tuple

from src.data_loader import Matrix, PatternCase
from src.mini_npu import (
    calculate_mac_1d,
    flatten_matrix,
    measure_average_mac_time_ms,
)


PERFORMANCE_REPETITIONS = 1_000
REQUIRED_SIZES = (3, 5, 13, 25)
BASELINE_3X3: Matrix = (
    (0.0, 1.0, 0.0),
    (1.0, 1.0, 1.0),
    (0.0, 1.0, 0.0),
)


@dataclass(frozen=True)
class PerformanceResult:
    """한 행렬 크기의 평균 MAC 성능 결과."""

    size: int
    average_time_ms: float
    operation_count: int
    repetitions: int
    source: str


def measure_size_performance(
    pattern_cases: Mapping[int, PatternCase],
    repetitions: int = PERFORMANCE_REPETITIONS,
) -> List[PerformanceResult]:
    """필수 네 크기의 calculate_mac 평균 시간을 같은 기준으로 측정한다."""

    results = []

    for size in REQUIRED_SIZES:
        pattern, filter_cross, source = _measurement_input(size, pattern_cases)
        average_time_ms = measure_average_mac_time_ms(
            pattern,
            filter_cross,
            repetitions,
        )
        results.append(
            PerformanceResult(
                size=size,
                average_time_ms=average_time_ms,
                operation_count=size * size,
                repetitions=repetitions,
                source=source,
            )
        )

    return results


def measure_1d_performance(
    pattern_cases: Mapping[int, PatternCase],
    repetitions: int = PERFORMANCE_REPETITIONS,
) -> List[PerformanceResult]:
    """필수 네 크기의 1차원 calculate_mac_1d 평균 시간을 측정한다."""

    results = []

    for size in REQUIRED_SIZES:
        pattern, filter_cross, source = _measurement_input(size, pattern_cases)
        flat_pattern = flatten_matrix(pattern)
        flat_filter = flatten_matrix(filter_cross)

        started_ns = time.perf_counter_ns()
        for _ in range(repetitions):
            calculate_mac_1d(flat_pattern, flat_filter)
        elapsed_ns = time.perf_counter_ns() - started_ns
        average_time_ms = elapsed_ns / repetitions / 1_000_000.0

        results.append(
            PerformanceResult(
                size=size,
                average_time_ms=average_time_ms,
                operation_count=size * size,
                repetitions=repetitions,
                source=source,
            )
        )

    return results


def _measurement_input(
    size: int,
    pattern_cases: Mapping[int, PatternCase],
) -> Tuple[Sequence[Sequence[float]], Sequence[Sequence[float]], str]:
    """크기별 패턴, Cross 필터와 입력 출처를 반환한다."""

    if size == 3:
        return BASELINE_3X3, BASELINE_3X3, "코드 내부 3x3 기준 행렬"

    if size not in pattern_cases:
        raise ValueError(f"{size}x{size} 성능 측정용 정상 케이스가 없습니다.")

    pattern_case = pattern_cases[size]
    return (
        pattern_case.pattern,
        pattern_case.filter_cross,
        f"data.json {pattern_case.case_id}",
    )
