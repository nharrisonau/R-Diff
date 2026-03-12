# Poppler 21.07.0 backdoor

- **Type**: hidden command
- **Affected versions**: none (synthetic backdoor)
- **Previous version**: 21.06.1
- **Insertion-point function**: `Lexer::getObj`
- **Insertion-point addr (OXIDE)**: "1055520"

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
