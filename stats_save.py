import pstats
 
p = pstats.Stats('file.prof')
p.sort_stats('tottime')
p.print_stats(20)