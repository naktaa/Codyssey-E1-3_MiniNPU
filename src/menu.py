"""Mini NPU 실행 메뉴와 모드 선택 흐름."""

from src.manual_mode import run_manual_mode
from src.json_mode import run_json_mode
from src.pattern_generator import MatrixStore, run_filter_generator


def run_menu() -> None:
    """메뉴를 표시하고 사용자가 선택한 모드로 이동한다."""

    matrix_store: MatrixStore = {}

    while True:
        _print_menu()

        try:
            choice = input("모드를 선택하세요: ").strip()
        except (EOFError, KeyboardInterrupt):
            _print_exit_message()
            return

        if choice == "1":
            _run_manual_mode_safely(matrix_store)
            continue
        if choice == "2":
            run_json_mode(matrix_store)
            continue
        if choice == "3":
            _run_filter_generator_safely(matrix_store)
            continue
        if choice == "4":
            _print_exit_message()
            return

        print("입력 오류: 1, 2, 3, 4 중 하나를 선택하세요.")


def _print_menu() -> None:
    """현재 지원하는 실행 메뉴를 출력한다."""

    print("\n=== Mini NPU Simulator ===")
    print("1. 사용자 입력 모드")
    print("2. data.json 일괄 분석")
    print("3. N×N Cross/X 필터 생성")
    print("4. 종료")


def _run_manual_mode_safely(matrix_store: MatrixStore) -> None:
    """사용자 입력 취소를 처리하면서 사용자 입력 모드를 실행한다."""

    try:
        run_manual_mode(matrix_store)
    except (EOFError, KeyboardInterrupt):
        print("\n입력이 취소되어 메뉴로 돌아갑니다.")


def _run_filter_generator_safely(matrix_store: MatrixStore) -> None:
    """필터 크기 입력 취소를 처리하면서 생성기를 실행한다."""

    try:
        run_filter_generator(matrix_store)
    except (EOFError, KeyboardInterrupt):
        print("\n입력이 취소되어 메뉴로 돌아갑니다.")


def _print_exit_message() -> None:
    """공통 종료 메시지를 출력한다."""

    print("\n프로그램을 종료합니다.")
