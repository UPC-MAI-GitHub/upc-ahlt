## ------------------- 
## -- check pattern:  LCS is a verb, one entity is under its "nsubj" and the other under its "obj"      

def check_LCS_svo(tree,tkE1,tkE2):

   if tkE1 is not None and tkE2 is not None:
      lcs = tree.get_LCS(tkE1,tkE2)

      if tree.get_tag(lcs)[0:2] == "VB" :      
         path1 = tree.get_up_path(tkE1,lcs)
         path2 = tree.get_up_path(tkE2,lcs)
         func1 = tree.get_rel(path1[-1]) if path1 else None
         func2 = tree.get_rel(path2[-1]) if path2 else None
         
         if (func1=='nsubj' and func2=='obj') or (func1=='obj' and func2=='nsubj') :
            lemma = tree.get_lemma(lcs).lower()
            if lemma in ['diminish','augment','attenuate','amplify','exacerbate','potientate','reduce','enhance'] :
               return 'effect'
            if lemma in ['displace','delay','bind','induce','inhibit','elevate','impair','indicate','accelerate'] :
               return 'mechanism'
            if lemma in ['exceed'] :
               return 'advise'
            if lemma in ['suggest'] :
               return 'int'
         
   return None

## ------------------- 
## -- check pattern:  A word in between both entities belongs to certain list

def check_wib(tree,tkE1,tkE2,entities,e1,e2):

   if tkE1 is not None and tkE2 is not None:
      # get actual start/end of both entities
      l1,r1 = entities[e1]['start'],entities[e1]['end']
      l2,r2 = entities[e2]['start'],entities[e2]['end']
      
      p = []
      for t in range(tkE1+1,tkE2) :
         # get token span
         l,r = tree.get_offset_span(t)
         # if the token is in between both entities
         if r1 < l and r < l2:
            lemma = tree.get_lemma(t).lower()
            if lemma in ['tendency','stimulate','regulate','modification','augment','exacerbate','counteract'] :
               return 'effect'
            if lemma in ['determinant','react','modest','faster','presumably','species','fruit','accelerate'] :
               return 'mechanism'
            if lemma in ['exceed','cautiously','doctor','narrow','index'] :
               return 'advise'
            if lemma in ['interact'] :
               return 'int'

   return None

