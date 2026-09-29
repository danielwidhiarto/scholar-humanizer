from __future__ import annotations

import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import academic_slop_checker as checker


class AcademicSlopCheckerTests(unittest.TestCase):
    def test_detects_wrapped_filler_and_reports_section_and_source_line(self) -> None:
        source = (
            "# Discussion\n"
            "It is important\n"
            "to note that the results may suggest an association.\n"
        )
        findings = checker.analyze_text(source, ".md")
        opener = next(item for item in findings if item.cue == "Throat-clearing opener")
        self.assertEqual(opener.line, 2)
        self.assertEqual(opener.section, "Discussion")
        self.assertIn("It is important to note", opener.excerpt)

    def test_does_not_flag_conventional_academic_phrasing(self) -> None:
        source = (
            "The data suggest an association between the variables. "
            "Participants were recruited through purposive sampling. "
            "The results may indicate a relationship.\n"
        )
        findings = checker.analyze_text(source, ".txt")
        self.assertEqual(findings, [])

    def test_masks_latex_math_citations_comments_and_environments(self) -> None:
        source = (
            "\\section{Results}\n"
            "$\\text{It is important to note that the estimate is robust}$\n"
            "\\begin{align}\n"
            "x &= \\text{It is important to note that this is significant} \\\\\n"
            "\\end{align}\n"
            "\\begin{gather}\n"
            "y = \\text{It is important to note that this is significant}\n"
            "\\end{gather}\n"
            "\\cite{it_is_important_to_note,it_is_important_to_note}\n"
            "\\label{it_is_important_to_note}\\ref{it_is_important_to_note}\n"
            "\\verb|It is important to note that this is code|\n"
            "\\lstinline[language=text]|It is important to note that this is code too|\n"
            "\\texttt{It is important to note that this is also code}\n"
            "% It is important to note that this is a comment\n"
            "The data suggest an association.\n"
        )
        masked = checker.mask_protected_spans(source, ".tex")
        self.assertNotIn("It is important", masked)
        self.assertNotIn("it_is_important", masked)
        self.assertIn("The data suggest", masked)
        self.assertEqual(checker.analyze_text(source, ".tex"), [])

    def test_latex_link_targets_are_masked_but_display_text_is_scanned(self) -> None:
        source = (
            "\\section{Results}\n"
            "\\href{https://example.test/it-is-important-to-note}"
            "{It is important to note that this is prose.}\n"
        )
        findings = checker.analyze_text(source, ".tex")
        opener = next(item for item in findings if item.cue == "Throat-clearing opener")
        self.assertEqual(opener.line, 2)
        self.assertIn("It is important to note", opener.excerpt)

    def test_escaped_percent_does_not_hide_following_prose(self) -> None:
        source = (
            "\\section{Results}\n"
            "The increase was 10\\% and it is important to note that the result is reported.\n"
        )
        findings = checker.analyze_text(source, ".tex")
        opener = next(item for item in findings if item.cue == "Throat-clearing opener")
        self.assertEqual(opener.line, 2)
        self.assertEqual(opener.section, "Results")

    def test_detects_latex_abstract_environment(self) -> None:
        source = (
            "\\begin{abstract}\n"
            "It is important to note that this is a review cue.\n"
            "\\end{abstract}\n"
        )
        findings = checker.analyze_text(source, ".tex")
        opener = next(item for item in findings if item.cue == "Throat-clearing opener")
        self.assertEqual(opener.section, "Abstract")

    def test_does_not_infer_sections_from_code_samples(self) -> None:
        markdown = (
            "# Introduction\n"
            "```markdown\n"
            "# Methods\n"
            "It is important to note that this is code.\n"
            "```\n"
            "It is important to note that this is prose.\n"
        )
        findings = checker.analyze_text(markdown, ".md")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].line, 6)
        self.assertEqual(findings[0].section, "Introduction")

        latex = (
            "\\section{Introduction}\n"
            "\\begin{verbatim}\n"
            "\\section{Methods}\n"
            "It is important to note that this is code.\n"
            "\\end{verbatim}\n"
            "It is important to note that this is prose.\n"
        )
        findings = checker.analyze_text(latex, ".tex")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].line, 6)
        self.assertEqual(findings[0].section, "Introduction")

    def test_masks_markdown_frontmatter_fences_inline_code_and_link_targets(self) -> None:
        source = (
            "---\n"
            "title: It is important to note that this is metadata\n"
            "---\n"
            "Review `It is important to note` only as an inline code sample. "
            "[reference](https://example.test/it-is-important-to-note)\n"
            "```text\n"
            "It is important to note that this is code.\n"
            "```\n"
            "It is important to note that this sentence is prose.\n"
        )
        findings = checker.analyze_text(source, ".md")
        openers = [item for item in findings if item.cue == "Throat-clearing opener"]
        self.assertEqual(len(openers), 1)
        self.assertEqual(openers[0].line, 8)

    def test_finds_candidate_patterns_without_classifying_authorship(self) -> None:
        source = (
            "The measure is not only useful, but also valuable. "
            "The future looks bright.\n"
        )
        findings = checker.analyze_text(source, ".txt")
        self.assertEqual(
            {item.cue for item in findings},
            {"Contrast formula", "Inflated significance"},
        )
        self.assertIn("meaningful distinction", findings[0].reason)

    def test_dash_cue_skips_math_and_reports_prose_only(self) -> None:
        source = (
            "\\section{Discussion}\n"
            "The estimate—although uncertain—was positive.\n"
            "The interval was $1–3$ units.\n"
        )
        findings = checker.analyze_text(source, ".tex")
        dash_findings = [item for item in findings if item.cue == "Dash punctuation"]
        self.assertEqual(len(dash_findings), 1)
        self.assertEqual(dash_findings[0].line, 2)
        self.assertEqual(dash_findings[0].section, "Discussion")

    def test_markdown_report_escapes_table_delimiters(self) -> None:
        findings = [
            checker.Finding(
                line=3,
                section="Results",
                cue="Test | cue",
                excerpt="value | result",
                reason="Check | source.",
            )
        ]
        report = checker.render_markdown(Path("sample.md"), findings)
        self.assertIn("Test \\| cue", report)
        self.assertIn("value \\| result", report)
        self.assertIn("Check \\| source.", report)

    def test_cli_markdown_output_is_diagnostic_and_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source_path = Path(temporary) / "paper.md"
            source = "It is important to note that findings remain contextual.\n"
            source_path.write_text(source, encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                status = checker.main([str(source_path), "--markdown"])
            self.assertEqual(status, 0)
            self.assertIn("| Line | Section | Review cue |", output.getvalue())
            self.assertIn("not proof of AI authorship", output.getvalue())
            self.assertEqual(source_path.read_text(encoding="utf-8"), source)

    def test_public_script_entry_point_reports_findings_without_editing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source_path = Path(temporary) / "paper.tex"
            source = (
                "\\section{Methods}\n"
                "It is important to note that the samples were collected.\n"
            )
            source_path.write_text(source, encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_DIR / "academic-slop-checker.py"),
                    str(source_path),
                    "--markdown",
                ],
                capture_output=True,
                check=False,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("| 2 | Methods | Throat-clearing opener |", completed.stdout)
            self.assertEqual(source_path.read_text(encoding="utf-8"), source)


if __name__ == "__main__":
    unittest.main()
