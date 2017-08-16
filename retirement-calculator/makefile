all:
	sed -e '/PLACEHOLDER_APP_PY/r app.py' -e 's/PLACEHOLDER_APP_PY//' page.html > index.html

clean:
	rm -f index.html
