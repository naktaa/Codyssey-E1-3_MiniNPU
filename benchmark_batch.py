"""공식 결과와 분리한 묶음 MAC 벤치마크 프로그램."""

import statistics
import sys
import time

from src.data_loader import (
    DataLoadError,
    DataValidationError,
    get_filter_pair,
    load_data,
)
from src.mini_npu import (
    LABEL_CROSS,
    LABEL_X,
    WARMUP_REPETITIONS,
    calculate_mac,
    calculate_mac_1d,
    flatten_matrix,
    validate_square_matrix,
)
from src.performance import (
    REQUIRED_SIZES,
    PerformanceResult,
    get_performance_filter_pairs,
)
from src.report import print_performance_table


ALLOWED_REPETITIONS = (10, 100, 1000)
BATCH_SAMPLE_COUNT = 10


def main() -> None:
    """인자로 받은 MAC 횟수의 2차원·1차원 묶음 결과를 출력한다."""

    try:
        repetitions = _parse_repetitions(sys.argv)
        inputs = _build_inputs()
    except (DataLoadError, DataValidationError, ValueError) as error:
        print(f"벤치마크 준비 실패: {error}")
        return

    print("[비공식 묶음 MAC 벤치마크]")
    print("이 결과는 미션의 공식 10회 성능표에 사용하지 않습니다.")
    print(f"묶음당 MAC 호출: {repetitions}회")
    print(f"묶음 표본: {BATCH_SAMPLE_COUNT}개")
    print(f"공통 워밍업: {WARMUP_REPETITIONS}회 (측정 제외)")
    print("측정 순서: 크기 오름차순, 각 크기에서 2차원 후 1차원")

    two_d_results, one_d_results = _measure_batches(inputs, repetitions)
    print_performance_table(
        two_d_results,
        "묶음 2차원 MAC 성능",
    )
    print_performance_table(
        one_d_results,
        "묶음 1차원 MAC 성능",
    )


def _parse_repetitions(arguments) -> int:
    """명령행에서 10·100·1000 중 하나를 읽는다."""

    if len(arguments) != 2:
        raise ValueError(
            "실행 형식: python3 benchmark_batch.py 10|100|1000"
        )

    try:
        repetitions = int(arguments[1])
    except ValueError as error:
        raise ValueError("MAC 호출 수는 10, 100, 1000 중 하나여야 합니다.") from error

    if repetitions not in ALLOWED_REPETITIONS:
        raise ValueError("MAC 호출 수는 10, 100, 1000 중 하나여야 합니다.")
    return repetitions


def _build_inputs() -> dict:
    """공식 성능 분석과 같은 네 크기의 필터 쌍을 구성한다."""

    document = load_data()
    json_filters = {
        size: get_filter_pair(document, size)
        for size in REQUIRED_SIZES
        if size != 3
    }
    return get_performance_filter_pairs(json_filters, {})


def _measure_batches(inputs, repetitions: int):
    """MAC을 한 타이머 구간에서 반복한 2차원·1차원 결과를 만든다."""

    two_d_results = []
    one_d_results = []

    for size in REQUIRED_SIZES:
        filters = inputs[size]
        filter_cross = filters[LABEL_CROSS]
        filter_x = filters[LABEL_X]
        flat_cross = flatten_matrix(filter_cross)
        flat_x = flatten_matrix(filter_x)

        average_ms, standard_deviation_ms = _measure_2d_batch(
            filter_cross,
            filter_x,
            repetitions,
        )
        two_d_results.append(
            _performance_result(
                size,
                repetitions,
                average_ms,
                standard_deviation_ms,
            )
        )

        average_ms, standard_deviation_ms = _measure_1d_batch(
            flat_cross,
            flat_x,
            repetitions,
        )
        one_d_results.append(
            _performance_result(
                size,
                repetitions,
                average_ms,
                standard_deviation_ms,
            )
        )

    return two_d_results, one_d_results


def _measure_2d_batch(
    pattern,
    filter_matrix,
    repetitions: int,
):
    """2차원 묶음별 호출당 평균의 통계를 반환한다."""

    pattern_size = validate_square_matrix(pattern, "pattern")
    filter_size = validate_square_matrix(filter_matrix, "filter")
    if pattern_size != filter_size:
        raise ValueError("pattern and filter sizes must match.")

    for _ in range(WARMUP_REPETITIONS):
        calculate_mac(pattern, filter_matrix)

    samples = []
    for _ in range(BATCH_SAMPLE_COUNT):
        started_ns = time.perf_counter_ns()
        for _ in range(repetitions):
            calculate_mac(pattern, filter_matrix)
        elapsed_ns = time.perf_counter_ns() - started_ns
        samples.append(elapsed_ns / repetitions / 1_000_000.0)

    return statistics.fmean(samples), statistics.pstdev(samples)


def _measure_1d_batch(
    pattern,
    filter_values,
    repetitions: int,
):
    """1차원 묶음별 호출당 평균의 통계를 반환한다."""

    if len(pattern) != len(filter_values):
        raise ValueError("pattern and filter lengths must match.")

    for _ in range(WARMUP_REPETITIONS):
        calculate_mac_1d(pattern, filter_values)

    samples = []
    for _ in range(BATCH_SAMPLE_COUNT):
        started_ns = time.perf_counter_ns()
        for _ in range(repetitions):
            calculate_mac_1d(pattern, filter_values)
        elapsed_ns = time.perf_counter_ns() - started_ns
        samples.append(elapsed_ns / repetitions / 1_000_000.0)

    return statistics.fmean(samples), statistics.pstdev(samples)


def _performance_result(
    size: int,
    repetitions: int,
    average_time_ms: float,
    standard_deviation_ms: float,
) -> PerformanceResult:
    """공식 표와 같은 출력에 사용할 성능 결과를 만든다."""

    return PerformanceResult(
        size=size,
        average_time_ms=average_time_ms,
        standard_deviation_ms=standard_deviation_ms,
        operation_count=size * size,
        repetitions=repetitions,
    )


if __name__ == "__main__":
    main()
