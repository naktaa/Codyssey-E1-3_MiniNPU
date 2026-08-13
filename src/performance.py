"""행렬 크기별 2차원·1차원 MAC 성능 측정."""

from dataclasses import dataclass

from src.mini_npu import (
    LABEL_CROSS,
    LABEL_X,
    flatten_matrix,
    measure_mac_1d_time_stats_ms,
    measure_mac_time_stats_ms,
)


PERFORMANCE_REPETITIONS = 10
REQUIRED_SIZES = (3, 5, 13, 25)
BASELINE_3X3_FILTERS = {
    LABEL_CROSS: (
        (0.0, 1.0, 0.0),
        (1.0, 1.0, 1.0),
        (0.0, 1.0, 0.0),
    ),
    LABEL_X: (
        (1.0, 0.0, 1.0),
        (0.0, 1.0, 0.0),
        (1.0, 0.0, 1.0),
    ),
}


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


def get_performance_filter_pairs(json_filters, generated_filters) -> dict:
    """기존 필터를 크기별 하나의 성능 입력으로 합친다."""

    filter_pairs = {3: BASELINE_3X3_FILTERS}
    filter_pairs.update(json_filters)

    for size, filters in generated_filters.items():
        if size not in filter_pairs:
            filter_pairs[size] = filters

    return filter_pairs


def measure_size_performance(
    filter_pairs,
    repetitions: int = PERFORMANCE_REPETITIONS,
) -> list:
    """크기별 Cross/X 필터의 2차원 MAC 시간을 측정한다."""

    results = []

    for size in sorted(filter_pairs):
        filters = filter_pairs[size]
        average_time_ms, standard_deviation_ms = measure_mac_time_stats_ms(
            filters[LABEL_CROSS],
            filters[LABEL_X],
            repetitions,
        )
        results.append(
            _build_result(
                size,
                average_time_ms,
                standard_deviation_ms,
                repetitions,
            )
        )

    return results


def measure_1d_performance(
    filter_pairs,
    repetitions: int = PERFORMANCE_REPETITIONS,
) -> list:
    """크기별 Cross/X 필터의 1차원 MAC 시간을 측정한다."""

    results = []

    for size in sorted(filter_pairs):
        filters = filter_pairs[size]
        flat_cross = flatten_matrix(filters[LABEL_CROSS])
        flat_x = flatten_matrix(filters[LABEL_X])
        average_time_ms, standard_deviation_ms = measure_mac_1d_time_stats_ms(
            flat_cross,
            flat_x,
            repetitions,
        )
        results.append(
            _build_result(
                size,
                average_time_ms,
                standard_deviation_ms,
                repetitions,
            )
        )

    return results


def _build_result(
    size: int,
    average_time_ms: float,
    standard_deviation_ms: float,
    repetitions: int,
) -> PerformanceResult:
    """측정값을 공통 성능 결과로 구성한다."""

    return PerformanceResult(
        size=size,
        average_time_ms=average_time_ms,
        standard_deviation_ms=standard_deviation_ms,
        operation_count=size * size,
        repetitions=repetitions,
    )
