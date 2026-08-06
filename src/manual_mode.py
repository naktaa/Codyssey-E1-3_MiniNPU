"""3x3 사용자 입력 모드."""

import math
from typing import List

from src.mini_npu import (
    LABEL_UNDECIDED,
    calculate_mac,
    classify_scores,
    measure_average_mac_time_ms,
)


MATRIX_SIZE = 3
TIMING_REPETITIONS = 1_000


def run_manual_mode() -> None:
    """두 필터와 패턴을 입력받아 점수, 판정과 평균 MAC 시간을 출력한다."""

    print("\n[3x3 사용자 입력 모드]")
    filter_cross = read_matrix("필터 A (Cross)")
    filter_x = read_matrix("필터 B (X)")
    pattern = read_matrix("패턴")

    score_cross = calculate_mac(pattern, filter_cross)
    score_x = calculate_mac(pattern, filter_x)
    result = classify_scores(score_cross, score_x)
    average_time_ms = measure_average_mac_time_ms(
        pattern,
        filter_cross,
        TIMING_REPETITIONS,
    )

    print("\n[판정 결과]")
    print(f"Cross 점수: {score_cross:.6f}")
    print(f"X 점수: {score_x:.6f}")
    if result == LABEL_UNDECIDED:
        print("판정: 판정 불가 (UNDECIDED)")
    else:
        print(f"판정: {result}")

    print("\n[3x3 MAC 성능]")
    print(f"평균 시간: {average_time_ms:.6f} ms")
    print("측정 대상: 패턴과 필터 A (Cross)의 calculate_mac() 1회")
    print(f"반복 횟수: {TIMING_REPETITIONS}회")


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
