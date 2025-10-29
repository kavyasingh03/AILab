def var(x):
    return isinstance(x, str) and x.islower()

def const(x):
    return isinstance(x, str) and x[0].isupper()

def occurs(v, e, s):
    if v == e:
        return True
    elif isinstance(e, list):
        return any(occurs(v, el, s) for el in e)
    elif e in s:
        return occurs(v, s[e], s)
    return False

def unify(a, b, s=None, d=0):
    tab = "  " * d
    if s is None:
        print(tab + "Substitution failed.")
        return None
    print(tab + f"Unify({a}, {b}) with subst = {s}")
    if a == b:
        print(tab + "Terms are identical, no change.")
        return s
    elif var(a):
        return unify_var(a, b, s, d)
    elif var(b):
        return unify_var(b, a, s, d)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            print(tab + "Lists have different lengths. Fail.")
            return None
        for x1, x2 in zip(a, b):
            s = unify(x1, x2, s, d + 1)
            if s is None:
                print(tab + "Failed to unify list elements.")
                return None
        return s
    else:
        print(tab + "Cannot unify different constants or structures. Fail.")
        return None

def unify_var(v, x, s, d):
    tab = "  " * d
    if v in s:
        print(tab + f"{v} is in subst, unify({s[v]}, {x})")
        return unify(s[v], x, s, d + 1)
    elif var(x) and x in s:
        print(tab + f"{x} is in subst, unify({v}, {s[x]})")
        return unify(v, s[x], s, d + 1)
    elif occurs(v, x, s):
        print(tab + f"Occurs check failed: {v} occurs in {x}")
        return None
    else:
        print(tab + f"Add {v} -> {x} to subst")
        s[v] = x
        return s

e1 = ['f', 'X', ['g', 'Y']]
e2 = ['f', 'a', ['g', 'b']]

print("Starting Unification:\n")
res = unify(e1, e2, s={})
print("\nFinal Unification Result:", res)
