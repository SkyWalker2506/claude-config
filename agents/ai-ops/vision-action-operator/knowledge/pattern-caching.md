---
last_updated: 2026-04-18
confidence: high
sources: 6
---

# Pattern Caching

## Quick Reference

`.unity-craft/patterns/` schema: cached UI → CRAFT ops mapping. Hit-rate optimization, miss fallback, pattern validation.

| Kavram | Açıklama |
|--------|----------|
| Pattern | UI state (screenshot hash) + deriv. CRAFT ops cache |
| Cache Hit | Pattern'in trigger_image_hash match → reuse ops |
| Cache Miss | Hash mismatch → live analysis (screenshot re-detect) |
| Hit Rate | Successful reuse % (optimize threshold) |

## Pattern Schema

### Directory Structure

```
project/.unity-craft/
├── patterns/
│   ├── _metadata.json
│   ├── pattern_001_button_save_click.json
│   ├── pattern_002_dialog_confirm_open.json
│   ├── pattern_003_input_name_clear.json
│   └── ...
└── state/
    ├── last_scene_hash.txt
    └── session_log.jsonl
```

### Pattern File Format

```json
{
  "id": "pattern_001_button_save_click",
  "goal": "Click 'Save' button and trigger confirmation dialog",
  "trigger_image_hash": "sha256:a1b2c3d4e5f6...",
  "trigger_image_resolution": [1920, 1080],
  "craft_ops": [
    {
      "type": "Modify",
      "target": "UI/Buttons/SaveButton",
      "changes": {"focused": true, "state": "pressed"}
    },
    {
      "type": "Create",
      "target": "UI/Dialogs/ConfirmDialog",
      "params": {
        "parent": "Canvas",
        "active": true,
        "position": [960, 540]
      }
    }
  ],
  "expected_state_hash": "sha256:f6e5d4c3b2a1...",
  "success_count": 42,
  "last_used": "2026-04-18T14:32:15Z",
  "confidence": 0.96,
  "tags": ["ui-action", "dialog", "user-intent"],
  "metadata": {
    "created_at": "2026-03-10T09:15:00Z",
    "created_by": "vision-action-operator",
    "project": "CCUC",
    "scene": "MainMenu"
  }
}
```

### Metadata Index

```json
{
  "project": "CCUC",
  "version": 1,
  "total_patterns": 127,
  "hit_rate_global": 0.73,
  "hit_rate_last_24h": 0.81,
  "miss_count_last_24h": 6,
  "patterns": [
    {
      "id": "pattern_001_button_save_click",
      "hits": 42,
      "misses": 2,
      "hit_rate": 0.95,
      "last_used": "2026-04-18T14:32:15Z"
    },
    ...
  ]
}
```

## Cache Hit Detection

### Hash Matching

Screenshot'ın trigger_image_hash'i ile karşılaştırma:

```python
def detect_cache_hit(
    screenshot: Image,
    patterns_dir: Path
) -> Tuple[Optional[Pattern], float]:
    """
    Screenshot'ın cached pattern match'i var mı?
    
    Returns: (pattern, confidence) or (None, 0.0)
    """
    screenshot_hash = compute_image_hash(screenshot)
    
    # Load metadata index
    metadata = load_json(patterns_dir / "_metadata.json")
    
    best_match = None
    best_confidence = 0.0
    
    for pattern_info in metadata['patterns']:
        pattern_file = patterns_dir / f"{pattern_info['id']}.json"
        pattern = load_json(pattern_file)
        
        # Exact match
        if pattern['trigger_image_hash'] == screenshot_hash:
            return pattern, 1.0
        
        # Fuzzy match (perceptual hash distance < threshold)
        phash_dist = perceptual_hash_distance(
            screenshot_hash,
            pattern['trigger_image_hash']
        )
        
        if phash_dist < 0.1:  # 10% tolerance
            confidence = 1.0 - phash_dist
            if confidence > best_confidence:
                best_match = pattern
                best_confidence = confidence
    
    if best_match and best_confidence >= 0.85:
        return best_match, best_confidence
    
    return None, 0.0
```

### Confidence Thresholds

| Threshold | Meaning | Action |
|-----------|---------|--------|
| >= 0.95 | High confidence match | Use cached ops directly |
| 0.85-0.94 | Moderate confidence | Use cached ops + verify state hash |
| 0.75-0.84 | Low confidence | Warn, ask user confirmation |
| < 0.75 | No reliable match | Force live analysis |

## Miss Handling

### Cache Miss Fallback

Pattern'i bulamazsa live analysis:

```python
def handle_cache_miss(
    screenshot: Image,
    patterns_dir: Path,
    current_state_hash: str
) -> Tuple[List[Op], str, Pattern]:
    """
    Cache miss → live analysis + yeni pattern ekle.
    
    Returns: (ops, next_state_hash, new_pattern)
    """
    # 1. Live analysis (fresh detection + derivation)
    detected_state = detect_ui_elements(screenshot)
    expected_state = get_expected_ui_state()  # From CRAFT config?
    
    ops, next_state_hash = derive_craft_ops(
        detected_state, expected_state, current_state_hash
    )
    
    # 2. Create new pattern for future reuse
    screenshot_hash = compute_image_hash(screenshot)
    new_pattern = {
        'id': generate_pattern_id(),
        'goal': f"Auto-detected pattern from screenshot {screenshot_hash[:8]}",
        'trigger_image_hash': screenshot_hash,
        'trigger_image_resolution': screenshot.size,
        'craft_ops': ops,
        'expected_state_hash': next_state_hash,
        'success_count': 0,
        'last_used': datetime.now().isoformat() + 'Z',
        'confidence': 0.5,  # Low, unverified
        'tags': ['auto-detected', 'unverified'],
        'metadata': {
            'created_at': datetime.now().isoformat() + 'Z',
            'created_by': 'vision-action-operator',
            'project': get_current_project(),
            'scene': get_current_scene()
        }
    }
    
    # 3. Save pattern
    pattern_file = patterns_dir / f"{new_pattern['id']}.json"
    save_json(pattern_file, new_pattern)
    
    # 4. Update metadata index
    update_metadata_index(patterns_dir, new_pattern)
    
    return ops, next_state_hash, new_pattern
```

## Hit-Rate Policies

### Optimization Strategy

Hit rate'i artırmak için cache warmup ve cleanup:

```python
def optimize_cache_hit_rate(
    patterns_dir: Path,
    min_hit_rate: float = 0.7
) -> Dict[str, int]:
    """
    Cache hit-rate optimization: düşük confidence patterns'i temizle.
    
    Returns: {cleaned: N, merged: M, kept: K}
    """
    metadata = load_json(patterns_dir / "_metadata.json")
    stats = {'cleaned': 0, 'merged': 0, 'kept': 0}
    
    # 1. Remove low-confidence unverified patterns
    patterns_to_remove = [
        p for p in metadata['patterns']
        if p['hit_rate'] < 0.3 and p['confidence'] < 0.6
    ]
    
    for pattern_info in patterns_to_remove:
        pattern_file = patterns_dir / f"{pattern_info['id']}.json"
        pattern_file.unlink()
        stats['cleaned'] += 1
    
    # 2. Merge similar patterns (same goal, similar ops)
    similar_groups = cluster_patterns(metadata['patterns'])
    
    for group in similar_groups:
        if len(group) > 1:
            # Keep highest-confidence pattern
            primary = max(group, key=lambda p: p['hit_rate'])
            for secondary in group:
                if secondary['id'] != primary['id']:
                    secondary_file = patterns_dir / f"{secondary['id']}.json"
                    secondary_file.unlink()
                    stats['merged'] += 1
    
    # 3. Recompute global hit rate
    total_hits = sum(p['hits'] for p in metadata['patterns'])
    total_uses = total_hits + sum(p['misses'] for p in metadata['patterns'])
    metadata['hit_rate_global'] = total_hits / total_uses if total_uses > 0 else 0.0
    
    # 4. Save updated metadata
    save_json(patterns_dir / "_metadata.json", metadata)
    
    stats['kept'] = len(metadata['patterns'])
    
    return stats
```

### Hit-Rate Monitoring

```python
def log_cache_usage(
    patterns_dir: Path,
    pattern_id: str,
    hit: bool
):
    """
    Cache hit/miss'i session log'a kaydet.
    """
    session_log = patterns_dir.parent / "state" / "session_log.jsonl"
    
    entry = {
        'timestamp': datetime.now().isoformat() + 'Z',
        'pattern_id': pattern_id,
        'hit': hit,
        'project': get_current_project(),
        'scene': get_current_scene()
    }
    
    with open(session_log, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    
    # Update metadata
    metadata = load_json(patterns_dir / "_metadata.json")
    for p in metadata['patterns']:
        if p['id'] == pattern_id:
            if hit:
                p['hits'] += 1
            else:
                p['misses'] += 1
            p['last_used'] = entry['timestamp']
            break
    
    save_json(patterns_dir / "_metadata.json", metadata)
```

## Validation & Integrity

### Pattern Verification

Cached pattern'inin doğruluğunu kontrol et:

```python
def verify_pattern_integrity(
    pattern: Pattern,
    current_scene: Scene,
    screenshot: Image
) -> Tuple[bool, str]:
    """
    Pattern'in current scene'de geçerli olup olmadığını kontrol et.
    
    Returns: (is_valid, message)
    """
    # 1. Check target GameObjects exist
    for op in pattern['craft_ops']:
        target = op['target']
        if not current_scene.find(target):
            return False, f"Target not found: {target}"
    
    # 2. Verify image resolution compatibility
    if screenshot.size != pattern['trigger_image_resolution']:
        return False, f"Resolution mismatch: {screenshot.size} vs {pattern['trigger_image_resolution']}"
    
    # 3. Re-detect UI and compare with expected
    detected = detect_ui_elements(screenshot)
    expected = pattern.get('expected_ui_elements', [])
    
    if expected and not matches_detected_to_expected(detected, expected):
        return False, "Detected UI doesn't match pattern expectation"
    
    return True, "Pattern verified"
```

## Patterns & Decision Matrix

### When to Use Cache

| Scenario | Cached Hit Rate | Action |
|----------|-----------------|--------|
| Exact screenshot match | 100% | Use ops immediately |
| Similar UI layout, same resolution | 90%+ | Use ops + verify state hash |
| Different resolution but same content | 75-85% | Ask user confirm before apply |
| Unknown pattern | 0% | Live analysis + store new pattern |

### Cache Invalidation

| Trigger | Action | Hit-Rate Impact |
|---------|--------|-----------------|
| Scene changed | Clear all scene-specific patterns | -80% |
| Layout resolution changed | Recompute patterns for new res | -50% |
| Package updated | Validation check all patterns | -10% |
| Manual pattern delete | Remove from metadata + disk | Minimal |

## Code Examples

### Pattern Creation Pseudocode

```python
def create_pattern_from_analysis(
    screenshot: Image,
    detected_state: Dict,
    ops: List[Op],
    next_state_hash: str,
    goal: str,
    scene: str
) -> Pattern:
    """
    Screenshot analiz sonucundan pattern oluştur.
    """
    pattern = {
        'id': f"pattern_{int(time.time() * 1000)}_{hashlib.md5(goal.encode()).hexdigest()[:8]}",
        'goal': goal,
        'trigger_image_hash': compute_image_hash(screenshot),
        'trigger_image_resolution': list(screenshot.size),
        'craft_ops': ops,
        'expected_state_hash': next_state_hash,
        'expected_ui_elements': detected_state,
        'success_count': 0,
        'last_used': datetime.now().isoformat() + 'Z',
        'confidence': 0.5,  # Start low, increase with use
        'tags': ['auto-detected'],
        'metadata': {
            'created_at': datetime.now().isoformat() + 'Z',
            'created_by': 'vision-action-operator',
            'scene': scene
        }
    }
    
    return pattern
```

### Cache Lookup Pseudocode

```python
def lookup_and_reuse_pattern(
    screenshot: Image,
    patterns_dir: Path
) -> Tuple[Optional[List[Op]], float]:
    """
    Cache'den pattern lookup ve ops reuse.
    
    Returns: (ops, confidence) or (None, 0.0)
    """
    pattern, confidence = detect_cache_hit(screenshot, patterns_dir)
    
    if pattern is None:
        return None, 0.0
    
    # Log hit
    log_cache_usage(patterns_dir, pattern['id'], hit=True)
    
    # Return cached ops
    return pattern['craft_ops'], confidence
```

## Anti-Patterns

- **Blind reuse**: Hash match'i doğrulayıp ops'ı target scene'de validate etmemek
- **Staleness**: Pattern'i months older without revalidation
- **Resolution bias**: Pattern create'i ve reuse'u farklı resolution'larda yapıp mismatch'i miss etmek
- **No cleanup**: Düşük hit-rate patterns'i silmeden cache'i sönüy kütlemesine bırakmak
- **Metadata desync**: Pattern file'ı sil ama metadata update etme → orphan entries

## Deep Dive Sources

- [Image Hashing Algorithms](https://docs.opencv.org/4.x/d4/d8c/tutorial_py_template_matching.html) — perceptual hashing
- [Cache Hit Rate Optimization](https://en.wikipedia.org/wiki/Cache_replacement_policies) — LRU, LFU strategies
- [Git LFS Pattern Caching](https://github.blog/2015-04-02-git-large-file-storage-public-beta/) — distributed cache models
- [Pattern Recognition in ML](https://www.cs.cmu.edu/~awm/tutorials) — clustering, similarity metrics

---

**Revision**: Pattern caching 2026-04-18 güncellenmiş; hit-rate optimization v2 + validation schema.
