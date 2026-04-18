# Human In The Loop (HITL) — LangGraph

A focused project demonstrating **Human In The Loop** patterns in LangGraph agentic AI systems. Includes a basic notebook walkthrough and two real-world chatbot scripts — one with HITL approval gates and one without.

---

## 📁 Repository Structure

```
.
├── basic_HITL.ipynb            # Step-by-step notebook: interrupt, approve, resume
├── chatbot_with_HITL.py        # Stock bot — purchase requires human approval
├── chatbot_without_HITL.py     # Stock bot — fully autonomous (no approval gate)
├── pyproject.toml              # Project dependencies (managed with uv)
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) installed on your machine
- An OpenAI API key
- An Alpha Vantage API key (for stock price tool)

### Installation

```bash
# Clone the repo
git clone <your-repo-url>
cd <repo-folder>

# Create virtual environment and install dependencies
uv sync
```

### Environment Setup

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
STOCK_PRICE_API_KEY=your_alphavantage_api_key
```

---

## 📓 Files

### `basic_HITL.ipynb`

A beginner-friendly notebook that introduces the core HITL pattern in LangGraph:

1. A `chat_node` calls `interrupt()` before answering — pausing execution and surfacing an approval prompt
2. The human reviews the question and responds `yes` or `no`
3. The workflow resumes via `Command(resume={...})` — either answering or returning `"Not approved."`

**Key concepts:** `interrupt()`, `Command(resume=...)`, `MemorySaver`, `thread_id`

---

### `chatbot_without_HITL.py`

A fully autonomous stock chatbot with two tools:

- **`get_stock_price(symbol)`** — fetches live stock data from Alpha Vantage
- **`dummy_purchase_stock(symbol, quantity)`** — simulates a stock purchase with no human gate

The LLM decides when to call tools and the workflow runs end-to-end without any interruption.

Run it:

```bash
uv run chatbot_without_HITL.py
```

---

### `chatbot_with_HITL.py`

The same stock chatbot, but with a **human approval gate on purchases**:

- **`get_stock_price(symbol)`** — runs autonomously (no gate)
- **`dummy_purchase_stock(symbol, quantity)`** — calls `interrupt()` inside the tool, pausing execution until a human types `yes` or `no`

If approved → returns a success confirmation  
If declined → returns a cancellation message

Run it:

```bash
uv run chatbot_with_HITL.py
```

**Example session:**
```
📈 Stock Bot with Tools (get_stock_price, purchase_stock)
You: Buy 10 shares of AAPL
HITL: Approve buying 10 shares of AAPL
Your decision: yes
AI: Purchase order placed for 10 shares of AAPL.
```

---

## 📦 Dependencies

Managed via `pyproject.toml` and `uv`:

| Package | Purpose |
|--------|---------|
| `langgraph` | Core workflow framework with HITL support |
| `langchain-openai` | GPT model integration |
| `langchain-community` | Community tools and integrations |
| `langchain` | Base LangChain library |
| `python-dotenv` | Environment variable loading |
