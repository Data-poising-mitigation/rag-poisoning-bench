# rag-poisoning-bench

a 'test suite' for data poisoning success/ defense success

### Per-test folder

| Path                     | Who edits | Purpose                                                                                                                                                                        |
| ------------------------ | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `config.json`            | You       | Test definition: which corpus files, optional `top_k`, `description`. Pipeline/retrieval options (e.g. multi-embedding) go here so test2 can differ from test1 only by config. |
| `queries/queries.json`   | You       | List of queries: `{ "id": "q1", "text": "..." }`.                                                                                                                              |
| `state/corpus_used.json` | Runner    | Generated. `hasUploaded`, and for each document `corpus_path` → `document_id`. Do not edit by hand.                                                                            |
| `runs/<timestamp>/`      | Runner    | One folder per run. `results.json`, `metrics.json`, `summary.md`.                                                                                                              |

### config.json (authored)

- **corpus_paths** (required): list of paths relative to repo root, e.g. `["corpus/policy.txt", "corpus/poison_policy.txt"]`.
- **top_k** (optional): retrieval top_k (default e.g. 5).
- **description** (optional): short note for humans and for `tests.md`.
- Any future options (e.g. **multi_embedding**: true for test2) live here so test1 vs test2 is a config diff.

### state/corpus_used.json (generated)

- **hasUploaded**: true after the runner has uploaded all documents (Option A).
- **documents**: list of `{ "corpus_path": "...", "document_id": "uuid" }` in the same order as `config.json`’s `corpus_paths`.
- **seeded_at** (optional): ISO timestamp of last upload.

### test-cases/tests.md

One short line per test so you can see at a glance what each test does (e.g. “test1: baseline poison, no defense”; “test2: same corpus, multi-embedding retrieval”). Human-readable and useful for the write-up.
