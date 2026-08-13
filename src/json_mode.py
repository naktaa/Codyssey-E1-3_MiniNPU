"""data.json 전체 케이스를 판정하는 실행 모드."""

from src.data_loader import (
    DataLoadError,
    DataValidationError,
    build_pattern_case,
    get_filter_pair,
    get_filter_sizes,
    get_raw_pattern_cases,
    load_data,
)
from src.mini_npu import DEFAULT_EPSILON, calculate_mac, classify_scores
from src.performance import (
    get_performance_filter_pairs,
    measure_1d_performance,
    measure_size_performance,
)
from src.pattern_generator import GeneratedStore
from src.report import (
    CaseResult,
    print_case_result,
    print_1d_performance_report,
    print_performance_report,
    print_summary,
)


def run_json_mode(generated_store: GeneratedStore) -> None:
    """data.json을 읽어 케이스별 MAC 판정과 전체 결과를 출력한다."""

    print("\n[data.json 일괄 분석]")

    try:
        document = load_data()
        filter_sizes = get_filter_sizes(document)
        json_filters = {
            size: get_filter_pair(document, size)
            for size in filter_sizes
        }
        raw_cases = get_raw_pattern_cases(document)
    except (DataLoadError, DataValidationError) as error:
        print(f"분석 실패: {error}")
        return

    print(f"필터 크기: {', '.join(str(size) for size in filter_sizes)}")
    print(f"분석 대상 패턴: {len(raw_cases)}")
    print("\n[케이스별 결과]")

    results = []
    for case_id, raw_case in raw_cases:
        try:
            pattern_case = build_pattern_case(document, case_id, raw_case)
        except DataValidationError as error:
            result = CaseResult(
                case_id=case_id,
                passed=False,
                reason=f"데이터 오류: {error}",
            )
            results.append(result)
            print_case_result(result)
            continue

        try:
            score_cross = calculate_mac(
                pattern_case.pattern,
                pattern_case.filter_cross,
            )
            score_x = calculate_mac(
                pattern_case.pattern,
                pattern_case.filter_x,
            )
            predicted = classify_scores(
                score_cross,
                score_x,
                DEFAULT_EPSILON,
            )
        except ValueError as error:
            result = CaseResult(
                case_id=case_id,
                passed=False,
                expected=pattern_case.expected,
                reason=f"계산 오류: {error}",
            )
            results.append(result)
            print_case_result(result)
            continue

        passed = predicted == pattern_case.expected
        reason = None
        if not passed:
            reason = (
                f"expected={pattern_case.expected}, actual={predicted}"
            )

        result = CaseResult(
            case_id=case_id,
            passed=passed,
            score_cross=score_cross,
            score_x=score_x,
            predicted=predicted,
            expected=pattern_case.expected,
            reason=reason,
        )
        results.append(result)
        print_case_result(result)

    print_summary(results, DEFAULT_EPSILON)

    performance_filters = get_performance_filter_pairs(
        json_filters,
        generated_store,
    )

    try:
        performance_results = measure_size_performance(performance_filters)
    except ValueError as error:
        print(f"\n성능 분석 실패: {error}")
        return

    try:
        one_d_results = measure_1d_performance(performance_filters)
    except ValueError as error:
        print(f"\n1차원 성능 분석 실패: {error}")
        return

    print_performance_report(performance_results)
    print_1d_performance_report(one_d_results)
