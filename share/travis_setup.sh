#!/bin/bash
set -evx

mkdir ~/.germancccore

# safety check
if [ ! -f ~/.germancccore/.germancc.conf ]; then
  cp share/germancc.conf.example ~/.germancccore/germancc.conf
fi
