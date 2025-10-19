# King Tutte Scrolls

This repo is a how-to manual for making
[datamaps](https://www.youtube.com/watch?v=r8dWZX8IGw8&ab_channel=PyData)
of collections of embedding vectors.

<img src="./images/king_tutte_funerary_mask.png" width="100%" />

Large collections of neural embedding vectors are proliferating
rapidly. For example, at its core every vector database and RAG
knowledge base consists of such a collection. Datamaps make for great
web-tech based, interactive visulizations of embedding vector
collections. 

These "scrolls" (read: code, documentation, recorded talks, and
associated commentary) are an agglomeration of permissively licensed
repos and web content related to building datamaps, the bulk of which
originates out of the **Tutte** Institute of Canada -- hence the nod
to them in this repo's name.

The **goal** of this King Tutte Scrolls repo is to **create a one-stop
shop** for any developer (human and/or
[agent](https://simonwillison.net/2025/Sep/18/agents/)) wishing to
bang out datamaps of any "AI-ready data," that is, data with embedding
vectors.

Note that this repo can built into an **Claud Skill** for use by
agents. See [connoiter.com for pre-built
distros](https://connoiter.com/king_tutte_scrolls/distros/).


## Use cases

A bitological coder (read: "**AI coding agent**" or "coder daemon") can immediately make
use of this repo simply by telling the LLM to check out
[connoiter.com](https://connoiter.com). It will find, via the llms.txt
file on connoiter.com, the content of this repo, the King Tutte
Scrolls, transcribed to context window-friendly markdown and Python,
packaged as [a Claud
Skill](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).
(More on how you can self-deploy the same later in this document, in [the Deploying section](#deploying).)

A **solo human coder** can use the King Tutte Scrolls for
self-study. The content (code and docs previously written by others)
has been curated and commentary in included. The included King Tutte
Scrolls Jupyter Book is probably the place to start.

For **conference workshop contexts**, there are Jupyter notebooks
amongst these scrolls which are designed to run on Colab. Most of the
code has been previously written elsewhere -- including most of the Jupyter
notebooks -- but they have been tweaked as needed to ensure they all
work out of the box on Google's Colab service.

For workshops, a Colab-based set-up is:
- free
- including optional free GPUs, which King Tutte tools know how to use
- involved no set-up hassles beyond asking for a GPU runtime
- is scalable for large workshops

So, a workshop can quickly get started, and after the workshop is
completed, attendees can continue to hack on their own versions of the
notebooks they were working on at the workshop, which should help
diffuse these datamap innovations.

## Tut juxt Tutte

“Humor can be dissected, as a frog can, but the thing dies in the process” ― E.B. White

### The Tutte Institute

<figure>
    <a href="https://newmarkethistory.org.uk/newmarket-people/personalities/professor-william-tutte/">
        <img src="./images/tutte_at_cambridge.jpg" width="30%" align="right" alt="Tutte's Cambridge undergraduate portrait" />
    </a>
    <figcapture>Tutte at Cambridge</figcapture>
</figure>

[The Tutte Institute for Mathematics and Computing
(TIMC)](https://www.cse-cst.gc.ca/en/mission/research-cse/tutte-institute-mathematics-computing)
is a Canadian government funded academic institute, named after
[W. T. Tutte](https://en.wikipedia.org/wiki/W._T._Tutte). Bill Tutte
was an English and Canadian code breaker and mathematician. During
WW2, he was working alongside the likes of Alan Turing cracking the
Nazi's encrypted comms at Bletchley Park.

Notably, Tutte worked to crack the German High Command communications
code known as “Fish,” an even tougher nut to crack than the more
famous Enigma machine. Feel free to nerd out on his tools such as the Δ
and double-delta methods, wherein the cracker digitally simulates
mechanical crypto wheel based comm boxes, an en silico picking of
physical locks by tuning into (via XOR filters on bit streams) their
encrypted digital broadcasts. Bonus points, the Allies never captured
a Lorenz machine during the war. Unlike with Enigma, where they had
the machine including its code books, which proved quite handy while
reverse enginering the machine, otherwise all you'd have to go on is
the ciphertext to work it all out. :(

### King Tut

In ancient Egypt during the late Eighteenth Dynasty, King Tutankhamun,
also known as **King Tut** (not Tutte), was an Egyptian pharaoh who
ruled around 1332 to 1323 BC. King Tut has been immortalized in song
[(on YouTube)](https://www.youtube.com/embed/k-fc3UrLRLQ?autoplay=1&mute=1&loop=0).

## Repo structure

- External as-is repos as submodules
  - KTS makes no changes to the content of the repos
  - Goal is simply to one-stop-shop agglomerate relevant info
- For Colab-based workshops, some Jupyter notebooks from the
  (permissively licensed) external as-is repos have been copied and
  modified, and packaged as a Jupyter Book (whose Jupyter notebooks
  just so happen to run out-of-the-box on Colab). In an ideal world,
  there would be only on version, but in Colab Google has done some
  "embrace and extend" work that requires separate variants of the
  notebooks. C'est la vie.

## King Tutte Scrolls

Back to modern times: some of the folks at TIMC are high dimensional
mathemeticians, a type of scientist not a type of
engineer. Nonetheless, they have come down out of their icy ivory
tower and have engaged in the grubby practice of software
*engieneering* for the purpose of diffusing their applied *science*
innovations. This involved the development of scalable algorithms (for
example, basic King Tutte pipelines cane currently handle on the order
of 10s of millions of high dimensional data points).

For example, tools such as UMAP and HDBSCAN which implement provably
correct algorithms (unlike, say, LLMs). After all the numbers have
been crunched, a report in order.  DataMapPlot is Python code the
generate web widgets to interactively navigate datamaps (generated by
UMAP, t-SNE, etc.)

So, "King Tutte Scrolls" is just an unique, memorable name for a repos
which is essentially just a datamap toolbox, full of tools that mostly
come out of the Tutte Instutute. Packaged with lots of documentation
and sample code, it's a single git repo that a software writer can
read in order to learn how to make and tune datamaps.

# Deploying

Or equivalently use
[gitinjest](https://github.com/coderamp-labs/gitingest); connoiter.com
simply hosts the pre-rendered results of running this repo through
gitinjest.


One convenient deploy option is run individual Jupyter notebooks on
Colab. See [the list of Colab-ready notebooks]() in this repo.

Bonus, it would be trivial to run this repo through
[gitingest](https://github.com/coderamp-labs/gitingest) and feed the
markdown-based output to a transformer-based LLM programming
assistant, a.k.a. ka code daemon. 

With this repo in its context window, it should be able to crank out
Python code to make datamaps, which are webUI(HTML&JS&c.) widgets that
run live inside notebooks (Jupyter and Marimo) or can be exported as
    stand-along static file HTML web-apps that can be run in browsers
later.

For convenience, a pre-built run of this repo through gitingest is
available at:

https://connoiter.com/king_tutte_scrolls

Or just tell your coding LLM to check out
[connoiter.com](https://connoiter.com), and it will find the King Tutte Scrolls via the
site's llms.txt file.

## King Tutte pipelines

Multiple Tutte Institute repos|tools|softwares can be chained together in a regular datamap pipeline.

<a href="https://connoiter.com/blog/data_map_pipeline/">
<img src="images/data_map_pipeline.jpeg" width="80%" />
</a>

These repos can be configured together to implement –– amongst other
things –– what is herein called a King Tutte pipeline. In this repo,
these King Tutte pipeline-variants (code and Jypyter notebooks) use
multiple repositories of code out of the Tutte Institute, such as UMAP,
HDBSCAN, EVoC, DataMapPlot, Toponymy, Glasbly, and Vectorizers. Ergo
the name King Tutte.


