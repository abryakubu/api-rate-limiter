from src.rate_limiter import RateLimiter

# Create a rate limiter with a limit of 5 requests per 60 seconds.
limiter = RateLimiter(limit=5, window_seconds=60)

# Identify the client making requests.
client_id = "client_A"

# Send six requests.
for request_number in range(1, 7):
    result = limiter.allow_request(client_id)

    print(f"Request {request_number}")
    print(f"Allowed: {result['allowed']}")
    print(f"Requests remaining: {result['remaining']}")
    print("--------------------")