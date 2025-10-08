# Mirai Agent API Documentation

## Overview

The Mirai Agent API provides a RESTful interface for interacting with the autonomous AI agent. All API endpoints follow a standardized response format and include rate limiting for security.

**Base URL:** `http://localhost:8000`  
**API Version:** 1.0.0

## Standardized Response Format

All API endpoints (except static files) return responses in the following format:

### Success Response
```json
{
  "status": "success",
  "timestamp": "2024-10-08T12:34:56.789Z",
  "data": {
    // Response data here
  }
}
```

### Error Response
```json
{
  "status": "error",
  "timestamp": "2024-10-08T12:34:56.789Z",
  "error": "Error message description"
}
```

## Rate Limiting

- **Limit:** 60 requests per minute per IP address
- **Response Code:** 429 (Too Many Requests) when limit exceeded
- **Static files** (.css, .js, .html, /) are excluded from rate limiting

### Rate Limit Error Response
```json
{
  "status": "error",
  "timestamp": "2024-10-08T12:34:56.789Z",
  "error": "Rate limit exceeded. Try again later."
}
```

## Endpoints

### System Status

#### GET /api
Get basic API information.

**Response:**
```json
{
  "status": "success",
  "timestamp": "2024-10-08T12:34:56.789Z",
  "data": {
    "service": "Mirai Agent API",
    "version": "1.0.0"
  }
}
```

#### GET /health
Check system health and AI usage statistics.

**Response:**
```json
{
  "status": "success",
  "timestamp": "2024-10-08T12:34:56.789Z",
  "data": {
    "status": "healthy",
    "agent_running": true,
    "trader_running": true,
    "ai_usage": {
      "total_tokens": 12450,
      "requests_count": 127
    }
  }
}
```

**Fields:**
- `agent_running` (boolean): Whether the autonomous agent is running
- `trader_running` (boolean): Whether the trading module is active
- `ai_usage.total_tokens` (integer): Total AI tokens consumed
- `ai_usage.requests_count` (integer): Total AI API requests made

### Agent Statistics

#### GET /agent/stats
Get agent performance statistics.

**Response:**
```json
{
  "status": "success",
  "timestamp": "2024-10-08T12:34:56.789Z",
  "data": {
    "tasks_completed": 127,
    "learning_sessions": 45,
    "tasks_total": 150,
    "tasks_pending": 23
  }
}
```

**Fields:**
- `tasks_completed` (integer): Number of completed tasks
- `learning_sessions` (integer): Number of learning sessions conducted
- `tasks_total` (integer): Total number of tasks
- `tasks_pending` (integer): Number of pending tasks

### Trading Statistics

#### GET /trader/stats
Get trading module statistics.

**Response:**
```json
{
  "status": "success",
  "timestamp": "2024-10-08T12:34:56.789Z",
  "data": {
    "balance": 10000.50,
    "positions": 5
  }
}
```

**Fields:**
- `balance` (number): Current account balance
- `positions` (integer): Number of open positions

### Combined Statistics

#### GET /stats
Get combined system statistics.

**Response:**
```json
{
  "status": "ok",
  "agent": {
    "tasks_completed": 127,
    "learning_sessions": 45,
    "tasks_total": 150,
    "tasks_pending": 23
  },
  "trading": {
    "balance": 10000.50,
    "positions": 5
  }
}
```

## AI Engine Features

The AI engine includes the following improvements:

### Timeout Handling
- **Default Timeout:** 60 seconds for all AI API calls
- **Graceful Degradation:** Returns error message instead of hanging on timeout

### Retry Logic
- **Max Retries:** 3 attempts
- **Retry Delay:** Exponential backoff (2s, 4s, 6s)
- **Smart Retry:** Doesn't retry on authentication/configuration errors

### Token Tracking
- Automatically tracks token usage for OpenAI API calls
- Available via `/health` endpoint
- Helps monitor and control API costs

## Error Handling

The API implements comprehensive error handling:

1. **Timeout Errors:** Returns error after 60 seconds with retry attempts
2. **Authentication Errors:** Immediate failure without retries
3. **Rate Limit Errors:** 429 status code with retry-after guidance
4. **Server Errors:** 500 status code with error details

## Best Practices

### Rate Limiting
- Implement exponential backoff when receiving 429 responses
- Cache responses when possible to reduce API calls
- Use WebSocket connections for real-time updates instead of polling

### Error Handling
- Always check the `status` field in responses
- Log `timestamp` for debugging
- Handle both `data` and `error` fields appropriately

### Token Usage
- Monitor `ai_usage.total_tokens` to track costs
- Set budgets and alerts based on token consumption
- Use shorter prompts when possible to reduce token usage

## Examples

### Python Example
```python
import requests

# Basic health check
response = requests.get('http://localhost:8000/health')
data = response.json()

if data['status'] == 'success':
    print(f"System is healthy!")
    print(f"Tokens used: {data['data']['ai_usage']['total_tokens']}")
else:
    print(f"Error: {data['error']}")

# Get agent statistics
response = requests.get('http://localhost:8000/agent/stats')
data = response.json()

if data['status'] == 'success':
    stats = data['data']
    print(f"Tasks completed: {stats['tasks_completed']}")
    print(f"Tasks pending: {stats['tasks_pending']}")
```

### cURL Examples
```bash
# Health check
curl http://localhost:8000/health

# Agent statistics
curl http://localhost:8000/agent/stats

# Combined stats
curl http://localhost:8000/stats
```

### JavaScript Example
```javascript
// Using fetch API
async function getHealth() {
  const response = await fetch('http://localhost:8000/health');
  const data = await response.json();
  
  if (data.status === 'success') {
    console.log('System is healthy!');
    console.log('AI Usage:', data.data.ai_usage);
  } else {
    console.error('Error:', data.error);
  }
}

// With error handling
async function getStats() {
  try {
    const response = await fetch('http://localhost:8000/stats');
    if (response.status === 429) {
      console.log('Rate limited, waiting...');
      await new Promise(resolve => setTimeout(resolve, 60000));
      return getStats(); // Retry after delay
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Network error:', error);
    return null;
  }
}
```

## Migration Guide

If you're migrating from the old API format, here are the key changes:

### Old Format
```json
{
  "status": "healthy",
  "agent_running": true
}
```

### New Format
```json
{
  "status": "success",
  "timestamp": "2024-10-08T12:34:56.789Z",
  "data": {
    "status": "healthy",
    "agent_running": true,
    "ai_usage": {...}
  }
}
```

### Migration Checklist
1. ✅ Update response parsing to look for `data` field
2. ✅ Check `status` field for "success" or "error"
3. ✅ Handle new `timestamp` field for logging
4. ✅ Implement rate limiting handling (429 responses)
5. ✅ Update monitoring to track `ai_usage` metrics

## Support

For issues or questions:
- Check logs in `data/logs/` directory
- Review the timestamp in error responses for debugging
- Monitor rate limiting to ensure you're within limits
- Track token usage to optimize costs

## Changelog

### Version 1.0.0 (2024-10-08)
- ✅ Implemented standardized API response format
- ✅ Added rate limiting (60 req/min per IP)
- ✅ Improved AI engine with timeout handling and retry logic
- ✅ Added token usage tracking
- ✅ Fixed datetime deprecation warnings
- ✅ Enhanced error handling with proper status codes
