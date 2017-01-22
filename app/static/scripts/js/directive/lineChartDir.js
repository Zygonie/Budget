var app = angular.module('lineChartDir', ['d3']);

app.directive('lineChart', ['$window', '$timeout', 'd3Service',
  function ($window, $timeout, d3Service) {
      return {
          restrict: 'EA',
          scope: {
              data: '=',
              height: '=',
              width: '='
          },
          template: "<svg></svg>",
          link: function (scope, elem, attrs) {
              d3Service.d3().then(function (d3) {

                  var padding = 30;
                  var pathClass = "path";
                  var xScale, yScale, xAxisGen, yAxisGen, lineFun;
                  
                  var rawSvg = elem.find("svg")[0];
                  var svg = d3.select(rawSvg)
                      .attr('width', scope.width)
                      .attr('height', scope.height);

                  scope.$watch(function () {
                      return angular.element($window)[0].innerWidth;
                  }, function () {
                      scope.render(scope.data);
                  });

                  scope.$watch('data', function (newData) {
                      scope.render(newData);
                  }, true);

                  // Scales
                  h = rawSvg.clientHeight;
                  w = rawSvg.clientWidth;
                  var xScale = d3.scale.linear()
                             .range([padding, w - padding]);
                  var yScale = d3.scale.linear()
                      .range([h - padding, padding]);

                  // Line function
                  var line = d3.svg.line().interpolate("monotone")
                          .x(function (d) { return xScale(d.x); })
                          .y(function (d) { return yScale(d.y); });

                  // Render function
                  scope.render = function (data) {

                      svg.selectAll('*').remove();
                      if (!data) return;

                      // absolute min and max
                      var yMin = data.reduce(function (pv, cv) {
                          var currentMin = cv.reduce(function (pv, cv) {
                              return Math.min(pv, cv.y);
                          }, 100)
                          return Math.min(pv, currentMin);
                      }, 100);
                      var yMax = data.reduce(function (pv, cv) {
                          var currentMax = cv.reduce(function (pv, cv) {
                              return Math.max(pv, cv.y);
                          }, 0)
                          return Math.max(pv, currentMax);
                      }, 0);

                      // absolute min and max
                      var xMin = data.reduce(function (pv, cv) {
                          var currentMin = cv.reduce(function (pv, cv) {
                              return Math.min(pv, cv.x);
                          }, 100)
                          return Math.min(pv, currentMin);
                      }, 100);
                      var xMax = data.reduce(function (pv, cv) {
                          var currentMax = cv.reduce(function (pv, cv) {
                              return Math.max(pv, cv.x);
                          }, 0)
                          return Math.max(pv, currentMax);
                      }, 0);

                      // set domain for axis
                      xScale.domain([xMin, xMax]);
                      yScale.domain([yMin, yMax]);

                      // Generate axes
                      xAxisGen = d3.svg.axis()
                                       .scale(xScale)
                                       .orient("bottom")
                                       .ticks(Math.min(data.length - 1, 10));

                      yAxisGen = d3.svg.axis()
                                   .scale(yScale)
                                   .orient("left")
                                   .ticks(5);

                      // if there is no axis, create ones
                      if (svg.selectAll(".x.axis")[0].length < 1) {
                          svg.append("svg:g")
                              .attr("class", "axis")
                             .attr("transform", "translate(0," + (h - padding) + ")")
                             .call(xAxisGen);

                          svg.append("svg:g")
                              .attr("class", "axis")
                              .attr("transform", "translate(" + padding + ",0)")
                              .call(yAxisGen);
                      }
                      // otherwise update currents
                      else {
                          svg.selectAll(".x.axis").transition().duration(1500).call(xAxisGen);
                          svg.selectAll(".y.axis").transition().duration(1500).call(yAxisGen);
                      }

                      // Build lines
                      // generate line paths
                      var lines = svg.selectAll(".line").data(data).attr("class", "line");

                      // Transition from previous paths to new paths
                      lines.transition().duration(1500)
                        .attr("d", line);

                      // Enter any new data
                      lines.enter()
                        .append("path")
                        .attr("class", "line")
                        .attr("d", line);

                      // Exit
                      lines.exit()
                        .remove();
                  }
              })
          }
      }
  }])