dispatcher -t flowdroid -b droidbench --task taint -j 10 -i 5 --timeout 5 --results ./results_II --nondex
dispatcher -t flowdroid -b fossdroid-all-apks --task taint -j 10 -i 5 --timeout 60 --results ./results_II --nondex

dispatcher -t amandroid -b droidbench --task taint -j 10 -i 5 --timeout 5 --results ./results_II --nondex
dispatcher -t amandroid -b fossdroid-all-apks --task taint -j 10 -i 5 --timeout 60 --results ./results_II --nondex

dispatcher -t soot -b cats-microbenchmark --task cg -j 10 -i 5 --timeout 15 --results ./results_II --nondex
dispatcher -t soot -b dacapo-2006 --task cg -j 10 -i 5 --timeout 120 --results ./results_II --nondex

dispatcher -t tajs -b sunspider_test --task cg -j 10 -i 10 --timeout 5 --results ./results_II --nondex
dispatcher -t tajs -b jquery --task cg -j 10 -i 10 --timeout 120 --results ./results_II --nondex