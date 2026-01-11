# WinCloud API Documentation

## Base URL
```
https://5.249.160.54:8443/api/v1
```

## Authentication

All API requests (except `/health` and `/auth`) require authentication via Bearer token.

### Headers
```
Authorization: Bearer <token>
```

## Endpoints

### 1. Health Check

Check if server is operational.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "WinCloud Server",
  "version": "1.0.0",
  "timestamp": "2026-01-11T12:00:00Z"
}
```

**Status Codes:**
- `200`: Server is healthy
- `503`: Server unavailable

---

### 2. Authentication

Obtain authentication token.

**Endpoint:** `POST /auth`

**Request Body:**
```json
{
  "user_id": "user-device-id",
  "client_version": "1.0.0"
}
```

**Response:**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": "user-device-id"
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid request

---

### 3. Upload Archive (Small Files)

Upload cloud portion of archive for small files (<5MB).

**Endpoint:** `POST /archives/upload`

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/octet-stream
```

**Request Body:**
Binary data (encrypted cloud portion)

**Response:**
```json
{
  "success": true,
  "archive_id": "550e8400-e29b-41d4-a716-446655440000",
  "file_ids": ["file-id-1", "file-id-2"]
}
```

**Status Codes:**
- `200`: Upload successful
- `401`: Unauthorized
- `413`: File too large
- `500`: Server error

---

### 4. Upload Archive (Large Files - Chunked)

Upload cloud portion in chunks for large files (>5MB).

**Endpoint:** `POST /archives/upload`

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/octet-stream
X-Chunk-Index: <chunk_number>
X-Total-Size: <total_bytes>
X-Chunk-Size: <chunk_bytes>
X-Upload-Id: <upload_id>  # After first chunk
```

**Request Body:**
Binary chunk data

**Response (first chunk):**
```json
{
  "success": true,
  "upload_id": "upload-session-id",
  "chunk_index": 0
}
```

**Response (subsequent chunks):**
```json
{
  "success": true,
  "upload_id": "upload-session-id",
  "chunk_index": 1
}
```

**Status Codes:**
- `200`: Chunk uploaded
- `401`: Unauthorized
- `500`: Server error

---

### 5. Finalize Chunked Upload

Complete chunked upload session.

**Endpoint:** `POST /archives/upload/finalize/<upload_id>`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "archive_id": "550e8400-e29b-41d4-a716-446655440000",
  "file_ids": ["file-id-1"]
}
```

**Status Codes:**
- `200`: Upload finalized
- `401`: Unauthorized
- `404`: Upload session not found
- `500`: Server error

---

### 6. Download Archive

Download cloud portion of archive.

**Endpoint:** `GET /archives/<archive_id>/download`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
Binary data stream (encrypted cloud portion)

**Status Codes:**
- `200`: Download successful
- `401`: Unauthorized
- `404`: Archive not found
- `500`: Server error

---

### 7. Delete Archive

Delete archive from server.

**Endpoint:** `DELETE /archives/<archive_id>`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true
}
```

**Status Codes:**
- `200`: Deleted successfully
- `401`: Unauthorized
- `404`: Archive not found
- `500`: Server error

---

## Error Response Format

All errors follow this format:

```json
{
  "error": "Error description message"
}
```

## Rate Limiting

- **Upload**: 10 GB per hour per user
- **Download**: 50 GB per hour per user
- **API calls**: 1000 requests per hour per user

Exceeded limits return `429 Too Many Requests`.

## Example Usage (Python)

### Authentication
```python
import requests

response = requests.post(
    'https://5.249.160.54:8443/api/v1/auth',
    json={'user_id': 'my-device-id', 'client_version': '1.0.0'},
    verify=False  # In production, use proper SSL
)

token = response.json()['token']
```

### Upload Small File
```python
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/octet-stream'
}

with open('cloud_data.bin', 'rb') as f:
    data = f.read()

response = requests.post(
    'https://5.249.160.54:8443/api/v1/archives/upload',
    headers=headers,
    data=data,
    verify=False
)

archive_id = response.json()['archive_id']
```

### Upload Large File (Chunked)
```python
chunk_size = 5 * 1024 * 1024  # 5MB
upload_id = None

with open('large_cloud_data.bin', 'rb') as f:
    chunk_index = 0
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/octet-stream',
            'X-Chunk-Index': str(chunk_index),
            'X-Total-Size': str(total_size),
            'X-Chunk-Size': str(len(chunk))
        }
        
        if upload_id:
            headers['X-Upload-Id'] = upload_id
        
        response = requests.post(
            'https://5.249.160.54:8443/api/v1/archives/upload',
            headers=headers,
            data=chunk,
            verify=False
        )
        
        upload_id = response.json()['upload_id']
        chunk_index += 1

# Finalize upload
response = requests.post(
    f'https://5.249.160.54:8443/api/v1/archives/upload/finalize/{upload_id}',
    headers={'Authorization': f'Bearer {token}'},
    verify=False
)

archive_id = response.json()['archive_id']
```

### Download Archive
```python
headers = {'Authorization': f'Bearer {token}'}

response = requests.get(
    f'https://5.249.160.54:8443/api/v1/archives/{archive_id}/download',
    headers=headers,
    stream=True,
    verify=False
)

with open('downloaded_data.bin', 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            f.write(chunk)
```

### Delete Archive
```python
headers = {'Authorization': f'Bearer {token}'}

response = requests.delete(
    f'https://5.249.160.54:8443/api/v1/archives/{archive_id}',
    headers=headers,
    verify=False
)

print(response.json())  # {'success': True}
```

## Security Notes

1. **HTTPS**: Always use HTTPS in production
2. **SSL Certificates**: Install proper SSL certificates
3. **Token Storage**: Store tokens securely
4. **Token Expiration**: Implement token refresh mechanism
5. **Input Validation**: All inputs are validated server-side
6. **Rate Limiting**: Respect rate limits to avoid blocking

## Support

For API issues or questions:
- Check server logs: `journalctl -u wincloud -f`
- Review error messages in responses
- Verify authentication token validity
