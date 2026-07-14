from __future__ import annotations

import asyncio
import csv
import statistics
import time
from dataclasses import dataclass
from pathlib import Path

import httpx

BASE_URL = "http://127.0.0.1:8000"
ENDPOINT = "/work?delay_ms=20"
CONCURRENCY_LEVELS = [1, 5, 10, 25, 50, 100]
TOTAL_REQUESTS = 500
TIMEOUT_SECONDS = 10.0
OUTPUT_FILE = Path(__file__).with_name("results.csv")


@dataclass
class BenchmarkResult:
    concurrency: int
    total_requests: int
    successful_requests: int
    failed_requests: int
    duration_seconds: float
    requests_per_second: float
    average_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float


def percentile(values: list[float], percentile_value: float) -> float:
    if not values:
        return 0.0

    ordered = sorted(values)
    index = (len(ordered) - 1) * percentile_value
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    weight = index - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


async def make_request(
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
) -> tuple[bool, float]:
    async with semaphore:
        started = time.perf_counter()
        try:
            response = await client.get(ENDPOINT)
            response.raise_for_status()
            success = True
        except (httpx.HTTPError, TimeoutError):
            success = False

        latency_ms = (time.perf_counter() - started) * 1000
        return success, latency_ms


async def run_benchmark(concurrency: int) -> BenchmarkResult:
    semaphore = asyncio.Semaphore(concurrency)
    limits = httpx.Limits(
        max_connections=concurrency,
        max_keepalive_connections=concurrency,
    )

    async with httpx.AsyncClient(
        base_url=BASE_URL,
        timeout=TIMEOUT_SECONDS,
        limits=limits,
    ) as client:
        started = time.perf_counter()
        tasks = [
            make_request(client, semaphore)
            for _ in range(TOTAL_REQUESTS)
        ]
        results = await asyncio.gather(*tasks)
        duration = time.perf_counter() - started

    successful_latencies = [
        latency for success, latency in results if success
    ]
    failed_requests = sum(1 for success, _ in results if not success)
    successful_requests = len(successful_latencies)

    return BenchmarkResult(
        concurrency=concurrency,
        total_requests=TOTAL_REQUESTS,
        successful_requests=successful_requests,
        failed_requests=failed_requests,
        duration_seconds=duration,
        requests_per_second=successful_requests / duration if duration else 0.0,
        average_latency_ms=(
            statistics.mean(successful_latencies)
            if successful_latencies
            else 0.0
        ),
        p50_latency_ms=percentile(successful_latencies, 0.50),
        p95_latency_ms=percentile(successful_latencies, 0.95),
        p99_latency_ms=percentile(successful_latencies, 0.99),
    )


def save_results(results: list[BenchmarkResult]) -> None:
    fieldnames = list(BenchmarkResult.__dataclass_fields__.keys())

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result.__dict__)


async def main() -> None:
    print(f"Target: {BASE_URL}{ENDPOINT}")
    print(f"Requests per test: {TOTAL_REQUESTS}\n")

    all_results: list[BenchmarkResult] = []

    for concurrency in CONCURRENCY_LEVELS:
        result = await run_benchmark(concurrency)
        all_results.append(result)

        print(
            f"Concurrency={result.concurrency:>3} | "
            f"RPS={result.requests_per_second:>8.2f} | "
            f"Avg={result.average_latency_ms:>8.2f} ms | "
            f"p95={result.p95_latency_ms:>8.2f} ms | "
            f"p99={result.p99_latency_ms:>8.2f} ms | "
            f"Failed={result.failed_requests}"
        )

    save_results(all_results)
    print(f"\nSaved results to {OUTPUT_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
