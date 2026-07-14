# Day 1 Theory — Latency, Throughput, and Concurrency

## Today's learning goal

Understand how a service behaves when more requests arrive at the same time.

The main question is:

> How does increasing concurrency affect throughput and tail latency?

## 1. Latency

Latency is the time taken to complete one request.

Example:

```text
Request sent → server processes it → response received
```

If this takes 40 milliseconds, the request latency is 40 ms.

Important latency values:

- **Average latency** — average time across all requests
- **p50 latency** — 50% of requests completed within this time
- **p95 latency** — 95% completed within this time
- **p99 latency** — 99% completed within this time

p95 and p99 reveal slow requests that the average can hide.

## 2. Throughput

Throughput is how much work the system completes in a period of time.

For an HTTP service, it is usually measured as:

```text
requests completed per second
```

A service completing 200 requests per second has higher throughput than one completing 50 requests per second.

High throughput does not automatically mean low latency.

## 3. Concurrency

Concurrency is the number of requests that are in progress at the same time.

Example:

- Concurrency 1: one request at a time
- Concurrency 10: up to ten requests in progress
- Concurrency 100: up to one hundred requests in progress

Concurrency is not the same as parallelism.

- **Concurrency** means several tasks are active and making progress.
- **Parallelism** means several tasks are executing at the same instant, usually on different CPU cores.

## 4. Blocking and non-blocking I/O

Blocking work prevents the current worker from doing other work until the operation finishes.

Examples:

- A blocking database call
- Reading a large file synchronously
- Calling `time.sleep()`

Non-blocking I/O allows the worker to pause one waiting task and continue with another.

Examples:

- `await asyncio.sleep()`
- An asynchronous HTTP request
- An asynchronous database driver

The current `/work` endpoint uses non-blocking waiting:

```python
await asyncio.sleep(delay_ms / 1000)
```

## 5. Why increasing concurrency helps

When requests spend time waiting for I/O, the service can work on other requests during that waiting time.

Therefore, throughput may increase when concurrency increases.

## 6. Why too much concurrency hurts

Concurrency is not free.

High concurrency can introduce:

- Queueing
- Connection contention
- Memory usage
- Scheduling overhead
- Context switching
- Timeouts
- Resource saturation

At some point, adding more concurrent requests may increase latency without meaningfully increasing throughput.

## 7. Queueing intuition

Suppose a service can effectively handle 20 requests at once.

If 100 requests arrive together:

- Some begin immediately.
- The rest wait.
- Waiting time becomes part of total latency.
- p95 and p99 increase sharply.

This is why production systems use rate limits, queues, autoscaling, and backpressure.

## 8. Connection to AI systems

The same behaviour appears in AI inference services.

When many inference requests arrive:

- Requests may wait for the GPU.
- The runtime may batch them.
- GPU memory may become full.
- Throughput may increase while individual latency becomes worse.
- Some requests may time out.

Understanding basic HTTP concurrency is the first step toward understanding model-serving systems.

## What you should be able to explain today

After completing the experiment, answer these without memorising definitions:

1. What is the difference between latency and throughput?
2. Why is p99 useful?
3. Why can concurrency improve throughput?
4. Why can excessive concurrency increase latency?
5. What is the difference between blocking and non-blocking work?
6. How does this relate to AI model serving?
