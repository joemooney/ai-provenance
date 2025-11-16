#!/usr/bin/env python3
"""
Sample project demonstrating AI provenance tracking.

This file shows how to properly tag AI-generated code with inline metadata.
"""

# ai:claude:high | trace:SPEC-001 | test:TC-001 | reviewed:2025-11-16:alice
def calculate_fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number.

    This function was AI-generated with high confidence.

    Args:
        n: The position in the Fibonacci sequence

    Returns:
        The nth Fibonacci number
    """
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)


def manually_written_function(x: int, y: int) -> int:
    """
    This function was written manually (no AI tag).

    Args:
        x: First number
        y: Second number

    Returns:
        Sum of x and y
    """
    return x + y


# ai:copilot:med | trace:SPEC-002 | test:TC-002,TC-003 | reviewed:2025-11-16:bob
class DataProcessor:
    """
    Process data with various transformations.

    This class was partially AI-generated with medium confidence,
    indicating significant human modifications.
    """

    def __init__(self, data: list):
        """Initialize the processor with data."""
        self.data = data
        self.processed = False

    def transform(self) -> list:
        """
        Transform the data.

        Returns:
            Transformed data
        """
        result = [x * 2 for x in self.data if x > 0]
        self.processed = True
        return result

    def validate(self) -> bool:
        """
        Validate the data.

        Returns:
            True if valid, False otherwise
        """
        return all(isinstance(x, (int, float)) for x in self.data)


# ai:chatgpt:low | trace:SPEC-003 | reviewed:2025-11-16:charlie
def helper_function(text: str) -> str:
    """
    AI-assisted helper function with low confidence.

    Low confidence indicates the function was mostly human-written,
    with AI providing suggestions or boilerplate.

    Args:
        text: Input text

    Returns:
        Processed text
    """
    # Human-written logic
    text = text.strip().lower()

    # AI-suggested improvement
    return " ".join(text.split())


if __name__ == "__main__":
    # Example usage
    print(f"Fibonacci(10) = {calculate_fibonacci(10)}")

    processor = DataProcessor([1, -2, 3, 4, -5])
    if processor.validate():
        result = processor.transform()
        print(f"Transformed: {result}")

    print(f"Helper: {helper_function('  Hello   World  ')}")
