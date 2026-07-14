# Day 1 Checklist

## Theory — 30 minutes

- [ ] Read `notes/day-01-theory.md`
- [ ] Write your own one-sentence definitions of latency, throughput, and concurrency
- [ ] Explain the difference between average latency and p99 latency
- [ ] Predict what will happen as concurrency increases

## Experiment — 55 minutes

- [ ] Create and activate the Python virtual environment
- [ ] Install dependencies
- [ ] Start the FastAPI service
- [ ] Test `/health`
- [ ] Test `/work?delay_ms=20`
- [ ] Run `benchmarks/load_test.py`
- [ ] Confirm that `benchmarks/results.csv` was created

## Analysis — 25 minutes

- [ ] Complete the results table in `notes/day-01-findings.md`
- [ ] Identify the point where latency begins increasing
- [ ] Identify the point where throughput stops improving significantly
- [ ] Write at least three observations
- [ ] Write one limitation of the experiment

## Showcase — 10 minutes

- [ ] Add the results table to `README.md`
- [ ] Commit with a meaningful message
- [ ] Push to GitHub
- [ ] Save a screenshot of the benchmark output

## Final Day 1 statement

Complete this sentence:

> Today I learned that increasing concurrency __________, but after __________ the system __________ because __________.
