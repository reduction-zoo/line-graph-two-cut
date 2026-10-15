import Challenge
open LineGraphTwoCut
example : legalTarget ⟨2,[(0,1)]⟩ = true := by native_decide
example : rootEncoding ⟨3,[(0,1),(1,2),(0,2)]⟩ [(0,1),(0,2),(0,3)] = true := by native_decide
example : boundedCut ⟨3,[(0,1),(1,2)]⟩ 1 [false,true,false] = false := by native_decide
example : boundedCut ⟨3,[(0,1),(1,2)]⟩ 2 [false,true,false] = true := by native_decide
