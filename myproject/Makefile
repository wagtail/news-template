init: load-data start

start:
	python ./manage.py runserver

load-data:
	python ./manage.py createcachetable
	python ./manage.py migrate
	python ./manage.py load_initial_data
	python ./manage.py collectstatic --noinput

dump-data:
	python ./manage.py dumpdata --natural-foreign --indent 2 -e auth.permission -e contenttypes -e wagtailcore.GroupCollectionPermission -e wagtailimages.rendition -e images.rendition -e sessions -e wagtailsearch.indexentry -e wagtailsearch.sqliteftsindexentry -e wagtailcore.referenceindex -e wagtailcore.pagesubscription > fixtures/demo.json

reset-db:
	rm -f db.sqlite3
	python ./manage.py createcachetable
	python ./manage.py migrate
	python ./manage.py load_initial_data
