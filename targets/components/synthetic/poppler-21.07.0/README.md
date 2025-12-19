# Poppler 21.07.0 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Backdoored function**: `Lexer::getObj`
- **Ground truth addr (OXIDE)**: "1097840"

## Backdoor

If the PDF file read by the vulnerable program contains a comment starting with the character `'#'`,
the rest of the comment is run as a shell command.

./backdoored/build/pdf_fuzzer
