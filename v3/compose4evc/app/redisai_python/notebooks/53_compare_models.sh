cmp -l ./tmp/IrisDatasetModel.pt ./tmp/IrisDatasetModel_clone.pt | gawk '{printf "%08X %02X %02X\n", $1-1, strtonum(0$2), strtonum(0$3)}'
