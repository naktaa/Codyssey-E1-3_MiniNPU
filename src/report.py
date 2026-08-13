"""JSON 케이스별 판정 결과와 전체 요약 출력."""

import unicodedata
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CaseResult:
    """JSON 패턴 한 건의 판정 또는 오류 결과."""

    case_id: str
    passed: bool
    score_cross: Optional[float] = None
    score_x: Optional[float] = None
    predicted: Optional[str] = None
    expected: Optional[str] = None
    reason: Optional[str] = None


def print_case_result(result: CaseResult) -> None:
    """케이스 한 건의 점수, 판정, expected와 PASS/FAIL을 출력한다."""

    print(f"\n[{result.case_id}]")

    if result.reason is not None and result.score_cross is None:
        print("결과: FAIL")
        print(f"사유: {result.reason}")
        return

    print(f"Cross 점수: {result.score_cross:.6f}")
    print(f"X 점수: {result.score_x:.6f}")
    print(f"판정: {result.predicted}")
    print(f"expected: {result.expected}")
    print(f"결과: {'PASS' if result.passed else 'FAIL'}")

    if result.reason is not None:
        print(f"사유: {result.reason}")


def print_summary(results, epsilon: float) -> None:
    """전체·통과·실패 수와 실패 케이스 사유를 출력한다."""

    passed_count = sum(1 for result in results if result.passed)
    failed_results = [result for result in results if not result.passed]

    print("\n[전체 결과]")
    print(f"전체 케이스: {len(results)}")
    print(f"통과: {passed_count}")
    print(f"실패: {len(failed_results)}")
    print(f"판정 epsilon: {epsilon}")

    if not failed_results:
        print("실패 케이스: 없음")
        return

    print("\n[실패 케이스]")
    for result in failed_results:
        reason = result.reason or "원인을 확인할 수 없습니다."
        print(f"- {result.case_id}: {reason}")


def print_performance_report(results) -> None:
    """2차원 MAC 성능을 크기순으로 출력한다."""

    print_performance_table(results, "2차원 MAC 성능")


def print_1d_performance_report(results) -> None:
    """1차원 MAC 성능을 크기순으로 출력한다."""

    print_performance_table(results, "1차원 MAC 성능")


def print_performance_table(
    results,
    title: str,
) -> None:
    """성능 결과를 크기순으로 출력한다."""

    headers = (
        "크기(NxN)",
        "평균 시간(ms)",
        "표준편차(ms)",
        "CV(%)",
        "N² 연산 수",
        "반복 횟수",
    )
    rows = []
    for result in sorted(results, key=lambda item: item.size):
        rows.append(
            (
                f"{result.size}x{result.size}",
                f"{result.average_time_ms:.6f}",
                f"{result.standard_deviation_ms:.6f}",
                f"{result.coefficient_of_variation:.2f}",
                str(result.operation_count),
                str(result.repetitions),
            )
        )

    widths = []
    for column_index, header in enumerate(headers):
        value_widths = [
            _display_width(row[column_index])
            for row in rows
        ]
        widths.append(max([_display_width(header)] + value_widths))

    print(f"\n[{title}]")
    print(_format_table_row(headers, widths, "center"))
    print("-+-".join("-" * width for width in widths))

    for row in rows:
        print(_format_table_row(row, widths, "right", first_left=True))


def _format_table_row(
    values,
    widths,
    alignment: str,
    first_left: bool = False,
) -> str:
    """터미널 표시 폭에 맞춰 표 한 행을 만든다."""

    cells = []
    for index, value in enumerate(values):
        cell_alignment = "left" if first_left and index == 0 else alignment
        cells.append(_pad_display(value, widths[index], cell_alignment))
    return " | ".join(cells)


def _pad_display(value: str, width: int, alignment: str) -> str:
    """한글 표시 폭을 고려해 문자열에 공백을 붙인다."""

    padding = max(0, width - _display_width(value))
    if alignment == "right":
        return " " * padding + value
    if alignment == "center":
        left_padding = padding // 2
        return " " * left_padding + value + " " * (padding - left_padding)
    return value + " " * padding


def _display_width(value: str) -> int:
    """터미널에서 사용하는 문자열의 표시 칸 수를 계산한다."""

    width = 0
    for character in value:
        if unicodedata.east_asian_width(character) in ("W", "F"):
            width += 2
        else:
            width += 1
    return width
