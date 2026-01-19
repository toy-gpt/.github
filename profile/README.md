# Toy GPT

A family of small repositories that demonstrate how language models are trained and
how model behavior changes with architecture and data.

This organization is designed for illustration, experimentation, and structural understanding;
the repositories are not suitable for production use.
Several corpora are intentionally neutral, serving as negative controls to show
when additional context provides little or no benefit.

- [App](https://toy-gpt.github.io/toy-gpt-chat/) -interactive visualization of next-word (token) prediction in GPT-style language models.
- [App Repo](https://github.com/toy-gpt/toy-gpt-chat)

## Matrix (Model – Corpus)

| Training repo                                                                           | Corpus trained         | Notes (corpus type)                                    |
| --------------------------------------------------------------------------------------- | ---------------------- | ------------------------------------------------------ |
| [`train-100-unigram`](https://github.com/toy-gpt/train-100-unigram)                     | `000_cat_dog.txt`      | single-token model (neutral)                           |
| [`train-200-bigram`](https://github.com/toy-gpt/train-200-bigram)                       | `000_cat_dog.txt`      | conditional next-token with 2-token stats (neutral)    |
| [`train-300-context-2`](https://github.com/toy-gpt/train-300-context-2)                 | `000_cat_dog.txt`      | canonical context-2 (neutral)                          |
| [`train-400-context-3`](https://github.com/toy-gpt/train-400-context-3)                 | `000_cat_dog.txt`      | canonical context-3 (neutral)                          |
| [`train-100-unigram-animals`](https://github.com/toy-gpt/train-100-unigram-animals)     | `001_animals.txt`      | single-token model (structured)                        |
| [`train-200-bigram-animals`](https://github.com/toy-gpt/train-200-bigram-animals)       | `001_animals.txt`      | conditional next-token with 2-token stats (structured) |
| [`train-300-context-2-animals`](https://github.com/toy-gpt/train-300-context-2-animals) | `001_animals.txt`      | canonical context-2 (structured)                       |
| [`train-400-context-3-animals`](https://github.com/toy-gpt/train-400-context-3-animals) | `001_animals.txt`      | canonical context-3 (structured)                       |
| [`train-301-context-2-llm-glossary`](https://github.com/toy-gpt/train-301-context-2-llm-glossary) | `010_llm_glossary.txt` | same architecture as 300, different corpus             |
| `train-302-context-2-repo-tour`                                                         | `020_repo_tour.txt`    | same architecture as 300, different corpus             |
| `train-500-embeddings`                                                                  | `030_analytics.txt`    | canonical embeddings demo corpus                       |
| `train-600-attention`                                                                   | `030_analytics.txt`    | same corpus as 500 to isolate effect                   |

## Grid View

| Corpus ID          | Description                                | 100 unigram | 200 bigram | 300 context-2 | 400 context-3 | 500 embeddings | 600 attention |
| ------------------ | ------------------------------------------ | ----------: | ---------: | ------------: | ------------: | -------------: | ------------: |
| `000_cat_dog`      | small neutral (low-signal) corpus          |           X |          X |             X |             X |                |               |
| `001_animals`      | small structured (proximity-signal) corpus |           X |          X |             X |             X |                |               |
| `010_llm_glossary` | language model definitions                 |             |            |     X (`301`) |               |                |               |
| `020_repo_tour`    | repo files and folders                     |             |            |     X (`302`) |               |                |               |
| `030_analytics`    | technical micro-lessons                    |             |            |               |               |              X |             X |

Legend:
`X` indicates a completed training run with committed artifacts.
Blank cells indicate combinations intentionally not explored.

## Model numbering

Model codes increase with architectural complexity:

- **100/unigram**: predicts the next token using only overall frequency, without considering surrounding context.
- **200/bigram**: predicts the next token conditioned on the immediately preceding token.
- **300/context-2**: predicts the next token using the previous two tokens as context. Architecturally equivalent to a bigram model, but implemented in a way that generalizes to longer contexts.
- **400/context-3**: predicts the next token using the previous three tokens as context.
- **500/embeddings**: learns numeric vector representations of tokens so related tokens occupy nearby locations in a learned space.
- **600/attention**: dynamically weights which prior tokens matter most when predicting the next token, rather than treating all context equally.

See the paper [**Attention Is All You Need**](https://arxiv.org/abs/1706.03762) for background on attention-based models.

## Corpus numbering

Corpus IDs are three digits and follow a project-wide standard:

- **000–009**: canonical reference corpora
- **010–049**: curated explanatory corpora for focused demonstrations
- **100–799**: additional contributions

Each corpus file is named `NNN_slug.txt`.
The corpus ID and slug are recorded in `SE_MANIFEST.toml`.

## Terms

- **neutral corpus**
  A corpus deliberately constructed so that adjacency carries little or no predictive signal.
  Increasing context length (bigram, context-2, context-3) should provide minimal benefit.
  Used as a negative control.

- **structured corpus**
  A corpus where adjacency or proximity carries meaningful predictive signal
  (e.g., attributes, phrases, or semantic groupings).
  Increasing context length should measurably improve predictions.

- **unigram**
  A model that conditions on a single token (`uni` = one).

- **bigram**
  A model that conditions on two tokens (`bi` = two).

## Purpose

This organization emphasizes clarity, reproducibility, and explicit boundaries
between models, data, corpora, and claims.
