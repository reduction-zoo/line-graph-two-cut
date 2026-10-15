module

public import Mathlib.Computability.TuringMachine.Computable

@[expose] public section

namespace LineGraphTwoCut

/-- Q001's self-delimiting binary natural; length is logarithmic, not unary. -/
def encodeNat (n : Nat) : List Bool :=
  let bits := (Nat.toDigits 2 n).map (fun c => c == '1')
  List.replicate bits.length true ++ [false] ++ bits

def encodeList {α : Type} (encode : α → List Bool) (xs : List α) : List Bool :=
  encodeNat xs.length ++ xs.flatMap encode

def encodeOption {α : Type} (encode : α → List Bool) : Option α → List Bool
  | none => [false]
  | some x => true :: encode x

/-- None denotes mathematical nonexistence, never an execution error. -/
def searchOutput {I W : Type} (legal : I → Bool) (witness : I → W → Bool)
    (x : I) : Option W → Prop
  | some w => legal x = true ∧ witness x w = true
  | none => legal x = true ∧ ¬ ∃ w, witness x w = true

/-- Relational version for witnesses with quantified real or optimality conditions. -/
def relationalOutput {I W : Type} (legal : I → Bool) (witness : I → W → Prop)
    (x : I) : Option W → Prop
  | some w => legal x = true ∧ witness x w
  | none => legal x = true ∧ ¬ ∃ w, witness x w

structure Graph where
  n : Nat
  edges : List (Nat × Nat)
  deriving Repr

def adjacent (g : Graph) (u v : Nat) : Bool :=
  g.edges.any (fun e => (e.1 == u && e.2 == v) || (e.1 == v && e.2 == u))

def simple (g : Graph) : Bool :=
  g.edges.all (fun e => e.1 < g.n && e.2 < g.n && e.1 != e.2) &&
  decide ((g.edges.map (fun e => (min e.1 e.2, max e.1 e.2))).Nodup)

/-- Vertices at distance at most the supplied bound, including the starting set. -/
def ballFrom (g : Graph) : Nat → List Nat → List Nat
  | 0, seen => seen
  | k + 1, seen => ballFrom g k ((List.range g.n).filter (fun v =>
      seen.contains v || seen.any (fun u => adjacent g u v)))

def connected (g : Graph) : Bool :=
  g.n > 0 && (ballFrom g g.n [0]).length == g.n

def diameterAtMost (g : Graph) (d : Nat) : Bool :=
  (List.range g.n).all (fun v => (ballFrom g d [v]).length == g.n)

def radiusAtMost (g : Graph) (r : Nat) : Bool :=
  (List.range g.n).any (fun v => (ballFrom g r [v]).length == g.n)

def boolWords : Nat → List (List Bool)
  | 0 => [[]]
  | n + 1 => (boolWords n).flatMap (fun xs => [false :: xs, true :: xs])

def bipartite (g : Graph) : Bool :=
  (boolWords g.n).any (fun side => g.edges.all (fun e => side[e.1]? != side[e.2]?))

def crossingDegree (g : Graph) (side : List Bool) (v : Nat) : Nat :=
  ((List.range g.n).filter (fun u => adjacent g u v && side[u]? != side[v]?)).length

def nontrivialCut (g : Graph) (side : List Bool) : Bool :=
  side.length == g.n && side.contains true && side.contains false

def perfectCut (g : Graph) (side : List Bool) : Bool :=
  nontrivialCut g side && (List.range g.n).all (fun v => crossingDegree g side v == 1)

def boundedCut (g : Graph) (d : Nat) (side : List Bool) : Bool :=
  nontrivialCut g side && (List.range g.n).all (fun v => crossingDegree g side v ≤ d)

def encodeGraph (g : Graph) : List Bool :=
  encodeList encodeNat (List.range g.n) ++
  encodeList (fun e => encodeNat e.1 ++ encodeNat e.2) g.edges
def words (alphabet : Nat) : Nat → List (List Nat)
  | 0 => [[]]
  | k+1 => (List.range alphabet).flatMap (fun v => (words alphabet k).map (v :: ·))

def legalSource (g : Graph) : Bool := simple g && connected g &&
  (List.range g.n).all (fun v => ((List.range g.n).filter (adjacent g v)).length ≤ 4)
def rootEncoding (g : Graph) (ends : List (Nat × Nat)) : Bool :=
  ends.length == g.n && ends.all (fun e => e.1 < 2*g.n && e.2 < 2*g.n && e.1 != e.2) &&
  decide ((ends.map (fun e => (min e.1 e.2,max e.1 e.2))).Nodup) &&
  (List.range g.n).all (fun u => (List.range g.n).all (fun v =>
    if u == v then true else
      let a := ends[u]?.getD (0,0)
      let b := ends[v]?.getD (0,0)
      adjacent g u v == (a.1 == b.1 || a.1 == b.2 || a.2 == b.1 || a.2 == b.2)))
def lineGraph (g : Graph) : Bool :=
  (words (2*g.n) (2*g.n)).any (fun xs =>
    rootEncoding g ((List.range g.n).map (fun i => (xs[2*i]?.getD 0,xs[2*i+1]?.getD 0))))
def legalTarget (g : Graph) := simple g && connected g && lineGraph g
def validSourceOutput := searchOutput legalSource (fun g => boundedCut g 1)
def validTargetOutput := searchOutput legalTarget (fun g => boundedCut g 2)

/-- Both algorithms use Q001's explicit bit encoding and TM2 cost model.
Recovery receives the full pair of source instance and target output. -/
def Reduction (forward : Graph → Graph)
    (recover : Graph × Option (List Bool) → Option (List Bool)) : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime encodeGraph encodeGraph forward) ∧
  Nonempty (Turing.TM2ComputableInPolyTime
    (fun input => encodeGraph input.1 ++ (encodeOption (encodeList (fun b => [b]))) input.2)
    (encodeOption (encodeList (fun b => [b]))) recover) ∧
  (∃ bound : Polynomial Nat, ∀ x,
    (encodeGraph (forward x)).length ≤ bound.eval (encodeGraph x).length) ∧
  (∃ bound : Polynomial Nat, ∀ input,
    ((encodeOption (encodeList (fun b => [b]))) (recover input)).length ≤
      bound.eval (encodeGraph input.1 ++ (encodeOption (encodeList (fun b => [b]))) input.2).length) ∧
  (∀ x, legalSource x = true → legalTarget (forward x) = true) ∧
  (∀ x, legalSource x = true → ∀ y, validTargetOutput (forward x) y →
    validSourceOutput x (recover (x, y)))


def Goal : Prop :=
  ∃ (forward : Graph → Graph)
    (recover : Graph × Option (List Bool) → Option (List Bool)), Reduction forward recover

/-- Open question only; this placeholder is not a solution. -/
theorem solve : Goal := by
  sorry

end LineGraphTwoCut
