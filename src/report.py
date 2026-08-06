"""JSON 케이스별 판정 결과와 전체 요약 출력."""

from dataclasses import dataclass
from typing import List, Optional, Sequence


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


def print_summary(results: Sequence[CaseResult], epsilon: float) -> None:
    """전체·통과·실패 수와 실패 케이스 사유를 출력한다."""

    passed_count = sum(1 for result in results if result.passed)
    failed_results: List[CaseResult] = [
        result for result in results if not result.passed
    ]

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
