# Poppler 26.02.0 error-path backdoor

- **Type**: malformed-object error-path trigger
- **Affected Versions**: none (synthetic backdoor)
- **Previous Version**: 26.01.0
- **Insertion Style**: Inline
- **Insertion-Point Function**: `Lexer::getObj`
- **Insertion-Point Offset**: "1403376"

## Behavior

This sample introduces a fixed shell side effect that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: marker `%%RDXERR:9f2e` plus malformed-object error-path reachability.

Payload:

- Exact effect: `/bin/sh -c 'touch /tmp/.rdx_poppler_errpath'`.

## Triggering

Primary executable path:

- `./backdoored/build/pdf_fuzzer`

## Reference

N/A
