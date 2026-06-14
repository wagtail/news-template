init: load-data start

start:
	python ./manage.py runserver

load-data:
	python ./manage.py dev_setup
	

dump-data:
	python ./manage.py dumpdata --natural-foreign --indent 2 -e auth.permission -e contenttypes -e wagtailcore.GroupCollectionPermission -e wagtailimages.rendition -e images.rendition -e sessions -e wagtailsearch.indexentry -e wagtailsearch.sqliteftsindexentry -e wagtailcore.referenceindex -e wagtailcore.pagesubscription > fixtures/demo.json

reset-db:
	python ./manage.py dev_reset
