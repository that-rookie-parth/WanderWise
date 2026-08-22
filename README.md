# WanderWise

WanderWise is a retrieval-augmented travel itinerary prototype for five Indian
states. It combines a Streamlit preference form with tourism context stored in
Pinecone and an OpenAI model that returns a personalized itinerary in Markdown.

## What it does

- Collects destination, activity, transport, trip-length, and free-text
  preferences through Streamlit.
- Retrieves relevant tourism context with GIST embeddings and Pinecone.
- Uses OpenAI GPT-3.5 Turbo to turn the preferences and retrieved context into
  an itinerary.
- Includes supporting experiments for collecting tourism pages, converting
  scraped text to PDF, and loading documents into the vector index.

The current interface covers Tamil Nadu, Uttar Pradesh, Andhra Pradesh,
Karnataka, and Maharashtra, with itineraries of up to seven days.

## Architecture

```mermaid
flowchart LR
    sources[Tourism PDFs and<br/>Incredible India pages] --> collect[Python and TypeScript<br/>collection scripts]
    collect --> prepare[Text extraction and<br/>PDF preparation]
    prepare --> embed[GIST embedding model<br/>768 dimensions]
    embed --> index[(Pinecone index)]

    user[Traveler preferences] --> ui[Streamlit form]
    ui --> prompt[Itinerary prompt builder]
    prompt --> retrieve[Similarity retrieval<br/>top 10, score ≥ 0.7]
    index --> retrieve
    retrieve --> llm[OpenAI GPT-3.5 Turbo<br/>context-grounded generation]
    llm --> result[Streamlit Markdown<br/>itinerary view]

    classDef entry fill:#0969DA,stroke:#79C0FF,color:#FFFFFF,stroke-width:2px
    classDef process fill:#334155,stroke:#CBD5E1,color:#FFFFFF,stroke-width:2px
    classDef action fill:#6D28D9,stroke:#C4B5FD,color:#FFFFFF,stroke-width:2px
    classDef service fill:#166534,stroke:#86EFAC,color:#FFFFFF,stroke-width:2px
    classDef output fill:#9F1239,stroke:#FDA4AF,color:#FFFFFF,stroke-width:2px

    class user,sources entry
    class collect,prepare,prompt,retrieve process
    class embed action
    class index,llm service
    class ui,result output
```

## Stack

- Python, Streamlit
- LangChain and LangChain community integrations
- OpenAI GPT-3.5 Turbo
- Pinecone vector search
- `avsolatorio/GIST-Embedding-v0` through Hugging Face sentence transformers
- Beautiful Soup, Selenium, and TypeScript/axios data-collection experiments

## Local setup

This repository preserves a May 2024 prototype. Its original Python environment
was not captured, and the LangChain APIs used here have since changed. Treat the
steps below as an environment outline rather than a reproducible current build.

```bash
git clone https://github.com/parthkulshreshtha/WanderWise.git
cd WanderWise

python -m venv .venv
source .venv/bin/activate

cp .env.example .env
```

Before running the project, create and test a compatible dependency set for
Streamlit, LangChain, OpenAI, Pinecone, sentence transformers, and the optional
scraping tools. Do not deploy the unreviewed historical dependency versions.

Configure the following values in `.env`:

```dotenv
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=your_pinecone_environment
PINECONE_INDEX_NAME=your_pinecone_index
```

The application expects an existing Pinecone index populated with 768-dimension
GIST embeddings. Start the interface with:

```bash
streamlit run main.py
```

### Data preparation

The repository contains separate experimental paths for collecting and loading
tourism context:

- `index.ts`, `async_queue.ts`, and `utils.ts` crawl selected Incredible India
  pages into a local `content/` directory.
- `selenium_web_scraping.py` demonstrates browser-based collection.
- `get_data.py` converts collected HTML text into PDFs under `output/`.
- `upload_data.py` chunks PDFs, creates GIST embeddings, and rebuilds the
  configured Pinecone index.
- `langchain_webscraping.ipynb` records an earlier web-scraping experiment; it
  is not part of the Streamlit runtime.

> **Caution:** `upload_data.py` deletes and recreates the configured Pinecone
> index. Use a disposable development index and review the script before
> running it.

## Repository structure

```text
.
├── main.py                       # Streamlit interface
├── llm.py                        # prompt, retrieval, and generation chain
├── db_utils.py                   # embeddings and Pinecone connection
├── upload_data.py                # PDF ingestion and index rebuild
├── get_data.py                   # scraped-text to PDF conversion
├── selenium_web_scraping.py      # browser-based collection experiment
├── index.ts / async_queue.ts     # TypeScript collection experiment
├── langchain_webscraping.ipynb   # exploratory notebook
└── data/                         # reference tourism publications
```

## Limitations

- This is a historical prototype, not a booking engine or production service.
- Destinations are limited to five states and trip length is capped at seven
  days.
- Results depend on the contents of a separately provisioned Pinecone index and
  are not grounded in live prices, schedules, availability, weather, or safety
  information.
- The original Python dependency versions were not recorded. The LangChain-era
  APIs should be migrated, locked, security-audited, and retested before active
  development.
- There is no automated test suite, deployment configuration, authentication,
  or persistent per-user conversation history.

## Data and attribution

The PDFs under `data/` are reference publications from the Government of India,
Ministry of Tourism. They remain subject to their source terms and are not
covered by this repository's MIT software license. Scraping references and
original learning resources are recorded in [`instruction.md`](instruction.md).

## License

The original software in this repository is available under the [MIT License](LICENSE).
