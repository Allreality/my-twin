"""
doc_agent.py
============
Total Reality Global — Documentation Agent
Extends the digital twin's ChromaDB memory with structured,
tagged documentation from across the entire ecosystem.

Usage:
    python3 doc_agent.py --store "content" --type decision --tags sig,book
    python3 doc_agent.py --query "SIG deployment" --tags sig
    python3 doc_agent.py --query "all" --destination book
    python3 doc_agent.py --stats
    python3 doc_agent.py --interactive

Memory Types:
    episodic        — personal experiences and events (existing)
    semantic        — factual knowledge (existing)
    github_change   — code changes pushed to GitHub
    decision        — architectural or business decisions
    narrative       — book-worthy process moments
    gallery         — BlackArt VIP / UE5 content
    governance      — TAN / Temne Nation content
    infrastructure  — server, deployment, config changes
    compliance      — NIST, NERC CIP, FERC, patent records
    trading         — bot performance, strategy changes
    sierra_leone    — Romkalaneh / Koya project content

Destination Tags:
    #sig            — Signal Intelligence Grid agents
    #midnight       — Midnight compliance platform
    #blackart       — BlackArt VIP gallery
    #tan            — Temne Abara Nation / TAN DAO
    #book           — Future book / narrative archive
    #twin           — Digital twin knowledge base
    #ue5            — Unreal Engine 5 gallery integration
    #romkalaneh     — Sierra Leone infrastructure project
    #trading        — Trading bot system
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import chromadb

# ── Config ────────────────────────────────────────────────────────────────────

MEMORY_DIR   = "/mnt/c/projects/twin/memory_db"
COLLECTION   = "twin_memories"
LOG_FILE     = "/mnt/c/projects/twin/doc_agent.log"

VALID_TYPES = {
    "episodic", "semantic", "github_change", "decision",
    "narrative", "gallery", "governance", "infrastructure",
    "compliance", "trading", "sierra_leone",
}

VALID_TAGS = {
    "#sig", "#midnight", "#blackart", "#tan", "#book",
    "#twin", "#ue5", "#romkalaneh", "#trading",
}

VALID_DESTINATIONS = {
    "sig", "midnight", "blackart", "tan", "book",
    "twin", "ue5", "romkalaneh", "trading",
}

# ── ChromaDB Setup ────────────────────────────────────────────────────────────

def get_collection():
    client = chromadb.PersistentClient(path=MEMORY_DIR)
    try:
        col = client.get_collection(name=COLLECTION)
    except Exception:
        col = client.create_collection(
            name=COLLECTION,
            metadata={"description": "Digital twin episodic and semantic memories"}
        )
    return col


# ── Logging ───────────────────────────────────────────────────────────────────

def log(message: str):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    line = f"[{ts}] {message}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


# ── Core Operations ───────────────────────────────────────────────────────────

def store_memory(
    content: str,
    memory_type: str,
    tags: list[str],
    importance: float = 0.8,
    emotional_valence: float = 0.7,
    source: str = "manual",
    project: str = "",
    extra_meta: dict = None,
) -> str:
    """Store a new memory with extended metadata."""

    if memory_type not in VALID_TYPES:
        raise ValueError(f"Invalid type '{memory_type}'. Valid: {VALID_TYPES}")

    # Normalize tags — strip # if included
    clean_tags = []
    for t in tags:
        t = t.lower().strip()
        if not t.startswith("#"):
            t = "#" + t
        if t in VALID_TAGS:
            clean_tags.append(t)
        else:
            log(f"⚠️  Unknown tag '{t}' — skipping")

    col = get_collection()
    memory_id = f"doc_{int(datetime.now(timezone.utc).timestamp() * 1000)}"

    metadata = {
        "type":             memory_type,
        "tags":             ",".join(clean_tags),
        "source":           source,
        "project":          project,
        "importance":       importance,
        "emotional_valence": emotional_valence,
        "timestamp":        datetime.now(timezone.utc).isoformat(),
        "agent":            "doc_agent",
    }

    if extra_meta:
        metadata.update(extra_meta)

    col.add(
        documents=[content],
        metadatas=[metadata],
        ids=[memory_id],
    )

    log(f"✅ Stored [{memory_type}] tags={clean_tags} id={memory_id}")
    log(f"   Content: {content[:100]}{'...' if len(content) > 100 else ''}")
    return memory_id


def query_memories(
    query: str,
    memory_type: str = None,
    destination: str = None,
    limit: int = 10,
) -> list[dict]:
    """
    Search memories by semantic query, type, or destination tag.
    query='all' returns recent memories without semantic search.
    """
    col = get_collection()

    if query.lower() == "all":
        # Return most recent memories
        results = col.get(limit=limit)
        memories = []
        for i, doc in enumerate(results["documents"]):
            meta = results["metadatas"][i]
            # Filter by destination if specified
            if destination:
                tags = meta.get("tags", "")
                if f"#{destination}" not in tags:
                    continue
            # Filter by type if specified
            if memory_type and meta.get("type") != memory_type:
                continue
            memories.append({"content": doc, "metadata": meta, "id": results["ids"][i]})
        return memories

    # Semantic search
    results = col.query(
        query_texts=[query],
        n_results=min(limit, col.count()),
    )

    memories = []
    for i, doc in enumerate(results["documents"][0]):
        meta = results["metadatas"][0][i]
        # Filter by destination tag
        if destination:
            tags = meta.get("tags", "")
            if f"#{destination}" not in tags:
                continue
        # Filter by type
        if memory_type and meta.get("type") != memory_type:
            continue
        memories.append({
            "content": doc,
            "metadata": meta,
            "id": results["ids"][0][i],
            "distance": results["distances"][0][i] if "distances" in results else None,
        })

    return memories


def get_stats() -> dict:
    """Return memory statistics broken down by type and tag."""
    col = get_collection()
    total = col.count()

    # Get all metadata to compute breakdowns
    all_data = col.get(limit=total)
    type_counts  = {}
    tag_counts   = {}
    source_counts = {}

    for meta in all_data["metadatas"]:
        # Type breakdown
        t = meta.get("type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1

        # Tag breakdown
        for tag in meta.get("tags", "").split(","):
            tag = tag.strip()
            if tag:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # Source breakdown
        s = meta.get("source", "unknown")
        source_counts[s] = source_counts.get(s, 0) + 1

    return {
        "total_memories": total,
        "by_type":        dict(sorted(type_counts.items(), key=lambda x: -x[1])),
        "by_tag":         dict(sorted(tag_counts.items(), key=lambda x: -x[1])),
        "by_source":      dict(sorted(source_counts.items(), key=lambda x: -x[1])),
        "collection":     COLLECTION,
        "storage_path":   MEMORY_DIR,
    }


def store_github_event(
    repo: str,
    branch: str,
    commit_message: str,
    files_changed: list[str],
    tags: list[str],
) -> str:
    """Store a GitHub push event as a structured memory."""
    content = (
        f"GitHub push to {repo} ({branch}): {commit_message}. "
        f"Files changed: {', '.join(files_changed[:10])}"
        f"{'...' if len(files_changed) > 10 else ''}."
    )

    # Auto-detect project from repo name
    project_map = {
        "trading-bot-v2":          "trading",
        "sig-platform":            "sig",
        "midnight-infrastructure": "midnight",
        "blackart.vip":            "blackart",
        "twin":                    "twin",
    }
    project = next((v for k, v in project_map.items() if k in repo), repo)

    return store_memory(
        content=content,
        memory_type="github_change",
        tags=tags,
        importance=0.7,
        emotional_valence=0.6,
        source="github",
        project=project,
        extra_meta={
            "repo":          repo,
            "branch":        branch,
            "commit":        commit_message,
            "files_changed": json.dumps(files_changed[:20]),
        },
    )


# ── Interactive Mode ──────────────────────────────────────────────────────────

def interactive_mode():
    """Interactive CLI for storing and querying memories."""
    print("\n" + "="*60)
    print("TOTAL REALITY GLOBAL — Documentation Agent")
    print("="*60)
    print("Commands: store | query | github | stats | help | exit\n")

    while True:
        try:
            cmd = input("doc_agent> ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if cmd in ("exit", "quit", "q"):
            break

        elif cmd == "help":
            print("""
Commands:
  store   — store a new memory
  query   — search memories
  github  — log a GitHub push event
  stats   — show memory statistics
  exit    — quit

Memory types:  episodic, semantic, github_change, decision,
               narrative, gallery, governance, infrastructure,
               compliance, trading, sierra_leone

Destination tags: sig, midnight, blackart, tan, book,
                  twin, ue5, romkalaneh, trading
""")

        elif cmd == "store":
            content = input("  Content: ").strip()
            if not content:
                print("  ⚠️  Content required")
                continue
            mtype = input(f"  Type [{'/'.join(sorted(VALID_TYPES))}]: ").strip() or "semantic"
            tags_raw = input("  Tags (comma separated, e.g. sig,book,twin): ").strip()
            tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
            imp = input("  Importance [0.0-1.0, default 0.8]: ").strip() or "0.8"
            src = input("  Source [default: manual]: ").strip() or "manual"
            proj = input("  Project [optional]: ").strip()
            try:
                store_memory(
                    content=content,
                    memory_type=mtype,
                    tags=tags,
                    importance=float(imp),
                    source=src,
                    project=proj,
                )
            except Exception as e:
                print(f"  ❌ Error: {e}")

        elif cmd == "query":
            query = input("  Query (or 'all'): ").strip()
            dest  = input("  Filter by destination [optional]: ").strip() or None
            mtype = input("  Filter by type [optional]: ").strip() or None
            limit = input("  Limit [default 10]: ").strip() or "10"
            results = query_memories(query, memory_type=mtype, destination=dest, limit=int(limit))
            if not results:
                print("  No results found.")
            else:
                print(f"\n  Found {len(results)} memories:\n")
                for r in results:
                    meta = r["metadata"]
                    print(f"  [{meta.get('type','?')}] tags={meta.get('tags','')} | {meta.get('timestamp','')[:10]}")
                    print(f"  {r['content'][:120]}{'...' if len(r['content']) > 120 else ''}")
                    print()

        elif cmd == "github":
            repo    = input("  Repo name: ").strip()
            branch  = input("  Branch [default: main]: ").strip() or "main"
            commit  = input("  Commit message: ").strip()
            files   = input("  Files changed (comma separated): ").strip()
            files_list = [f.strip() for f in files.split(",") if f.strip()]
            tags_raw = input("  Tags (e.g. sig,book): ").strip()
            tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
            try:
                store_github_event(repo, branch, commit, files_list, tags)
            except Exception as e:
                print(f"  ❌ Error: {e}")

        elif cmd == "stats":
            stats = get_stats()
            print(f"\n  Total memories: {stats['total_memories']}")
            print(f"  By type:   {json.dumps(stats['by_type'], indent=4)}")
            print(f"  By tag:    {json.dumps(stats['by_tag'], indent=4)}")
            print(f"  By source: {json.dumps(stats['by_source'], indent=4)}")

        else:
            print(f"  Unknown command: '{cmd}'. Type 'help' for options.")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Total Reality Global — Documentation Agent")
    parser.add_argument("--store",       help="Content to store")
    parser.add_argument("--type",        default="semantic", help="Memory type")
    parser.add_argument("--tags",        default="", help="Comma-separated destination tags")
    parser.add_argument("--importance",  type=float, default=0.8)
    parser.add_argument("--source",      default="manual")
    parser.add_argument("--project",     default="")
    parser.add_argument("--query",       help="Search query (or 'all')")
    parser.add_argument("--destination", help="Filter by destination tag")
    parser.add_argument("--limit",       type=int, default=10)
    parser.add_argument("--stats",       action="store_true")
    parser.add_argument("--interactive", action="store_true")
    parser.add_argument("--github",      action="store_true", help="Log a GitHub push event")
    parser.add_argument("--repo",        default="")
    parser.add_argument("--branch",      default="main")
    parser.add_argument("--commit",      default="")
    parser.add_argument("--files",       default="", help="Comma-separated files changed")

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()

    elif args.stats:
        stats = get_stats()
        print(json.dumps(stats, indent=2))

    elif args.store:
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        store_memory(
            content=args.store,
            memory_type=args.type,
            tags=tags,
            importance=args.importance,
            source=args.source,
            project=args.project,
        )

    elif args.query:
        results = query_memories(args.query, destination=args.destination, limit=args.limit)
        for r in results:
            meta = r["metadata"]
            print(f"[{meta.get('type','?')}] tags={meta.get('tags','')} | {meta.get('timestamp','')[:10]}")
            print(f"{r['content'][:200]}")
            print()

    elif args.github:
        files = [f.strip() for f in args.files.split(",") if f.strip()]
        tags  = [t.strip() for t in args.tags.split(",") if t.strip()]
        store_github_event(args.repo, args.branch, args.commit, files, tags)

    else:
        interactive_mode()


if __name__ == "__main__":
    main()