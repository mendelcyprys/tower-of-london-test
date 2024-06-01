const colours = ["#EF3636", "#30C953", "#2C7FB7"];

let matrix = [[1, 2], [3], []];

function getCol(cx) {
  if (cx < 36 + 2 / 3) return 1;
  else if (cx < 63 + 1 / 3) return 2;
  else return 3;
}

const diff = { x: undefined, y: undefined };
let startCol;

function startDragging(event) {
  // bring to front (with svg need to reappend)
  const parent = this.parentNode; // the <g> element
  parent.parentNode.appendChild(parent);
  const cx = Number(this.getAttribute("cx"));
  startCol = getCol(cx);
  diff.x = cx - event.x;
  diff.y = Number(this.getAttribute("cy")) - event.y;
}

function dragging(event) {
  this.setAttribute("cx", event.x + diff.x);
  this.setAttribute("cy", event.y + diff.y);
}

function endDragging(event) {
  const cx = Number(this.getAttribute("cx"));
  const end = getCol(cx) - 1;
  if (matrix[end].length < 3 - end) {
    const num = matrix[startCol - 1].pop();
    matrix[end].push(num);
  }
  render();
}

function render() {
  d3.select("svg")
    .selectAll("g")
    .data(matrix)
    .join("g")
    .selectAll("circle")
    .data((d, i) => d.map((x) => [x, i, d.length - 1]))
    .join("circle")
    .attr("cy", (_, j) => 80 - j * 20)
    .attr("cx", (d) => 23 + 1 / 3 + d[1] * (26 + 2 / 3))
    .attr("fill", (d) => colours[d[0] - 1])
    .attr("r", "9")
    .attr("stroke", "black")
    .attr("stroke-opacity", "0.7")
    .attr("stroke-width", "2")
    .classed("last-child", (d, j) => j === d[2])
    .on(".drag", null);

  d3.selectAll(".last-child").call(
    d3
      .drag()
      .on("start", startDragging)
      .on("drag", dragging)
      .on("end", endDragging)
  );
}

render();
