#!/bin/bash
# 2025.07.0 Test of code onlinebookstore with rate limiting
# Exit on error
set -e



./Step1_Enhanced.sh production
./Step2_Enhanced.sh production          # Traditional requirements
./Step3_Enhanced.sh production          # Modern requirements