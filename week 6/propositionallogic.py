import itertools
import re

def eval_expr(expr, model):
    expr = expr.replace("<->", " == ")
    expr = expr.replace("->", " <= ")
    expr = re.sub(r'~(\w+)', r'(not \1)', expr)
    expr = re.sub(r'~\(([^)]+)\)', r'(not (\1))', expr)
    expr = expr.replace("^", " and ")
    expr = expr.replace("v", " or ")
    for s, v in model.items():
        expr = re.sub(r'\b' + re.escape(s) + r'\b', str(v), expr)
    return eval(expr)

def truth_table_entails(kb, query, symbols):
    entail = True
    combos = list(itertools.product([True, False], repeat=len(symbols)))
    print("Truth Table Evaluation:\n")
    head = " | ".join(symbols) + " | KB | Query | KB ⇒ Query"
    print(head)
    print("-" * len(head) * 2)
    for vals in combos:
        model = dict(zip(symbols, vals))
        kb_val = eval_expr(kb, model)
        q_val = eval_expr(query, model)
        implies = (not kb_val) or q_val
        if kb_val and not q_val:
            entail = False
        row = " | ".join(['T' if v else 'F' for v in vals])
        row += f" | {'T' if kb_val else 'F'}  | {'T' if q_val else 'F'}   | {'T' if implies else 'F'}"
        print(row)
    print("\nResult:")
    if entail:
        print("The Knowledge Base entails the Query (KB ⊨ Query)")
    else:
        print("The Knowledge Base does NOT entail the Query (KB ⊭ Query)")

kb = "(Q -> P) ^ (P -> ~Q) ^ (Q v R)"
symbols = ["P", "Q", "R"]
queries = ["R", "R -> P", "Q -> R"]

for q in queries:
    print(f"\nEvaluating Query: {q}\n")
    truth_table_entails(kb, q, symbols)
    print("\n" + "="*50 + "\n")
