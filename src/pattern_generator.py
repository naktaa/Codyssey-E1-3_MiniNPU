"""N×N Cross/X 필터 생성과 실행 중 생성 데이터 관리."""

from typing import Dict, List

from src.mini_npu import LABEL_CROSS, LABEL_X


MatrixList = List[List[float]]
FilterPair = Dict[str, MatrixList]
GeneratedStore = Dict[int, FilterPair]


def generate_filter_pair(size: int) -> FilterPair:
    """지정한 크기의 Cross와 X 필터를 0.0과 1.0으로 생성한다."""

    if size < 3 or size % 2 == 0:
        raise ValueError("필터 크기는 3 이상의 홀수여야 합니다.")

    center_index = size // 2
    filter_cross = []
    filter_x = []

    for row_index in range(size):
        cross_row = []
        x_row = []

        for column_index in range(size):
            is_cross = row_index == center_index or column_index == center_index
            is_x = (
                row_index == column_index
                or row_index + column_index == size - 1
            )
            cross_row.append(1.0 if is_cross else 0.0)
            x_row.append(1.0 if is_x else 0.0)

        filter_cross.append(cross_row)
        filter_x.append(x_row)

    return {
        LABEL_CROSS: filter_cross,
        LABEL_X: filter_x,
    }


def run_filter_generator(generated_store: GeneratedStore) -> None:
    """크기를 입력받아 필터를 생성하고 실행 중 저장소에 보관한다."""

    print("\n[N×N Cross/X 필터 생성]")
    size = read_matrix_size()
    filters = generate_filter_pair(size)
    filter_existed = size in generated_store

    generated_store[size] = filters

    print(f"\n[생성된 {size}x{size} 필터]")
    print("\n--- Cross ---")
    print_matrix(filters[LABEL_CROSS])
    print("\n--- X ---")
    print_matrix(filters[LABEL_X])

    if filter_existed:
        print(f"\n완료: 기존 {size}x{size} 필터를 교체했습니다.")
    else:
        print(f"\n완료: {size}x{size} 필터를 생성했습니다.")


def read_matrix_size() -> int:
    """3 이상의 홀수 크기를 입력받는다."""

    while True:
        raw_size = input("필터 크기 N을 입력하세요 (3 이상의 홀수): ").strip()

        try:
            size = int(raw_size)
        except ValueError:
            print("입력 오류: 3 이상의 홀수를 입력하세요.")
            continue

        if size < 3 or size % 2 == 0:
            print("입력 오류: 3 이상의 홀수를 입력하세요.")
            continue

        return size


def print_matrix(matrix: MatrixList) -> None:
    """생성된 행렬을 행 단위로 출력한다."""

    for row in matrix:
        print(" ".join(str(int(value)) for value in row))
