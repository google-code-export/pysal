# developer Makefile for repeated tasks
# 
.PHONY: clean

clean: 
	find pysal -name "*.pyc" -exec rm '{}' ';'
	find pysal -name "__pycache__" -exec rm -rf '{}' ';'
