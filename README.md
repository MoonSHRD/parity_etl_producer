
make deps
make proto
//keep calm
make

cd build/
loom init
cp ../genesis_template.json genesis.json 
loom run