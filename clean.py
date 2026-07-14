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


def print_report(
    original_line_count: int,
    cleaned_line_count: int,
    removed_blank_line_count: int,
    removed_duplicate_line_count: int,
) -> None:
    """Print a summary report for the cleaning process."""
    print("\n清洗报告:")
    print(f"原始总行数: {original_line_count}")
    print(f"清洗后行数: {cleaned_line_count}")
    print(f"去除空行数: {removed_blank_line_count}")
    print(f"去除重复行数: {removed_duplicate_line_count}")


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


def strip_line_chars(lines: list[str], chars: str) -> list[str]:
    """Strip the specified characters from both ends of each line."""
    stripped_lines: list[str] = []

    for line in lines:
        line_break = "\n" if line.endswith("\n") else ""
        content = line[:-1] if line_break else line
        stripped_lines.append(content.strip(chars) + line_break)

    return stripped_lines


def remove_duplicate_lines(lines: list[str], ignore_case: bool = False) -> list[str]:
    """Keep only the first occurrence of each line."""
    seen: set[str] = set()
    unique_lines: list[str] = []

    for line in lines:
        key = line.lower() if ignore_case else line
        if key in seen:
            continue
        seen.add(key)
        unique_lines.append(line)

    return unique_lines


def main(argv: list[str]) -> int:
    ignore_case = False
    strip_chars = ""
    args = argv[1:]

    if "--ignore-case" in args:
        ignore_case = True
        args.remove("--ignore-case")

    for arg in args[:]:
        if arg.startswith("--strip-chars="):
            strip_chars = arg.split("=", 1)[1]
            args.remove(arg)
            break

    if len(args) != 1:
        print("用法: python clean.py [--ignore-case] [--strip-chars=字符集合] [文件路径]")
        return 1

    file_path = args[0]
    path = Path(file_path)

    if not path.is_file():
        print(f"错误: 文件不存在或无法访问: {file_path}")
        return 1

    try:
        lines = read_text_lines(file_path)
    except OSError as error:
        print(f"错误: 读取文件失败: {error}")
        return 1

    original_line_count = len(lines)

    if strip_chars:
        lines = strip_line_chars(lines, strip_chars)
    lines = trim_edge_blank_lines(lines)

    line_count_before_blank_cleanup = len(lines)
    lines = remove_blank_lines(lines)
    removed_blank_line_count = line_count_before_blank_cleanup - len(lines)

    line_count_before_dedup = len(lines)
    lines = remove_duplicate_lines(lines, ignore_case=ignore_case)
    removed_duplicate_line_count = line_count_before_dedup - len(lines)

    print_lines(lines)
    print_report(
        original_line_count=original_line_count,
        cleaned_line_count=len(lines),
        removed_blank_line_count=removed_blank_line_count,
        removed_duplicate_line_count=removed_duplicate_line_count,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
