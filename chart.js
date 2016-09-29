var Chart = (function(document,window,d3) {

	var svg, map, csv, proj, path, nation, states, bubbles, tooltip, stats, width, height, padding, radius;

	d3.queue()
		.defer(d3.json, 'us.json')
		.defer(d3.csv, 'orders_demos.csv')
		.await(init);

	function type(d) {

		d['Profit'] = +d['Profit'];
		d['Lat'] = +d['Lat'];
		d['Lng'] = +d['Lng'];
		d['Population'] = +d['Population'];
		d['Median-Age'] = +d['Median-Age'];
		d['Race-White'] = +d['Race-White'];
		d['Median-Household-Income'] = +d['Median-Household-Income'];
		d['Bachelors-Degree'] = +d['Bachelors-Degree'];
		d['Graduate-Degree'] = +d['Graduate-Degree'];

		return d;

	}

	function init(error, us, orders) {

		if (error) return console.error(error);

		map = us;
		csv = type(orders);

		svg = d3.select('#pane-1')
			.append('svg');

		proj = d3.geo.albersUsa()

		path = d3.geo.path();

		nation = svg.append("path")
			.datum(topojson.feature(map, us.objects.nation))
			.attr("class", "land")

		states = svg.append("path")
			.datum(topojson.mesh(map, us.objects.states, function(a, b) { return a !== b; }))
			.attr("class", "border border--state")

		bubbles = svg.selectAll("circle")
			.data(csv)
				.sort(function(a, b) { return parseInt(b.Profit) - parseInt(a.Profit); })
		.enter()
		.append("circle")
			.attr("class", "bubble")
			.attr("class", function(d) {
				return "bubble bubble-" + d.Zipcode.substring(0,1);
			})

		tooltip = d3.select("body")
			.append("div")
			.attr("class", "tooltip")
			.style("opacity", 0);

		stats = d3.select("#pane-2")
			.append("div")
			.attr("class", "stats")
			.html("<h3>Click on a zip code bubble to view demographic statistics for the area...</h3>")

		bubbles.on("mouseover", function(d) {
			tooltip.transition()
				.duration(500)
				.style("opacity", .7);
			var tip = "<strong>Zip Code:</strong> " + d.Zipcode + "<br/>";
			tip = tip + "<strong>Profit:</strong> $" + d3.format(",.0f")(d.Profit);
			tooltip.html(tip)
				.style("left", (d3.event.pageX) + "px")
				.style("top", (d3.event.pageY) + "px");
		})
		.on("mouseout", function(d) {
			tooltip.transition()
				.duration(500)
				.style("opacity", 0);
		})
		.on("click", function(d) {
			var stat = "<div class='stat'>Zipcode<h2>" + d.Zipcode + "</h2></div>";
			stat = stat + "<div class='stat'>Profit<h2>$" + d3.format(",.0f")(d.Profit) + "</h2></div>";
			stat = stat + "<div class='stat'>Population<h2>" + d3.format(",.0f")(d.Population) + "</h2></div>";
			stat = stat + "<div class='stat'>Race (White)<h2>" + d3.format(",.1f")(d['Race-White']) + "%</h2></div>";
			stat = stat + "<div class='stat'>Median Age<h2>" + d3.format(",.1f")(d['Median-Age']) +  "</h2></div>";
			stat = stat + "<div class='stat'>Median Household Income<h2>$" + d3.format(",.0f")(d['Median-Household-Income']) + "</h2></div>";
			stat = stat + "<div class='stat'>Bachelors Degree (Adults 25+)<h2>" + d3.format(",.1f")(d['Bachelors-Degree']) + "%</h2></div>";
			stat = stat + "<div class='stat'>Graduate Degree (Adults 25+)<h2>" + d3.format(",.1f")(d['Graduate-Degree']) + "%</h2></div>";
			stats.html(stat);
		});

		render();

	}

	function render() {

		updateDimensions();

		radius = d3.scale.sqrt()
			.domain([0, d3.max(csv, function(d) { return d.Profit })])
			.range([0, width/100]);

		svg
			.attr('width', width)
			.attr('height', height);

		proj
			.scale(width)
			.translate([width / 2 - padding, height / 2 - padding]);

		path
			.projection(proj);

		nation
			.attr('d', path)

		states
			.attr('d', path)

		bubbles
			.attr("cx", function (d) {
				return proj([d.Lng, d.Lat])[0];
			})
			.attr("cy", function (d) {
				return proj([d.Lng, d.Lat])[1];
			})
			.attr("r", function (d) {
				return radius(d.Profit);
			})

	}

	function updateDimensions() {

		var wide = getElementContentWidth('pane-1');
		padding = 20;
		width =  wide - 2 * padding;
		height = wide / 1.5 - 2 * padding;

	}

	function getElementContentWidth(element) {
		return document.getElementById(element).clientWidth;
	}

	return {

		render : render

	}

})(document,window,d3);

window.addEventListener('resize', Chart.render);
