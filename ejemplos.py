"""Los 6 ejemplos del enunciado: cada uno es (fórmula legible, lista de cláusulas de texto)."""

EJEMPLOS = [
    ("p ∧ ¬p",
     [["p"], ["-p"]]),
    ("q ∨ p ∨ ¬p",
     [["q", "p", "-p"]]),
    ("(¬p ∨ ¬r ∨ ¬s) ∧ (¬q ∨ ¬p ∨ ¬s)",
     [["-p", "-r", "-s"], ["-q", "-p", "-s"]]),
    ("(¬p ∨ ¬q) ∧ (q ∨ ¬s) ∧ (¬p ∨ s) ∧ (¬q ∨ s)",
     [["-p", "-q"], ["q", "-s"], ["-p", "s"], ["-q", "s"]]),
    ("(¬p ∨ ¬q ∨ ¬r) ∧ (q ∨ ¬r ∨ p) ∧ (¬p ∨ q ∨ r)",
     [["-p", "-q", "-r"], ["q", "-r", "p"], ["-p", "q", "r"]]),
    ("r ∧ (¬q ∨ ¬r) ∧ (¬p ∨ q ∨ ¬r) ∧ q",
     [["r"], ["-q", "-r"], ["-p", "q", "-r"], ["q"]]),
]
