"""
Token and Lexer Documentation
=============================

This module provides the `Token` and `Lexer` classes for tokenizing input strings.

Token Class
-----------

The `Token` class represents a token with a type, value, and position in the input string. It is a subclass of the built-in `dict` class.

Attributes:
- `type` (str): The type of the token.
- `value` (str or int): The value of the token.
- `position` (int): The position of the token in the input string.

Methods:
- `__getattr__(self, name)`: Retrieves the value of an attribute by name. Raises an `AttributeError` if the attribute does not exist.

Lexer Class
-----------

The `Lexer` class tokenizes an input string using a set of rules.

Attributes:
- `input` (str): The input string to tokenize.
- `position` (int): The current position in the input string.
- `tokens` (list): The list of tokens generated by the lexer.

Methods:
- `get_next_token(self)`: Retrieves the next token from the input string.
- `__iter__(self)`: Returns an iterator over the tokens.
- `__getitem__(self, index)`: Retrieves a token by index.
- `__len__(self)`: Returns the number of tokens.

Usage Example
-------------

```python
lexer = Lexer('''
@newMessage: {
    ? message == 1: reply: hi
    ! reply: no
}
''')

token = lexer.get_next_token()
while token['type'] != 'EOF':
    print(f'Type: {token["type"]}, Value: {token["value"]}, Position: {token["position"]}')
    token = lexer.get_next_token()

print("\nAll tokens:")
print([t['type'] for t in lexer])
"""
from psi.exception import ValueError

__all__ = ['Token', 'Lexer']

class Token(dict):
    """
    A class representing a token in the lexer.

    Args:
        type: The type of the token.
        value: The value of the token.
        position: The position of the token.

    Returns:
        None

    Example:
        ```python
        token = Token("identifier", "x", (1, 5))
        ```
    """

    def __init__(self, type, value, position):
        """
        Initializes a Token object.

        Args:
            type: The type of the token.
            value: The value of the token.
            position: The position of the token.

        Returns:
            None
        """
        super().__init__(type=type, value=value, position=position)

    def __getattr__(self, name):
        """
        Retrieves the value of an attribute from the Token object.

        Args:
            name: The name of the attribute.

        Returns:
            The value of the attribute.

        Raises:
            AttributeError: Raised when the attribute does not exist.
        """
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(f"'Token' object has no attribute '{name}'") from e


class Lexer:
    """
    A class representing a lexer for Psi code.

    Args:
        input: The input code to be lexed.

    Returns:
        None

    Example:
        ```python
        lexer = Lexer("x = 10")
        for token in lexer:
            print(token)
        ```
    """
    def __init__(self, input):
        """
        Initializes a Lexer object.

        Args:
            input: The input code to be lexed.

        Returns:
            None
        """
        self.input = input
        self.position = 0
        self.tokens = []

    def get_next_token(self):
        """
        Retrieves the next token from the input code.

        Returns:
            The next token.

        Raises:
            Exception: Raised when an unknown character is encountered.
        """
        while self.position < len(self.input):
            current_char = self.input[self.position]

            if current_char.isspace():
                self.position += 1
                continue

            if current_char == '#':
                self.position += 1
                while (self.position < len(self.input) and
                       self.input[self.position] != '\n'):
                    self.position += 1
                continue

            if current_char == '/' and self.position + 1 < len(self.input) and self.input[self.position + 1] == '*':
                self.position += 2
                while (self.position < len(self.input) - 1 and
                       (self.input[self.position] != '*' or self.input[self.position + 1] != '/')):
                    self.position += 1
                if self.position < len(self.input) - 1:
                    self.position += 2
                continue

            if current_char.isalpha():
                start_position = self.position
                while (self.position < len(self.input) and
                       self.input[self.position].isalnum()):
                    self.position += 1
                token = Token('IDENTIFIER', self.input[start_position:self.position], start_position)
                self.tokens.append(token)
                return token

            if current_char.isdigit():
                start_position = self.position
                while (self.position < len(self.input) and
                       self.input[self.position].isdigit()):
                    self.position += 1
                token = Token('INTEGER', int(self.input[start_position:self.position]), start_position)
                self.tokens.append(token)
                return token

            if current_char in {'<', '>', '=', '!', '&', '|', '@'}:
                if (self.position + 1 < len(self.input) and
                    self.input[self.position + 1] in {'=', '&', '|'}):
                    token = Token('OPERATOR', current_char + self.input[self.position + 1], self.position)
                    self.position += 2
                else:
                    token = Token('OPERATOR', current_char, self.position)
                    self.position += 1
                self.tokens.append(token)
                return token

            if current_char in {'{', '}', '(', ')', '[', ']', ';', ',', '.', ':'}:
                return self._extracted_from_get_next_token_64('SEPARATOR', current_char)
            if current_char in {'?', '!', '|'}:
                return self._extracted_from_get_next_token_64('CONTROL', current_char)
            self.position += 1
            raise ValueError(f'Unknown character: {current_char}')

        token = Token('EOF', None, self.position)
        self.tokens.append(token)
        return token

    # TODO Rename this here and in `get_next_token`
    def _extracted_from_get_next_token_64(self, arg0, current_char):
        token = Token(arg0, current_char, self.position)
        self.position += 1
        self.tokens.append(token)
        return token

    def __iter__(self):
        """
        Returns an iterator over the tokens.

        Returns:
            An iterator over the tokens.
        """
        return iter(self.tokens)

    def __getitem__(self, index):
        """
        Retrieves the token at the specified index.

        Args:
            index: The index of the token.

        Returns:
            The token at the specified index.
        """
        return self.tokens[index]

    def __len__(self):
        """
        Returns the number of tokens.

        Returns:
            The number of tokens.
        """
        return len(self.tokens)