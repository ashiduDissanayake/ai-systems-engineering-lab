# AI Systems Engineering Lab

A practical learning repository focused on backend performance, distributed systems,
AI infrastructure, model serving, reliability, and production engineering.

## Current Track

### Week 1 — HTTP Services, Concurrency, and Latency

The first experiment measures how a small FastAPI service behaves as concurrency increases.

## Repository Structure

```text
app/                Application code
benchmarks/         Benchmark scripts and result files
notes/              Technical notes and explanations
weekly-reviews/     Weekly learning summaries
roadmap.md          Learning plan
```

## Day 1 Experiment

### Question

How does increasing concurrency affect the latency and throughput of a basic HTTP service?

### Run the service

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Run the benchmark

Open another terminal:

```bash
source .venv/bin/activate
python benchmarks/load_test.py
```

The script tests several concurrency levels and saves the output to:

```text
benchmarks/results.csv
```

## Metrics

- Average latency
- p50 latency
- p95 latency
- p99 latency
- Requests per second
- Successful and failed requests

## Day 1 Deliverables

- [ ] Run the API
- [ ] Run the benchmark
- [ ] Commit `benchmarks/results.csv`
- [ ] Complete `notes/day-01-findings.md`
- [ ] Add one chart or results table to this README
- [ ] Push the repository to GitHub
