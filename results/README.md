# Results

This directory stores generated outputs after reasoning and SPARQL query execution.

Expected generated file:

- `graspable_objects_output.txt`: output of `queries/graspable_objects.rq` executed over the inferred model.
- `gripper_fit_candidates_output.txt`: optional bonus output of `queries/gripper_fit_candidates.rq` executed over the inferred model.
- `shacl_validation_output.txt`: optional bonus SHACL validation report.

These files are not manually authored. Generate them after exporting `ontology/inferred-results.ttl`.
