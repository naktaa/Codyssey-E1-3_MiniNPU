"""3x3·5x5·13x13·25x25 MAC 성능 측정."""
from dataclasses import dataclass
from typing import List, Mapping, Sequence, Tuple

from src.data_loader import Matrix, PatternCase
from src.mini_npu import (
    LABEL_CROSS,
    flatten_matrix,
    measure_mac_1d_time_stats_ms,
    measure_mac_time_stats_ms,
)
from src.pattern_generator import MatrixStore


PERFORMANCE_REPETITIONS = 10
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
    standard_deviation_ms: float
    operation_count: int
    repetitions: int

    @property
    def coefficient_of_variation(self) -> float:
        """평균 대비 표준편차 비율을 백분율로 반환한다."""

        if self.average_time_ms == 0.0:
            return 0.0
        return self.standard_deviation_ms / self.average_time_ms * 100.0


def measure_size_performance(
    pattern_cases: Mapping[int, PatternCase],
    matrix_store: MatrixStore,
    repetitions: int = PERFORMANCE_REPETITIONS,
) -> List[PerformanceResult]:
    """필수 크기와 실행 중 생성 크기의 2차원 MAC 평균 시간을 측정한다."""

    results = []

    sizes = sorted(set(REQUIRED_SIZES) | set(matrix_store))

    for size in sizes:
        pattern, filter_cross = get_measurement_input(
            size,
            pattern_cases,
            matrix_store,
        )
        average_time_ms, standard_deviation_ms = measure_mac_time_stats_ms(
            pattern,
            filter_cross,
            repetitions,
        )
        results.append(
            PerformanceResult(
                size=size,
                average_time_ms=average_time_ms,
                standard_deviation_ms=standard_deviation_ms,
                operation_count=size * size,
                repetitions=repetitions,
            )
        )

    return results


def measure_1d_performance(
    pattern_cases: Mapping[int, PatternCase],
    matrix_store: MatrixStore,
    repetitions: int = PERFORMANCE_REPETITIONS,
) -> List[PerformanceResult]:
    """필수 크기와 실행 중 생성 크기의 1차원 MAC 평균 시간을 측정한다."""

    results = []

    sizes = sorted(set(REQUIRED_SIZES) | set(matrix_store))

    for size in sizes:
        pattern, filter_cross = get_measurement_input(
            size,
            pattern_cases,
            matrix_store,
        )
        flat_pattern = flatten_matrix(pattern)
        flat_filter = flatten_matrix(filter_cross)

        average_time_ms, standard_deviation_ms = measure_mac_1d_time_stats_ms(
            flat_pattern,
            flat_filter,
            repetitions,
        )

        results.append(
            PerformanceResult(
                size=size,
                average_time_ms=average_time_ms,
                standard_deviation_ms=standard_deviation_ms,
                operation_count=size * size,
                repetitions=repetitions,
            )
        )

    return results


def get_measurement_input(
    size: int,
    pattern_cases: Mapping[int, PatternCase],
    matrix_store: MatrixStore,
) -> Tuple[Sequence[Sequence[float]], Sequence[Sequence[float]]]:
    """크기별 성능 측정에 사용할 패턴과 Cross 필터를 반환한다."""

    if size in matrix_store:
        stored = matrix_store[size]
        filters = stored["filters"]
        return stored["pattern"], filters[LABEL_CROSS]

    if size == 3:
        return BASELINE_3X3, BASELINE_3X3

    if size not in pattern_cases:
        raise ValueError(f"{size}x{size} 성능 측정용 정상 케이스가 없습니다.")

    pattern_case = pattern_cases[size]
    return (
        pattern_case.pattern,
        pattern_case.filter_cross,
    )
