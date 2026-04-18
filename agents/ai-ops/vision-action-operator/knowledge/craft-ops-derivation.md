---
last_updated: 2026-04-18
confidence: high
sources: 4
---

# CRAFT Ops Derivation

## Quick Reference

Screenshot analizi → CRAFT Create/Modify/Delete operation batch'i türetme; idempotency ve no-op skipping.

| Kavram | Açıklama |
|--------|----------|
| Ops Batch | Sıralı CRAFT operasyonları (Create → Modify → Delete) |
| Idempotency | Same input → same output, repeatable without side effects |
| State Hash | Current scene state'in SHA256 checksum'u |
| No-Op | Durumu değiştirmeyen op (skip et) |

## Derivation Process

### 1. Analysis → Ops Mapping

Screenshot analiz sonucundan CRAFT operations türetme:

```
Detected State:
  - Button "Save" (bounds=[120,450,80,40], state=active, focused=false)
  - Dialog "Confirm" (bounds=[300,200,150,100], state=hidden)
  - Input Field "Name" (bounds=[50,200,300,25], text="John", enabled=true)

Derivation Logic:
  1. Dialog "Confirm" is hidden BUT should be shown
     → Op: Create GameObject "UI/Dialogs/ConfirmDialog" with properties
  
  2. Button "Save" is active but not focused
     → Op: Modify "UI/Buttons/SaveButton" { focused=true }
  
  3. Input Field text is "John" but should be empty
     → Op: Modify "UI/InputFields/NameInput" { text="" }
  
Output CRAFT ops:
  [
    {type: "Create", target: "UI/Dialogs/ConfirmDialog", params: {...}},
    {type: "Modify", target: "UI/Buttons/SaveButton", changes: {focused: true}},
    {type: "Modify", target: "UI/InputFields/NameInput", changes: {text: ""}}
  ]
```

### 2. Create Operations

Yeni GameObject ve component'ler oluşturma:

```json
{
  "type": "Create",
  "target": "UI/Dialogs/ConfirmDialog",
  "params": {
    "parent": "Canvas",
    "components": [
      {
        "type": "Image",
        "properties": {
          "color": "rgba(200, 200, 200, 0.8)",
          "raycastTarget": true
        }
      },
      {
        "type": "Button",
        "properties": {
          "interactable": true,
          "targetGraphic": "Image"
        }
      }
    ],
    "position": {x: 300, y: 200},
    "size": {width: 150, height: 100}
  }
}
```

**Validation:**
- Parent GameObject mevcut mu?
- Component types valid mi (Image, Button, Text vb.)?
- Properties CRAFT schema'ya uyuyor mu?

### 3. Modify Operations

Mevcut GameObject property'lerini değiştirme:

```json
{
  "type": "Modify",
  "target": "UI/Buttons/SaveButton",
  "changes": {
    "components": {
      "Button": {
        "interactable": true,
        "focused": true
      },
      "Image": {
        "color": "rgb(0, 122, 204)"
      }
    },
    "position": {x: 120, y: 450},
    "size": {width: 80, height: 40}
  }
}
```

**Validation:**
- Target GameObject mevcut mu?
- Changes CRAFT schema'ya uyuyor mu?
- Type coercion safe mi (string → number, vb.)?

### 4. Delete Operations

GameObject ve child'lerini silme:

```json
{
  "type": "Delete",
  "target": "UI/Modals/OldDialog",
  "recursive": true
}
```

**Validation:**
- Target var mı?
- Dependencies kontrol et (silinirse başka op'lar fail mi?)

## Idempotency Rules

### State Hashing

Current scene state'in deterministic hash'ini hesapla:

```python
def compute_state_hash(scene_state: Dict) -> str:
    """
    Scene state'in SHA256 hash'i.
    """
    canonical = json.dumps(scene_state, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()
```

**State dict örneği:**
```json
{
  "gameobjects": {
    "UI/Buttons/SaveButton": {
      "active": true,
      "enabled": true,
      "position": [120, 450, 0],
      "components": {
        "Button": {"interactable": true},
        "Image": {"color": [0, 122, 204, 255]}
      }
    },
    "UI/InputFields/NameInput": {
      "text": "John",
      "enabled": true
    }
  }
}
```

### No-Op Detection

Eğer `previous_state_hash == next_state_hash` → ops'ın state'i değiştirmediği anlamına gelir (no-op).

```python
def skip_no_op_ops(ops: List[Op], prev_hash: str, next_hash: str) -> List[Op]:
    """
    No-op ops'ı filtrele (state değiştirilmeyecekse skip et).
    """
    if prev_hash == next_hash:
        return []  # Tüm ops no-op
    
    # Partial no-op: bir op no-op ise skip et
    result = []
    for op in ops:
        if op_changes_state(op, prev_hash):
            result.append(op)
        else:
            log(f"SKIP no-op: {op}")
    
    return result

def op_changes_state(op: Op, current_hash: str) -> bool:
    """
    Op'ın state'i değiştirecek mi?
    """
    # Simulated ops apply, check hash change
    simulated_next = apply_op(op, current_state_from_hash(current_hash))
    next_hash = compute_state_hash(simulated_next)
    return next_hash != current_hash
```

### Idempotency Enforcement

Her batch execution'da aynı result garantisi:

```
Execution 1:
  Input: screenshot + previous_state_hash=abc123
  Output: ops[], next_state_hash=def456
  
Execution 2 (same screenshot + state):
  Input: screenshot + previous_state_hash=abc123
  Output: ops[] (same), next_state_hash=def456
  
Idempotent? YES → Safe to retry
```

## Patterns & Decision Matrix

### High-Confidence Ops

| Detected State | Derivation | Confidence |
|---|---|---|
| Button not focused → should focus | Modify op (Button.focused=true) | 0.95 |
| Dialog hidden → should show | Create child elements + Modify Dialog.active=true | 0.90 |
| Input text wrong | Modify op (TextComponent.text="correct") | 0.92 |
| Property color mismatch | Modify op (Image.color=correct) | 0.88 |

### Low-Confidence / Risky

| Scenario | Risk | Mitigation |
|---|---|---|
| Unknown GameObject target | Op fails (target not found) | Validate target exists before deriving Delete/Modify |
| Complex nested structure | Child creation order matters | Use DAG ordering (parent before child) |
| Property type mismatch | Type coercion error | Validate schema beforehand |
| Circular dependency | Create loop | Dependency graph acyclic check |

## Code Examples

### Derivation Algorithm Pseudocode

```python
def derive_craft_ops(
    detected_state: Dict,
    expected_state: Dict,
    previous_state_hash: str
) -> Tuple[List[Op], str]:
    """
    Detected state vs. expected state → CRAFT ops batch.
    
    Returns: (ops[], next_state_hash)
    """
    ops = []
    
    # 1. Detect deletions (expected but not detected)
    for target, expected_props in expected_state.items():
        if target not in detected_state:
            ops.append({
                'type': 'Delete',
                'target': target,
                'recursive': True
            })
    
    # 2. Detect creations (detected but not expected)
    for target, detected_props in detected_state.items():
        if target not in expected_state:
            ops.append({
                'type': 'Create',
                'target': target,
                'params': detected_props
            })
    
    # 3. Detect modifications (both present, properties differ)
    for target in expected_state:
        if target in detected_state:
            changes = diff_properties(
                expected_state[target],
                detected_state[target]
            )
            if changes:
                ops.append({
                    'type': 'Modify',
                    'target': target,
                    'changes': changes
                })
    
    # 4. Apply ops, compute next state hash
    next_state = apply_ops(detected_state, ops)
    next_hash = compute_state_hash(next_state)
    
    # 5. Filter no-ops
    filtered_ops = skip_no_op_ops(ops, previous_state_hash, next_hash)
    
    return filtered_ops, next_hash
```

### Validation Pseudocode

```python
def validate_ops_batch(ops: List[Op], scene: Scene) -> (bool, str):
    """
    Ops batch'inin validity kontrolü.
    
    Returns: (is_valid, error_message)
    """
    targets_seen = set()
    
    for op in ops:
        if op['type'] == 'Create':
            target = op['target']
            if target in targets_seen:
                return False, f"Duplicate Create: {target}"
            targets_seen.add(target)
            
            # Parent exists mi?
            parent = op['params'].get('parent')
            if parent and not scene.find(parent):
                return False, f"Parent not found: {parent}"
        
        elif op['type'] == 'Modify':
            target = op['target']
            if not scene.find(target):
                return False, f"Target not found for Modify: {target}"
        
        elif op['type'] == 'Delete':
            target = op['target']
            if not scene.find(target):
                return False, f"Target not found for Delete: {target}"
    
    return True, ""
```

## Anti-Patterns

- **State assumption**: Previous state'i önceki hash'ten restore etmeden ops apply etmek
- **Order insensitivity**: Create before parent op'ı etmemek — DAG ordering zorunlu
- **Hash blindness**: State hash kontrol etmeden no-op assumption — always validate
- **Partial validation**: Sadece ilk op'ı validate et → tüm batch'i validate et
- **Circular deps**: Modify op'ları sonsuz döngü oluşturacak şekilde sıralamak

## Deep Dive Sources

- [CRAFT Tool SKILL.md](../../../../../../ccplugin-unity-craft/SKILL.md) — ops spec, validation rules
- [Idempotency in Distributed Systems](https://en.wikipedia.org/wiki/Idempotence) — theory
- [Scene Graph Algorithms](https://www.cs.cmu.edu/~scandal/papers/scenegraph.pdf) — parent-child ordering
- [Deterministic Hashing](https://www.usenix.org/system/files/atc21-papamanthou.pdf) — state reproducibility

---

**Revision**: CRAFT ops derivation 2026-04-18 güncellenmiş; idempotency rules v2 + no-op detection algorithm.
