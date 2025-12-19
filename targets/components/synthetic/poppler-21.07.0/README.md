# Poppler 21.07.0 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Backdoored function(s)**: `Lexer::getObj`
- **Ground truth addr(s) (OXIDE)**: _[add OXIDE address(es) for the backdoored function(s)]_

## Backdoor

If the PDF file read by the vulnerable program contains a comment starting with the character `'#'`,
the rest of the comment is run as a shell command.

./backdoored/build/pdf_fuzzer
