all: us.json

clean:
	rm -rf -- us.json build

.PHONY: all clean

build/cb_2015_us_state_20m.zip:
	mkdir -p $(dir $@)
	curl -o $@ http://www2.census.gov/geo/tiger/GENZ2015/shp/$(notdir $@)

build/cb_2015_us_state_20m.shp: build/cb_2015_us_state_20m.zip
	unzip -od $(dir $@) $<
	touch $@

build/states.json: build/cb_2015_us_state_20m.shp
	node_modules/.bin/topojson \
		-o $@ \
		-- states=$<

us.json: build/states.json
	node_modules/.bin/topojson-merge \
		-o $@ \
		--in-object=states \
		--out-object=nation \
		-- $<
