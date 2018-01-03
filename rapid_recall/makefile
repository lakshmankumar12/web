all:
	sed -e '/PLACEHOLDER_APP_PY/r app.py' -e 's/PLACEHOLDER_APP_PY//' page.html > index.html

push: all
	mv index.html /tmp
	comment=$(git log -1 --pretty=%B)
	git checkout gh-pages
	mv /tmp/index.html .
	git commit -am "${comment}"
	git push
	git checkout master

clean:
	rm -f index.html
