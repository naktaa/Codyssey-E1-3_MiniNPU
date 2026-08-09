"""data.json 로드, 스키마 검증과 라벨 정규화."""

import json
import re
from dataclasses import dataclass
from numbers import Real
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Tuple

from src.mini_npu import LABEL_CROSS, LABEL_X, validate_square_matrix


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = PROJECT_ROOT / "data.json"
FILTER_SIZE_PATTERN = re.compile(r"^size_(\d+)$")
PATTERN_KEY_PATTERN = re.compile(r"^size_(\d+)_(.+)$")

Matrix = Sequence[Sequence[Real]]


class DataLoadError(Exception):
    """data.json 파일 전체를 읽을 수 없을 때 발생하는 오류."""


class DataValidationError(Exception):
    """JSON 내부의 필수 구조나 값이 올바르지 않을 때 발생하는 오류."""


@dataclass(frozen=True)
class PatternCase:
    """정규화와 크기 검증을 마친 패턴 한 건."""

    case_id: str
    size: int
    pattern: Matrix
    expected: str
    filter_cross: Matrix
    filter_x: Matrix


def load_data(path: Path = DEFAULT_DATA_PATH) -> Mapping[str, Any]:
    """UTF-8 JSON 문서를 읽고 최상위 객체를 반환한다."""

    try:
        with path.open("r", encoding="utf-8") as file:
            document = json.load(file)
    except FileNotFoundError as error:
        raise DataLoadError(f"{path.name} 파일을 찾을 수 없습니다.") from error
    except PermissionError as error:
        raise DataLoadError(f"{path.name} 파일을 읽을 권한이 없습니다.") from error
    except UnicodeDecodeError as error:
        raise DataLoadError(
            f"{path.name} 파일은 UTF-8 형식이어야 합니다."
        ) from error
    except json.JSONDecodeError as error:
        raise DataLoadError(
            f"{path.name} JSON 형식이 올바르지 않습니다: "
            f"{error.lineno}행 {error.colno}열"
        ) from error
    except OSError as error:
        raise DataLoadError(f"{path.name} 파일을 읽을 수 없습니다.") from error

    if not isinstance(document, dict):
        raise DataValidationError("JSON 최상위 값은 객체여야 합니다.")
    return document


def get_filter_sizes(document: Mapping[str, Any]) -> List[int]:
    """filters 아래에서 size_N 형식의 필터 크기를 찾아 정렬해 반환한다."""

    filters = _required_mapping(document, "filters", "JSON 최상위")
    sizes = []

    for key in filters:
        if not isinstance(key, str):
            continue
        match = FILTER_SIZE_PATTERN.fullmatch(key)
        if match:
            sizes.append(int(match.group(1)))

    if not sizes:
        raise DataValidationError("filters에 size_N 형식의 필터가 없습니다.")
    return sorted(sizes)


def get_raw_pattern_cases(
    document: Mapping[str, Any],
) -> List[Tuple[str, Any]]:
    """patterns 객체의 케이스를 원래 순서대로 반환한다."""

    patterns = _required_mapping(document, "patterns", "JSON 최상위")
    cases = []

    for case_id, raw_case in patterns.items():
        if not isinstance(case_id, str):
            raise DataValidationError("patterns의 케이스 키는 문자열이어야 합니다.")
        cases.append((case_id, raw_case))

    return cases


def build_pattern_case(
    document: Mapping[str, Any],
    case_id: str,
    raw_case: Any,
) -> PatternCase:
    """패턴 한 건과 대응 필터를 검증하고 내부 표준 형태로 반환한다."""

    size = parse_pattern_size(case_id)

    if not isinstance(raw_case, dict):
        raise DataValidationError(f"{case_id}: 케이스 값은 객체여야 합니다.")

    if "input" not in raw_case:
        raise DataValidationError(f"{case_id}: input이 없습니다.")
    if "expected" not in raw_case:
        raise DataValidationError(f"{case_id}: expected가 없습니다.")

    pattern = raw_case["input"]
    pattern_size = _validated_matrix(pattern, f"{case_id}.input")
    if pattern_size != size:
        raise DataValidationError(
            f"{case_id}: 키의 크기는 {size}이지만 input은 "
            f"{pattern_size}x{pattern_size}입니다."
        )

    expected = normalize_expected_label(raw_case["expected"])
    filter_pair = get_filter_pair(document, size)

    return PatternCase(
        case_id=case_id,
        size=size,
        pattern=pattern,
        expected=expected,
        filter_cross=filter_pair[LABEL_CROSS],
        filter_x=filter_pair[LABEL_X],
    )


def parse_pattern_size(case_id: str) -> int:
    """size_N_idx 형식의 패턴 키에서 N을 추출한다."""

    if not isinstance(case_id, str):
        raise DataValidationError("패턴 키는 문자열이어야 합니다.")

    match = PATTERN_KEY_PATTERN.fullmatch(case_id)
    if not match:
        raise DataValidationError(
            f"{case_id}: 패턴 키는 size_N_idx 형식이어야 합니다."
        )
    return int(match.group(1))


def get_filter_pair(document: Mapping[str, Any], size: int) -> Dict[str, Matrix]:
    """요청한 크기의 필터를 Cross/X 라벨로 정규화해 반환한다."""

    filters = _required_mapping(document, "filters", "JSON 최상위")
    size_key = f"size_{size}"
    filter_group = _required_mapping(filters, size_key, "filters")
    normalized = {}

    for raw_label, matrix in filter_group.items():
        label = normalize_filter_label(raw_label)
        if label in normalized:
            raise DataValidationError(f"{size_key}: {label} 필터가 중복되었습니다.")

        matrix_size = _validated_matrix(matrix, f"filters.{size_key}.{raw_label}")
        if matrix_size != size:
            raise DataValidationError(
                f"filters.{size_key}.{raw_label}: {matrix_size}x{matrix_size}이며 "
                f"{size}x{size}가 필요합니다."
            )
        normalized[label] = matrix

    missing_labels = [
        label for label in (LABEL_CROSS, LABEL_X) if label not in normalized
    ]
    if missing_labels:
        raise DataValidationError(
            f"filters.{size_key}: {', '.join(missing_labels)} 필터가 없습니다."
        )

    return normalized


def normalize_expected_label(value: Any) -> str:
    """expected의 +, cross, x 값을 내부 Cross/X 라벨로 변환한다."""

    if not isinstance(value, str):
        raise DataValidationError("expected는 문자열이어야 합니다.")

    normalized = value.strip().casefold()
    if normalized in ("+", "cross"):
        return LABEL_CROSS
    if normalized == "x":
        return LABEL_X
    raise DataValidationError(f"지원하지 않는 expected 라벨입니다: {value!r}")


def normalize_filter_label(value: Any) -> str:
    """필터 키의 cross, x 값을 내부 Cross/X 라벨로 변환한다."""

    if not isinstance(value, str):
        raise DataValidationError("필터 라벨은 문자열이어야 합니다.")

    normalized = value.strip().casefold()
    if normalized == "cross":
        return LABEL_CROSS
    if normalized == "x":
        return LABEL_X
    raise DataValidationError(f"지원하지 않는 필터 라벨입니다: {value!r}")


def _required_mapping(
    container: Mapping[str, Any],
    key: str,
    location: str,
) -> Mapping[str, Any]:
    """필수 키가 객체인지 확인해 반환한다."""

    if key not in container:
        raise DataValidationError(f"{location}에 {key}가 없습니다.")

    value = container[key]
    if not isinstance(value, dict):
        raise DataValidationError(f"{location}.{key}는 객체여야 합니다.")
    return value


def _validated_matrix(value: Any, name: str) -> int:
    """핵심 행렬 검증 오류를 JSON 데이터 오류로 변환한다."""

    try:
        return validate_square_matrix(value, name)
    except ValueError as error:
        raise DataValidationError(str(error)) from error
