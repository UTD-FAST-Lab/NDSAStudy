dispatcher -t flowdroid -b droidbench --task taint -j 10 -i 5 --timeout 5
dispatcher -t flowdroid -b fossdroid-all-apks --task taint -j 10 -i 5 --timeout 60

dispatcher -t amandroid -b droidbench --task taint -j 10 -i 5 --timeout 5
dispatcher -t amandroid -b fossdroid-all-apks --task taint -j 10 -i 5 --timeout 60

dispatcher -t droidsafe -b droidbench --task taint -j 10 -i 5 --timeout 60
dispatcher -t droidsafe -b fossdroid-all-apks --task taint -j 10 -i 5 --timeout 120

dispatcher -t soot -b cats-microbenchmark --task cg -j 10 -i 5 --timeout 15
dispatcher -t soot -b dacapo-2006 --task cg -j 10 -i 5 --timeout 120

dispatcher -t wala -b cats-microbenchmark --task cg -j 10 -i 5 --timeout 5
dispatcher -t wala -b dacapo-2006 --task cg -j 10 -i 5 --timeout 60

dispatcher -t doop -b cats-microbenchmark --task cg -j 10 -i 5 --timeout 30
dispatcher -t doop -b dacapo-2006 --task cg -j 10 -i 5 --timeout 120

dispatcher -t opal -b cats-microbenchmark --task cg -j 10 -i 5 --timeout 5
dispatcher -t opal -b dacapo-2006 --task cg -j 10 -i 5 --timeout 30

dispatcher -t infer -b itc-benchmarks --task violation -j 10 -i 5 --timeout 30
dispatcher -t infer -b toybox --task violation -j 10 -i 5 --timeout 30
dispatcher -t infer -b sqlite --task violation -j 10 -i 5 --timeout 30
dispatcher -t infer -b openssl --task violation -j 10 -i 5 --timeout 30

dispatcher -t tajs -b sunspider_test --task cg -j 10 -i 10 --timeout 5
dispatcher -t tajs -b jquery --task cg -j 10 -i 10 --timeout 120

dispatcher -t wala-js -b sunspider_test --task cg -j 10 -i 10 --timeout 5
dispatcher -t wala-js -b jquery --task cg -j 10 -i 10 --timeout 120

dispatcher -t code2flow -b pycg-micro --task cg -j 10 -i 10 --timeout 5
dispatcher -t code2flow -b pycg-macro --task cg -j 10 -i 10 --timeout 5