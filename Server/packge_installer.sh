#!/bin/bash - 
#===============================================================================
#
#          FILE: mongo_intaller.sh
# 
#         USAGE: ./mongo_intaller.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 18/12/18 16:37
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
sudo rm -r node_modules
sudo npm install mongodb@2.2.19
sudo npm install dateformat
