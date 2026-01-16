# Toy GPT

A family of small repositories that demonstrate how language models are trained and
how model behavior changes with architecture and data.

This organization is designed for illustration, experimentation, and structural
understanding - they are not robust and not suitable for production use.

## Matrix (Model – Corpus)

| Training repo                                                           | Corpus trained         | Notes                                      |
| ----------------------------------------------------------------------- | ---------------------- | ------------------------------------------ |
| [`train-100-unigram`](https://github.com/toy-gpt/train-100-unigram)     | `000_cat_dog.txt`      | neutral baseline, single-token model       |
| [`train-200-bigram`](https://github.com/toy-gpt/train-200-bigram)       | `000_cat_dog.txt`      | conditional next-token with 2-token stats  |
| [`train-300-context-2`](https://github.com/toy-gpt/train-300-context-2) | `000_cat_dog.txt`      | canonical context-2 neutral baseline       |
| `train-301-context-2-llm-glossary`                                      | `010_llm_glossary.txt` | same architecture as 300, different corpus |
| `train-302-context-2-repo-tour`                                         | `020_repo_tour.txt`    | same architecture as 300, different corpus |
| [`train-400-context-3`](https://github.com/toy-gpt/train-400-context-3) | `000_cat_dog.txt`      | canonical context-3 neutral baseline       |
| `train-500-embeddings`                                                  | `030_analytics.txt`    | canonical embeddings demo corpus           |
| `train-600-attention`                                                   | `030_analytics.txt`    | same corpus as 500 to isolate effect       |
| `train-100-unigram-animals`                                             | `001_animals.txt`      | baseline, single-token model               |
| `train-200-bigram-animals`                                              | `001_animals.txt`      | conditional next-token with 2-token stats  |
| `train-300-context-2-animals`                                           | `001_animals.txt`      | canonical context-2 baseline               |
| `train-400-context-3-animals`                                           | `001_animals.txt`      | canonical context-3 baseline               |

## Grid View

| Corpus ID          | Description                | 100 unigram | 200 bigram | 300 context-2 | 400 context-3 | 500 embeddings | 600 attention |
| ------------------ | -------------------------- | ----------: | ---------: | ------------: | ------------: | -------------: | ------------: |
| `000_cat_dog`      | tiny neutral corpus        |           X |          X |             X |             X |                |               |
| `001_animals`      | tiny structured corpus     |           X |          X |             X |             X |                |               |
| `010_llm_glossary` | language model definitions |             |            |     X (`301`) |               |                |               |
| `020_repo_tour`    | repo files and folders     |             |            |     X (`302`) |               |                |               |
| `030_analytics`    | technical micro-lessons    |             |            |               |               |              X |             X |

Legend:
`X` indicates a completed training run with committed artifacts.
Blank cells indicate combinations intentionally not explored.

## Model numbering

Model codes increase with architectural complexity:

- **100/unigram**: predicts the next token using only overall frequency, without considering surrounding context.
- **200/bigram**: predicts the next token conditioned on the immediately preceding token.
- **300/context-2**: predicts the next token using the previous two tokens as context.
- **400/context-3**: predicts the next token using the previous three tokens as context.
- **500/embeddings**: learns numeric vector representations of tokens so related tokens occupy nearby locations in a learned space.
- **600/attention**: dynamically weights which prior tokens matter most when predicting the next token, rather than treating all context equally.

See the paper [**Attention Is All You Need**](https://arxiv.org/abs/1706.03762) for background on attention-based models.

## Corpus numbering

Corpus IDs are three digits and follow a project-wide standard:

- **000–009**: canonical baselines maintained by the project
- **010–049**: instructor-curated teaching corpora
- **100–799**: additional contributions, allocated in non-overlapping blocks

Each corpus file is named `NNN_slug.txt`.
The corpus ID and slug are recorded in `SE_MANIFEST.toml`.

See [CORPUS_NUMBERING.md](./CORPUS_NUMBERING.md) for full details.

## Terms

- **baseline corpus**
  A reference corpus used to compare model behavior across architectures.

- **neutral corpus**
  A corpus where additional context adds little predictive power under n-gram modles; the learned
  geometry is relatively flat with few gradients.

- **unigram**
  A model that conditions on a single token (`uni` = one).

- **bigram**
  A model that conditions on two tokens (`bi` = two).

## Purpose

This organization emphasizes clarity, reproducibility, and explicit boundaries
between models, data, and claims.
