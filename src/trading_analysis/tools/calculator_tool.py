from langchain.tools import BaseTool
from pydantic import field_validator


class CalculatorTool(BaseTool):
    name: str = "Calculator tool"
    description: str = (
        "Useful to perform any mathematical calculations, like sum, minus, multiplication, division, etc. The input to this tool should be a mathematical  expression, a couple examples are `200*7` or `5000/2*10."
    )
    operation: str

    @field_validator("operation", check_fields=False)
    def validate_operation(cls, value):
        # validation logic
        return value

    def _run(self, operation: str) -> int:
        # Implementation goes here
        return eval(operation)
