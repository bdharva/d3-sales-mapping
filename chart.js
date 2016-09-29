var Chart = (function(document,window,d3) {

	var svg, map, csv, proj, path, nation, states, bubbles, tooltip, tooltipper, width, height, padding, radius;

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

		svg = d3.select('#chart')
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

		bubbles.on("mouseover", function(d) {
			tooltip.transition()
				.duration(500)
				.style("opacity", .7);
			var tip = "<strong>" + d.Zipcode + "</strong><br/>";
			var tip = tip+"$" + d3.format(",.0f")(d.Profit) + "<br/><br/>";
			var tip = tip + d3.format(",.0f")(d.Population) + " people, " + d3.format(",.1f")(d['Race-White']) + "% white<br/>";
			var tip = tip + "Median Age: " + d3.format(",.1f")(d['Median-Age']) +  "<br/>";
			var tip = tip + "Median Income: $" + d3.format(",.0f")(d['Median-Household-Income']) + "<br/>";
			var tip = tip + d3.format(",.1f")(d['Bachelors-Degree']) + "% with Bachelors degrees <br/>";
			var tip = tip + d3.format(",.1f")(d['Graduate-Degree']) + "% with Graduate degrees";
			tooltip.html(tip)
				.style("left", (d3.event.pageX) + "px")
				.style("top", (d3.event.pageY) + "px");
		})
		.on("mouseout", function(d) {
			tooltip.transition()
				.duration(500)
				.style("opacity", 0);
		});

		render();

	}

	function render() {

		updateDimensions();

		radius = d3.scale.sqrt()
			.domain([0, d3.max(csv, function(d) { return d.Profit })])
			.range([0, width/150]);

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

		var wide = getElementContentWidth('chart');
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
