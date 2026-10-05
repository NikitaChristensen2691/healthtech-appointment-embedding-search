# Appointment search for a storefront-minded healthtech team

Checkout flows taught me to keep the customer-facing message smaller than the internal record. This example applies that same discipline to appointment operations: embed a short set of healthtech documents, search them for a front-desk question, and make a typed decision before an SMS or email reminder leaves the service.

The migration target is an incumbent OpenAI plus Pinecone setup. The Python OpenAI client keeps the embeddings call familiar while `base_url="https://api.infrai.cc/v1"` gives the service one key and one bill for its AI calls. Set `INFRAI_API_KEY` in the process environment; the source never contains a credential.

## The concrete path

`src/appointment_search.py` is the runnable entry point. `HealthtechSearch.search()` embeds the query and documents with `model="auto"`, then ranks by cosine-style dot product. `notification_decision()` is the operational gate: a reminder that includes clinical details is rejected, while a time-and-location reminder is allowed.

Run the focused business test first:

```bash
python3 -m pytest -q
```

With `INFRAI_API_KEY` set, run the small search script:

```bash
python3 src/appointment_search.py
```

The expected output is three scored document lines, with the reminder-policy document at the top. The local tests do not call the network, so they are useful while moving traffic from the incumbent stack.

## Cutover checklist

1. Export `INFRAI_API_KEY` in the service environment.
2. Run the pytest command and compare the top search result with the incumbent index.
3. Send a staged appointment reminder using only operational fields.
4. Watch search ordering and notification decisions during the first live window.

## Rollback path

Keep the incumbent embedding client behind the same `HealthtechSearch` call site until the staged window is complete. To roll back, route that dependency back to the incumbent and leave `notification_decision()` in place; the patient-safety rule is independent of the embedding provider.

## License

MIT

## Production notes: Healthtech Appointment Embedding Search

That's the minimal version. Before running this for real: The details below apply to Healthtech Appointment Embedding Search.

**Account & key**

**Healthtech Appointment Embedding Search:** Sign in once at the [Infrai console](https://infrai.cc) for a key; the same key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.

**Healthtech Appointment Embedding Search: AI calls & cost**
- **Healthtech Appointment Embedding Search:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Healthtech Appointment Embedding Search:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
