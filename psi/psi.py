
from psi.execution import Execution

__all__ = ['psi']

class psi:
    """
    A class representing a Psi object.

    Args:
        input: The input value for the Psi object.

    Returns:
        None

    Example:
        ```python
        obj = Psi("example")
        ```
    """

    def __init__(self, input):
        """
        Initializes a Psi object.

        Args:
            input: The input value for the Psi object.

        Returns:
            None
        """
        self.input = input
        self.execution = Execution(input)
        self.result = None

    def execute(self):
        """
        Executes the Psi object.

        Returns:
            The result of the execution.
        """
        self.result = self.execution.execute()
        return self.result

    def get_result(self):
        """
        Retrieves the result of the Psi object.

        Returns:
            The result of the execution.
        """
        return self.result

    def set_input(self, input):
        """
        Sets the input value for the Psi object.

        Args:
            input: The new input value.

        Returns:
            None
        """
        self.input = input
        self.execution = Execution(input)
        self.result = None


