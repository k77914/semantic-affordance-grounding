# Validation

This directory contains SHACL shapes for the optional advanced extension.

The shapes check:

- each physical task object has an object label, task role, pose frame, and approximate width;
- each object with a grasping affordance fits within the modeled maximum gripper width.

Generate a validation report with:

```bash
pyshacl -s validation/shapes.ttl --imports -i rdfs -f human ontology/group-ontology.ttl > results/shacl_validation_output.txt
```
