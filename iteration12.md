**Hierarchical Semantic Chunking Strategy Optimized for Qwen3-Coder:**

1. **Multi-Level Chunking Architecture for 1M Token Context**
   ```
   Repository Level (Root - up to 800KB context)
   ├── Module/Package Level (Parent Chunks: 50-100KB)
   │   ├── File Level (Child Chunks: 10-25KB)
   │   │   ├── Class/Interface Level (Granular Chunks: 2-8KB)
   │   │   │   └── Method/Function Level (Micro Chunks: 512-2KB)
   │   │   └── Documentation/Comment Chunks (Context: 1-4KB)
   │   └── Cross-Reference Chunks (Integration: 5-15KB)
   └── Dependency/Import Graph (Meta Chunks: 10-50KB)
   ```

2. **Qwen3-Coder Optimized Semantic Boundary Detection**
   - AST-based parsing optimized for Qwen3-Coder's code understanding
   - Repository-scale context awareness leveraging 1M token window
   - Semantic overlap optimization (15-25% for better code continuity)
   - Cross-reference maintenance with repository-wide dependency tracking

3. **1M Token Context Window Utilization Strategy**
   - Dynamic context assembly targeting 950,000+ tokens utilization
   - Repository-aware hierarchical context building (micro → granular → file → module → repository)
   - Context window efficiency target: 98% (approaching 1M token limit)
   - Lost-in-the-middle problem eliminated through strategic token placement
   - Qwen3-Coder's MoE architecture optimization (3.3B active parameters from 30B total)

**Enhanced Metadata Extraction Leveraging Qwen3-Coder Capabilities:**