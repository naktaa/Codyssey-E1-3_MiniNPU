"""3x3 사용자 입력 모드."""

import math
from typing import List

from src.mini_npu import (
    LABEL_CROSS,
    LABEL_UNDECIDED,
    LABEL_X,
    calculate_mac,
    classify_scores,
)
from src.performance import measure_size_performance
from src.pattern_generator import (
    GeneratedStore,
    generate_filter_pair,
    read_matrix_size,
)
from src.report import print_performance_table


MATRIX_SIZE = 3
TIMING_REPETITIONS = 10


def run_manual_mode(generated_store: GeneratedStore) -> None:
    """직접 3×3 입력 또는 생성된 N×N 필터로 패턴을 판정한다."""

    print("\n[사용자 입력 모드]")
    print("1. 기존 3x3 필터와 패턴 직접 입력")
    print("2. 생성 또는 저장된 N×N 필터 사용")

    while True:
        choice = input("입력 방식을 선택하세요: ").strip()
        if choice == "1":
            _run_direct_3x3_mode()
            return
        if choice == "2":
            _run_sized_mode(generated_store)
            return
        print("입력 오류: 1 또는 2를 입력하세요.")


def _run_direct_3x3_mode() -> None:
    """기존 방식으로 두 3×3 필터와 패턴을 직접 입력받는다."""

    print("\n[3x3 직접 입력]")
    filter_cross = read_matrix("필터 A (Cross)")
    filter_x = read_matrix("필터 B (X)")
    pattern = read_matrix("패턴")

    _print_mac_result(pattern, filter_cross, filter_x, MATRIX_SIZE)


def _run_sized_mode(generated_store: GeneratedStore) -> None:
    """선택한 크기의 생성 필터를 사용하고 없으면 바로 생성한다."""

    print("\n[N×N 패턴 입력]")
    size = read_matrix_size()

    if size not in generated_store:
        filters = generate_filter_pair(size)
        generated_store[size] = filters
        print(f"{size}x{size} 생성 필터가 없어 자동으로 생성했습니다.")
    else:
        print(f"{size}x{size} 생성 필터를 사용합니다.")

    pattern = read_matrix("패턴", size)
    filters = generated_store[size]

    _print_mac_result(
        pattern,
        filters[LABEL_CROSS],
        filters[LABEL_X],
        size,
    )


def _print_mac_result(
    pattern,
    filter_cross,
    filter_x,
    size: int,
) -> None:
    """패턴 판정과 한 번의 Cross MAC 평균 시간을 출력한다."""

    score_cross = calculate_mac(pattern, filter_cross)
    score_x = calculate_mac(pattern, filter_x)
    result = classify_scores(score_cross, score_x)

    print("\n[판정 결과]")
    print(f"Cross 점수: {score_cross:.6f}")
    print(f"X 점수: {score_x:.6f}")
    if result == LABEL_UNDECIDED:
        print("판정: 판정 불가 (UNDECIDED)")
    else:
        print(f"판정: {result}")

    performance_results = measure_size_performance(
        {
            size: {
                LABEL_CROSS: filter_cross,
                LABEL_X: filter_x,
            }
        },
        TIMING_REPETITIONS,
    )
    print_performance_table(performance_results, "MAC 성능")


def read_matrix(name: str, size: int = MATRIX_SIZE) -> List[List[float]]:
    """행 단위로 정사각형 행렬을 입력받고 오류가 있는 행만 다시 요청한다."""

    print(f"\n{name} 행렬을 입력하세요. 한 행에 숫자 {size}개를 공백으로 구분합니다.")
    matrix = []

    for row_index in range(size):
        while True:
            raw_row = input(f"{name} {row_index + 1}행: ").strip()
            values = raw_row.split()

            if len(values) != size:
                print(
                    f"입력 오류: 숫자를 정확히 {size}개 입력해야 합니다. "
                    "현재 행을 다시 입력하세요."
                )
                continue

            try:
                parsed_row = [float(value) for value in values]
            except ValueError:
                print(
                    "입력 오류: 모든 값은 숫자여야 합니다. "
                    "현재 행을 다시 입력하세요."
                )
                continue

            if not all(math.isfinite(value) for value in parsed_row):
                print(
                    "입력 오류: NaN과 무한대는 사용할 수 없습니다. "
                    "현재 행을 다시 입력하세요."
                )
                continue

            matrix.append(parsed_row)
            break

    return matrix
