cmp -l ./tmp/resnet50.pb ./tmp/resnet50_clone.pb | gawk '{printf "%08X %02X %02X\n", $1-1, strtonum(0$2), strtonum(0$3)}'
