GRAMMAR = {
    'S': [['A', 'B', 'uno']],
    'A': [['dos', 'B'], ['epsilon']],
    'B': [['C', 'D'], ['tres'], ['epsilon']],
    'C': [['cuatro', 'A', 'B'], ['cinco']],
    'D': [['seis'], ['epsilon']],
}

START_SYMBOL = 'S'
NON_TERMINALS = set(GRAMMAR.keys())
TERMINALS = set()
for prods in GRAMMAR.values():
    for prod in prods:
        for sym in prod:
            if sym not in NON_TERMINALS and sym != 'epsilon':
                TERMINALS.add(sym)


def compute_first():
    first = {nt: set() for nt in NON_TERMINALS}
    changed = True
    while changed:
        changed = False
        for nt, productions in GRAMMAR.items():
            for prod in productions:
                before = len(first[nt])
                if prod == ['epsilon']:
                    first[nt].add('epsilon')
                else:
                    all_eps = True
                    for sym in prod:
                        if sym in TERMINALS:
                            first[nt].add(sym)
                            all_eps = False
                            break
                        elif sym in NON_TERMINALS:
                            first[nt].update(first[sym] - {'epsilon'})
                            if 'epsilon' not in first[sym]:
                                all_eps = False
                                break
                    if all_eps:
                        first[nt].add('epsilon')
                if len(first[nt]) > before:
                    changed = True
    return first


def first_of_string(string, first):
    result = set()
    for sym in string:
        if sym == 'epsilon':
            result.add('epsilon')
            break
        elif sym in TERMINALS:
            result.add(sym)
            break
        elif sym in NON_TERMINALS:
            result.update(first[sym] - {'epsilon'})
            if 'epsilon' not in first[sym]:
                break
    else:
        result.add('epsilon')
    return result


def compute_follow(first):

    follow = {nt: set() for nt in NON_TERMINALS}
    follow[START_SYMBOL].add('$')

    changed = True
    while changed:
        changed = False
        for nt, productions in GRAMMAR.items():
            for prod in productions:
                if prod == ['epsilon']:
                    continue
                for i, sym in enumerate(prod):
                    if sym in NON_TERMINALS:
                        before = len(follow[sym])
                        beta = prod[i+1:]

                        if beta:
                            fp = first_of_string(beta, first)
                            follow[sym].update(fp - {'epsilon'})
                            if 'epsilon' in fp:
                                follow[sym].update(follow[nt])
                        else:
                            follow[sym].update(follow[nt])

                        if len(follow[sym]) > before:
                            changed = True
    return follow


if __name__ == '__main__':
    first = compute_first()
    follow = compute_follow(first)

    print("EJERCICIO 2 - Conjuntos SIGUIENTES (FOLLOW)")
    print()
    print("Gramática:")
    for nt, prods in GRAMMAR.items():
        for prod in prods:
            print(f"  {nt} -> {' '.join(prod)}")
    print()
    print("Conjuntos PRIMEROS (necesarios para calcular SIGUIENTES):")
    print("-" * 40)
    for nt in ['S', 'A', 'B', 'C', 'D']:
        simbolos = sorted(first[nt], key=lambda x: (x == 'epsilon', x))
        print(f"  PRIMEROS({nt}) = {{ {', '.join(simbolos)} }}")
    print()
    print("Conjuntos SIGUIENTES de cada no terminal:")
    print("-" * 40)
    for nt in ['S', 'A', 'B', 'C', 'D']:
        simbolos = sorted(follow[nt], key=lambda x: (x == '$', x))
        print(f"  SIGUIENTES({nt}) = {{ {', '.join(simbolos)} }}")
