# Semantic Affordance Grounding for AI Capstone Homework 5

This repository contains Group 13's ontology-based semantic grounding submission
for AI Capstone Homework 5. It models course task objects, task roles,
manipulation affordances, and inferred graspability for a robot agent with a
gripper.

## Group Members

| Name | Student ID |
|---|---|
| 陳詩諺 | 112550004 |
| 謝嘉宸 | 112550019 |
| 徐瑋晨 | 112550047 |
| 蔡烝旭 | 112550099 |
| 游翔宇 | 112550103 |
| 孫傅康 | 112550176 |

## Task Coverage

The entry-level task is cutlery arrangement. To keep the HW5 submission aligned
with the full project setting, the ontology also includes the baseline objects
from cup stacking and toy block collection. The toy block task uses three block
instances.

The advanced extension models the dining cleanup simulator task. In that task,
only `bowl`, `spoon`, and `cloth` are modeled as graspable. `tray`, `tissue`,
and `vase` are modeled as task-relevant but non-graspable objects.

## Repository Structure

| Path | Purpose |
|---|---|
| `README.md` | Repository overview and reproducibility instructions. |
| `report.md` | Written report explaining modeling choices, reasoning pattern, query design, expected results, and limitations. |
| `ontology/group-ontology.ttl` | Group-authored ontology containing metadata, object instances, task instances, affordance individuals, and the graspability reasoning pattern. |
| `ontology/imports/course-affordance.ttl` | Imported course ontology containing shared classes, properties, task roles, affordance classes, and object classes. |
| `ontology/imports/course-alignment.ttl` | Imported course alignment file documenting links to external robotics ontology terms. |
| `ontology/inferred-results.ttl` | Generated graspability memberships, written by `src/run_reasoning.py`. |
| `ontology/shapes.ttl` | SHACL shapes for structural validation of the asserted graph. |
| `queries/graspable_objects.rq` | Required SPARQL query for retrieving inferred graspable objects. |
| `queries/task_objects.rq` | Optional SPARQL query for inspecting modeled task objects, roles, and affordances. |
| `results/graspable_objects_output.txt` | Output of `queries/graspable_objects.rq` over the materialized model. |
| `results/shacl_validation_report.txt` | Output of the SHACL validation run. |
| `results/screenshots/` | Optional screenshots from Protege, Fuseki, Jena, or another reasoning/query interface. |
| `src/run_reasoning.py` | Headless RDFLib workflow that materializes `cap:GraspableObject` memberships and regenerates the query output. |
| `src/run_validation.py` | Headless SHACL validation workflow using pySHACL. |

## Namespaces

| Prefix | Namespace | Usage |
|---|---|---|
| `cap:` | `https://hcis.io/ontology/aicapstone/2026/` | Shared AI Capstone course vocabulary. |
| `g13:` | `https://hcis.io/ontology/aicapstone/2026/group13/` | Group 13 individuals, task instances, and local extension classes. |

Group-specific individuals are declared under `g13:`. Shared course terms such
as `cap:Cup`, `cap:Knife`, `cap:ToyBlock`, `cap:TargetObject`,
`cap:GraspingAffordance`, and `cap:GraspableObject` are reused from the course
vocabulary.

## Modeled Objects and Affordances

| Object instance | Object type | Task role | Asserted affordance individuals | Expected graspable? |
|---|---|---|---|---|
| `g13:blueCup01` | `cap:Cup` | `cap:TargetObject` | `g13:graspingAffordance`, `g13:stackabilityAffordance` | Yes |
| `g13:pinkCup01` | `cap:Cup` | `cap:TargetObject` | `g13:graspingAffordance`, `g13:stackabilityAffordance` | Yes |
| `g13:knife01` | `cap:Knife` | `cap:TargetObject` | `g13:graspingAffordance` | Yes |
| `g13:fork01` | `cap:Fork` | `cap:TargetObject` | `g13:graspingAffordance` | Yes |
| `g13:plate01` | `cap:Plate` | `cap:ReferenceObject` | `g13:supportAffordance` | No |
| `g13:block01` | `cap:ToyBlock` | `cap:CollectableObject` | `g13:graspingAffordance` | Yes |
| `g13:block02` | `cap:ToyBlock` | `cap:CollectableObject` | `g13:graspingAffordance` | Yes |
| `g13:block03` | `cap:ToyBlock` | `cap:CollectableObject` | `g13:graspingAffordance` | Yes |
| `g13:basket01` | `cap:Basket` | `cap:ContainerTarget` | `g13:containmentAffordance` | No |
| `g13:bowl01` | `g13:Bowl` | `cap:TargetObject` | `g13:graspingAffordance` | Yes |
| `g13:spoon01` | `g13:Spoon` | `cap:TargetObject` | `g13:graspingAffordance` | Yes |
| `g13:cloth01` | `g13:Cloth` | `g13:CleanupTool` | `g13:graspingAffordance`, `g13:wipingAffordance` | Yes |
| `g13:tray01` | `g13:Tray` | `cap:ContainerTarget` | `g13:containmentAffordance`, `g13:supportAffordance` | No |
| `g13:tissue01` | `g13:Tissue` | `g13:ProtectedObject` | `g13:stabilityAffordance` | No |
| `g13:vase01` | `g13:Vase` | `g13:ProtectedObject` | `g13:stabilityAffordance` | No |

## Reasoning Pattern

The ontology defines `cap:GraspableObject` as an OWL equivalent class:

```text
cap:GraspableObject == cap:PhysicalObject
                       and cap:hasAffordance some cap:GraspingAffordance
```

The intended inference is:

```text
If an individual is a physical object and has at least one grasping affordance,
then it should be classified as cap:GraspableObject.
```

The following memberships are generated rather than asserted directly in
`ontology/group-ontology.ttl`:

```text
g13:block01
g13:block02
g13:block03
g13:blueCup01
g13:bowl01
g13:cloth01
g13:fork01
g13:knife01
g13:pinkCup01
g13:spoon01
```

The following task-relevant objects are intentionally not inferred as graspable:

```text
g13:basket01
g13:plate01
g13:tray01
g13:tissue01
g13:vase01
```

## Recommended Result Generation

The most reproducible workflow for this repository is the Python CLI workflow.
It requires only `rdflib` and `pyshacl`, both of which are lightweight Python
packages.

```bash
python3 -m pip install rdflib pyshacl
python3 src/run_reasoning.py
python3 src/run_validation.py
```

This regenerates:

```text
ontology/inferred-results.ttl
results/graspable_objects_output.txt
results/shacl_validation_report.txt
```

`src/run_reasoning.py` is not a complete OWL DL reasoner. It materializes the
specific `cap:GraspableObject` equivalent-class rule used in this homework,
including the RDFS subclass hierarchy and the `owl:someValuesFrom` restrictions
used by the course ontology. This gives a deterministic, headless result that is
easy to reproduce in VS Code.

## Optional Protege and Jena Workflow

If a GUI OWL reasoner result is required, use Protege:

1. Open `ontology/group-ontology.ttl`.
2. Confirm that `ontology/imports/course-affordance.ttl` and
   `ontology/imports/course-alignment.ttl` are loaded.
3. Select `Reasoner -> HermiT` or `Reasoner -> Pellet`.
4. Click `Reasoner -> Start reasoner`.
5. Inspect inferred members of `cap:GraspableObject`.
6. Export inferred results to `ontology/inferred-results.ttl`.

After exporting inferred results, Apache Jena can run the required query:

```bash
arq --data ontology/imports/course-affordance.ttl \
    --data ontology/group-ontology.ttl \
    --data ontology/inferred-results.ttl \
    --query queries/graspable_objects.rq \
    > results/graspable_objects_output.txt
```

## Structural Validation

OWL-style reasoning derives class membership; SHACL is used separately to check
that the asserted graph satisfies structural constraints. `ontology/shapes.ttl`
checks that every physical object has an object label, a task role, and at least
one affordance. It also checks that manipulation targets and the advanced cleanup
tool have a grasping affordance.

Run:

```bash
python3 src/run_validation.py
```

The expected report is `Conforms: True`.

## Expected Query Output

The required query should return ten graspable object individuals:

| obj | label | role |
|---|---|---|
| `g13:block01` | `toy_block` | `cap:CollectableObject` |
| `g13:block02` | `toy_block` | `cap:CollectableObject` |
| `g13:block03` | `toy_block` | `cap:CollectableObject` |
| `g13:blueCup01` | `blue_cup` | `cap:TargetObject` |
| `g13:bowl01` | `bowl` | `cap:TargetObject` |
| `g13:cloth01` | `cloth` | `g13:CleanupTool` |
| `g13:fork01` | `fork` | `cap:TargetObject` |
| `g13:knife01` | `knife` | `cap:TargetObject` |
| `g13:pinkCup01` | `pink_cup` | `cap:TargetObject` |
| `g13:spoon01` | `spoon` | `cap:TargetObject` |

## Limitations

This model treats graspability as a semantic affordance. It does not evaluate
geometry, mass, collision, pose uncertainty, gripper aperture, deformability, or
policy success probability. Those constraints can be added later as a stricter
robot-capability extension, but they are outside the baseline HW5 reasoning
pattern.
