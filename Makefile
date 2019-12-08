.PHONY: update
.PHONY: test
.PHONY: install
	
update:
	rm -r  __pycache__
	cp * /usr/lib/halibut

test:
	python3 main.py
install:
	gcc halibut.c -o halibut
	rm -r /usr/lib/halibut
	mkdir /usr/lib/halibut
	python3 conf.py
	cp *.py /usr/lib/halibut
	mv halibut /usr/bin
	cp config /usr/lib/halibut
