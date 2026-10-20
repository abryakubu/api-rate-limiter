# API Rate Limiter

## Overview

This project implements a simple API rate limiter using Python.

It uses the Fixed Window algorithm to control how many requests a client can make within a specified period.

## Configuration

- **Request limit:** 5 requests
- **Time window:** 60 seconds
- **Algorithm:** Fixed Window
- **Client tracking:** Each client has an independent request limit.

## Project Structure

```text
api-rate-limiter/
├── demo.py
├── README.md
├── src/
│   └── rate_limiter.py
└── tests/
    └── test_rate_limiter.py
