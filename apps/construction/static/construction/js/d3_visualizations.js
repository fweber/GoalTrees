var WIDTH = 800;
var HEIGHT = 800;
var MARGIN = 200;
var LINECOLOR = "black";
var FILLCOLOR = "white";
var FONTSIZE = "15px";
var TEXTWIDTH = 150;

function clear_svg(svg_id="construct_svg") {
    d3.select('#'+svg_id).selectAll('*').remove();
}

function visualize(condition, nodeData, svg_id="construct_svg") {
    console.log("hello");
    console.log(condition);
    console.log(nodeData)
    switch (condition) {
        case 1:
            // console.log(1);
            draw_sunburst(nodeData, svg_id);
            break;
        case 2:
            // console.log(2);
            draw_treemap(nodeData, svg_id);
            break;
        case 3:
            draw_dendrogram(nodeData, svg_id);
            break;
            // console.log(3);
        case 4:
            draw_circlepacking(nodeData, svg_id);
            break;
            // console.log(4);
    }
    ;
}

function wrap(text, width) {
    text.each(function () {
        var text = d3.select(this),
            words = text.text().split(/\s+/).reverse(),
            word,
            line = [],
            lineHeight = 1.1, // ems
            y = text.attr("y"),
            dy = 0,
            sum_dy = 0,
            first_tspan,
            tspan = first_tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y);
            line.push(words.pop());
            tspan.text(line.join(" "));
        while (word = words.pop()) {
            line.push(word);
            tspan.text(line.join(" "));
            if (tspan.node().getComputedTextLength() > width) {
                line.pop();
                tspan.text(line.join(" "));
                line = [word];
                tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", lineHeight + dy + "em").text(word);
                sum_dy += lineHeight;
            }
        }
        first_tspan.attr("dy", -sum_dy + dy + "em");
    });
}

// function wrap_circle(text, width) {
//     text.each(function () {
//         var text = d3.select(this),
//             words = text.text().split(/\s+/).reverse(),
//             word,
//             line = [],
//             lineNumber = 0,
//             lineHeight = 1.1, // ems
//             x = text.attr("x"),
//             y = text.attr("y"),
//             dy = 0, //parseFloat(text.attr("dy")),
//             tspan = text.text(null).append("tspan").attr("x", x).attr("y", y).attr("dy", dy + "em");
//             line.push(words.pop());
//             tspan.text(line.join(" "));
//         while (word = words.pop()) {
//             line.push(word);
//             tspan.text(line.join(" "));
//             if (tspan.node().getComputedTextLength() > width) {
//                 line.pop();
//                 tspan.text(line.join(" "));
//                 line = [word];
//                 tspan = text.append("tspan").attr("x", x).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
//             }
//         }
//     });
// }

function draw_sunburst(data, svg_id="construct_svg") {

    clear_svg(svg_id);

    // Variables
    var width = WIDTH;
    var height = HEIGHT;
    var radius = Math.min(width, height) / 2;
    /*    var data = {
            "name": "TOPICS", "children": [{
                "name": "Topic A",
                "children": [{"name": "Sub A1", "size": 4}, {"name": "Sub A2", "size": 4}]
            }, {
                "name": "Topic B",
                "children": [{"name": "Sub B1", "size": 3}, {"name": "Sub B2", "size": 3}, {
                    "name": "Sub B3", "size": 3}]
            }, {
                "name": "Topic C",
                "children": [{"name": "Sub A1", "size": 4}, {"name": "Sub A2", "size": 4}]
            }]
        };*/

    // Create primary <g> element
    var svg = d3.select('#'+svg_id)
            .attr('width', width+10)
            .attr('height', height+10)
            .append('g')
            .attr('transform', 'translate(' + width / 2 + ',' + height / 2 + ')');;

    // Data structure
    var partition = d3.partition()
        .size([2 * Math.PI, radius]);

    // Find data root
    const root = d3.hierarchy(data)
        .sum(function (d) {
            return d.size
        });

    // Size arcs
    partition(root);
    const arc = d3.arc()
        .startAngle(function (d) {
            return d.x0
        })
        .endAngle(function (d) {
            return d.x1
        })
        .innerRadius(function (d) {
            return d.y0
        })
        .outerRadius(function (d) {
            return d.y1
        })
    // .centroid(function (d) {
    //       const my_x = (d.x0 + d.x1)/2
    //       const my_y = (d.y0 + d.y1)/2
    //      return [my_x, my_y]
    // })


    // Put it all together
    const g = svg.selectAll('g')
        .data(root.descendants())
        .enter()
        .append('g')

    g.append("path")
        .attr("display", function (d) {
            return d.depth ? null : "none";
        })
        .attr("d", arc)
        .style('stroke', LINECOLOR)
        .style('fill', FILLCOLOR)
        .style('fill-opacity', "0.0")

    const text = g.append("text")
        .text(function (d) {
            return d.data.name
        })
        //.attr("cx",arc)
        //.attr("cy",arc)
        //.attr("d", arc)
        .attr("transform", function (d) {
            //    return "translate(" + d.centroid + ")"
            //})
            if (d.depth > 0) {
                return "translate(" + arc.centroid(d) + ")"
                //               "rotate(" + getAngle(d) + ")";
            } else {
                return "translate(0,0)"
            }
        })
        .attr("text-anchor", "middle")
        .attr("font-size", FONTSIZE)
        .attr("fill", LINECOLOR)

    text.call(wrap,TEXTWIDTH)
}

function draw_treemap(data, svg_id="construct_svg") {
    console.log("draw_treemap");
    clear_svg(svg_id);

    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 10, bottom: 10, left: 10};
    var width = WIDTH - margin.left - margin.right;
    var height = HEIGHT - margin.top - margin.bottom;

    // select the svg object
    var svg = d3.select('#'+svg_id)
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");;

    // Give the data to this cluster layout:
    var root = d3.hierarchy(data).sum(function (d) {
        return d.size
    }) // Here the size of each leave is given in the 'size' field in input data

    // Then d3.treemap computes the position of each element of the hierarchy
    d3.treemap()
        .size([width, height])
        .paddingOuter(3)
        .paddingTop(30)
        .paddingInner(1)
        (root);

    // use this information to add rectangles:
    svg.selectAll("rect")
        .data(root.descendants())
        .enter()
        .append("rect")
        .attr('x', function (d) {
            return d.x0;
        })
        .attr('y', function (d) {
            return d.y0;
        })
        .attr('width', function (d) {
            return d.x1 - d.x0;
        })
        .attr('height', function (d) {
            return d.y1 - d.y0;
        })
        .style("stroke", LINECOLOR)
        .style("fill", FILLCOLOR)

    // and to add the text labels
    svg.selectAll("text")
        .data(root.descendants())
        .enter()
        .append("text")
        .attr("x", function (d) {
            return d.x0 + 5
        })    // +10 to adjust position (more right)
        .attr("y", function (d) {
            return d.y0 + 20
        })    // +20 to adjust position (lower)
        .text(function (d) {
            return d.data.name
        })
        .attr("font-size", FONTSIZE)
        .attr("fill", LINECOLOR)
    //})

};


function draw_dendrogram(data, svg_id="construct_svg") {
    console.log("draw_dendrogram");
    clear_svg(svg_id);
// set the dimensions and margins of the graph
    var width = WIDTH
    var height = HEIGHT
    var margin = MARGIN

// append the svg object to the body of the page
    var svg = d3.select('#'+svg_id)
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", "translate(80,0)");  // bit of margin on the left = 80;

    // Create the cluster layout:
    var cluster = d3.cluster()
        .size([height, width - margin]);  // 100 is the margin I will have on the right side

    // Give the data to this cluster layout:
    var root = d3.hierarchy(data, function (d) {
        return d.children;
    });
    cluster(root)

    // Add the links between nodes:
    svg.selectAll('path')
        .data(root.descendants().slice(1))
        .enter()
        .append('path')
        .attr("d", function (d) {
            return "M" + d.y + "," + d.x
                + "C" + (d.parent.y + 50) + "," + d.x
                + " " + (d.parent.y + 150) + "," + d.parent.x // 50 and 150 are coordinates of inflexion, play with it to change links shape
                + " " + d.parent.y + "," + d.parent.x;
        })
        .style("fill", FILLCOLOR)
        .attr("fill-opacity", 0)
        .attr("stroke", LINECOLOR)


    // Add a circle for each node.
    nodes = svg.selectAll("g")
        .data(root.descendants())
        .enter()
        .append("g")
        .attr("transform", function (d) {
            return "translate(" + d.y + "," + d.x + ")"
        })

    nodes.append("circle")
        .attr("r", 7)
        .style("fill", FILLCOLOR)
        .attr("stroke", function (d) {
            if (d.data.done === true) {
                return "green";
            }
            return LINECOLOR;
        })
        .style("stroke-width", 2)

    const text = nodes.append("text")
        .attr("transform", function (d) {
            return "translate(0,-10)"
        })
        .text(function (d) {
            return d.data.name
        })
        .attr("text-anchor", "middle")
        .attr("font-size", FONTSIZE)
        .attr("fill", function (d) {
            if (d.data.done === true) {
                return "green";
            }
            return LINECOLOR;
        })
        .attr("height", "30")

    text.call(wrap,TEXTWIDTH)
};

function draw_circlepacking(data, svg_id="construct_svg") {
    console.log("draw_circlepacking");
    clear_svg(svg_id);

    var width = WIDTH, height = HEIGHT;

    var svg = d3.select('#'+svg_id)
            .attr('width', width)
            .attr('height', height);

    var nodes = d3.layout.pack()
        .value(function (d) {
            return d.size;
        })
        .size([width, height])
        .nodes(data);


    var node = svg.selectAll('g')
        .data(nodes)
        .enter()
        .append('g')


    node.append('circle')
        .attr('cx', function (d) {
            return d.x;
        })
        .attr('cy', function (d) {
            return d.y;
        })
        .attr('r', function (d) {
            var reduction = 0;
            let parent = d.parent
            while (parent != null) {
                if (parent.children && parent.children.length === 1) {
                    reduction += 25;
                }
                parent = parent.parent;
            }
            return d.r - reduction;
        })
        .attr('fill', FILLCOLOR)
        .attr('stroke', LINECOLOR)

    // Print the text at last to prevent overlapping with circles
    const text = svg.append("g")
        .selectAll("text")
        .data(nodes)
        .enter()
        .append("text")
        .attr('x', function (d) {
            return d.x;
        })
        .attr('y', function (d) {
            var reduction = 0;
            let parent = d.parent
            while (parent != null) {
                if (parent.children && parent.children.length === 1) {
                    reduction += 25;
                }
                parent = parent.parent;
            }
            // if outer circle
            if (d.children) {
                return d.y - d.r + reduction + 20;
            } else {
                // if leaf
                return d.y;
            }
        })
        .text(function (d) {
            return d.name;
        })
        .attr("text-anchor", "middle")
        .attr("font-size", FONTSIZE)
        .attr("fill", LINECOLOR);

    // text.call(wrap_circle,TEXTWIDTH)
};

function draw_icicle(data, svg_id="construct_svg") {

    // Variables
    var width = WIDTH;
    var height = HEIGHT;

    const root = d3.partition(data)
        .size([height, width])
        .padding(1)
        (d3.hierarchy(data)
            .sum(d => d.size)
            .sort((a, b) => b.height - a.height || b.size - a.size));

    // Create primary <g> element
    var svg = d3.select('#'+svg_id)
            .attr("viewBox", [0, 0, width, height])
            .style("font", "10px sans-serif");

    const cell = svg
        .selectAll("g")
        .data(root.descendants())
        .join("g")
        .attr("transform", d => `translate(${d.y0},${d.x0})`);

    cell.append("rect")
        .attr("width", d => d.y1 - d.y0)
        .attr("height", d => d.x1 - d.x0)
        .attr("fill-opacity", 0.6)
        .attr("fill", d => {
            if (!d.depth) return "#ccc";
            while (d.depth > 1) d = d.parent;
            return color(d.data.name);
        });

};




