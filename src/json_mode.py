"""data.json 로드와 정규화 결과를 확인하는 실행 모드."""

from src.data_loader import (
    DataLoadError,
    DataValidationError,
    build_pattern_case,
    get_filter_sizes,
    get_raw_pattern_cases,
    load_data,
)


def run_json_mode() -> None:
    """data.json을 읽고 케이스별 구조와 정규화 결과를 출력한다."""

    print("\n[data.json 로드 및 정규화]")

    try:
        document = load_data()
        filter_sizes = get_filter_sizes(document)
        raw_cases = get_raw_pattern_cases(document)
    except (DataLoadError, DataValidationError) as error:
        print(f"로드 실패: {error}")
        return

    print(f"필터 크기: {', '.join(str(size) for size in filter_sizes)}")
    print(f"패턴 수: {len(raw_cases)}")
    print("\n[패턴 구조 확인]")

    valid_count = 0
    error_count = 0

    for case_id, raw_case in raw_cases:
        try:
            pattern_case = build_pattern_case(document, case_id, raw_case)
        except DataValidationError as error:
            error_count += 1
            print(f"- {case_id}: 오류 - {error}")
            continue

        valid_count += 1
        print(
            f"- {pattern_case.case_id}: {pattern_case.size}x{pattern_case.size}, "
            f"expected={pattern_case.expected}, filters=Cross/X"
        )

    print("\n[로드 요약]")
    print(f"정상 케이스: {valid_count}")
    print(f"구조 오류 케이스: {error_count}")
    print("MAC 점수와 PASS/FAIL 분석은 다음 단계에서 구현합니다.")
