# Model Inventory Summary

Snapshot generated 2025-10-23 from `reports/model_inventory.csv` and `reports/blob_inventory.csv`.

## Large GGUF Assets (`D:\u0418\u0418\blobs`)

All Ollama GGUF blobs were removed on 2025-10-23 (per user request). The directory is currently empty; prior contents are listed below for historical context.

| File (sha256-*, removed) | Size (GiB) | Architecture | General name | Context length | Notes |
| --- | ---: | --- | --- | ---: | --- |
| 6be6d66a3f546d8c19b130dc41dc24b2fc159f84ffbc76a0ee0676205083cf5a | 60.88 | gptoss | *(missing)* | 131072 | tokenizer model: `gpt2`; mixture-of-experts (head_count 64, expert_used_count 4) |
| 58574f2e94b99fb9e4391408b57e5aeaaaec10f6384e9a699fc2cb43a5c8eabf-partial | 17.28 | qwen3moe | Qwen3 30B A3B Thinking 2507 | 262144 | looked complete despite the `-partial` suffix |
| e796792eba26c4d3b04b0ac5adb01a453dd9ec2dfd83b6c59cbf6fe5f30b0f68-partial | 16.20 | gemma3 | *(missing)* | 131072 | duplicate metadata keys suggested possible corruption |
| e7b273f9636059a689e3ddcab3716e4f65abe0143ac978e46673ad0e52d09efb | 12.85 | gptoss | *(missing)* | 131072 | same architecture family as the 60.88 GiB asset |

### Fragment files

Former `-partial-*` marker files (57-69 bytes) were also removed alongside the blobs.

## Repository Models (`F:\Mirai`)

Only small Chroma vector-store shards (`*.bin`, `*.header`) are present inside the repository tree. No full LLM weights are stored under `F:\Mirai` as of this snapshot.

## Recommended Actions

1. Relocate confirmed GGUF weights into a dedicated `F:\Mirai\models\` hierarchy (or document the external path) and update config files such as `mirai-pro/config.yaml`.
2. Validate the `gemma3` archive that reports duplicate keys; re-download if checksum differs from the expected model.
3. Rename hashed filenames using a `README` or manifest that maps sha256 IDs to human-readable model names to avoid confusion.
4. Remove or archive leftover `-partial-*` marker files after confirming that the main downloads are intact.
