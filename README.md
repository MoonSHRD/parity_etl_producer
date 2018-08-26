
## Build
```bash
make deps
make proto
//keep calm
make
```

## Run
```bash
cd build/
loom init
cp ../genesis_template.json genesis.json 
loom run
```





"Plugin Exited before we could connect"
```
plugin: plugin process exited: path=/bin/sh
panic: plugin exited before we could connect
```
This usually means there is a process hanging around that needs to be killed
```
ps -ef | grep %PLUGIN_NAME%
kill -9 xxxx 
```
