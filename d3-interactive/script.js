const colours = ["#EF3636", "#30C953", "#2C7FB7"];

const taskData = [
  {
    matrix: [[1], [2], [3]],
    target: [[3, 1], [], [2]],
    targetSVG: "",
  },
  {
    matrix: [[1, 2, 3], [], []],
    target: [[2, 1], [3], []],
    targetSVG: "",
  },
  {
    matrix: [[1, 2], [], [3]],
    target: [[3], [1], [2]],
    targetSVG: "",
  },
  {
    matrix: [[1, 2], [3], []],
    target: [[], [1, 2], [3]],
    targetSVG: "",
  },
  {
    matrix: [[3], [1, 2], []],
    target: [[1, 2], [3], []],
    targetSVG: "",
  },
]
let matrix;
let target;
let startTime;

let moves = 0;
const movesTextElement = d3.select("#moves");
const successTextElement = d3.select("#success-message");
const timeTextElement = d3.select("#time-message");
const targetSVGElement = d3.select("#target-svg");

function getCol(cx) {
  if (cx < 36 + 2 / 3) return 0;
  else if (cx < 63 + 1 / 3) return 1;
  else return 2;
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
  const end = getCol(cx);
  if (matrix[end].length < 3 - end && startCol !== end) {
    const num = matrix[startCol].pop();
    matrix[end].push(num);
    moves++;
    movesTextElement.text(`moves: ${moves}`);
    render();
    // check if target state has been reached
    if (JSON.stringify(matrix) === target) {
      const totalTime = Date.now() - startTime;
      targetSVGElement.attr("visibility", "hidden");
      successTextElement.attr("visibility", "visible");
      d3.selectAll("circle").on(".drag", null);
      timeString = (totalTime / 1000).toFixed(2);
      timeTextElement.text(`time: ${timeString}s`)
                     .attr("visibility", "visible");
    }
  } else {
    render();
  }
}

function render() {
  d3.select("#main-svg")
    .selectAll("#main-svg > g")
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

const menuButtons = d3.selectAll(".menu button");

function buttonClick(event, d) {
  menuButtons.classed("selected", false);
  event.target.classList.add("selected");
  currentTask = taskData[d];
  // deep copy the starting position
  matrix = JSON.parse(JSON.stringify(currentTask.matrix));
  target = JSON.stringify(currentTask.target);
  // reset the number of moves
  moves = 0;
  movesTextElement.text(`moves: ${moves}`);
  successTextElement.attr("visibility", "hidden");
  timeTextElement.attr("visibility", "hidden");

  // render target svg
  targetSVGElement
    .attr("visibility", "visible")
    .selectAll("g")
    .data(currentTask.target)
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
    .attr("stroke-width", "2");

  render();
  startTime = Date.now();
}

menuButtons
  .data([0, 1, 2, 3, 4])
  .on("click", buttonClick);
