# Placement Matrix — Golf Paper Craft

| Object | Class | Valid support/surface | Invalid placement | Purpose | Notes |
|---|---|---|---|---|---|
| tree | grounded_object | ground/platform | water/pit/void unless island/platform | air gate / corridor | “tree on water” must be caught |
| rock | grounded_object | ground/platform | water/pit/void unless island/platform | ricochet decision | small radius → easy decorative misuse |
| bridge | traversal_object | spans hazard gap | crosses nothing | traversal | gap>0 enables “plank precision” |
| water | hazard_zone | n/a | goal overlap unless intentional | reset hazard | edges must be readable |
| pit | hazard_zone | n/a | accidental hole confusion | reset hazard | keep intentional separation |
| mud | hazard_zone | ground strip | floating | speed tax | must be readable surface |
| ice | hazard_zone | ground strip | floating | momentum preserve | must be readable surface |

