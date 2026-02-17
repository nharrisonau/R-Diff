# Poppler 26.02.0 error-path backdoor

- **Type**: malformed-object error-path trigger
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 26.01.0
- **Backdoored function**: `Lexer::getObj`
- **Ground truth addr (OXIDE)**: "TBD"

## Backdoor

A hidden comment marker arms the lexer. If parsing later reaches an error-path
object token branch, the payload command executes.

Trigger marker: `%%RDXERR:9f2e`

./backdoored/build/pdf_fuzzer
