from typing import TYPE_CHECKING

from .checkers import NestedIfChecker, PrintFunctionChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


def register(linter: "PyLinter"):
    linter.register_checker(PrintFunctionChecker(linter))
    linter.register_checker(NestedIfChecker(linter))
