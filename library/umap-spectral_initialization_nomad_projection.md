# UMAP, Spectral Initialization, and NOMAD Projection: Conversation Report

*Prepared October 19, 2026. This summarizes a spoken, transcribed conversation. Where the transcription garbled a term, the intended meaning is used.*

---

## 1. How UMAP Works

**UMAP** (Uniform Manifold Approximation and Projection) reduces high-dimensional data to two or three dimensions for visualization, while trying to preserve the data's underlying shape. It is popular in genomics and machine learning, largely because it is faster than t-SNE and tends to keep more global structure.

UMAP runs in two stages:

1. **Linear stage: spectral embedding.** UMAP builds a graph of the data, computes the graph Laplacian, and uses its eigenvectors to produce a structure-aware starting layout.
2. **Nonlinear stage: optimization.** Starting from that layout, gradient descent pulls and pushes points based on a fuzzy topological model of the data. This stage is nonlinear because the forces are nonlinear functions of distance.

### The graph Laplacian

- Built from two matrices: the **degree matrix** (connections per point) and the **adjacency matrix** (which points connect to which). Subtracting adjacency from degree gives the Laplacian.
- Its eigenvectors with the smallest eigenvalues act like the **vibration modes of a drum skin**. The smoothest modes give coordinates in which connected points sit close together.

### Where the "topological" part comes in

UMAP treats each point as the center of a small fuzzy neighborhood whose size adapts to local density. These overlapping neighborhoods are fused into a single fuzzy topological structure, using ideas from **algebraic topology** (simplicial complexes). The low-dimensional layout is then optimized to preserve that connectivity pattern.

### Why "algebraic" topology?

It uses algebraic tools (groups, vector spaces) to turn questions about shape into calculable ones, such as counting holes and connected pieces. Other branches of topology include point-set (general) topology, differential topology, and geometric topology.

---

## 2. Initialization Matters

| Finding | Source |
| --- | --- |
| UMAP's advantage over t-SNE in preserving global structure is largely explained by **initialization**, not the core algorithm. With the same informative start (Laplacian eigenmaps or PCA), t-SNE preserves global structure about as well as UMAP. | Kobak & Linderman (2021) |
| PCA initialization is a cheaper alternative to spectral initialization on very large datasets. umap-learn documents it as an option when spectral initialization is too slow or fails. | umap-learn docs |
| **NUMAP** uses a neural approach (Sep-SpectralNet) to approximate spectral embedding and generalize to new data points. | Ben-Ari et al., arXiv:2501.11305 (2025) |

Spectral embedding can also initialize t-SNE, which is exactly what the Kobak and Linderman comparison did.

---

## 3. NOMAD Projection

**Paper:** *NOMAD Projection* (Negative Or Mean Affinity Discrimination), Duderstadt, Nussbaum, and van der Maaten, arXiv:2505.15511, May 2025.

**Goal:** Visualize very large datasets (multi-million points) with t-SNE/UMAP-style maps, in a way that runs across **multiple GPUs** during training. The authors describe it as the first method of its kind.

**Mechanism (high level):**

- Builds on the contrastive-learning view of data mapping, in which attractive forces act on kNN-graph neighbors and repulsive forces act on negative pairs. The unifying framework (InfoNC-t-SNE) is from Damrich et al.
- NOMAD minimizes a surrogate loss meant to approximate an upper bound on the InfoNC-t-SNE loss. Only **cluster means** must be shared across GPUs for the repulsive forces, which cuts communication cost.
- Evaluated on ArXiv, ImageNet, PubMed, and a new Multilingual Wikipedia map described as the largest data map computed to date.
- Open-source implementation: `nomic-ai/nomad_projection` on GitHub.

**Critique:** An independent review on Pith says the practical method looks real and useful, but the paper's theoretical claim (that NOMAD approximates an upper bound on InfoNC-t-SNE) is not supported by the proof as written. In short, the engineering appears stronger than the theory. The paper is recent, and no formal citation count was found.

### Related methods

| Method | Relevance |
| --- | --- |
| PaCMAP / ParamRepulsor | Attractive/repulsive-force framing; ParamRepulsor adds single-GPU PyTorch support |
| NCVis | Noise-contrastive approach with parallel batching for speed |
| InfoNC-t-SNE / Neg-t-SNE | Theoretical framework NOMAD builds on |
| IVHD-CUDA | GPU implementation that handled a 20M-point dataset in one comparison |

In the searches run, none of these were described as supporting true multi-GPU distributed training, which supports NOMAD's novelty claim. That was a search-based impression, not an exhaustive survey.

---

## 4. About Laurens van der Maaten

- Co-created **t-SNE** (2008, with Geoffrey Hinton) and developed the Barnes-Hut approximation.
- **Meta:** Distinguished Research Scientist on the GenAI Llama team, listed as 2023-2025, and technical co-lead for Llama 3.
- **Anthropic:** Member of Technical Staff since **August 2025**. His CV describes the work as reinforcement learning and code post-training for Claude. No more specific detail was found publicly.
- **NOMAD affiliation:** The paper lists him under Nomic AI with a personal Gmail address, while his co-authors use Nomic addresses. The conversation concluded this is consistent with an advisory role. The advisor detail came from the user's own knowledge and was not verified by search.
- No evidence was found for an Intel role, which was raised during the conversation.

---

## 5. Corrections and Caveats

- A "Nomic AI" affiliation on a paper does not by itself confirm employment. An early statement implying employment was walked back.
- The CV timeline (Meta through 2025, Anthropic from August 2025) alongside a May 2025 paper under a different affiliation looked inconsistent at first. The advisor explanation resolves it, but the exact dates of his Meta departure were not found.
- The characterization of van der Maaten as an "engineer rather than a scientist" was a conversational opinion, not a finding.

## 6. Sources Consulted

- arXiv:2505.15511, *NOMAD Projection*, plus Pith and The Moonlight reviews
- arXiv:2501.11305, *Generalizable Spectral Embedding with an Application to UMAP*
- Kobak & Linderman, *Initialization is critical for preserving global data structure in both t-SNE and UMAP*
- umap-learn and uwot documentation
- van der Maaten's homepage, CV, and publications page
- PaCMAP and NCVis repositories and papers