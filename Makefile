.PHONY: update
.PHONY: test
update:
	cp ~/bro/*.py /usr/share/sd9-browser
	cp ~/bro/config /usr/share/sd9-browser
test:
	python2 main.py
