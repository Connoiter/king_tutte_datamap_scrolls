# Datamapping papers

This directory is an index of the research papers behind King Tutte
pipelines: the Tutte Institute's own papers on UMAP, HDBSCAN and their
descendants, papers by close collaborators, and the foundational work
they build on.

Each entry says what the paper is and what you'll find in it, so a
reader (human or agent) can decide whether it's worth opening. Where
the license allows redistribution, a copy of the PDF is in
[`pdfs/`](pdfs/); otherwise the entry links to the canonical source.

## Licensing

This repo is meant to be used commercially, so everything stored in it
must be licensed for commercial redistribution. A paper is copied into
[`pdfs/`](pdfs/) only if it is under CC BY 4.0 (or CC0). Anything with a
non-commercial (NC) or no-derivatives (ND) term, arXiv's default
license, or publisher copyright is **never copied**: the entry gives its
identifier, where to get it and a short description, and a reader who
needs it downloads it from the source.

- **Copied (CC BY 4.0, commercial use allowed with attribution):** JOSS
  papers, `npj Computational Materials`, and arXiv preprints the authors
  released under CC BY. Each local copy is listed below with its
  authors, source and license, as CC BY requires. The PDFs are
  unmodified, and none of them carries third-party material under a
  separate license.
- **Linked only:** arXiv preprints under arXiv's default
  [non-exclusive distribution license](http://arxiv.org/licenses/nonexclusive-distrib/1.0/)
  (this includes the main UMAP and Accelerated HDBSCAN preprints), papers
  under CC BY-NC, CC BY-NC-ND or CC BY-ND, and publisher-copyright
  journal and conference versions.

A paper's license is separate from its code's. Several link-only papers
have BSD-licensed reference implementations, noted in their entries.

Licenses were checked on 2026-10-25 against the arXiv OAI-PMH metadata,
Crossref, bioRxiv and the PDFs' own notices. If you add a paper, check
its license the same way and record it here. When in doubt, link.

## Tutte Institute papers

### UMAP

- **UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction**
  - Leland McInnes, John Healy, James Melville · arXiv 2018 (v3, 2020) · [arXiv:1802.03426](https://arxiv.org/abs/1802.03426) · link only (arXiv license)
  - The main UMAP paper and the one to read for how and why it works.
    Section 2 builds the theory: data assumed uniform on a Riemannian
    manifold, local metrics glued into a fuzzy simplicial set (after
    Spivak), and a cross-entropy objective for the low-dimensional layout.
    Section 3 restates the same algorithm as weighted kNN graph
    construction plus force-directed layout, for readers who want to skip
    the category theory. Then the algorithm and hyperparameters
    (`n_neighbors`, `min_dist`, ...), comparisons with t-SNE, LargeVis,
    Laplacian eigenmaps and PCA, stability and scaling benchmarks, a
    candid Weaknesses section (spurious structure in noise, global
    structure owed partly to spectral initialization, small datasets) and
    an appendix deriving UMAP from t-SNE.
- **UMAP: Uniform Manifold Approximation and Projection** (JOSS software paper)
  - Leland McInnes, John Healy, Nathaniel Saul, Lukas Großberger · JOSS 3(29):861, 2018 · [doi:10.21105/joss.00861](https://doi.org/10.21105/joss.00861) · **local copy:** [pdfs/mcinnes_2018_umap_joss.pdf](pdfs/mcinnes_2018_umap_joss.pdf) (CC BY 4.0)
  - Two-page summary of the `umap-learn` package: scikit-learn API,
    supervised and semi-supervised modes, transforming new points. The
    citation the authors ask for when you use the software. Its Markdown
    source is in the submodule at `repos/umap/paper.md`.
- **Uniform manifold approximation and projection** (Nature Primer)
  - John Healy, Leland McInnes · Nature Reviews Methods Primers 4:82, 2024 · [doi:10.1038/s43586-024-00363-x](https://doi.org/10.1038/s43586-024-00363-x) · link only (publisher copyright)
  - Practitioner-oriented introduction: intuition for the algorithm,
    how to apply it well, and how to interpret (and not over-interpret)
    the results. Not read for this index (paywalled); summary from the
    published abstract.
- **Parametric UMAP embeddings for representation and semi-supervised learning**
  - Tim Sainburg, Leland McInnes, Timothy Q. Gentner · Neural Computation, 2021 · [arXiv:2009.12981](https://arxiv.org/abs/2009.12981) · [doi:10.1162/neco_a_01434](https://doi.org/10.1162/neco_a_01434) · link only
  - Replaces UMAP's per-point embedding optimization with a neural
    network, so new data can be embedded with a fast forward pass. Also
    uses the UMAP loss as a regularizer for autoencoders and
    semi-supervised classifiers. This is `umap.parametric_umap` in
    `umap-learn`.
- **Dimensionality reduction for visualizing single-cell data using UMAP**
  - Etienne Becht, Leland McInnes, John Healy, et al. · Nature Biotechnology 37(1), 2019 · [doi:10.1038/nbt.4314](https://doi.org/10.1038/nbt.4314) · bioRxiv preprint [10.1101/298430](https://doi.org/10.1101/298430) (CC BY-NC) · link only
  - The paper that made UMAP standard in single-cell biology:
    benchmarks UMAP against t-SNE and others on cytometry and
    transcriptomics data for speed, reproducibility and preserving
    cluster relationships.
- **Manifold learning of four-dimensional scanning transmission electron microscopy**
  - Xin Li, Ondrej E. Dyck, Mark P. Oxley, Andrew R. Lupini, Leland McInnes, John Healy, Stephen Jesse, Sergei V. Kalinin · npj Computational Materials 5:5, 2019 · [doi:10.1038/s41524-018-0139-y](https://doi.org/10.1038/s41524-018-0139-y) · **local copy:** [pdfs/li_2019_manifold_learning_4d_stem.pdf](pdfs/li_2019_manifold_learning_4d_stem.pdf) (CC BY 4.0)
  - An applied case study: UMAP and HDBSCAN on
    electron-microscopy diffraction patterns of graphene, picking out
    sublattices and single dopant atoms. Useful as a worked example of
    reduce-then-explore on non-text data.

### HDBSCAN and density clustering

- **hdbscan: Hierarchical density based clustering** (JOSS software paper)
  - Leland McInnes, John Healy, Steve Astels · JOSS 2(11):205, 2017 · [doi:10.21105/joss.00205](https://doi.org/10.21105/joss.00205) · **local copy:** [pdfs/mcinnes_2017_hdbscan_joss.pdf](pdfs/mcinnes_2017_hdbscan_joss.pdf) (CC BY 4.0)
  - Short summary of the `hdbscan` package: HDBSCAN* (DBSCAN over all
    epsilons, keeping the most stable clusters), robust single linkage,
    GLOSH outlier scores, prediction and soft clustering. The citation for
    the software. Markdown source in `repos/hdbscan/paper/paper.md`.
- **Accelerated Hierarchical Density Clustering**
  - Leland McInnes, John Healy · IEEE ICDM Workshops 2017, pp. 33–42 · [arXiv:1705.07321](https://arxiv.org/abs/1705.07321) · [doi:10.1109/ICDMW.2017.12](https://doi.org/10.1109/ICDMW.2017.12) · link only (arXiv license)
  - The algorithm paper behind `hdbscan`'s speed. Explains HDBSCAN*
    three ways (statistically, as density-level-set estimation;
    computationally, as mutual-reachability MST plus condensed tree;
    topologically, via persistence), then accelerates it with space-tree
    nearest neighbours and dual-tree Borůvka MST. Benchmarks against
    DBSCAN and other clustering algorithms. Background for
    `fast_hdbscan` too.
- **Persistent Multiscale Density-based Clustering** (PLSCAN)
  - Daniël Bot, Leland McInnes, Jan Aerts · arXiv 2025 · [arXiv:2512.16558](https://arxiv.org/abs/2512.16558) · link only (CC BY-NC-ND)
  - Replaces HDBSCAN*'s `min_cluster_size` with a persistence-based
    selection over all minimum cluster sizes, finding clusters that are
    stable across scales (equivalent to persistent homology on a new
    metric space). Reports better median ARI and less sensitivity to the
    neighbour count than HDBSCAN*. This is the cluster extraction used in
    **EVōC** and the PLSCAN mode of **fast_hdbscan**; the EVōC README asks
    you to cite this paper. Reference implementation:
    [JelmerBot/fast_plscan](https://github.com/JelmerBot/fast_plscan)
    (BSD-3-Clause, `pip install fast-plscan`), a submodule at
    `repos/fast_plscan`.
- **Topological Methods for Unsupervised Learning**
  - Leland McInnes · Geometric Science of Information (GSI 2019), LNCS 11712 · [doi:10.1007/978-3-030-26980-7_35](https://doi.org/10.1007/978-3-030-26980-7_35) · link only (publisher copyright)
  - Short overview of the topological view that ties UMAP and HDBSCAN
    together. Not read for this index; the talks
    [PyData Montreal 2019](../talks/by_tutte/mcinnes_at_pydata_montreal_2019.md)
    and [PyData LA 2019](../talks/by_tutte/mcinnes_at_pydata_la_2019.md)
    cover the same ground.

### Topological data analysis and surveys

- **Improving Mapper's Robustness by Varying Resolution According to Lens-Space Density**
  - Kaleb D. Ruscitti, Leland McInnes · arXiv 2024 · [arXiv:2410.03862](https://arxiv.org/abs/2410.03862) · **local copy:** [pdfs/ruscitti_2024_mapper_lens_space_density.pdf](pdfs/ruscitti_2024_mapper_lens_space_density.pdf) (CC BY 4.0)
  - Mapper with a cover whose resolution adapts to lens-space density,
    so results are less sensitive to the resolution parameter; proves
    convergence to the Reeb graph still holds. Motivated by embeddings of
    documents and images. Relevant if a datamap wants a graph skeleton as
    well as a scatter plot.
- **Low-dimensional embeddings of high-dimensional data**
  - Cyril de Bodt, Alex Diaz-Papkovich, …, Leland McInnes, …, Gal Mishne, Dmitry Kobak (21 authors) · arXiv 2025 · [arXiv:2508.15929](https://arxiv.org/abs/2508.15929) · **local copy:** [pdfs/de_bodt_2025_low_dimensional_embeddings.pdf](pdfs/de_bodt_2025_low_dimensional_embeddings.pdf) (CC BY 4.0)
  - A field-wide review by many of the main authors in the area. Covers
    what embeddings are for, a tour of method families (linear,
    distance-preserving, probabilistic, spectral, neighbour-embedding
    such as t-SNE and UMAP, parametric, supervised), example
    applications, **best-practice guidance**, and open problems in
    evaluation and interpretability. The best single starting point for
    context around UMAP.

## Collaborators and ecosystem

- **FLASC: a flare-sensitive clustering algorithm**
  - Daniël M. Bot, Jannes Peeters, Jori Liesenborgs, Jan Aerts · PeerJ Computer Science 11:e2792, 2025 · [doi:10.7717/peerj-cs.2792](https://doi.org/10.7717/peerj-cs.2792) · preprint [arXiv:2311.15887](https://arxiv.org/abs/2311.15887) · link only for now
  - Post-processing on HDBSCAN* that finds *branches* (flares) inside a
    cluster, such as the arms of a Y-shaped cluster, which ordinary
    density clustering can't separate. Two variants trade cost for noise
    robustness. This is the branch detection in `hdbscan` and
    `fast_hdbscan` and the standalone
    [vda-lab/pyflasc](https://github.com/vda-lab/pyflasc) (BSD-3-Clause).
    The PeerJ version is CC BY 4.0 and could be copied in; the download
    was blocked when this index was built. The arXiv preprint is CC BY-NC-ND.
- **Lens functions for exploring UMAP Projections with Domain Knowledge**
  - Daniël M. Bot, Jan Aerts · arXiv 2024 · [arXiv:2405.09204](https://arxiv.org/abs/2405.09204) · link only (CC BY-NC-ND)
  - Mapper-style lens functions for UMAP: filter the kNN graph by a
    chosen feature to get alternative views of the same data that bring
    out how that feature interacts with the structure. Code:
    [vda-lab/lensed_umap](https://github.com/vda-lab/lensed_umap) (BSD-3-Clause).
- **Assessing single-cell transcriptomic variability through density-preserving data visualization** (densMAP)
  - Ashwin Narayan, Bonnie Berger, Hyunghoon Cho · Nature Biotechnology 39, 2021 · [doi:10.1038/s41587-020-00801-7](https://doi.org/10.1038/s41587-020-00801-7) · bioRxiv [10.1101/2020.05.12.077776](https://doi.org/10.1101/2020.05.12.077776) · link only
  - Adds a term to the UMAP objective that keeps local density visible
    in the map, which plain UMAP flattens out. Available as
    `densmap=True` in `umap-learn`.
- **Initialization is critical for preserving global data structure in both t-SNE and UMAP**
  - Dmitry Kobak, George C. Linderman · Nature Biotechnology 39, 2021 · [doi:10.1038/s41587-020-00809-z](https://doi.org/10.1038/s41587-020-00809-z) · bioRxiv [10.1101/2019.12.19.877522](https://doi.org/10.1101/2019.12.19.877522) (CC BY-NC-ND) · link only
  - Shows that much of UMAP's global-structure advantage over t-SNE
    comes from its spectral initialization. The UMAP paper's Weaknesses
    section accepts the point. See also
    [library/umap-spectral_initialization_nomad_projection.md](../../library/umap-spectral_initialization_nomad_projection.md).

## Foundations

Older work the Tutte papers build on, all link only. Read these for
depth on a specific idea, not as a starting point.

- **Density-based clustering based on hierarchical density estimates** — Ricardo J. G. B. Campello, Davoud Moulavi, Jörg Sander · PAKDD 2013 · [doi:10.1007/978-3-642-37456-2_14](https://doi.org/10.1007/978-3-642-37456-2_14)
  - The original HDBSCAN* paper: mutual-reachability distance, the
    condensed cluster tree, and stability-based cluster selection.
- **Hierarchical density estimates for data clustering, visualization, and outlier detection** — Campello, Moulavi, Zimek, Sander · ACM TKDD 10(1), 2015 · [doi:10.1145/2733381](https://doi.org/10.1145/2733381)
  - Extended HDBSCAN* journal paper; adds the GLOSH outlier score.
- **A density-based algorithm for discovering clusters in large spatial databases with noise** (DBSCAN) — Martin Ester, Hans-Peter Kriegel, Jörg Sander, Xiaowei Xu · KDD 1996 · [AAAI library](https://cdn.aaai.org/KDD/1996/KDD96-037.pdf)
  - The fixed-epsilon density clustering that HDBSCAN* generalizes.
- **Rates of convergence for the cluster tree** — Kamalika Chaudhuri, Sanjoy Dasgupta · NeurIPS 2010 · [proceedings](https://papers.nips.cc/paper/4068-rates-of-convergence-for-the-cluster-tree)
  - Robust single linkage, the statistical grounding cited by `hdbscan`.
- **Efficient k-nearest neighbor graph construction for generic similarity measures** (NN-descent) — Wei Dong, Moses Charikar, Kai Li · WWW 2011 · [doi:10.1145/1963405.1963487](https://doi.org/10.1145/1963405.1963487)
  - The approximate kNN algorithm implemented by `pynndescent`, which
    UMAP uses for its neighbour graph.
- **Laplacian eigenmaps for dimensionality reduction and data representation** — Mikhail Belkin, Partha Niyogi · Neural Computation 15(6), 2003 · [doi:10.1162/089976603321780317](https://doi.org/10.1162/089976603321780317)
  - Spectral embedding; UMAP's theoretical starting point and its
    default initialization.
- **Visualizing data using t-SNE** — Laurens van der Maaten, Geoffrey Hinton · JMLR 9, 2008 · [jmlr.org](https://jmlr.org/papers/v9/vandermaaten08a.html)
  - The neighbour-embedding method UMAP is most often compared with.
- **Visualizing large-scale and high-dimensional data** (LargeVis) — Jian Tang, Jingzhou Liu, Ming Zhang, Qiaozhu Mei · WWW 2016 · [doi:10.1145/2872427.2883041](https://doi.org/10.1145/2872427.2883041)
  - Source of the negative-sampling SGD that UMAP's optimizer uses.
- **Metric realization of fuzzy simplicial sets** — David I. Spivak · self-published notes, 2009 · [PDF](https://dspivak.net/metric_realization090922.pdf)
  - The category-theory construction UMAP's fuzzy simplicial sets come
    from.
- **Colour displays for categorical images** — Chris Glasbey, Gerie van der Heijden, Vivian F. K. Toh, A. Gray · Color Research & Application 32(4), 2007 · [doi:10.1002/col.20327](https://doi.org/10.1002/col.20327)
  - The palette-generation method in the `glasbey` package, used for
    distinguishable cluster colours in datamaps.

## Tools without a paper

Several King Tutte tools have no paper (yet). For these, the README,
docs and the [talks](../talks/index.md) are the primary sources:

- **EVōC** ([TutteInstitute/evoc](https://github.com/TutteInstitute/evoc)): cluster extraction is PLSCAN, above.
- **fast_hdbscan** ([TutteInstitute/fast_hdbscan](https://github.com/TutteInstitute/fast_hdbscan)): implements Accelerated HDBSCAN*, FLASC and PLSCAN, above.
- **Toponymy** ([TutteInstitute/toponymy](https://github.com/TutteInstitute/toponymy)), **DataMapPlot** ([TutteInstitute/datamapplot](https://github.com/TutteInstitute/datamapplot)), **ThisNotThat** ([TutteInstitute/thisnotthat](https://github.com/TutteInstitute/thisnotthat)), **Vectorizers** ([TutteInstitute/vectorizers](https://github.com/TutteInstitute/vectorizers)), **PyNNDescent** ([lmcinnes/pynndescent](https://github.com/lmcinnes/pynndescent), algorithm from NN-descent above).
