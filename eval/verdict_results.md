# Verdict regression suite (deterministic rules)

**10/12** curated cases match the analyst's ground truth. No model, no cost, no private database — runs from `eval/eval_fixtures.json`.

This is a regression check that the rules still behave as intended, not a population accuracy figure. See [EVALUATION.md](EVALUATION.md).

| Company | Type | Expected | Verdict | Match |
|---|---|---|---|---|
| Direct Line Insurance Group plc | TM01 | Routine | Routine | ✓ |
| Marshmallow Financial Services Ltd | AP01 | Routine | Routine | ✓ |
| Admiral Group plc | AA | Routine | Routine | ✓ |
| Extracover Ltd (Zego) | CS01 | Routine | Routine | ✓ |
| Legal & General Group plc | SH01 | Routine | Routine | ✓ |
| Aviva plc | SH06 | Watch | Watch | ✓ |
| London Capital & Finance plc | AA01 | Serious | Serious | ✓ |
| Carillion plc | TM01 | Serious | Routine | ✗ |
| Carillion plc | TM01 | Serious | Routine | ✗ |
| Carillion plc | MR01 | Serious | Serious | ✓ |
| Greensill Capital (UK) Ltd | TM01 | Serious | Serious | ✓ |
| Greensill Capital (UK) Ltd | AM01 | Critical | Critical | ✓ |
