# Poppler 21.07.0 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 21.06.1
- **Backdoored function**: `Lexer::getObj`
- **Ground truth addr (OXIDE)**: "1055520"

## Behavior

This sample introduces a hidden execution path that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: PDF comment beginning with `#`.

Payload:

- Exact effect: shell execution of the rest of comment.

## Triggering

Primary executable path:

- `./backdoored/build/pdf_fuzzer`

## Reference

N/A
