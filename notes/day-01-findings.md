# Day 1 — HTTP Load Testing Findings

## Question

How does increasing concurrency affect the latency and throughput of a basic HTTP service?

## Environment

- Computer:
- Operating system:
- Python version:
- FastAPI version:
- Uvicorn workers:
- Endpoint:
- Simulated delay:
- Total requests per test:

## Results

Paste the important values from `benchmarks/results.csv`.

| Concurrency | Requests/sec | Average latency | p95 latency | p99 latency | Failures |
|---:|---:|---:|---:|---:|---:|
| 1 | | | | | |
| 5 | | | | | |
| 10 | | | | | |
| 25 | | | | | |
| 50 | | | | | |
| 100 | | | | | |

## Observations

1.
2.
3.

## Where performance started degrading

Write the concurrency level at which latency began increasing significantly.

## Explanation

Explain why throughput and latency changed as concurrency increased.

Consider:

- The service has a fixed simulated delay.
- Requests are asynchronous.
- The server and client have connection limits.
- High concurrency introduces queueing and scheduling overhead.

## Limitations

- The work is simulated using `asyncio.sleep`.
- This is not CPU-intensive work.
- The test runs locally.
- Network latency is minimal.
- Only one Uvicorn worker is used.

## Next Experiment

Replace the non-blocking `asyncio.sleep` with blocking work and compare the results.
