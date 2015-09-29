#!/bin/bash

fail () {
    status="$1"
    shift
    echo "$@"
    exit $status
}

pushd frontend || fail 1 pushd frontend
[[ -f node_modules/.bin/brunch ]] && BRUNCH=node_modules/.bin/brunch
[[ -z "$BRUNCH" && -f /usr/local/bin/brunch ]] && BRUNCH=/usr/local/bin/brunch
[[ -z "$BRUNCH" ]] && fail 1 no brunch
$BRUNCH build || fail 1 cannot build
sed -i -e 's/images\/ui-/..\/images\/ui-/g' ../app/static/stylesheets/style.css || fail 1 cannot sed
popd || fail 1 cannot popd

[[ -f .venv/bin/activate ]] && source .venv/bin/activate
[[ -f ../env/bin/activate ]] && source ../env/bin/activate

pushd app || fail 1 cannot pushd app
python manage.py collectstatic || fail 1 cannot collectstatic
