# Report: Ontology-based Semantic Grounding

## 1. Project Overview

This report describes Group 13's ontology-based semantic grounding model for AI
Capstone Homework 5. The selected entry-level task is cutlery arrangement, and
the ontology also includes baseline objects from cup stacking and toy block
collection. The toy block task is represented with three blocks, matching the
final project setting.

The advanced extension models the `dining_cleanup` simulator task. It adds
`bowl`, `spoon`, `cloth`, `tray`, `tissue`, and `vase`. Only `bowl`, `spoon`,
and `cloth` are modeled as graspable; `tray`, `tissue`, and `vase` are modeled
as task-relevant but non-graspable objects.

The goal is to model simulated task objects as typed ontology individuals,
connect them to task roles and manipulation affordances, and derive which
objects are graspable by a robot agent with a gripper.

## 2. Repository Contents

| Path | Description |
|---|---|
| `README.md` | Repository overview and reproducibility instructions. |
| `report.md` | This report. |
| `ontology/group-ontology.ttl` | Group-authored ontology. |
| `ontology/imports/course-affordance.ttl` | Imported course ontology. |
| `ontology/imports/course-alignment.ttl` | Imported alignment resource. |
| `ontology/inferred-results.ttl` | Generated graspability memberships. |
| `ontology/shapes.ttl` | SHACL shapes for structural validation. |
| `queries/graspable_objects.rq` | Required query for inferred graspable objects. |
| `queries/task_objects.rq` | Optional query for modeled task objects. |
| `results/graspable_objects_output.txt` | Generated SPARQL query output. |
| `results/shacl_validation_report.txt` | Generated SHACL validation report. |
| `results/screenshots/` | Optional GUI verification screenshots. |
| `src/run_reasoning.py`, `src/run_validation.py` | Headless result-generation and SHACL validation scripts. |

## 3. Namespace Policy

The shared course vocabulary uses:

```turtle
@prefix cap: <https://hcis.io/ontology/aicapstone/2026/> .
```

Group 13 uses:

```turtle
@prefix g13: <https://hcis.io/ontology/aicapstone/2026/group13/> .
```

The `cap:` namespace is used for shared course terms, including object classes,
task roles, affordance classes, properties, and the inferred class
`cap:GraspableObject`. The `g13:` namespace is used for group-specific
individuals, local advanced-task classes, group metadata, and local affordance
individuals.

## 4. Ontology Design

The ontology separates four modeling layers:

| Layer | Purpose | Examples |
|---|---|---|
| Object type | Classifies an object by semantic category. | `cap:Cup`, `cap:Knife`, `cap:ToyBlock`, `g13:Bowl`, `g13:Cloth` |
| Task role | Describes the role an object plays in a task. | `cap:TargetObject`, `cap:ReferenceObject`, `cap:CollectableObject`, `g13:CleanupTool` |
| Affordance | Describes an action possibility. | `cap:GraspingAffordance`, `cap:SupportAffordance`, `cap:ContainmentAffordance`, `g13:WipingAffordance` |
| Instance | Represents a perceived or simulated object. | `g13:blueCup01`, `g13:block03`, `g13:bowl01`, `g13:vase01` |

This distinction prevents task relevance from being confused with graspability.
For example, `g13:tray01` is important because it receives the bowl and spoon,
but it is not modeled as graspable in the advanced cleanup task.

## 5. Modeled Objects

| Instance | Type | Role | Affordance | Expected graspable |
|---|---|---|---|---|
| `g13:blueCup01` | `cap:Cup` | `cap:TargetObject` | grasping, stackability | Yes |
| `g13:pinkCup01` | `cap:Cup` | `cap:TargetObject` | grasping, stackability | Yes |
| `g13:knife01` | `cap:Knife` | `cap:TargetObject` | grasping | Yes |
| `g13:fork01` | `cap:Fork` | `cap:TargetObject` | grasping | Yes |
| `g13:plate01` | `cap:Plate` | `cap:ReferenceObject` | support | No |
| `g13:block01` | `cap:ToyBlock` | `cap:CollectableObject` | grasping | Yes |
| `g13:block02` | `cap:ToyBlock` | `cap:CollectableObject` | grasping | Yes |
| `g13:block03` | `cap:ToyBlock` | `cap:CollectableObject` | grasping | Yes |
| `g13:basket01` | `cap:Basket` | `cap:ContainerTarget` | containment | No |
| `g13:bowl01` | `g13:Bowl` | `cap:TargetObject` | grasping | Yes |
| `g13:spoon01` | `g13:Spoon` | `cap:TargetObject` | grasping | Yes |
| `g13:cloth01` | `g13:Cloth` | `g13:CleanupTool` | grasping, wiping | Yes |
| `g13:tray01` | `g13:Tray` | `cap:ContainerTarget` | containment, support | No |
| `g13:tissue01` | `g13:Tissue` | `g13:ProtectedObject` | stability | No |
| `g13:vase01` | `g13:Vase` | `g13:ProtectedObject` | stability | No |

The ontology defines task individuals for cup stacking, cutlery arrangement, toy
block collection, and advanced dining cleanup. These task individuals connect
tasks to target and reference objects with `cap:hasTargetObject` and
`cap:hasReferenceObject`.

## 6. Key Axiom and Reasoning Pattern

The main inferred class is `cap:GraspableObject`. It is defined in
`ontology/group-ontology.ttl` using an OWL equivalent-class expression:

```text
cap:GraspableObject == cap:PhysicalObject
                       and cap:hasAffordance some cap:GraspingAffordance
```

This axiom means that any physical object with at least one grasping affordance
should be classified as a graspable object. The group ontology asserts object
types, task roles, and affordance relations. It does not manually assert final
`cap:GraspableObject` memberships for task object individuals.

## 7. Expected Inferences

The following ten individuals are expected to be generated as
`cap:GraspableObject`:

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

The following five individuals are not expected to be graspable:

```text
g13:basket01
g13:plate01
g13:tray01
g13:tissue01
g13:vase01
```

This result matches the task assumptions: cups, cutlery targets, toy blocks,
bowl, spoon, and cloth can be grasped; the plate, basket, tray, tissue, and vase
serve as references, containers, or protected objects.

## 8. SPARQL Query Design

The required query is stored in `queries/graspable_objects.rq`. It retrieves all
`cap:GraspableObject` individuals and optionally returns each object's perception
label and task role.

The expected result contains ten graspable object individuals. The query must be
executed over a graph containing the generated `rdf:type cap:GraspableObject`
triples. Querying only the raw asserted graph is insufficient unless a reasoner
or materialization step has already added those triples.

The optional `queries/task_objects.rq` query lists all modeled physical task
objects, their object types, object labels, task roles, and asserted affordance
individuals. This query is useful for debugging the asserted graph before
reasoning.

## 9. Result Generation Workflow

The recommended workflow for this repository is:

```bash
python3 -m pip install rdflib pyshacl
python3 src/run_reasoning.py
python3 src/run_validation.py
```

`src/run_reasoning.py` loads `ontology/group-ontology.ttl`,
`ontology/imports/course-affordance.ttl`, and
`ontology/imports/course-alignment.ttl`. It materializes the graspability
memberships implied by the HW5 equivalent-class rule, writes
`ontology/inferred-results.ttl`, then runs `queries/graspable_objects.rq` and
writes `results/graspable_objects_output.txt`.

This script is not a complete OWL DL reasoner. It implements the exact
graspability materialization needed for this submission, including RDFS subclass
closure and the `owl:someValuesFrom` restrictions used by the course ontology.
For a GUI OWL workflow, the same ontology can be opened in Protege and checked
with HermiT or Pellet.

After exporting inferred results from Protege, Apache Jena can run the query:

```bash
arq --data ontology/imports/course-affordance.ttl \
    --data ontology/group-ontology.ttl \
    --data ontology/inferred-results.ttl \
    --query queries/graspable_objects.rq \
    > results/graspable_objects_output.txt
```

## 10. Structural Validation with SHACL

OWL-style reasoning and SHACL validation play complementary roles. Reasoning
derives new class memberships (`cap:GraspableObject`); SHACL checks that the
asserted graph is structurally well-formed.

The shapes in `ontology/shapes.ttl` encode two constraints:

- every `cap:PhysicalObject` instance must carry at least one
  `cap:hasObjectLabel`, one `cap:hasTaskRole`, and one `cap:hasAffordance`;
- every direct manipulation target, collectable object, and advanced cleanup
  tool must have at least one `cap:GraspingAffordance`.

Running `src/run_validation.py` over the asserted model reports
`Conforms: True`, confirming that all fifteen modeled physical objects satisfy
the expected structure.

## 11. Design Choices and Limitations

The model focuses on semantic affordance grounding rather than geometric grasp
planning. It does not check object dimensions, mass, collision constraints,
gripper aperture, deformability, pose uncertainty, or learned policy success
rates.

The tray, tissue, and vase are intentionally not inferred as graspable in the
advanced dining cleanup model. They are task-relevant objects, but their modeled
affordances are containment, support, or stability rather than grasping.

## 12. Conclusion

This ontology provides a compact semantic layer for the AI Capstone task
environment. It grounds simulated objects as ontology individuals, distinguishes
object type from task role and affordance, defines a formal graspability pattern,
and provides reproducible scripts and SPARQL queries for retrieving inferred
graspable objects.
