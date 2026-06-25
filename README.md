# GCON - Decentralized Verified GPU Compute Network

A blockchain-free platform for verifiable execution of AI workloads on rented GPUs.

## Project Overview

**GCON** is a distributed system that enables:

- **GPU Providers** to rent their hardware with cryptographic proof of honest execution
- **Customers** to submit AI workloads and receive verified receipts proving:
  - The job actually executed
  - It ran on the advertised hardware (RTX 4090, H100, A100, etc.)
  - The output was not tampered with
  - The provider didn't cheat

## Comparison to Alternatives

| Platform | GPU Rentals | Verifiable Execution | Decentralized |
|----------|-------------|----------------------|---------------|
| NVIDIA DGX Cloud | ✅ | ❌ | ❌ |
| RunPod | ✅ | ❌ | ❌ |
| Vast.ai | ✅ | ❌ | ❌ |
| Akash Network | ✅ | ⚠️ Limited | ✅ |
| **GCON** | ✅ | **✅** | ✅ |

## MVP Architecture

```
Customer Submits Job
        ↓
GCON Agent (on Provider's Machine)
        ↓
    ├─ Executes Workload
    ├─ Monitors GPU/CPU
    ├─ Records Metrics
    └─ Collects Evidence
        ↓
Verification & Hashing
    ├─ Input Hash
    ├─ Output Hash
    └─ Cryptographic Signature
        ↓
Receipt Issuance
    └─ Signed Proof of Work
```

## Core Components

### 1. **Agent** (`agent.py`)
Runs on the provider's machine, executing workloads and monitoring execution.

**Key Features:**
- GPU detection and hardware identification
- Job execution in subprocess
- Real-time metrics collection (CPU, memory, GPU utilization)
- Execution monitoring and logging

**Usage:**
```python
from agent import GCONAgent

agent = GCONAgent("job-12345")
result = agent.execute_job("python train.py", timeout=300)
print(result)
```

### 2. **Verifier** (`verifier.py`)
Generates cryptographic proofs and validates execution receipts.

**Key Features:**
- SHA256/SHA512 hashing of inputs and outputs
- HMAC-based signature generation
- Execution proof generation
- Receipt validation and verification

**Usage:**
```python
from verifier import ExecutionVerifier

verifier = ExecutionVerifier("secret-key")
proof = verifier.generate_execution_proof(
    job_id="job-001",
    gpu_name="RTX 4090",
    runtime=120.5,
    input_hash="abc123...",
    output_hash="def456..."
)
```

### 3. **Receipt Manager** (`receipt.py`)
Manages execution receipts - storage, retrieval, and formatting.

**Key Features:**
- Persistent receipt storage to JSON files
- Receipt filtering and listing
- Multiple output formats (JSON, CSV, human-readable summary)

**Usage:**
```python
from receipt import ReceiptManager, ReceiptFormatter

manager = ReceiptManager("./receipts")
manager.save_receipt(receipt)
receipts = manager.list_receipts(job_id="job-001")
```

### 4. **Job Runner** (`run_job.py`)
High-level orchestrator coordinating agent execution, verification, and receipt generation.

**Key Features:**
- End-to-end job execution with verification
- Automatic hash collection and proof generation
- Receipt issuance and storage
- CLI interface for job submission

**Usage:**
```python
from run_job import JobRunner

runner = JobRunner()
result = runner.run_job(
    "python train.py",
    input_file="data.csv",
    output_file="model.pkl"
)
```

## Installation

### Requirements
- Python 3.8+
- `psutil` (for system metrics)
- Optional: `GPUtil` (for GPU detection)

### Setup

```bash
# Clone repository
git clone https://github.com/Jug-data/GCON.git
cd GCON

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Run a Simple Job

```bash
python run_job.py "echo 'Hello GCON'" --job-id job-001
```

### Run with Python Script

```bash
python run_job.py "python train.py" \
  --job-id job-training-001 \
  --input data.csv \
  --output model.pkl \
  --timeout 300
```

### Verify Receipt

```python
from run_job import JobRunner

runner = JobRunner()
receipt = runner.get_job_receipt("receipt-001")
print(runner.print_receipt("receipt-001", format="summary"))
```

## Output Example

```
╔════════════════════════════════════════════════════════════╗
║                  GCON EXECUTION RECEIPT                    ║
╠════════════════════════════════════════════════════════════╣
║ Receipt ID:      abc123def456                              ║
║ Job ID:          job-001                                   ║
║ Status:          success                                   ║
║ Issued At:       2024-01-15T10:30:45.123456               ║
╠════════════════════════════════════════════════════════════╣
║ Input Hash:      9f86d081884c7d6d9ffd60014fc7ee77e2b6 ║
║ Output Hash:     a665a45920422f9d417e4867efdc4fb8a04a ║
╠════════════════════════════════════════════════════════════╣
║ GPU:             RTX 4090                                  ║
║ Runtime:         120.5s                                    ║
║ Verified:        True                                      ║
╚════════════════════════════════════════════════════════════╝
```

## Testing

Run the test suite:

```bash
python -m pytest tests/ -v
# or
python -m unittest discover tests/
```

### Test Coverage

- ✅ Metrics collection and validation
- ✅ Hash generation and verification
- ✅ Signature creation and validation
- ✅ Receipt storage and retrieval
- ✅ Receipt formatting
- ✅ End-to-end job execution

## Data Structures

### Execution Metrics

```json
{
  "job_id": "job-001",
  "gpu_name": "RTX 4090",
  "gpu_memory_total": 24576,
  "gpu_memory_used": 12288,
  "cpu_percent": 45.5,
  "memory_percent": 60.0,
  "runtime_seconds": 120.5,
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### Execution Receipt

```json
{
  "receipt_id": "abc123def456",
  "job_id": "job-001",
  "agent_id": "agent-001",
  "status": "success",
  "input_hash": "9f86d081884c7d6d9ffd60014fc7ee77e2b6...",
  "output_hash": "a665a45920422f9d417e4867efdc4fb8a04a...",
  "proof": {
    "job_id": "job-001",
    "gpu": "RTX 4090",
    "runtime_seconds": 120.5,
    "input_hash": "9f86d081884c7d6d9ffd60014fc7ee77e2b6...",
    "output_hash": "a665a45920422f9d417e4867efdc4fb8a04a...",
    "timestamp": "2024-01-15T10:30:45.123456",
    "signature": "9e7d3c2b1a0f8e7d6c5b4a3f2e1d0c9b...",
    "verified": true
  },
  "issued_at": "2024-01-15T10:30:45.123456"
}
```

## Architecture Roadmap

### Phase 1: MVP (Current)
- ✅ Local agent execution
- ✅ Verified receipts
- ✅ Cryptographic proofs
- ⏳ Basic scheduling (next)

### Phase 2: Network
- ⏳ Distributed scheduler
- ⏳ Provider registry
- ⏳ Job marketplace

### Phase 3: Token/Blockchain (Future)
- ⏳ GCON token economics
- ⏳ Smart contracts
- ⏳ Dispute resolution

## File Structure

```
GCON/
├── agent.py          # Agent execution & monitoring
├── verifier.py       # Cryptographic verification
├── receipt.py        # Receipt management
├── run_job.py        # Job orchestration CLI
├── tests/
│   └── test_gcon.py  # Unit tests
├── README.md         # This file
└── requirements.txt  # Python dependencies
```

## Future Enhancements

- [ ] Container support (Docker/Singularity)
- [ ] Multi-GPU scheduling
- [ ] WebSocket API for real-time monitoring
- [ ] Dashboard UI
- [ ] Blockchain integration
- [ ] Advanced proof systems (zero-knowledge proofs)

## Contributing

Contributions welcome! Please follow:

1. Write tests for new features
2. Maintain code style
3. Document changes
4. Submit PR with description

## License

MIT

## Contact

For questions or support: [contact info]

---

**GCON** - Verify your compute. Trust your provider.
