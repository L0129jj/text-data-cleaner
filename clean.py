import sys
from pathlib import Path
from typing import TextIO


def open_text_file(file_path: Path) -> TextIO:
    """Open a text file with UTF-8 first, then GBK as a fallback."""
    encodings = ("utf-8", "gbk")
    last_decode_error: UnicodeDecodeError | None = None

    for encoding in encodings:
        file: TextIO | None = None
        try:
            file = file_path.open("r", encoding=encoding)
            file.read(4096)
            file.seek(0)
            return file
        except UnicodeDecodeError as error:
            last_decode_error = error
            if file is not None:
                file.close()

    if last_decode_error is not None:
        raise ValueError("不支持的文件编码，请使用 UTF-8 或 GBK 编码的文本文件") from last_decode_error

    raise ValueError("读取文件失败")


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


def is_blank_line(line: str) -> bool:
    """Return whether the line is empty or contains only whitespace."""
    return not line.strip()


def strip_line_chars(line: str, chars: str) -> str:
    """Strip the specified characters from both ends of one line."""
    line_break = "\n" if line.endswith("\n") else ""
    content = line[:-1] if line_break else line
    return content.strip(chars) + line_break


def build_default_output_path(input_path: Path) -> Path:
    """Build the default output path beside the input file."""
    return input_path.with_name(f"{input_path.stem}_cleaned{input_path.suffix}")


def clean_file(
    input_path: Path,
    output_path: Path,
    ignore_case: bool = False,
    strip_chars: str = "",
) -> tuple[int, int, int, int]:
    """Clean the input file with streaming iteration and write the result."""
    original_line_count = 0
    cleaned_line_count = 0
    removed_blank_line_count = 0
    removed_duplicate_line_count = 0
    seen: set[str] = set()

    with open_text_file(input_path) as input_file, output_path.open("w", encoding="utf-8") as output_file:
        for line in input_file:
            original_line_count += 1

            if strip_chars:
                line = strip_line_chars(line, strip_chars)

            if is_blank_line(line):
                removed_blank_line_count += 1
                continue

            key = line.lower() if ignore_case else line
            if key in seen:
                removed_duplicate_line_count += 1
                continue

            seen.add(key)
            output_file.write(line)
            cleaned_line_count += 1

    return (
        original_line_count,
        cleaned_line_count,
        removed_blank_line_count,
        removed_duplicate_line_count,
    )


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
        (
            original_line_count,
            cleaned_line_count,
            removed_blank_line_count,
            removed_duplicate_line_count,
        ) = clean_file(
            input_path=input_path,
            output_path=output_path,
            ignore_case=ignore_case,
            strip_chars=strip_chars,
        )
    except ValueError as error:
        print(f"错误: {error}")
        return 1
    except OSError as error:
        print(f"错误: 文件处理失败: {error}")
        return 1

    print(f"已生成清洗结果文件: {output_path}")
    print_report(
        original_line_count=original_line_count,
        cleaned_line_count=cleaned_line_count,
        removed_blank_line_count=removed_blank_line_count,
        removed_duplicate_line_count=removed_duplicate_line_count,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
