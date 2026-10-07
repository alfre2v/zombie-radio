#!/bin/bash
# Sample every GPU process's memory every 200 ms into $1 until killed: time, pid, process, MiB.
exec nvidia-smi --query-compute-apps=timestamp,pid,process_name,used_memory --format=csv,noheader,nounits -lms 200 > "$1"
