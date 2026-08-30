"""CS 505 Module Eight activity: executable models and verification.

Run: python3 cs505_relations_recursion_models.py
The report is also saved to cs505_model_outputs/results.txt. Optional PNG
figures are created when Matplotlib is installed.

Important: finite tests illustrate and check examples; they do not replace the
written general proofs required for congruence, inverse functions, or induction.
"""
from itertools import product
from pathlib import Path
from time import perf_counter

def function_properties(domain, codomain, mapping):
    values=[mapping[x] for x in domain]
    injective=len(values)==len(set(values))
    surjective=set(values)==set(codomain)
    return injective,surjective

def relation_properties(universe, relation):
    relation=set(relation)
    missing_reflexive=[(x,x) for x in universe if (x,x) not in relation]
    missing_symmetric=[(y,x) for x,y in relation if (y,x) not in relation]
    missing_transitive=[]
    for x,y in relation:
        for middle,z in relation:
            if y==middle and (x,z) not in relation:
                missing_transitive.append(((x,y),(y,z),(x,z)))
    return {
        "reflexive":not missing_reflexive,
        "symmetric":not missing_symmetric,
        "transitive":not missing_transitive,
        "missing_reflexive":sorted(missing_reflexive),
        "symmetric_counterexamples":sorted(missing_symmetric),
        "transitive_counterexamples":sorted(set(missing_transitive)),
    }

def compose(first, second):
    """first ∘ second: apply second, then first."""
    return {(x,z) for x,y in second for middle,z in first if y==middle}

def inverse_mapping(mapping):
    if len(set(mapping.values())) != len(mapping):
        raise ValueError("An inverse function requires an injective mapping")
    return {value:key for key,value in mapping.items()}

def factorial(n):
    if n<0: raise ValueError("n must be nonnegative")
    return 1 if n==0 else n*factorial(n-1)

def fibonacci(n):
    if n<0: raise ValueError("n must be nonnegative")
    if n<2: return n
    return fibonacci(n-1)+fibonacci(n-2)

def recursive_sum(arr,n=None,counter=None):
    if n is None: n=len(arr)
    if counter is not None: counter["calls"]+=1
    if n==0: return 0
    return arr[n-1]+recursive_sum(arr,n-1,counter)

def iterative_sum(arr):
    total=0
    for value in arr: total+=value
    return total

def line(title=""):
    return f"\n{'='*72}\n{title}\n{'='*72}" if title else ""

def build_report():
    out=[]
    A={1,2,3}; B={'a','b','c'}
    f1={1:'a',2:'b',3:'c'}
    out += [line("1–2. FUNCTIONS"),f"f = {f1}",f"Injective, surjective = {function_properties(A,B,f1)}"]
    all_injective=[dict(zip(sorted(A),values)) for values in product(sorted(B),repeat=3)
                   if len(set(values))==3]
    non_onto=[m for m in all_injective if not function_properties(A,B,m)[1]]
    out.append(f"Injective but non-surjective A→B mappings found: {len(non_onto)} (expected 0)")
    bigger={'a','b','c','d'}; f2={1:'a',2:'b',3:'c'}
    out.append(f"Extended codomain example: {f2}; properties={function_properties(A,bigger,f2)}")

    R={(1,3),(1,2),(2,2)}; S={(1,2),(2,3),(3,1)}
    R4={(1,1),(1,3),(2,1),(2,3),(3,3)}
    out += [line("3–4. RELATION PROPERTIES"),f"R: {relation_properties(A,R)}",
            f"S: {relation_properties(A,S)}",f"Problem 4 R: {relation_properties(A,R4)}"]

    # A concrete sibling model illustrates the logical properties in 5–7.
    people={'Alex','Blair','Casey'}
    siblings={('Alex','Blair'),('Blair','Alex'),('Blair','Casey'),('Casey','Blair')}
    out += [line("5–7. SIBLING RELATION MODEL"),f"Relation: {sorted(siblings)}",
            f"Properties: {relation_properties(people,siblings)}",
            "The model is symmetric, not reflexive, and not transitive."]

    sample=range(-12,13)
    mod6={(x,y) for x in sample for y in sample if (x-y)%6==0}
    classes={r:[x for x in sample if x%6==r] for r in range(6)}
    out += [line("8–9. CONGRUENCE MODULO 6"),
            f"Finite sample properties: {relation_properties(set(sample),mod6)}",
            "Sample equivalence classes:"]
    out += [f"  [{r}] = {values}" for r,values in classes.items()]
    out.append("The written divisibility argument is still needed to prove the result on all integers.")

    out += [line("10. COMPOSITION OF RELATIONS"),
            f"R ∘ S = {sorted(compose(R,S))}",f"S ∘ R = {sorted(compose(S,R))}"]

    inv=inverse_mapping(f1)
    out += [line("11. INVERSE FUNCTION MODEL"),f"f = {f1}",f"f⁻¹ = {inv}",
            f"f⁻¹ properties = {function_properties(B,A,inv)}"]

    out += [line("12–13. RECURSIVE FACTORIAL AND FIBONACCI"),
            "n | factorial(n) | Fibonacci(n)"]
    out += [f"{n:>1} | {factorial(n):>12} | {fibonacci(n):>12}" for n in range(11)]
    out.append("These computed cases support testing; the induction arguments prove correctness generally.")

    out += [line("14–16. RECURSIVE SUM COMPLEXITY"),"n | result | recursive calls | predicted depth n+1"]
    for n in (0,1,5,10,25,100):
        data=list(range(1,n+1)); counter={"calls":0}; result=recursive_sum(data,counter=counter)
        assert result==iterative_sum(data)==sum(data)
        out.append(f"{n:>3} | {result:>6} | {counter['calls']:>15} | {n+1:>19}")
    out += ["Measured call count is n+1, matching T(n)=T(n-1)+Θ(1)=Θ(n).",
            "Recursive auxiliary stack space is Θ(n); iterative auxiliary space is Θ(1)."]
    return "\n".join(out)+"\n"

def save_models(output_dir):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        return False
    output_dir.mkdir(parents=True,exist_ok=True)
    sizes=list(range(1,301,10)); recursive_calls=[n+1 for n in sizes]; iterative_space=[1]*len(sizes)
    fig,ax=plt.subplots(figsize=(7,4.5)); ax.plot(sizes,recursive_calls,label='Recursive stack frames (n+1)'); ax.plot(sizes,iterative_space,label='Iterative auxiliary space (constant)')
    ax.set(title='Recursive vs. Iterative Sum Space Model',xlabel='Input size n',ylabel='Relative auxiliary units'); ax.grid(alpha=.25); ax.legend(); fig.tight_layout(); fig.savefig(output_dir/'recursive_sum_space.png',dpi=180); plt.close(fig)
    # Visualize modulo classes as six horizontal groups.
    fig,ax=plt.subplots(figsize=(8,4.5))
    for r in range(6):
        values=[x for x in range(-18,19) if x%6==r]; ax.scatter(values,[r]*len(values),label=f'[{r}]')
    ax.set(title='Equivalence Classes Modulo 6',xlabel='Integer sample',ylabel='Remainder class',yticks=range(6)); ax.grid(axis='x',alpha=.2); fig.tight_layout(); fig.savefig(output_dir/'mod6_equivalence_classes.png',dpi=180); plt.close(fig)
    return True

def main():
    report=build_report(); print(report)
    out=Path(__file__).resolve().parent/'cs505_model_outputs'; out.mkdir(exist_ok=True)
    (out/'results.txt').write_text(report,encoding='utf-8')
    made=save_models(out)
    print(f"Saved report{' and figures' if made else ''} to {out}")

if __name__=='__main__': main()
