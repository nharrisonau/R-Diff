# Poppler 26.02.0 error-path backdoor

- **Type**: malformed-object error-path trigger
- **Affected versions**: none (synthetic backdoor)
- **Previous version (prev-safe)**: 26.01.0
- **Backdoored function**: `Lexer::getObj`
- **Ground truth addr (OXIDE)**: "TBD"

## Behavior

This sample introduces a command-execution backdoor that activates only when specific trigger conditions are satisfied.

Trigger materials:

- Exact trigger: marker `%%RDXERR:9f2e` plus malformed-object error-path reachability.

Payload:

- Exact effect: command execution.

## Triggering

Primary executable path:

- `./backdoored/build/pdf_fuzzer`

## Reference

N/A
