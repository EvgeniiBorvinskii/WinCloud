# WinCloud Architecture Documentation

## System Overview

WinCloud is a hybrid cloud archiver that splits compressed files into local and cloud components for optimal storage efficiency.

## Architecture Components

### 1. Client Application (Windows Desktop)

```
┌─────────────────────────────────────────┐
│         WinCloud Client GUI              │
│         (PyQt6 Interface)                │
└────────────┬────────────────────────────┘
             │
             ├──────────┐
             │          │
    ┌────────▼──┐  ┌───▼──────────┐
    │Compression│  │   Network     │
    │  Engine   │  │    Client     │
    └────┬──────┘  └───┬───────────┘
         │             │
    ┌────▼─────────────▼───┐
    │  Common Utilities    │
    │  - Crypto            │
    │  - File Splitter     │
    │  - Logger            │
    │  - Config            │
    └──────────────────────┘
```

### 2. Server Infrastructure

```
┌─────────────────────────────────────────┐
│    Server: 5.249.160.54:8443            │
│    Location: /srv/WinCloud               │
└────────────┬────────────────────────────┘
             │
    ┌────────▼──────────┐
    │   Flask REST API   │
    │   - Auth           │
    │   - Upload         │
    │   - Download       │
    │   - Health Check   │
    └────────┬───────────┘
             │
    ┌────────▼───────────┐
    │  SQLite Database   │
    │  - Archives Meta   │
    │  - Upload Sessions │
    └────────────────────┘
             │
    ┌────────▼───────────┐
    │  File Storage      │
    │  /srv/WinCloud/    │
    │    storage/        │
    └────────────────────┘
```

## Data Flow

### Archive Creation Flow

```
1. User selects files
   ↓
2. GUI → Compression Engine
   ↓
3. Compress files (LZMA2 + Zstandard)
   ↓
4. Split: 10% local, 90% cloud
   ↓
5. Encrypt cloud part (AES-256-GCM)
   ↓
6. Upload to server (chunks if large)
   ├─ Server stores in /srv/WinCloud/storage/
   └─ Database records metadata
   ↓
7. Create .cloud file locally
   ├─ Header (magic + version)
   ├─ Metadata (JSON)
   └─ Local data (10%)
   ↓
8. Show success + statistics
```

### Archive Extraction Flow

```
1. User opens .cloud file
   ↓
2. Read local archive
   ├─ Parse metadata
   └─ Extract 10% local data
   ↓
3. Download 90% from server
   ├─ Authenticate
   ├─ Request by archive_id
   └─ Stream download
   ↓
4. Decrypt cloud data
   ↓
5. Merge: local 10% + cloud 90%
   ↓
6. Decompress (reverse order)
   ├─ LZMA2 decompression
   └─ Zstandard decompression
   ↓
7. Verify checksums (SHA-256)
   ↓
8. Write files to disk
   ↓
9. Show success
```

## File Format Specification

### .cloud Archive Structure

```
┌──────────────────────────────────────┐
│ Magic Header (8 bytes)               │
│ "WCLOUD10"                           │
├──────────────────────────────────────┤
│ Metadata Length (4 bytes, LE)       │
│ Integer: length of JSON metadata     │
├──────────────────────────────────────┤
│ Metadata (JSON, UTF-8)               │
│ {                                    │
│   version: "1.0",                    │
│   files: [...],                      │
│   created: timestamp,                │
│   cloud_archive_id: "uuid",          │
│   ...                                │
│ }                                    │
├──────────────────────────────────────┤
│ Local Data (10%)                     │
│ Compressed file data                 │
│ (Multiple files concatenated)        │
└──────────────────────────────────────┘
```

### Metadata Schema

```json
{
  "version": "1.0",
  "created": 1704988800.0,
  "total_size": 104857600,
  "compression": "zstd+lzma2",
  "cloud_archive_id": "550e8400-e29b-41d4-a716-446655440000",
  "files": [
    {
      "name": "document.pdf",
      "path": "C:/Users/User/document.pdf",
      "size": 10485760,
      "compressed_size": 5242880,
      "local_offset": 0,
      "local_size": 524288,
      "cloud_offset": 0,
      "cloud_size": 4718592,
      "checksum": "abc123...",
      "cloud_id": "file-uuid"
    }
  ]
}
```

## Compression Strategy

### Two-Stage Compression

1. **Stage 1: Zstandard (Fast)**
   - Level: 10
   - Speed-focused
   - Good compression ratio
   - Low CPU usage

2. **Stage 2: LZMA2 (Maximum)**
   - Preset: 9 (maximum)
   - Best compression ratio
   - Higher CPU usage
   - Applied after Zstandard

### Split Ratio: 10/90

- **Local (10%)**: Essential recovery data
- **Cloud (90%)**: Bulk compressed data
- Configurable in config.json

## Security Architecture

### Encryption

```
┌─────────────────────────────────────┐
│ Original Data                       │
└──────────────┬──────────────────────┘
               │
         ┌─────▼──────┐
         │  Compress  │
         └─────┬──────┘
               │
         ┌─────▼──────┐
         │Split 10/90 │
         └──┬──────┬──┘
            │      │
     Local  │      │ Cloud
     (10%)  │      │ (90%)
            │      │
            │   ┌──▼────────────┐
            │   │ AES-256-GCM   │
            │   │ Encrypt       │
            │   └──┬────────────┘
            │      │
            │   ┌──▼────────────┐
            │   │Upload to      │
            │   │Server         │
            │   └───────────────┘
            │
         ┌──▼────────────┐
         │Store in .cloud  │
         └───────────────┘
```

### Key Management

- Master key: AES-256 (256 bits)
- Stored in: `~/.wincloud/.key`
- Per-file IV: Random 12 bytes (GCM mode)
- Authentication: Tag 16 bytes

## Network Protocol

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Server health check |
| POST | `/api/v1/auth` | User authentication |
| POST | `/api/v1/archives/upload` | Upload cloud data |
| POST | `/api/v1/archives/upload/finalize/<id>` | Finalize chunked upload |
| GET | `/api/v1/archives/<id>/download` | Download cloud data |
| DELETE | `/api/v1/archives/<id>` | Delete archive |

### Chunked Upload

For files > 5MB:
1. Split into 5MB chunks
2. Upload sequentially with chunk index
3. Server assembles on finalization
4. Automatic retry on failure

## Performance Optimizations

### Client-Side

1. **Multi-threading**
   - GUI thread: UI updates
   - Worker thread: Compression/network
   - Prevents UI freezing

2. **Streaming Processing**
   - Large files processed in chunks
   - Memory-efficient

3. **Progress Tracking**
   - Real-time speed calculation
   - ETA estimation
   - Detailed statistics

### Server-Side

1. **SQLite for Metadata**
   - Fast queries
   - ACID compliance
   - Easy backups

2. **File-based Storage**
   - Direct I/O
   - No intermediate buffers
   - OS-level caching

3. **Connection Pooling**
   - Reuse HTTP connections
   - Reduce latency

## Scalability Considerations

### Current Capacity

- Storage: Limited by disk space
- Concurrent users: ~1000 (single server)
- Max file size: 50GB

### Scale-Out Plan

1. **Load Balancer**
   - nginx reverse proxy
   - Round-robin distribution

2. **Database Upgrade**
   - Migrate to PostgreSQL
   - Sharding by user_id

3. **Storage**
   - Object storage (S3-compatible)
   - CDN for downloads

4. **Caching**
   - Redis for sessions
   - Frequently accessed metadata

5. **Monitoring**
   - Prometheus metrics
   - Grafana dashboards
   - Alert system

## Error Handling

### Client Strategies

1. **Network Failures**
   - Automatic retry (3 attempts)
   - Exponential backoff
   - User notification

2. **Server Unavailable**
   - Graceful degradation
   - Local-only mode
   - Queue for later upload

3. **Corruption Detection**
   - SHA-256 checksums
   - Integrity verification
   - Automatic re-download

### Server Strategies

1. **Rate Limiting**
   - Per-user quotas
   - DDoS protection

2. **Storage Limits**
   - User quotas
   - Automatic cleanup

3. **Backup System**
   - Daily database backups
   - Disaster recovery plan

## Testing Strategy

### Unit Tests
- Compression algorithms
- Encryption/decryption
- File splitting/merging
- Network client

### Integration Tests
- Client-server communication
- Upload/download flows
- Error scenarios

### Performance Tests
- Large file handling
- Concurrent users
- Memory usage

### Security Tests
- Encryption strength
- Authentication bypass attempts
- SQL injection prevention

## Deployment

### Client
- PyInstaller executable
- Windows 10/11 compatible
- Automatic updates (future)

### Server
- Systemd service
- Automatic restart
- Log rotation
- Monitoring integration

## Maintenance

### Regular Tasks
- Database vacuum (weekly)
- Log rotation (daily)
- Backup verification (daily)
- Security updates (as needed)

### Monitoring Metrics
- Storage usage
- API response times
- Error rates
- Active users
- Upload/download bandwidth
