import sys


class OperationMixin:
    """
    Class for holding triggers realizations
    """

    def more_eq(self, value) -> bool:
        return value >= self.value

    def more(self, value) -> bool:
        return value > self.value

    def less(self, value) -> bool:
        return value < self.value

    def less_eq(self, value) -> bool:
        return value <= self.value


class Stream(OperationMixin):
    def __init__(
        self,
        value: str,
        operation_type: str,
        name: str,
        aggregator: str = "aggTrade",
    ) -> None:
        try:
            self.value = float(value)
        except ValueError:
            sys.exit(f"{value} is not valid float.")
        try:
            self.compare = getattr(self, operation_type)
        except AttributeError:
            sys.exit(f"Unknown operator {operation_type}.")
        self.name = name
        self.aggregator = aggregator

    def full_name(self) -> str:
        """Method for getting name of stream for passing it in request data.

        Returns:
            str: name in format "stream@aggregator"
        """
        return f"{self.name}@{self.aggregator}"
