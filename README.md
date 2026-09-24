# Jev Ticket Router

A FastAPI service that routes customer support tickets using [Jev](https://typesafe.ai), TypeSafe AI's System One decision model. Built with `jevlang`, a Python DSL that makes Jev feel like a smart `if` statement.

## How it works

You send a ticket as plain text. The service asks Jev three typed questions in a single batched API call:

- **Choice** — which team should handle this? (`billing`, `technical`, `account`, `human`)
- **Score** — how urgent is it? (`low`, `medium`, `high`, `critical`)
- **Noul** — is the customer upset? (yes/no probability)

If Jev's confidence on the team classification is below **0.6**, the ticket is routed to `human` for review instead of being auto-routed. This confidence-gated pattern is the whole point.

## Quick start

```bash
uv sync
cp .env.example .env   # then add your key
uv run python test_router.py
```

Run the API:

```bash
uv run --env-file .env uvicorn main:app --reload
```

Then open http://127.0.0.1:8000/docs for interactive docs.

## Example

```bash
curl -X POST http://127.0.0.1:8000/route \
  -H "Content-Type: application/json" \
  -d '{"text": "I was charged twice, please refund me!"}'
```

```json
{
  "team": "billing",
  "confidence": 1.0,
  "urgency": 1.96,
  "is_angry": true,
  "auto_routed": true,
  "reason": null
}
```

An ambiguous ticket:

```json
{
  "team": "human",
  "confidence": 0.49,
  "urgency": 0.82,
  "is_angry": true,
  "auto_routed": false,
  "reason": "Low confidence (0.49) on department classification. Sent to human review."
}
```

## Safety

- Jev returns **calibrated probabilities**, not certainties. Always keep a confidence threshold below which a human reviews the ticket.
- Never send customer PII in the ticket text — it goes to TypeSafe's API.
- This is a prototype. No caching, retry, or async handling is included.

## License

MIT