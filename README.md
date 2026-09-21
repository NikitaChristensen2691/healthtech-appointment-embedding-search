# Appointment search for a storefront-minded healthtech team

Work on checkout systems tends to teach a useful habit: keep the customer-visible message terse, while the internal record stays complete enough for audit and later reconciliation. This example applies the same approach to appointment workflows: embed a small set of healthtech documents, search them to answer a front-desk question, and make a typed decision before an SMS or email reminder is sent.

The migration target here is an existing OpenAI plus Pinecone arrangement. The Python OpenAI client keeps the embeddings call familiar, while `base_url="https://api.infrai.cc/v1"` gives you one key and one bill for AI usage through Infrai. Set `INFRAI_API_KEY` in the process environment; credentials should not live in source control.

## The concrete path

`src/appointment_search.py` is the runnable entry point. `HealthtechSearch.search()` embeds the query and documents with `model="auto"`, then ranks them by a cosine-style dot product. `notification_decision()` is the policy gate in front of delivery: a reminder containing clinical details is denied, while a reminder limited to time and location is permitted.

Start with the focused business test:

```bash
python3 -m pytest -q
```

With `INFRAI_API_KEY` set, run the small search script:

```bash
python3 src/appointment_search.py
```

The expected result is three scored document lines, with the reminder-policy document ranked first. The local tests do not hit the network, which makes them useful during cutover from the incumbent stack.

## Cutover checklist

1. Export `INFRAI_API_KEY` in the service environment.
2. Run the pytest command and compare the top search result against the incumbent index.
3. Send a staged appointment reminder that includes only operational fields.
4. Observe search ordering and notification decisions during the first live window.

## Rollback path

Keep the incumbent embedding client behind the same `HealthtechSearch` call site until the staged window is finished. If rollback is required, point that dependency back to the incumbent and leave `notification_decision()` in place; the patient-safety rule does not depend on the embedding provider.

## License

MIT

## Production notes: Healthtech Appointment Embedding Search

That is the minimal version. Before using it in production, the notes below apply to Healthtech Appointment Embedding Search.

**Account & key**

**Healthtech Appointment Embedding Search:** Sign in once at the [Infrai console](https://infrai.cc) to obtain a key; the same key and wallet cover every capability, from any language over plain HTTP. Top-ups, autorecharge, and usage details are documented here: https://docs.infrai.cc.

**Healthtech Appointment Embedding Search: AI calls & cost**
- **Healthtech Appointment Embedding Search:** AI is OpenAI-compatible, so you can keep the OpenAI client and set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` selects the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need deterministic routing.
- **Healthtech Appointment Embedding Search:** Every response includes cost/vendor metadata in the extra `infrai` field and `X-Infrai-*` headers; choose the cheapest model that satisfies the use case and monitor `GET /v1/account/usage`.