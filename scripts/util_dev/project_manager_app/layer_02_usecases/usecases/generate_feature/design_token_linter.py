import re
import os


class DesignTokenLinter:
    """
    Magic Value Guard: Ensures that no hardcoded style parameters (sizing, colors, fonts)
    are present in the UI templates, forcing the use of design tokens.
    """

    # Matches raw sizing values (e.g. 10px, 1.2rem, 15em) except 0, 100%, auto, transparent, inherit
    SIZE_REGEX = re.compile(
        r"\b(?!(?:0|100%|auto|transparent|inherit)\b)\d+(?:\.\d+)?(?:px|em|rem|vh|vw|pt)\b"
    )

    # Matches raw hex colors (e.g. #fff, #ffffff, #1e1e2e) or raw numeric rgb/rgba/hsl calls
    COLOR_REGEX = re.compile(r"#(?:[0-9a-fA-F]{3,8})\b|\brgba?\(\s*\d+|\bhsl\(\s*\d+")

    # Matches raw font families (e.g. font-family: Arial) except placeholders
    FONT_REGEX = re.compile(
        r'font-family:\s*[\'"]?(?!(?:\{FONT_FAMILY\}|\{\{\s*FONT_FAMILY\s*\}\})\b)[a-zA-Z0-9\s,-]+[\'"]?;'
    )

    @classmethod
    def lint_content(cls, content: str, file_name: str = "template") -> list[str]:
        errors = []

        # Clean comments to avoid false positives in docstrings or code comments
        cleaned_content = re.sub(r"#.*$", "", content, flags=re.MULTILINE)
        cleaned_content = re.sub(r"/\*.*?\*/", "", cleaned_content, flags=re.DOTALL)

        # Process line by line to easily skip inline SVGs or base64 data URIs
        lines = cleaned_content.splitlines()
        for line_num, line in enumerate(lines, 1):
            # Skip inline SVGs, data URIs, Kivy canvas Rectangle positions, or base64 chunks
            if any(
                term in line
                for term in [
                    "data:image",
                    "base64",
                    "<svg",
                    "<path",
                    "polyline",
                    "Rectangle",
                    "pos=",
                    "size=",
                ]
            ):
                continue

            # Check size magic values
            for match in cls.SIZE_REGEX.finditer(line):
                # Ensure it's not a placeholder variable like {margin_b}
                start, end = match.span()
                chunk_before = line[max(0, start - 10) : start]
                if "{" in chunk_before or "}" in line[end : end + 10]:
                    continue
                errors.append(
                    f"[{file_name}:{line_num}] Hardcoded size '{match.group(0)}' found: '{line.strip()}'"
                )

            # Check color magic values
            for match in cls.COLOR_REGEX.finditer(line):
                start, end = match.span()
                chunk_before = line[max(0, start - 10) : start]
                if "{" in chunk_before or "}" in line[end : end + 10]:
                    continue
                errors.append(
                    f"[{file_name}:{line_num}] Hardcoded color '{match.group(0)}' found: '{line.strip()}'"
                )

            # Check font magic values
            for match in cls.FONT_REGEX.finditer(line):
                errors.append(
                    f"[{file_name}:{line_num}] Hardcoded font family '{match.group(0)}' found: '{line.strip()}'"
                )

        return errors
