# rag-poisoning-bench

a 'test suite' for data poisoning success/ defense success

# Test case folder

A test case is a single folder (e.g. `test1/`, `test2/`) with this layout:

```
test1/
  config.json              # Authored. Lists corpus paths and optional options (e.g. top_k). Defines test.
  queries/
    queries.json           # Authored. Queries to run: list of { "id", "text" }.
  state/
    corpus_used.json       # Generated. hasUploaded and, per document, corpus_path → document_id. Do not edit.
  runs/
    <timestamp>/           # Generated. One folder per run; holds results.json, metrics.json, summary.md.
```

| Item                       | Authored / Generated | Purpose                                                  |
| -------------------------- | -------------------- | -------------------------------------------------------- |
| **config.json**            | Authored             | Which corpus files and any test options.                 |
| **queries/queries.json**   | Authored             | The queries (id + text) for this test.                   |
| **state/corpus_used.json** | Generated            | Upload state and corpus_path → document_id. Do not edit. |
| **runs/<timestamp>/**      | Generated            | One run's outputs: results, metrics, summary.            |
