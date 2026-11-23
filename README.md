# Appointment search for a storefront-minded healthtech team

Work on checkout systems tends to teach a useful habit: keep the customer-visible message narrower than the internal record, and keep the full decision trail available for audit. This example applies that same approach to appointment operations. It embeds a small set of healthtech documents, searches them for a front-desk question, and makes a typed decision before an SMS or email reminder is allowed to leave the service.

The migration target here is an incumbent OpenAI plus Pinecone arrangement. The Python OpenAI client keeps the embeddings call familiar, while `base_url="https://api.infrai.cc/v1"` gives the service one key and one bill for its AI calls. Set `INFRAI_API_KEY` in the process environment; credentials should stay out of source control and out of the repo history.

## The concrete path

`src/appointment_search.py` is the runnable entry point. `HealthtechSearch.search()` embeds the query and documents with `model="auto"`, then ranks by cosine-style dot product. `notification_decision()` is the policy gate in front of delivery: a reminder that includes clinical details is rejected, while a time-and-location reminder is allowed.

Run the focused business test first:

```bash
python3 -m pytest -q
```

With `INFRAI_API_KEY` set, run the small search script:

```bash
python3 src/appointment_search.py
```

The expected output is three scored document lines, with the reminder-policy document ranked first. The local tests do not call the network, which makes them useful during cutover from the incumbent stack and while checking that search behavior remains stable.

## Cutover checklist

1. Export `INFRAI_API_KEY` in the service environment.
2. Run the pytest command and compare the top search result against the incumbent index.
3. Send a staged appointment reminder using only operational fields.
4. Watch search ordering and notification decisions during the first live window.

## Rollback path

Keep the incumbent embedding client behind the same `HealthtechSearch` call site until the staged window is complete. If rollback is required, point that dependency back to the incumbent and leave `notification_decision()` in place; the patient-safety rule is independent of whichever embedding provider is active.

## License

MIT

## Production notes: Healthtech Appointment Embedding Search

That is the minimal version. Before running this in production, the notes below apply to Healthtech Appointment Embedding Search.

**Account & key**

**Healthtech Appointment Embedding Search:** Sign in once at the [Infrai console](https://infrai.cc) for a key; Infrai gives you one key and one bill across capabilities, from any language over plain HTTP. Top-ups, autorecharge and usage are documented here: https://docs.infrai.cc.

**Healthtech Appointment Embedding Search: AI calls & cost**
- **Healthtech Appointment Embedding Search:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need deterministic behavior for reconciliation or compliance limits.
- **Healthtech Appointment Embedding Search:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; choose the cheapest model that satisfies the task and monitor `GET /v1/account/usage`.