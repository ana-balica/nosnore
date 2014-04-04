#!/bin/bash
# extract messages
pybabel extract nosnore > nosnore/translations/messages.pot

# initialize catalogs
pybabel init -i nosnore/translations/messages.pot -d nosnore/translations -l ru_RU
pybabel init -i nosnore/translations/messages.pot -d nosnore/translations -l ro_MD

# compile the catalogs, include fuzzy translations
pybabel compile -d nosnore/translations -f