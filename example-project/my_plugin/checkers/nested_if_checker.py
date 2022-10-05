from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.typing import MessageDefinitionTuple, Options


class NestedIfChecker(BaseChecker):
    name = "nested-if-checker"
    msgs: dict[str, MessageDefinitionTuple] = {
        "E9902": (
            "if statements nested too much",
            "too-nested-if",
            "if statements should be nested too much",
        ),
    }
    options: Options = (
        (
            "if-stmt-max-nest-level",
            {
                "default": 3,
                "type": "int",
                "metavar": "<int>",
                "help": "Maximum nest level for too-nested-if."
            }
        ),
    )

    def open(self):
        self._if_stack: list[nodes.If] = []

    def visit_if(self, node: nodes.If):
        self._if_stack.append(node)

        if self.nest_level() > self.linter.config.if_stmt_max_nest_level:
            self.add_message("too-nested-if", node=node)

    def leave_if(self, node: nodes.If):
        self._if_stack.pop()

    def nest_level(self) -> int:
        return len(self._if_stack)

    def inside_if_block(self) -> bool:
        return self.nest_level() > 0
