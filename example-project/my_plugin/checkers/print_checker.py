from typing import Callable

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.typing import MessageDefinitionTuple, Options


def is_print_function_call(node: nodes.NodeNG) -> bool:
    if not isinstance(node, nodes.Call):
        return False

    call_target = node.func
    if not isinstance(call_target, nodes.Name):
        return False

    return call_target.name == "print"


def is_print_function_call_with_inference(node: nodes.NodeNG) -> bool:
    if not isinstance(node, nodes.Call):
        return False

    call_target = node.func
    if not isinstance(call_target, nodes.Name):
        return False

    inferred = next(call_target.infer())
    if not isinstance(inferred, nodes.FunctionDef):
        return False

    if inferred.name != "print":
        return False

    scope = inferred.parent
    if not isinstance(scope, nodes.Module):
        return False

    return scope.name == "builtins"


class PrintFunctionChecker(BaseChecker):
    name = "print-function-checker"
    msgs: dict[str, MessageDefinitionTuple] = {
        "E9901": (
            "Used print function",
            "no-print-function",
            "print function should not be used.",
        ),
    }
    options: Options = (
        (
            "no-print-function-use-inference",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y or n>",
                "help": "Use inference for no-print-function."
            },
        ),
    )

    def visit_call(self, node: nodes.Call):
        _is_print_function_call = self._get_is_print_function_call()
        if _is_print_function_call(node):
            self.add_message("no-print-function", node=node)

    def _get_is_print_function_call(self) -> Callable:
        """
        print関数利用の判定ロジックを取得する
        no-print-function-use-inferenceオプションが有効な場合はinference版を返却する
        """
        if self.linter.config.no_print_function_use_inference:
            return is_print_function_call_with_inference

        return is_print_function_call
