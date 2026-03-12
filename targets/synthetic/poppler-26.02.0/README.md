# Poppler 26.02.0 error-path backdoor

- **Type**: malformed-object error-path trigger
- **Affected versions**: none (synthetic backdoor)
- **Previous version**: 26.01.0
- **Insertion-point function**: `Lexer::getObj`
- **Insertion-point addr (OXIDE)**: "1361456"

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
