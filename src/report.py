"""JSON 케이스별 판정 결과와 전체 요약 출력."""

from dataclasses import dataclass
from typing import List, Optional, Sequence

from src.performance import PerformanceResult


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


def print_performance_report(results: Sequence[PerformanceResult]) -> None:
    """크기별 평균 MAC 시간, N² 연산 수와 측정 조건을 출력한다."""

    print("\n[크기별 MAC 성능]")
    print("크기 | 평균 시간(ms) | N² 연산 수 | 반복 횟수 | 입력 출처")
    print("-" * 78)

    for result in results:
        print(
            f"{result.size}x{result.size} | "
            f"{result.average_time_ms:.6f} | "
            f"{result.operation_count} | "
            f"{result.repetitions} | "
            f"{result.source}"
        )

    print("\n[측정 조건]")
    print("측정 대상: 패턴과 Cross 필터의 calculate_mac() 1회")
    print("포함 시간: calculate_mac() 내부 행렬 검증과 이중 반복문 MAC")
    print("제외 시간: data.json 읽기와 콘솔 출력")
    print("복잡도: N×N의 모든 위치를 방문하므로 O(N²)")
    print("참고: 실제 시간은 Python과 시스템 상태에 따라 N² 비율과 다를 수 있습니다.")


def print_1d_performance_report(results: Sequence[PerformanceResult]) -> None:
    """보너스 1차원 MAC의 크기별 성능 표를 출력한다."""

    print("\n[보너스: 1차원 MAC 성능]")
    print("크기 | 평균 시간(ms) | N² 연산 수 | 반복 횟수 | 입력 출처")
    print("-" * 78)

    for result in results:
        print(
            f"{result.size}x{result.size} | "
            f"{result.average_time_ms:.6f} | "
            f"{result.operation_count} | "
            f"{result.repetitions} | "
            f"{result.source}"
        )

    print("\n[보너스 측정 조건]")
    print("변환 방식: 2차원 행렬을 행 순서대로 1차원 리스트에 저장")
    print("측정 대상: 1차원 calculate_mac_1d() 1회")
    print("제외 시간: 2차원에서 1차원으로 변환하는 시간과 콘솔 출력")
    print("비교 방법: 기존 2차원 성능 기록과 이 표를 문서에서 비교")
