# Referenced from https://github.com/int-brain-lab/IBL-pipeline/blob/master/Makefile
all:
	@echo 'MakeFile for retinal ganglion pipeline packaging                              '
	@echo '                                                                              '
	@echo 'make sdist                              Creates source distribution           '
	@echo 'make wheel                              Creates Wheel distribution            '
#	@echo 'make pypi                               Package and upload to PyPI            '
#	@echo 'make pypitest                           Package and upload to PyPI test server'
	@echo 'make clean                              Remove all build related directories  '
	

sdist:
#	python3 setup.py sdist >/dev/null 2>&1
	python3 setup.py sdist

wheel:
#	python3 setup.py bdist_wheel >/dev/null 2>&1
	python3 setup.py bdist_wheel

# pypi:clean sdist wheel
# 	twine upload dist/*
	
# pypitest: clean sdist wheel
# 	twine upload -r pypitest dist/*

clean:
	rm -rf dist && rm -rf build && rm -rf *.egg-info