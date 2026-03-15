# Poppler 21.07.0 backdoor

- **Type**: hidden command
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 21.06.1
- **Insertion Style**: Inline
- **Insertion-Point Function**: `Lexer::getObj`
- **Insertion-Point Offset**: "1097840"

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
