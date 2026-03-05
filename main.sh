#python3 src/main.py "/" "static" "content2" "docs2"
python3 src/main.py $1 $2 $3 $4
cd $4 && python3 -m http.server 8888
