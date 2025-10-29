# === STEP 1: Input FOL Statements ===

FOL_data = {
    'a': "∀x: food(x) → likes(John, x)",
    'b': "food(Apple) ∧ food(Vegetables)",
    'c': "∀x∀y: eats(x, y) ∧ ¬killed(x) → food(y)",
    'd': "eats(Anil, Peanuts) ∧ alive(Anil)",
    'e': "∀x: eats(Anil, x) → eats(Harry, x)",
    'f': "∀x: ¬killed(x) → alive(x)",
    'g': "∀x: alive(x) → ¬killed(x)",
    'h': "likes(John, Peanuts)"
}

print("=== STEP 1: Given FOL Statements ===")
for label, formula in FOL_data.items():
    print(f"{label}. {formula}")

# === STEP 2: Remove Implications ===

print("\n=== STEP 2: After Removing Implications ===")

CNF_no_implications = {
    'a': "¬food(x) ∨ likes(John, x)",
    'b1': "food(Apple)",
    'b2': "food(Vegetables)",
    'c': "¬eats(x, y) ∨ killed(x) ∨ food(y)",
    'd1': "eats(Anil, Peanuts)",
    'd2': "alive(Anil)",
    'e': "¬eats(Anil, x) ∨ eats(Harry, x)",
    'f': "killed(x) ∨ alive(x)",
    'g': "¬alive(x) ∨ ¬killed(x)",
    'h': "likes(John, Peanuts)"
}

for label, clause in CNF_no_implications.items():
    print(f"{label}. {clause}")

# === STEP 3: Standardize Variables ===

print("\n=== STEP 3: Standardized Variables (Dropped Quantifiers) ===")
for key, val in CNF_no_implications.items():
    print(f"{key}. {val}")

# === STEP 4: Final CNF Knowledge Base ===

print("\n=== STEP 4: Final CNF Clauses ===")

CNF_final = [
    "¬food(x) ∨ likes(John, x)",
    "food(Apple)",
    "food(Vegetables)",
    "¬eats(y, z) ∨ killed(y) ∨ food(z)",
    "eats(Anil, Peanuts)",
    "alive(Anil)",
    "¬eats(Anil, w) ∨ eats(Harry, w)",
    "killed(g) ∨ alive(g)",
    "¬alive(k) ∨ ¬killed(k)",
    "likes(John, Peanuts)"
]

for i, clause in enumerate(CNF_final, start=1):
    print(f"{i}. {clause}")

# === STEP 5: Resolution Proof ===

print("\n=== STEP 5: Resolution Proof ===")

resolution_steps = [
    ("1", "Negate the Goal", "¬likes(John, Peanuts)"),
    ("2", "Resolve (1) with (¬food(x) ∨ likes(John, x)) using {x/Peanuts}", "¬food(Peanuts)"),
    ("3", "Resolve (2) with (¬eats(y,z) ∨ killed(y) ∨ food(z)) using {z/Peanuts}", "¬eats(y,Peanuts) ∨ killed(y)"),
    ("4", "Resolve (3) with (eats(Anil, Peanuts)) using {y/Anil}", "killed(Anil)"),
    ("5", "Resolve (4) with (¬alive(k) ∨ ¬killed(k)) using {k/Anil}", "¬alive(Anil)"),
    ("6", "Resolve (5) with (alive(Anil))", "⊥ (Contradiction)")
]

for step_num, description, outcome in resolution_steps:
    print(f"Step {step_num}: {description}")
    print(f"      ⇒ {outcome}\n")

print("Contradiction reached ⇒ Therefore, John likes Peanuts is TRUE.\n")
