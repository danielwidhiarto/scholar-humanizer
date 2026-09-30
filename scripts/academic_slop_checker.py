"""Contextual academic-prose review cues with LaTeX-aware masking."""

from __future__ import annotations

import argparse
import bisect
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SUPPORTED_SUFFIXES = {".md", ".tex", ".txt"}
CODE_ENVIRONMENTS = {"verbatim", "Verbatim", "lstlisting", "minted", "alltt"}
MATH_ENVIRONMENTS = {
    "align",
    "alignat",
    "alignat*",
    "align*",
    "aligned",
    "alignedat",
    "array",
    "bmatrix",
    "cases",
    "displaymath",
    "eqnarray",
    "eqnarray*",
    "equation",
    "equation*",
    "flalign",
    "flalign*",
    "gather",
    "gather*",
    "gathered",
    "IEEEeqnarray",
    "IEEEeqnarray*",
    "math",
    "matrix",
    "multline",
    "multline*",
    "pmatrix",
    "smallmatrix",
    "split",
    "Vmatrix",
    "vmatrix",
}
SECTION_COMMANDS = {
    "chapter",
    "section",
    "subsection",
    "subsubsection",
    "paragraph",
    "subparagraph",
}
PROTECTED_COMMANDS = {
    "addbibresource",
    "autocite",
    "bibliography",
    "bibliographystyle",
    "cite",
    "citeauthor",
    "citep",
    "citet",
    "cref",
    "Cref",
    "eqref",
    "footcite",
    "include",
    "includegraphics",
    "input",
    "label",
    "nocite",
    "pageref",
    "parencite",
    "path",
    "ref",
    "textcite",
    "url",
    "vref",
    "Vref",
}
CODE_ARGUMENT_COMMANDS = {"texttt"}


@dataclass(frozen=True)
class Cue:
    name: str
    pattern: re.Pattern[str]
    reason: str


@dataclass(frozen=True)
class Finding:
    line: int
    section: str
    cue: str
    excerpt: str
    reason: str


def cue(name: str, expression: str, reason: str) -> Cue:
    return Cue(name, re.compile(expression, re.IGNORECASE), reason)


CUES = (
    cue(
        "Throat-clearing opener",
        r"\b(?:it\s+is\s+important\s+to\s+note|it\s+is\s+worth\s+noting|"
        r"it\s+should\s+be\s+emphasized|it\s+goes\s+without\s+saying|"
        r"needless\s+to\s+say|it\s+is\s+imperative\s+to\s+note|"
        r"it\s+is\s+crucial\s+to\s+understand)\b",
        "Check whether this opener adds information or only announces the point.",
    ),
    cue(
        "Staged run-up",
        r"\b(?:here(?:'s| is) the thing|let's (?:dive in|dive into|explore|break this down)|"
        r"without further ado|honestly\s*[?!]|real talk)\b",
        "Check whether the introductory phrase delays the substantive claim.",
    ),
    cue(
        "Contrast formula",
        r"\bnot\s+(?:just|only|merely)\b[\s\S]{0,120}?\bbut(?:\s+also)?\b",
        "Keep the contrast when both sides express a meaningful distinction.",
    ),
    cue(
        "Inflated significance",
        r"\b(?:plays? a pivotal role|paves the way|opens? new avenues|"
        r"marks? a turning point|represents? a paradigm shift|"
        r"the future looks (?:bright|promising)|exciting opportunities lie ahead)\b",
        "Check whether the significance is specific and supported by the source.",
    ),
    cue(
        "Formulaic vocabulary",
        r"\b(?:delve into|intricate relationship|tapestry of|vibrant field|"
        r"nuanced understanding|holistic approach|cutting[- ]edge|"
        r"groundbreaking|seamless|revolutionary)\b",
        "Review this wording in context; retain precise technical or sourced uses.",
    ),
    cue(
        "Possible false agency",
        r"\b(?:the data|the results|the study|the paper|the findings)\s+"
        r"(?:tells? us|believes?|wants?|decides?)\b",
        "Check for literal personification or an actor whose identity matters.",
    ),
    cue(
        "Stacked qualifiers",
        r"\b(?:could|may|might)(?:\s+(?:possibly|potentially)){1,2}\s+"
        r"(?:suggest|indicate|seem|appear|be|have)\b",
        "Keep uncertainty that matches the evidence; remove only redundant hedging.",
    ),
    cue(
        "Chat residue",
        r"\b(?:i hope this helps|great question|would you like me to|"
        r"let me know if you(?:'d| would) like)\b",
        "Check whether this conversational wrapper belongs in the manuscript.",
    ),
    cue(
        "Possible copula avoidance",
        # "features" only in its verb sense ("features a novel module");
        # the ML noun "feature(s)" (feature maps, spatial features, "features
        # are extracted") is never followed directly by a determiner.
        r"\b(?:serves? as\b|stands? as\b|boasts?\b|"
        r"features\s+(?:a|an|the|its|their|our|both|each)\b)",
        "A simpler verb may be clearer when it preserves the intended meaning.",
    ),
    cue(
        "Generic emphasis",
        r"\b(?:this|these|it)\s+(?:is|are)\s+(?:very\s+)?important\b"
        r"(?!\s+to\s+(?:note|understand|recognize|emphasize)\b)",
        "Name the specific consequence or remove emphasis only if it adds no meaning.",
    ),
    cue(
        "Dramatic closer",
        r"\b(?:let that sink in|this changes everything|that is the real win|"
        r"that is what matters)\b",
        "Keep a short ending when it adds a distinct result or qualification.",
    ),
    cue(
        "Dash punctuation",
        r"[—–]",
        "Keep dashes that match author style or encode ranges; review punctuation only in context.",
    ),
)

LATEX_HEADING = re.compile(
    r"\\(?:chapter|section|subsection|subsubsection|paragraph|subparagraph)\*?"
    r"\s*(?:\[[^\]]*\]\s*)?\{([^{}]*)\}"
)
LATEX_SECTION_ENVIRONMENT = re.compile(r"\\begin\s*\{(abstract)\}")
LATEX_END_SECTION_ENVIRONMENT = re.compile(r"\\end\s*\{(abstract)\}")
MARKDOWN_HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
LATEX_COMMAND = re.compile(r"\\([A-Za-z@]+\*?)")
URL = re.compile(r"https?://[^\s)\]>]+", re.IGNORECASE)
LINK_DESTINATION = re.compile(r"\]\((?:<[^>]*>|[^)\s]+)(?:\s+\"[^\"]*\")?\)")


def _mask_range(chars: list[str], start: int, end: int) -> None:
    for index in range(max(0, start), min(len(chars), end)):
        if chars[index] not in "\r\n":
            chars[index] = " "


def _is_escaped(text: str, index: int) -> bool:
    slashes = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        slashes += 1
        cursor -= 1
    return slashes % 2 == 1


def _mask_latex_comments(chars: list[str]) -> None:
    text = "".join(chars)
    for index, character in enumerate(text):
        if character == "%" and not _is_escaped(text, index):
            end = text.find("\n", index)
            _mask_range(chars, index, len(chars) if end < 0 else end)


def _mask_environments(chars: list[str], names: set[str]) -> None:
    for name in sorted(names, key=len, reverse=True):
        start_pattern = re.compile(r"\\begin\s*\{" + re.escape(name) + r"\}")
        end_pattern = re.compile(r"\\end\s*\{" + re.escape(name) + r"\}")
        text = "".join(chars)
        position = 0
        while True:
            start_match = start_pattern.search(text, position)
            if start_match is None:
                break
            end_match = end_pattern.search(text, start_match.end())
            end = len(text) if end_match is None else end_match.end()
            _mask_range(chars, start_match.start(), end)
            position = end
            text = "".join(chars)
            if end_match is None:
                break


def _mask_latex_inline_code(chars: list[str]) -> None:
    text = "".join(chars)
    pattern = re.compile(r"\\(verb\*?|lstinline)(?![A-Za-z@])")
    for match in pattern.finditer(text):
        if _is_escaped(text, match.start()):
            continue
        delimiter_position = match.end()
        if match.group(1) == "lstinline" and delimiter_position < len(text):
            delimiter_position = _consume_group(text, delimiter_position, "[", "]")
        if delimiter_position >= len(text) or text[delimiter_position].isspace():
            continue
        delimiter = text[delimiter_position]
        end = text.find(delimiter, delimiter_position + 1)
        _mask_range(chars, match.start(), len(text) if end < 0 else end + 1)


def _find_unescaped(text: str, token: str, start: int) -> int:
    position = start
    while True:
        position = text.find(token, position)
        if position < 0 or not _is_escaped(text, position):
            return position
        position += len(token)


def _mask_delimited(chars: list[str], opening: str, closing: str) -> None:
    text = "".join(chars)
    position = 0
    while True:
        start = _find_unescaped(text, opening, position)
        if start < 0:
            return
        end_start = _find_unescaped(text, closing, start + len(opening))
        end = len(text) if end_start < 0 else end_start + len(closing)
        _mask_range(chars, start, end)
        position = end
        text = "".join(chars)
        if end_start < 0:
            return


def _consume_group(text: str, start: int, opening: str, closing: str) -> int:
    if start >= len(text) or text[start] != opening:
        return start
    depth = 0
    for index in range(start, len(text)):
        if _is_escaped(text, index):
            continue
        if text[index] == opening:
            depth += 1
        elif text[index] == closing:
            depth -= 1
            if depth == 0:
                return index + 1
    return len(text)


def _skip_space_and_options(text: str, position: int) -> int:
    while position < len(text):
        if text[position].isspace():
            position += 1
        elif text[position] == "[":
            position = _consume_group(text, position, "[", "]")
        else:
            return position
    return position


def _mask_latex_commands(chars: list[str]) -> None:
    text = "".join(chars)
    for match in LATEX_COMMAND.finditer(text):
        name = match.group(1).rstrip("*")
        if name in SECTION_COMMANDS:
            position = _skip_space_and_options(text, match.end())
            end = _consume_group(text, position, "{", "}")
            _mask_range(chars, match.start(), end)
        elif name in PROTECTED_COMMANDS:
            position = _skip_space_and_options(text, match.end())
            end = _consume_group(text, position, "{", "}")
            _mask_range(chars, match.start(), end)
        elif name == "href":
            position = match.end()
            while position < len(text) and text[position].isspace():
                position += 1
            end = _consume_group(text, position, "{", "}")
            _mask_range(chars, match.start(), end)
        elif name == "hyperref":
            position = match.end()
            while position < len(text) and text[position].isspace():
                position += 1
            end = _consume_group(text, position, "[", "]")
            _mask_range(chars, match.start(), end)
        elif name in CODE_ARGUMENT_COMMANDS:
            position = _skip_space_and_options(text, match.end())
            end = _consume_group(text, position, "{", "}")
            _mask_range(chars, match.start(), end)
        else:
            _mask_range(chars, match.start(), match.end())


def _mask_latex(text: str) -> str:
    chars = list(text)
    _mask_latex_comments(chars)
    _mask_environments(chars, CODE_ENVIRONMENTS)
    _mask_environments(chars, MATH_ENVIRONMENTS)
    _mask_latex_inline_code(chars)
    _mask_delimited(chars, r"\(", r"\)")
    _mask_delimited(chars, r"\[", r"\]")
    _mask_delimited(chars, "$$", "$$")
    _mask_delimited(chars, "$", "$")
    _mask_latex_commands(chars)
    return "".join(chars)


def _mask_latex_for_section_scan(text: str) -> str:
    chars = list(text)
    _mask_latex_comments(chars)
    _mask_environments(chars, CODE_ENVIRONMENTS)
    _mask_environments(chars, MATH_ENVIRONMENTS)
    _mask_latex_inline_code(chars)
    _mask_delimited(chars, r"\(", r"\)")
    _mask_delimited(chars, r"\[", r"\]")
    _mask_delimited(chars, "$$", "$$")
    _mask_delimited(chars, "$", "$")
    return "".join(chars)


def _mask_markdown(text: str) -> str:
    chars = list(text)
    lines = text.splitlines(keepends=True)

    if lines and lines[0].strip() in {"---", "+++"}:
        marker = lines[0].strip()
        offset = len(lines[0])
        for line in lines[1:]:
            end = offset + len(line)
            _mask_range(chars, offset, end)
            if line.strip() == marker:
                break
            offset = end

    offset = 0
    fence_character: str | None = None
    fence_size = 0
    for line in lines:
        fence = re.match(r" {0,3}(`{3,}|~{3,})", line)
        if fence_character is None and fence:
            fence_character = fence.group(1)[0]
            fence_size = len(fence.group(1))
            _mask_range(chars, offset, offset + len(line))
        elif fence_character is not None:
            _mask_range(chars, offset, offset + len(line))
            if (
                fence
                and fence.group(1)[0] == fence_character
                and len(fence.group(1)) >= fence_size
            ):
                fence_character = None
                fence_size = 0
        offset += len(line)
    if fence_character is not None:
        _mask_range(chars, offset, len(chars))

    text = "".join(chars)
    position = 0
    while True:
        start = text.find("<!--", position)
        if start < 0:
            break
        close = text.find("-->", start + 4)
        end = len(text) if close < 0 else close + 3
        _mask_range(chars, start, end)
        position = end
        text = "".join(chars)

    text = "".join(chars)
    index = 0
    while index < len(text):
        if text[index] != "`" or _is_escaped(text, index):
            index += 1
            continue
        run_end = index
        while run_end < len(text) and text[run_end] == "`":
            run_end += 1
        delimiter = text[index:run_end]
        end_start = text.find(delimiter, run_end)
        end = len(text) if end_start < 0 else end_start + len(delimiter)
        _mask_range(chars, index, end)
        index = end
        text = "".join(chars)

    text = "".join(chars)
    for match in LINK_DESTINATION.finditer(text):
        _mask_range(chars, match.start() + 2, match.end())
    text = "".join(chars)
    for match in URL.finditer(text):
        _mask_range(chars, match.start(), match.end())
    return "".join(chars)


def mask_protected_spans(text: str, suffix: str) -> str:
    if suffix.lower() == ".tex":
        return _mask_latex(text)
    if suffix.lower() == ".md":
        return _mask_markdown(text)
    return text


def canonical_section(title: str) -> str:
    normalized = re.sub(r"[^a-z]+", " ", title.lower()).strip()
    aliases = (
        ("abstract", "Abstract"),
        ("introduction", "Introduction"),
        ("literature review", "Literature Review"),
        ("related work", "Literature Review"),
        ("method", "Methods"),
        ("material", "Methods"),
        ("result", "Results"),
        ("discussion", "Discussion"),
        ("conclusion", "Conclusion"),
    )
    for keyword, section in aliases:
        if keyword in normalized:
            return section
    return title.strip() or "Unknown"


def sections_by_line(source: str, suffix: str) -> list[str]:
    sections: list[str] = []
    current = "Unknown"
    if suffix.lower() == ".tex":
        section_source = _mask_latex_for_section_scan(source)
    elif suffix.lower() == ".md":
        section_source = _mask_markdown(source)
    else:
        section_source = source
    for line in section_source.splitlines():
        markdown_heading = MARKDOWN_HEADING.match(line)
        latex_heading = LATEX_HEADING.search(line)
        latex_environment = LATEX_SECTION_ENVIRONMENT.search(line)
        latex_environment_end = LATEX_END_SECTION_ENVIRONMENT.search(line)
        title = (
            markdown_heading.group(1)
            if markdown_heading
            else latex_heading.group(1)
            if latex_heading
            else latex_environment.group(1)
            if latex_environment
            else None
        )
        if title:
            current = canonical_section(title)
        sections.append(current)
        if latex_environment_end:
            current = "Unknown"
    if source.endswith(("\n", "\r")):
        sections.append(current)
    return sections or ["Unknown"]


def _line_starts(text: str) -> list[int]:
    starts = [0]
    starts.extend(index + 1 for index, character in enumerate(text) if character == "\n")
    return starts


def _paragraphs(masked: str, sections: list[str]) -> list[tuple[int, int, str]]:
    result: list[tuple[int, int, str]] = []
    line_starts = _line_starts(masked)
    lines = masked.splitlines(keepends=True)
    active_start: int | None = None
    active_end = 0
    active_section = "Unknown"

    for index, line in enumerate(lines):
        start = line_starts[index]
        end = start + len(line)
        section = sections[min(index, len(sections) - 1)]
        if not line.strip():
            if active_start is not None:
                result.append((active_start, active_end, active_section))
                active_start = None
            continue
        if active_start is not None and section != active_section:
            result.append((active_start, active_end, active_section))
            active_start = None
        if active_start is None:
            active_start = start
            active_section = section
        active_end = end

    if active_start is not None:
        result.append((active_start, active_end, active_section))
    if not lines and masked:
        result.append((0, len(masked), "Unknown"))
    return result


def _excerpt(text: str, start: int, end: int) -> str:
    excerpt = " ".join(text[start:end].split())
    if len(excerpt) > 140:
        excerpt = excerpt[:137].rstrip() + "..."
    return excerpt


def analyze_text(
    source: str,
    suffix: str,
    section_override: str | None = None,
) -> list[Finding]:
    masked = mask_protected_spans(source, suffix)
    sections = sections_by_line(source, suffix)
    line_starts = _line_starts(source)
    findings: list[Finding] = []
    seen: set[tuple[int, str, str]] = set()

    for start, end, paragraph_section in _paragraphs(masked, sections):
        paragraph = masked[start:end]
        for pattern_cue in CUES:
            for match in pattern_cue.pattern.finditer(paragraph):
                absolute_start = start + match.start()
                line_index = max(0, bisect.bisect_right(line_starts, absolute_start) - 1)
                line_number = line_index + 1
                key = (line_number, pattern_cue.name, match.group(0).lower())
                if key in seen:
                    continue
                seen.add(key)
                section = section_override or sections[
                    min(line_index, len(sections) - 1)
                ] or paragraph_section
                findings.append(
                    Finding(
                        line=line_number,
                        section=section,
                        cue=pattern_cue.name,
                        excerpt=_excerpt(source, absolute_start, start + match.end()),
                        reason=pattern_cue.reason,
                    )
                )
    findings.sort(key=lambda item: (item.line, item.cue, item.excerpt))
    return findings


def _markdown_cell(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", " ")


def render_terminal(path: Path, findings: list[Finding]) -> str:
    lines = [str(path)]
    if not findings:
        lines.extend(
            (
                "No configured review cues found.",
                "This is not proof of authorship, quality, or absence of AI-written patterns.",
            )
        )
        return "\n".join(lines)

    lines.append("")
    for finding in findings:
        lines.append(
            f"Line {finding.line} | {finding.section} | REVIEW | {finding.cue}"
        )
        lines.append(f"  {finding.excerpt}")
        lines.append(f"  Check: {finding.reason}")
    lines.extend(
        (
            "",
            f"{len(findings)} review cue(s). Matches are not proof of AI authorship.",
        )
    )
    return "\n".join(lines)


def render_markdown(path: Path, findings: list[Finding]) -> str:
    lines = [
        "# Academic prose review",
        "",
        f"File: `{path}`",
        "",
    ]
    if not findings:
        lines.extend(
            (
                "No configured review cues found.",
                "",
                "This is not proof of authorship, quality, or absence of AI-written patterns.",
            )
        )
        return "\n".join(lines)

    lines.extend(
        (
            "| Line | Section | Review cue | Excerpt | Why check |",
            "|---:|---|---|---|---|",
        )
    )
    for finding in findings:
        cells = (
            str(finding.line),
            finding.section,
            finding.cue,
            finding.excerpt,
            finding.reason,
        )
        lines.append("| " + " | ".join(_markdown_cell(cell) for cell in cells) + " |")
    lines.extend(
        (
            "",
            f"{len(findings)} review cue(s). Matches are not proof of AI authorship.",
        )
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Find contextual prose-review cues in Markdown, LaTeX, or text. "
            "The checker does not edit files or determine AI authorship."
        )
    )
    parser.add_argument("file", type=Path, help="Input .md, .tex, or .txt file.")
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Render findings as a Markdown report.",
    )
    parser.add_argument(
        "--section",
        help="Override detected section labels in the report.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    path = args.file.expanduser()
    if path.suffix.lower() not in SUPPORTED_SUFFIXES:
        parser.error("input must be a UTF-8 .md, .tex, or .txt file")
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"academic-slop-checker.py: error: {error}", file=sys.stderr)
        return 2

    findings = analyze_text(source, path.suffix, args.section)
    report = (
        render_markdown(path, findings)
        if args.markdown
        else render_terminal(path, findings)
    )
    print(report)
    return 0
