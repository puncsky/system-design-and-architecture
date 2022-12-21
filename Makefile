.PHONY: install
install:
	npm install gitbook-cli -g

.PHONY: dev
dev:
	gitbook serve

.PHONY: build
build:
	gitbook pdf ./ ./_book/system-design-and-architecture-2nd-edition.pdf
	gitbook epub ./ ./_book/system-design-and-architecture-2nd-edition.epub
	gitbook mobi ./ ./_book/system-design-and-architecture-2nd-edition.mobi
