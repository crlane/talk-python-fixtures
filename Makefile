HOST_PORT=8889
SLIDES_PORT=8000
NOTEBOOKS=`pwd`:/home/jovyan/work
IMAGE=crlane/pytest-fixtures-pres
PRESENTATION=Pytest-Fixtures

.PHONY: pull image slides present run
.IGNORE: clean
clean:
	rm *.html

pull:
	docker pull jupyter/base-notebook

image:
	docker build -t $(IMAGE) .

slides: clean
	. venv/bin/activate && ipython nbconvert notebooks/$(PRESENTATION).ipynb --to slides --post serve

present: clean
	docker run --rm -it -p $(SLIDES_PORT):$(SLIDES_PORT) -v $(NOTEBOOKS) $(IMAGE) jupyter nbconvert $(PRESENTATION).ipynb --to slides --post serve --log-level DEBUG --ServePostProcessor.ip='0.0.0.0'

run:
	docker run --rm -p $(HOST_PORT):$(HOST_PORT) -v $(NOTEBOOKS) $(IMAGE)
