# Source

This folder contains the headless result-generation and validation workflows used
by the HW5 submission.

## `run_reasoning.py`

A single self-contained script that:

1. Loads `ontology/group-ontology.ttl` with the imported course ontology files.
2. Materializes the `cap:GraspableObject` memberships implied by the HW5 rule:

   ```text
   cap:GraspableObject == cap:PhysicalObject
                          and cap:hasAffordance some cap:GraspingAffordance
   ```

3. Writes those generated `rdf:type cap:GraspableObject` triples to
   `ontology/inferred-results.ttl`.
4. Executes `queries/graspable_objects.rq` over the asserted + generated graph
   and saves the formatted result to `results/graspable_objects_output.txt`.

The script is intentionally narrower than a full OWL DL reasoner. It supports
the RDFS subclass hierarchy and the `owl:someValuesFrom` restrictions used by
this submission, which is enough to reproduce the required graspability result
without depending on a GUI reasoner or Java tooling.

### Requirements

```bash
python3 -m pip install rdflib
```

### Run

From the repository root:

```bash
python3 src/run_reasoning.py
```

This regenerates `ontology/inferred-results.ttl` and
`results/graspable_objects_output.txt`.

## `run_validation.py`

Runs SHACL structural validation of `ontology/shapes.ttl` against the asserted
graph and writes `results/shacl_validation_report.txt`. This is separate from
reasoning: the reasoning workflow generates `cap:GraspableObject` membership,
while SHACL checks that every object has the expected labels, task roles, and
affordances.

```bash
python3 -m pip install pyshacl rdflib
python3 src/run_validation.py
```

## Alternative GUI Workflow

The same ontology can be inspected in Protege. Open `group-ontology.ttl`, load
the imports, run HermiT or Pellet, inspect the inferred members of
`cap:GraspableObject`, and export the inferred axioms if a GUI reasoner artifact
is required.
