.PHONY: update
.PHONY: test
.PHONY: install
update:
	cp *.py /usr/lib/pike
	cp config /usr/lib/pike
test:
	python3 main.py
install:
	mkdir /usr/lib/pike
	cp *.py /usr/lib/pike
