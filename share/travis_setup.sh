#!/bin/bash
set -evx

mkdir ~/.allcoingurucore

# safety check
if [ ! -f ~/.allcoingurucore/.allcoinguru.conf ]; then
  cp share/allcoinguru.conf.example ~/.allcoingurucore/allcoinguru.conf
fi
