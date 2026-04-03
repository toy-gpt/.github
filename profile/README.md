# Toy GPT

A family of small repositories that demonstrate how language models are trained and
how model behavior changes with architecture and data.

This organization is designed for illustration, experimentation, and structural understanding;
the repositories are not suitable for production use.
Several corpora are intentionally neutral, serving as negative controls to show
when additional context provides little or no benefit.

- [App](https://toy-gpt.github.io/toy-gpt-chat/) -interactive visualization of next-word (token) prediction in GPT-style language models.
- [App Repo](https://github.com/toy-gpt/toy-gpt-chat)

## Training Repositories

Each repository contains pre-trained artifacts for one model–corpus combination.
Two things vary independently: the model and the corpus.

### Choose One Model Per Training Repository

Select a model (how many previous tokens are used to predict the next one):

| Code | Model | Context window |
|---|---|---|
| 100 | Unigram | 0 tokens; predicts from overall frequency only |
| 200 | Bigram | 1 token; predicts from the immediately preceding token |
| 300 / 301 / 302 | Context-2 | 2 tokens; predicts from the previous two tokens |
| 400 | Context-3 | 3 tokens; predicts from the previous three tokens |
| 500 | Embeddings | learns vector representations of tokens |
| 600 | Attention | dynamically weights which prior tokens matter most |

### Chose One Corpus Per Training Repository

Select a corpus (the text the model is trained on):

| ID | File | Type | Signal |
|---|---|---|---|
| 000 | cat_dog.txt | Neutral | Low; adjacency carries little predictive value |
| 001 | animals.txt | Structured | Higher; natural language patterns |
| 010 | llm_glossary.txt | Domain | Technical NLP definitions |
| 020 | repo_tour.txt | Domain | Repository file and folder descriptions |
| 030 | analytics.txt | Domain | Technical micro-lessons |

### Training Respository Model-Corpus Matrix

| Repository | Model | Corpus |
|---|---|---|
| [train-100-unigram](https://github.com/toy-gpt/train-100-unigram) | Unigram | 000 cat_dog (**neutral**) |
| [train-200-bigram](https://github.com/toy-gpt/train-200-bigram) | Bigram | 000 cat_dog (**neutral**) |
| [train-300-context-2](https://github.com/toy-gpt/train-300-context-2) | Context-2 | 000 cat_dog (**neutral**) |
| [train-400-context-3](https://github.com/toy-gpt/train-400-context-3) | Context-3 | 000 cat_dog (**neutral**) |
| [train-100-unigram-animals](https://github.com/toy-gpt/train-100-unigram-animals) | Unigram | 001 animals (**structured**) |
| [train-200-bigram-animals](https://github.com/toy-gpt/train-200-bigram-animals) | Bigram | 001 animals (**structured**) |
| [train-300-context-2-animals](https://github.com/toy-gpt/train-300-context-2-animals) | Context-2 | 001 animals (**structured**) |
| [train-400-context-3-animals](https://github.com/toy-gpt/train-400-context-3-animals) | Context-3 | 001 animals (**structured**) |
| [train-301-context-2-llm-glossary](https://github.com/toy-gpt/train-301-context-2-llm-glossary) | Context-2 | 010 llm_glossary (**domain**) |
| [train-302-context-2-repo-tour](https://github.com/toy-gpt/train-302-context-2-repo-tour) | Context-2 | 020 repo_tour (**domain**) |
| [train-500-embeddings](https://github.com/toy-gpt/train-500-embeddings) | Embeddings | 030 analytics (**domain**) |
| [train-600-attention](https://github.com/toy-gpt/train-600-attention) | Attention | 030 analytics (**domain**) |

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
