#!/usr/bin/env python3
"""
Headless graspability materialization + SPARQL workflow for Group 13's HW5.

This script is intentionally narrow: it materializes the class memberships
implied by the HW5 axiom in ontology/group-ontology.ttl:

    cap:GraspableObject == cap:PhysicalObject
                          and cap:hasAffordance some cap:GraspingAffordance

It is not a complete OWL DL reasoner. It handles the RDFS subclass hierarchy and
the owl:someValuesFrom restrictions used by this submission, then writes the
materialized cap:GraspableObject triples and runs the required SPARQL query.

Run from the repository root:

    python3 src/run_reasoning.py
"""

from pathlib import Path

from rdflib import BNode, Graph, Namespace, RDF, RDFS, OWL, URIRef

REPO = Path(__file__).resolve().parents[1]
CAP = Namespace("https://hcis.io/ontology/aicapstone/2026/")
G13 = Namespace("https://hcis.io/ontology/aicapstone/2026/group13/")
OWL_IMPORTS = URIRef("http://www.w3.org/2002/07/owl#imports")

GROUP = REPO / "ontology" / "group-ontology.ttl"
AFFORD = REPO / "ontology" / "imports" / "course-affordance.ttl"
ALIGN = REPO / "ontology" / "imports" / "course-alignment.ttl"
INFERRED = REPO / "ontology" / "inferred-results.ttl"
QUERY = REPO / "queries" / "graspable_objects.rq"
OUTPUT = REPO / "results" / "graspable_objects_output.txt"


def load_graph() -> Graph:
    graph = Graph()
    for path in (GROUP, AFFORD, ALIGN):
        graph.parse(path, format="turtle")

    for s, _, o in list(graph.triples((None, OWL_IMPORTS, None))):
        graph.remove((s, OWL_IMPORTS, o))

    return graph


def superclass_closure(graph: Graph, cls: URIRef, cache: dict[URIRef, set[URIRef]]) -> set[URIRef]:
    if cls in cache:
        return cache[cls]

    closure = {cls}
    stack = [cls]
    while stack:
        current = stack.pop()
        for parent in graph.objects(current, RDFS.subClassOf):
            if isinstance(parent, URIRef) and parent not in closure:
                closure.add(parent)
                stack.append(parent)

    cache[cls] = closure
    return closure


def is_subclass_of(
    graph: Graph,
    cls: URIRef,
    target: URIRef,
    class_cache: dict[URIRef, set[URIRef]],
) -> bool:
    return target in superclass_closure(graph, cls, class_cache)


def restriction_requires_grasping(
    graph: Graph,
    restriction: BNode,
    class_cache: dict[URIRef, set[URIRef]],
) -> bool:
    if (restriction, RDF.type, OWL.Restriction) not in graph:
        return False
    if (restriction, OWL.onProperty, CAP.hasAffordance) not in graph:
        return False

    filler = graph.value(restriction, OWL.someValuesFrom)
    return isinstance(filler, URIRef) and is_subclass_of(
        graph,
        filler,
        CAP.GraspingAffordance,
        class_cache,
    )


def class_has_grasping_restriction(
    graph: Graph,
    cls: URIRef,
    class_cache: dict[URIRef, set[URIRef]],
    restriction_cache: dict[URIRef, bool],
) -> bool:
    if cls in restriction_cache:
        return restriction_cache[cls]

    for current in superclass_closure(graph, cls, class_cache):
        for parent in graph.objects(current, RDFS.subClassOf):
            if isinstance(parent, BNode) and restriction_requires_grasping(
                graph,
                parent,
                class_cache,
            ):
                restriction_cache[cls] = True
                return True

    restriction_cache[cls] = False
    return False


def individual_is_physical(
    graph: Graph,
    individual: URIRef,
    class_cache: dict[URIRef, set[URIRef]],
) -> bool:
    for cls in graph.objects(individual, RDF.type):
        if isinstance(cls, URIRef) and is_subclass_of(graph, cls, CAP.PhysicalObject, class_cache):
            return True
    return False


def individual_has_grasping_affordance(
    graph: Graph,
    individual: URIRef,
    class_cache: dict[URIRef, set[URIRef]],
    restriction_cache: dict[URIRef, bool],
) -> bool:
    for affordance in graph.objects(individual, CAP.hasAffordance):
        for affordance_type in graph.objects(affordance, RDF.type):
            if isinstance(affordance_type, URIRef) and is_subclass_of(
                graph,
                affordance_type,
                CAP.GraspingAffordance,
                class_cache,
            ):
                return True

    for cls in graph.objects(individual, RDF.type):
        if isinstance(cls, URIRef) and class_has_grasping_restriction(
            graph,
            cls,
            class_cache,
            restriction_cache,
        ):
            return True

    return False


def infer_graspable_objects(graph: Graph) -> list[URIRef]:
    class_cache: dict[URIRef, set[URIRef]] = {}
    restriction_cache: dict[URIRef, bool] = {}
    candidates = {
        s
        for s, _, _ in graph.triples((None, RDF.type, None))
        if isinstance(s, URIRef)
    }

    inferred = []
    for individual in candidates:
        if individual_is_physical(graph, individual, class_cache) and individual_has_grasping_affordance(
            graph,
            individual,
            class_cache,
            restriction_cache,
        ):
            inferred.append(individual)

    return sorted(inferred, key=str)


def short(term) -> str:
    if term is None:
        return ""
    text = str(term)
    if text.startswith(str(G13)):
        return "g13:" + text[len(str(G13)) :]
    if text.startswith(str(CAP)):
        return "cap:" + text[len(str(CAP)) :]
    return text


def write_inferred(inferred: list[URIRef]) -> None:
    out = Graph()
    out.bind("cap", CAP)
    out.bind("g13", G13)

    for individual in inferred:
        out.add((individual, RDF.type, CAP.GraspableObject))

    header = (
        "# Inferred results for Group 13 HW5.\n"
        "# Generated by src/run_reasoning.py.\n"
        "# Method: RDFLib materialization of the cap:GraspableObject equivalent-class rule\n"
        "# used in ontology/group-ontology.ttl. These memberships are generated from\n"
        "# object type, subclass, and cap:hasAffordance assertions, not manually asserted\n"
        "# in ontology/group-ontology.ttl.\n\n"
    )
    INFERRED.write_text(header + out.serialize(format="turtle"), encoding="utf-8")


def write_query_output() -> None:
    query_graph = Graph()
    for path in (GROUP, AFFORD, INFERRED):
        query_graph.parse(path, format="turtle")

    rows = list(query_graph.query(QUERY.read_text(encoding="utf-8")))

    lines = [
        "# Output of queries/graspable_objects.rq over the materialized model",
        "# Data: ontology/group-ontology.ttl + imports/course-affordance.ttl + inferred-results.ttl",
        "# Engine: rdflib SPARQL; inference: RDFLib graspability materialization.",
        "",
    ]
    header_cols = ["obj", "label", "role"]
    table = [header_cols] + [[short(r.obj), short(r.label), short(r.role)] for r in rows]
    widths = [max(len(row[i]) for row in table) for i in range(3)]
    sep = "-+-".join("-" * width for width in widths)
    for index, row in enumerate(table):
        lines.append(" | ".join(row[col].ljust(widths[col]) for col in range(3)).rstrip())
        if index == 0:
            lines.append(sep)
    lines.append("")
    lines.append(f"# {len(rows)} graspable objects retrieved.")

    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def main() -> int:
    graph = load_graph()
    inferred = infer_graspable_objects(graph)

    print("Materialized cap:GraspableObject memberships:")
    for individual in inferred:
        print(f"  {short(individual)}")

    write_inferred(inferred)
    print(f"\nWrote {INFERRED}")

    write_query_output()
    print(f"\nWrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
