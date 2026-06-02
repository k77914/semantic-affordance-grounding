# Report: Ontology-based Semantic Grounding

## 1. Project Overview

This report describes Group 13's ontology-based semantic grounding model for AI Capstone Homework 5. The selected entry-level task is cutlery arrangement, but the ontology also includes all required baseline objects from cup stacking and toy block collection.

The goal is to model perceived or simulated task objects as typed ontology individuals, connect them to task roles and manipulation affordances, and infer which objects are graspable by a robot agent with a gripper.

## 2. Repository Contents

The repository is organized as follows:

| Path | Description |
|---|---|
| `README.md` | Repository overview and reproducibility instructions. |
| `report.md` | This report. |
| `ontology/group-ontology.ttl` | Group-authored ontology. |
| `ontology/imports/course-affordance.ttl` | Imported course ontology. |
| `ontology/imports/course-alignment.ttl` | Imported SKOS alignment resource. |
| `ontology/inferred-results.ttl` | Generated after OWL reasoning. |
| `queries/graspable_objects.rq` | Required query for inferred graspable objects. |
| `queries/task_objects.rq` | Optional query for modeled task objects. |
| `results/graspable_objects_output.txt` | Generated SPARQL query output. |
| `results/screenshots/` | Optional GUI verification screenshots. |

## 3. Namespace Policy

The shared course vocabulary uses:

```turtle
@prefix cap: <https://hcis.io/ontology/aicapstone/2026/> .
```

Group 13 uses:

```turtle
@prefix g13: <https://hcis.io/ontology/aicapstone/2026/group13/> .
```

The `cap:` namespace is used for shared course terms, including object classes, task roles, affordance classes, properties, and the inferred class `cap:GraspableObject`. The `g13:` namespace is used for group-specific individuals such as observed objects, task instances, group metadata, and local affordance individuals.

## 4. Ontology Design

The ontology separates four modeling layers:

| Layer | Purpose | Examples |
|---|---|---|
| Object type | Classifies an object by semantic category. | `cap:Cup`, `cap:Knife`, `cap:Fork`, `cap:Plate`, `cap:ToyBlock`, `cap:Basket` |
| Task role | Describes the role an object plays in a task. | `cap:TargetObject`, `cap:ReferenceObject`, `cap:CollectableObject`, `cap:ContainerTarget` |
| Affordance | Describes an action possibility. | `cap:GraspingAffordance`, `cap:SupportAffordance`, `cap:ContainmentAffordance`, `cap:StackabilityAffordance` |
| Instance | Represents a perceived or simulated object. | `g13:blueCup01`, `g13:knife01`, `g13:block01` |

This distinction prevents task relevance from being confused with graspability. For example, `g13:plate01` is relevant to cutlery arrangement as a reference object, but it is not modeled as graspable in the current task context.

## 5. Modeled Objects

| Instance | Type | Role | Affordance | Expected graspable |
|---|---|---|---|---|
| `g13:blueCup01` | `cap:Cup` | `cap:TargetObject` | grasping, stackability | Yes |
| `g13:pinkCup01` | `cap:Cup` | `cap:TargetObject` | grasping, stackability | Yes |
| `g13:knife01` | `cap:Knife` | `cap:TargetObject` | grasping | Yes |
| `g13:fork01` | `cap:Fork` | `cap:TargetObject` | grasping | Yes |
| `g13:plate01` | `cap:Plate` | `cap:ReferenceObject` | support | No |
| `g13:block01` | `cap:ToyBlock` | `cap:CollectableObject` | grasping | Yes |
| `g13:basket01` | `cap:Basket` | `cap:ContainerTarget` | containment | No |

The ontology also defines task individuals for cup stacking, cutlery arrangement, and toy block collection. These task individuals connect tasks to target and reference objects with `cap:hasTargetObject` and `cap:hasReferenceObject`.

## 6. Key Axioms and Reasoning Pattern

The main inferred class is `cap:GraspableObject`. It is defined in `ontology/group-ontology.ttl` using an OWL equivalent-class expression:

```text
cap:GraspableObject ≡ cap:PhysicalObject
                      AND cap:hasAffordance some cap:GraspingAffordance
```

This axiom means that any physical object with at least one grasping affordance should be classified as a graspable object by an OWL reasoner.

The group ontology asserts object types, task roles, and affordance relations. It does not manually assert the final `cap:GraspableObject` class memberships for the task object individuals. Those memberships should be produced by the reasoning workflow.

## 7. Expected Inferences

The following individuals are expected to be inferred as `cap:GraspableObject`:

```text
g13:blueCup01
g13:pinkCup01
g13:knife01
g13:fork01
g13:block01
```

The following individuals are not expected to be inferred as graspable under the current model:

```text
g13:plate01
g13:basket01
```

This is because `g13:plate01` has a support affordance and `g13:basket01` has a containment affordance, but neither is asserted with a grasping affordance in this task model.

## 8. SPARQL Query Design

The required query is stored in `queries/graspable_objects.rq`. It retrieves all inferred `cap:GraspableObject` individuals and optionally returns each object's perception label and task role.

The expected result contains the five graspable object individuals listed above. The query must be executed over an inferred model or a graph containing the inferred class memberships. Querying only the raw asserted graph is insufficient unless the reasoner has already materialized the inferred `rdf:type cap:GraspableObject` triples.

The optional `queries/task_objects.rq` query lists all modeled physical task objects, their object types, object labels, task roles, and asserted affordance individuals. This query is useful for debugging the asserted graph before reasoning.

## 9. Reasoning and Result Generation Workflow

The recommended workflow is:

1. Open `ontology/group-ontology.ttl` in Protege.
2. Confirm that `ontology/imports/course-affordance.ttl` and `ontology/imports/course-alignment.ttl` are loaded.
3. Run an OWL reasoner such as HermiT or Pellet.
4. Check the inferred members of `cap:GraspableObject`.
5. Export the inferred graph to `ontology/inferred-results.ttl`.
6. Run `queries/graspable_objects.rq` over the inferred graph.
7. Save the result as `results/graspable_objects_output.txt`.

An Apache Jena workflow can be used after the inferred graph is exported:

```bash
arq --data ontology/imports/course-affordance.ttl \
    --data ontology/group-ontology.ttl \
    --data ontology/inferred-results.ttl \
    --query queries/graspable_objects.rq \
    > results/graspable_objects_output.txt
```

## 10. Design Choices and Limitations

The model focuses on semantic affordance grounding rather than geometric grasp planning. It does not check object dimensions, mass, pose uncertainty, collision constraints, gripper aperture, or learned policy success rates.

The plate and basket are intentionally not inferred as graspable in the current model. They are task-relevant objects, but their modeled affordances are support and containment, respectively. If a later robot workflow requires moving the plate or basket, the ontology can be extended by adding task-specific grasping affordances for those objects.

## 11. Conclusion

This ontology provides a compact semantic layer for the AI Capstone task environment. It grounds perceived or simulated objects as ontology individuals, distinguishes object type from task role and affordance, defines a formal graspability reasoning pattern, and provides SPARQL queries for retrieving inferred graspable objects.
