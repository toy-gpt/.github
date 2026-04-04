# Toy GPT

> Learn How Large Language Models (LLM) Work

_The project is designed for illustration, experimentation, and structural understanding;
and not for production use._

## Modern GPT Chat Agents

Modern GPT Chat Agents are built on a simple objective:
given some text, **predict the next word**.

Repeated many times, this produces full conversations.

What we recognize as a GPT-type chatbot is simply
the result of making useful **next-word predictions** over and over,
using the context of text seen so far.

## How They Work

During training, an LLM is exposed to large amounts of human language
and learns **patterns** in how words follow one another.

When generating a response, the model works step by step,
using the words so far (its context window) to choose the next one.

**At each step**, it makes a **best guess** based on what it has learned.

It doesn't plan a sentence in advance;
the result **emerges one word at a time**.

## Toy GPT Exploration (2D Matrix)

These examples illustrate how changing:

1. the **context window** (e.g., 0, 1, 2, or 3 prior words) and
2. the **training text** affects next-token predictions

The results determine how well the conversation goes.

We include a **neutral** cat-dog corpora to illustrate cases where
additional context (tracking prior words) intentionally provides no benefit.

## LLM Training Costs

Most computational effort occurs during training, not use.
Running a trained model in conversation is relatively inexpensive;
training it requires processing large amounts of human-written text
and repeatedly adjusting the model to improve predictions.
Large systems may take days or weeks of computation across many machines.
The pre-trained models in Toy GPT reflect the same process at a much smaller scale.

## Combinatorial Explosion

It takes space to track each word in context
(even if the context is only 2 or 3 words prior).
The context-3 model stores one weight row per **unique 3-token context**,
so the weight matrix grows as vocab³:

| Corpus       | Vocab size  | Model     | Weight matrix rows | Approx. size |
| ------------ | ----------- | --------- | ------------------ | ------------ |
| cat/dog      | ~20 tokens  | context-3 | 20³ = 8,000        | ~3 MB        |
| llm_glossary | ~119 tokens | context-2 | 119² = 14,161      | ~10 MB       |
| llm_glossary | ~119 tokens | context-3 | 119³ = 1,685,159   | **~428 MB**  |

Our simple Context-3 model (without embeddings) grew to **428 MB**,
consisting mostly of zeros (because relatively few combinations appear in context).

This rapid growth makes direct counting approaches impractical
and motivates more compact representations for capturing similarities across words.

## GPT: The Transformer Breakthrough

Modern GPT-style models use the transformer architecture from
[**"Attention Is All You Need"**](https://arxiv.org/abs/1706.03762)<sup>1</sup>.
They use:

- **embeddings** (numeric representations of words) and
- **attention** (selecting which prior words matter most)

to represent tokens and weigh
**which prior words are most relevant for prediction**.

These mechanisms produce much more **compact** output.
Attention is included in Toy GPT for completeness,
but its full effect is hard to demonstrate on such tiny corpora.

<sup>1</sup> Vaswani et al. (2017), _Attention Is All You Need_.

## App

Interactive visualization of next-word (token) prediction in GPT-style language models.

- [App](https://toy-gpt.github.io/toy-gpt-chat/) -interactive visualization of next-word (token) prediction in GPT-style language models.
- [App Repo](https://github.com/toy-gpt/toy-gpt-chat)

## Training Repositories

Each repository contains pre-trained artifacts for one model–corpus combination.
Two things vary independently: the model and the corpus.

### Choose One Model Per Training Repository

Select a model (how many previous tokens are used to predict the next one):

| Code            | Model      | Context window                                         |
| --------------- | ---------- | ------------------------------------------------------ |
| 100             | Unigram    | 0 tokens; predicts from overall frequency only         |
| 200 / 201       | Bigram     | 1 token; predicts from the immediately preceding token |
| 300 / 301 / 302 | Context-2  | 2 tokens; predicts from the previous two tokens        |
| 400             | Context-3  | 3 tokens; predicts from the previous three tokens      |
| 500             | Embeddings | learns vector representations of tokens                |
| 600             | Attention  | dynamically weights which prior tokens matter most     |

### Chose One Corpus Per Training Repository

Select a corpus (the text the model is trained on):

| ID  | File             | Type       | Signal                                         |
| --- | ---------------- | ---------- | ---------------------------------------------- |
| 000 | cat_dog.txt      | Neutral    | Low; adjacency carries little predictive value |
| 001 | animals.txt      | Structured | Higher; natural language patterns              |
| 010 | llm_glossary.txt | Domain     | Technical NLP definitions                      |
| 020 | repo_tour.txt    | Domain     | Repository file and folder descriptions        |
| 030 | analytics.txt    | Domain     | Technical micro-lessons                        |

### Training Repository Model-Corpus Matrix

| Repository                                                                                      | Model      | Corpus                                                                                                                                       | Context |
| ----------------------------------------------------------------------------------------------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| [train-100-unigram](https://github.com/toy-gpt/train-100-unigram)                               | Unigram    | [000 cat_dog](https://raw.githubusercontent.com/toy-gpt/train-100-unigram/refs/heads/main/corpus/000_cat_dog.txt) (**neutral**)              | 0       |
| [train-200-bigram](https://github.com/toy-gpt/train-200-bigram)                                 | Bigram     | [000 cat_dog](https://raw.githubusercontent.com/toy-gpt/train-200-bigram/refs/heads/main/corpus/000_cat_dog.txt) (**neutral**)               | 1       |
| [train-300-context-2](https://github.com/toy-gpt/train-300-context-2)                           | Context-2  | [000 cat_dog](https://raw.githubusercontent.com/toy-gpt/train-300-context-2/refs/heads/main/corpus/000_cat_dog.txt) (**neutral**)            | 2       |
| [train-400-context-3](https://github.com/toy-gpt/train-400-context-3)                           | Context-3  | [000 cat_dog](https://raw.githubusercontent.com/toy-gpt/train-400-context-3/refs/heads/main/corpus/000_cat_dog.txt) (**neutral**)            | 3       |
| [train-100-unigram-animals](https://github.com/toy-gpt/train-100-unigram-animals)               | Unigram    | [001 animals](https://raw.githubusercontent.com/toy-gpt/train-100-unigram-animals/refs/heads/main/corpus/001_animals.txt) (**structured**)   | 0       |
| [train-200-bigram-animals](https://github.com/toy-gpt/train-200-bigram-animals)                 | Bigram     | [001 animals](https://raw.githubusercontent.com/toy-gpt/train-200-bigram-animals/refs/heads/main/corpus/001_animals.txt) (**structured**)    | 1       |
| [train-300-context-2-animals](https://github.com/toy-gpt/train-300-context-2-animals)           | Context-2  | [001 animals](https://raw.githubusercontent.com/toy-gpt/train-300-context-2-animals/refs/heads/main/corpus/001_animals.txt) (**structured**) | 2       |
| [train-400-context-3-animals](https://github.com/toy-gpt/train-400-context-3-animals)           | Context-3  | [001 animals](https://raw.githubusercontent.com/toy-gpt/train-400-context-3-animals/refs/heads/main/corpus/001_animals.txt) (**structured**) | 3       |
| [train-201-bigram-llm-glossary](https://github.com/toy-gpt/train-201-bigram-llm-glossary)       | Bigram     | 010 llm_glossary (**domain**)                                                                                                                | 1       |
| [train-301-context-2-llm-glossary](https://github.com/toy-gpt/train-301-context-2-llm-glossary) | Context-2  | 010 llm_glossary (**domain**)                                                                                                                | 2       |
| [train-401-context-3-llm-glossary](https://github.com/toy-gpt/train-401-context-3-llm-glossary) | Context-3  | 010 llm_glossary (**domain**) ⚠️                                                                                                             | 3       |
| [train-302-context-2-repo-tour](https://github.com/toy-gpt/train-302-context-2-repo-tour)       | Context-2  | 020 repo_tour (**domain**)                                                                                                                   | 2       |
| [train-500-embeddings](https://github.com/toy-gpt/train-500-embeddings)                         | Embeddings | 030 analytics (**domain**)                                                                                                                   | 2       |
| [train-600-attention](https://github.com/toy-gpt/train-600-attention)                           | Attention  | 030 analytics (**domain**) ℹ️                                                                                                                | 2       |
| [train-600-attention-3](https://github.com/toy-gpt/train-600-attention-3)                       | Attention  | 030 analytics (**domain**) ℹ️                                                                                                                | 3       |

⚠️ Too large to commit (428 MB of mostly zeros).
ℹ️ Attention requires scale to produce meaningful position weighting.

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
