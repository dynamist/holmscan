.PHONY: help

# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

major: ## bump major version (1.x -> 2.x)
	bumpversion major

minor: ## bump minor version (1.1 -> 1.2)
	bumpversion minor

patch: ## bump patch version (1.1.0 -> 1.1.1)
	bumpversion patch
