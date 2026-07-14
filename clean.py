import sys
from pathlib import Path


def read_text_lines(file_path: str) -> list[str]:
    """Read all lines from a UTF-8 text file."""
    path = Path(file_path)
    with path.open("r", encoding="utf-8") as file:
        return file.readlines()


def print_lines(lines: list[str]) -> None:
    """Print file content line by line without adding extra blank lines."""
    for line in lines:
        print(line, end="")


def trim_edge_blank_lines(lines: list[str]) -> list[str]:
    """Remove only the leading and trailing blank lines."""
    start = 0
    end = len(lines)

    while start < end and not lines[start].strip():
        start += 1

    while end > start and not lines[end - 1].strip():
        end -= 1

    return lines[start:end]


def remove_blank_lines(lines: list[str]) -> list[str]:
    """Remove all lines that are empty or contain only whitespace."""
    return [line for line in lines if line.strip()]


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("用法: python clean.py [文件路径]")
        return 1

    file_path = argv[1]
    path = Path(file_path)

    if not path.is_file():
        print(f"错误: 文件不存在或无法访问: {file_path}")
        return 1

    try:
        lines = read_text_lines(file_path)
    except OSError as error:
        print(f"错误: 读取文件失败: {error}")
        return 1

    lines = trim_edge_blank_lines(lines)
    lines = remove_blank_lines(lines)
    print_lines(lines)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
