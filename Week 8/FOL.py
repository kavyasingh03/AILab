# -*- coding: utf-8 -*-
from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt

# -----------------------------------------------------
# Knowledge Base (KB)
# -----------------------------------------------------
KB = [
    {"if": ["American(p)", "Weapon(q)", "Sells(p, q, r)", "Hostile(r)"], "then": "Criminal(p)"},
    {"if": ["Missile(x)"], "then": "Weapon(x)"},
    {"if": ["Enemy(x, America)"], "then": "Hostile(x)"},
    {"if": ["Missile(x)", "Owns(A, x)"], "then": "Sells(Robert, x, A)"},
    {"fact": "American(Robert)"},
    {"fact": "Enemy(A, America)"},
    {"fact": "Missile(T1)"},
    {"fact": "Owns(A, T1)"}
]

goal = "Criminal(Robert)"


# -----------------------------------------------------
# Helper functions
# -----------------------------------------------------
def parse_predicate(expr):
    pred, args_str = expr.split("(")
    args = args_str[:-1].split(",")
    return pred.strip(), [a.strip() for a in args]


def is_variable(term):
    return term[0].islower()


def unify(expr1, expr2, subs=None):
    """Unify two predicates expr1 and expr2."""
    if subs is None:
        subs = {}
    p1, args1 = parse_predicate(expr1)
    p2, args2 = parse_predicate(expr2)
    if p1 != p2 or len(args1) != len(args2):
        return None
    for t1, t2 in zip(args1, args2):
        if t1 == t2:
            continue
        elif is_variable(t1):
            subs[t1] = t2
        elif is_variable(t2):
            subs[t2] = t1
        else:
            return None
    return subs


def substitute(expr, subs):
    pred, args = parse_predicate(expr)
    new_args = []
    for a in args:
        while a in subs:
            a = subs[a]
        new_args.append(a)
    return f"{pred}({', '.join(new_args)})"


# -----------------------------------------------------
# Forward Chaining Algorithm + Graph Recording
# -----------------------------------------------------
def FOL_FC_ASK(KB, query):
    known_facts = {item["fact"] for item in KB if "fact" in item}
    rules = [item for item in KB if "if" in item]
    inference_edges = []

    print("Initial known facts:")
    for f in known_facts:
        print("  ", f)
    print()

    new_facts_added = True

    while new_facts_added:
        new_facts_added = False

        for rule in rules:
            premises = rule["if"]
            conclusion = rule["then"]

            substitutions_list = [{}]

            for premise in premises:
                new_substitutions = []
                for subs in substitutions_list:
                    premise_substituted = substitute(premise, subs)
                    for fact in known_facts:
                        new_subs = unify(premise_substituted, fact, deepcopy(subs))
                        if new_subs is not None:
                            new_substitutions.append(new_subs)
                substitutions_list = new_substitutions
                if not substitutions_list:
                    break

            for subs in substitutions_list:
                inferred_fact = substitute(conclusion, subs)
                if inferred_fact not in known_facts:
                    print(f"Inferred: {inferred_fact}")
                    known_facts.add(inferred_fact)
                    new_facts_added = True

                    # record edges for graph
                    for premise in premises:
                        inference_edges.append((substitute(premise, subs), inferred_fact))

                    # stop if query is reached
                    if unify(inferred_fact, query):
                        print("\nQuery satisfied:", query)
                        visualize_graph(inference_edges, query)
                        return True

    print("\nQuery cannot be proved.")
    visualize_graph(inference_edges, query)
    return False


# -----------------------------------------------------
# Visualization
# -----------------------------------------------------
def visualize_graph(edges, goal):
    G = nx.DiGraph()
    G.add_edges_from(edges)

    plt.figure(figsize=(12, 7))
    pos = nx.spring_layout(G, seed=42)

    node_colors = ["lightgreen" if n == goal else "lightblue" for n in G.nodes()]
    nx.draw(
        G, pos, with_labels=True, node_color=node_colors,
        node_size=2200, font_size=10, font_weight="bold",
        arrows=True, arrowstyle="-|>", arrowsize=12
    )

    plt.title("Forward Chaining Inference Graph", fontsize=14, fontweight="bold")
    plt.show()


# -----------------------------------------------------
# Run Program
# -----------------------------------------------------
print("\n--- Forward Chaining (FOL-FC-ASK) ---\n")
FOL_FC_ASK(KB, goal)
