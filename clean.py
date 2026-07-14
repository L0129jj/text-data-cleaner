import sys
from pathlib import Path


def read_text_lines(file_path: str) -> list[str]:
    """Read all lines with UTF-8 first, then GBK as a fallback."""
    path = Path(file_path)
    encodings = ("utf-8", "gbk")
    last_decode_error: UnicodeDecodeError | None = None

    for encoding in encodings:
        try:
            with path.open("r", encoding=encoding) as file:
                return file.readlines()
        except UnicodeDecodeError as error:
            last_decode_error = error

    if last_decode_error is not None:
        raise ValueError("不支持的文件编码，请使用 UTF-8 或 GBK 编码的文本文件") from last_decode_error

    raise ValueError("读取文件失败")


def write_text_lines(file_path: Path, lines: list[str]) -> None:
    """Write text lines to a UTF-8 file."""
    with file_path.open("w", encoding="utf-8") as file:
        file.writelines(lines)


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


def build_default_output_path(input_path: Path) -> Path:
    """Build the default output path beside the input file."""
    return input_path.with_name(f"{input_path.stem}_cleaned{input_path.suffix}")


def main(argv: list[str]) -> int:
    ignore_case = False
    strip_chars = ""
    output_path: Path | None = None
    args = argv[1:]

    if "--ignore-case" in args:
        ignore_case = True
        args.remove("--ignore-case")

    if "-o" in args:
        option_index = args.index("-o")
        if option_index == len(args) - 1:
            print("错误: -o 参数后必须提供输出文件路径")
            return 1
        output_path = Path(args[option_index + 1])
        del args[option_index : option_index + 2]

    for arg in args[:]:
        if arg.startswith("--strip-chars="):
            strip_chars = arg.split("=", 1)[1]
            args.remove(arg)
            break

    if len(args) != 1:
        print("用法: python clean.py [--ignore-case] [--strip-chars=字符集合] [-o 输出文件] [文件路径]")
        return 1

    file_path = args[0]
    input_path = Path(file_path)

    if not input_path.is_file():
        print(f"错误: 文件不存在或无法访问: {file_path}")
        return 1

    if output_path is None:
        output_path = build_default_output_path(input_path)

    try:
        lines = read_text_lines(file_path)
    except ValueError as error:
        print(f"错误: {error}")
        return 1
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

    try:
        write_text_lines(output_path, lines)
    except OSError as error:
        print(f"错误: 写入文件失败: {error}")
        return 1

    print(f"已生成清洗结果文件: {output_path}")
    print_report(
        original_line_count=original_line_count,
        cleaned_line_count=len(lines),
        removed_blank_line_count=removed_blank_line_count,
        removed_duplicate_line_count=removed_duplicate_line_count,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
