.PHONY: test
.PHONY: compile
.PHONY: edit
	
all: compile

test:
	python3 main.py
compile:
	pyinstaller --name  halibut \
	  --add-data='./assets:./assets'\
	  --add-data='./parse.py:./parse.py' \
	  --onefile \
	  main.py
edit:
	vim main.py
