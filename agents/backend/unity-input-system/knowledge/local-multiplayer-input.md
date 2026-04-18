# Local Multiplayer Input — Same-Keyboard Patterns

## Overview

Same-keyboard local multiplayer in Unity InputSystem requires careful asset isolation. The core constraint: **two players sharing one keyboard must have two independent `InputActionAsset` instances**. A shared asset reference causes one player's runtime state to bleed into the other.

---

## PlayerInputManager vs Manual Setup

### PlayerInputManager (high-level, avoid for same-keyboard)

Unity's `PlayerInputManager` component handles player join/split flows automatically. It works well for gamepad multiplayer (each gamepad is a distinct device) but is poorly suited for same-keyboard setups because:

- It uses device filtering to route input — keyboard is one device, so both players map to the same device
- Control scheme separation requires manual scheme override that bypasses most of PlayerInputManager's automation
- Binding isolation cannot be enforced at the asset level when sharing one asset

**Use PlayerInputManager for:** gamepad-based multiplayer, mixed gamepad + keyboard where each player has a dedicated device.

### Manual Setup (recommended for same-keyboard)

Instantiate two `InputActionAsset` instances from two separate `.inputactions` files (or via `Instantiate()` on the same source asset), attach one `PlayerInput` component per player GO, and assign the respective asset. This gives full control over binding scope and lifecycle.

---

## Why 2 Separate InputActionAsset Instances

`InputActionAsset` holds runtime state: enabled/disabled flags, binding overrides, and active control state per action. When two `PlayerInput` components reference the **same asset object**:

1. Enabling the asset for P2 re-enables actions that P1 may have selectively disabled
2. Binding overrides applied for P2 (e.g., rebinding) write back to the shared asset, altering P1's bindings
3. `InputAction.ReadValue<>()` aggregates all bound controls — P1's "W" key and P2's "W" key both fire the same action object, making it impossible to distinguish which player triggered it

**Solution:** Each player gets its own `InputActionAsset` instance. Use `ScriptableObject.Instantiate(sourceAsset)` or maintain two distinct `.inputactions` files.

---

## DualInputHandler Pattern

`DualInputHandler` is a MonoBehaviour that owns both asset instances and routes callbacks.

### Structure

```csharp
public class DualInputHandler : MonoBehaviour
{
    [SerializeField] InputActionAsset p1SourceAsset;
    [SerializeField] InputActionAsset p2SourceAsset;

    InputActionAsset p1Asset;
    InputActionAsset p2Asset;

    InputAction p1Move, p1Jump, p1Attack, p1Skill;
    InputAction p2Move, p2Jump, p2Attack, p2Skill;

    void Awake()
    {
        // Instantiate — never share references
        p1Asset = Instantiate(p1SourceAsset);
        p2Asset = Instantiate(p2SourceAsset);

        // Resolve actions by map + action name
        p1Move   = p1Asset["Player/Move"];
        p1Jump   = p1Asset["Player/Jump"];
        p1Attack = p1Asset["Player/Attack"];
        p1Skill  = p1Asset["Player/Skill"];

        p2Move   = p2Asset["Player/Move"];
        p2Jump   = p2Asset["Player/Jump"];
        p2Attack = p2Asset["Player/Attack"];
        p2Skill  = p2Asset["Player/Skill"];

        // Subscribe callbacks
        p1Jump.performed  += _ => OnP1Jump();
        p1Attack.performed += _ => OnP1Attack();
        p2Jump.performed  += _ => OnP2Jump();
        p2Attack.performed += _ => OnP2Attack();
    }

    void OnEnable()
    {
        p1Asset.Enable();
        p2Asset.Enable();
    }

    void OnDisable()
    {
        p1Asset.Disable();
        p2Asset.Disable();
    }

    void Update()
    {
        // Axis reads per-frame
        Vector2 p1Dir = p1Move.ReadValue<Vector2>();
        Vector2 p2Dir = p2Move.ReadValue<Vector2>();
        // ... pass to player controllers
    }

    void OnDestroy()
    {
        // Unsubscribe to prevent memory leaks
        p1Jump.performed  -= _ => OnP1Jump();
        // ... repeat for all subscriptions
        Destroy(p1Asset);
        Destroy(p2Asset);
    }
}
```

### Key points

- Always call `Instantiate()` in `Awake`, not `Start` (before any Update cycle)
- Enable/disable the **asset**, not individual actions, to keep state consistent
- Destroy instantiated assets on `OnDestroy` — they are not managed by the AssetDatabase at runtime
- For 3–4 players, extend with `p3Asset`, `p4Asset` following the same pattern

---

## PlayerInput Component Setup Per Player

When using `PlayerInput` components instead of DualInputHandler directly:

1. Create one empty GO per player (`Player1`, `Player2`)
2. Add `PlayerInput` component to each
3. Set **Actions** field to the respective `.inputactions` asset (different asset per player)
4. Set **Behavior** to `Invoke Unity Events` or `Send Messages` — both work
5. Set **Default Control Scheme** to `Keyboard` for both (same scheme name, different bindings in separate assets)
6. Do **not** use `PlayerInput.neverAutoSwitchControlSchemes = false` — disable auto-switch to prevent the component from re-routing based on last-used device

---

## Same-Keyboard Split Input: Key Conflict Detection

Before generating dual `.inputactions` assets, validate that no binding path appears in both P1 and P2 action maps.

### Conflict detection pseudocode

```
function detectConflicts(p1Keys, p2Keys):
    p1Paths = resolveToPaths(p1Keys)   // e.g. "<Keyboard>/w", "<Keyboard>/space"
    p2Paths = resolveToPaths(p2Keys)
    conflicts = intersection(p1Paths, p2Paths)
    return conflicts

function resolveToPaths(keyMap):
    paths = []
    if keyMap.move == "wasd":
        paths += ["<Keyboard>/w", "<Keyboard>/a", "<Keyboard>/s", "<Keyboard>/d"]
    if keyMap.move == "arrows":
        paths += ["<Keyboard>/upArrow", "<Keyboard>/leftArrow",
                  "<Keyboard>/downArrow", "<Keyboard>/rightArrow"]
    paths += [toKeyboardPath(keyMap.jump)]
    paths += [toKeyboardPath(keyMap.attack)]
    paths += [toKeyboardPath(keyMap.skill)]
    return paths
```

Note: `"wasd"` preset and `"arrows"` preset share no keys — they are the canonical conflict-free split. Conflicts arise when both players assign the same letter/symbol key for jump/attack/skill.

---

## Common Pitfalls

### Shared InputActionAsset (most common mistake)

```csharp
// WRONG — both PlayerInput reference same asset object
p1PlayerInput.actions = sharedAsset;
p2PlayerInput.actions = sharedAsset;  // overrides P1 state
```

```csharp
// CORRECT
p1PlayerInput.actions = Instantiate(sharedAsset);
p2PlayerInput.actions = Instantiate(sharedAsset);
```

### Forgetting to Destroy Instantiated Assets

Instantiated `InputActionAsset` objects are not in the AssetDatabase; they live in memory. Always `Destroy(asset)` in `OnDestroy()` to avoid leaks across scene loads.

### Lambda Subscription Leaks

Subscribing with inline lambdas (`action.performed += _ => Foo()`) makes unsubscription impossible since the lambda reference is lost. Cache the delegate in a field or use named methods.

### AutoSwitchControlSchemes Interfering

`PlayerInput` by default switches control schemes when it detects a different device. With same-keyboard, this can cause both players to be rerouted to the same scheme. Set `playerInput.neverAutoSwitchControlSchemes = true` on both components.

### InputActionMap.Enable() vs InputActionAsset.Enable()

Enabling only a map (not the asset) can leave other maps in a stale state. Prefer `asset.Enable()` unless you intentionally want per-map control.

---

## Related Tools

- `Input_CreateDualScheme` — orchestrates dual `.inputactions` generation + DualInputHandler scaffold
- `Input_CreateActionMap` — single action map creation (use for per-player maps before dual wiring)
- `Input_AddBinding` — add individual bindings to an action map
