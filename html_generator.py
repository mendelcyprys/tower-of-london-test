from jinja2 import Environment, FileSystemLoader
from svg_generator import generate as g
from calculation import results, results_decreasing

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("doc.html")

coloured_examples = [
    ((), (2,), (3, 1)),
    ((3, 2, 1), (), ()),
    ((3, 1), (2,), ()),
    ((), (), (3, 2, 1)),
]
numbered_examples = [
    ((1, 2), (3,), ()),
    ((), (), (1, 3, 2)),
]

results_items = map(lambda x: x[1].items(), results.items())
table_rows = list(zip(*list(results_items)))

svg_table_rows = []
for x1, x2, x3 in table_rows[1:]:
    final1, d1 = x1
    final2, d2 = x2
    final3, d3 = x3
    svg_table_rows.append(
        (
            g(final1),
            d1[0],
            g(d1[1]),
            g(final2),
            d2[0],
            g(d2[1]),
            g(final3),
            d3[0],
            g(d3[1]),
        )
    )

decreasing_results_items = map(lambda x: x[1].items(), results_decreasing.items())
decreasing_table_rows = list(zip(*list(decreasing_results_items)))

svg_decreasing_table_rows = []
for x1, x2, x3, x4, x5, x6 in decreasing_table_rows[1:]:
    final1, d1 = x1
    final2, d2 = x2
    final3, d3 = x3
    final4, d4 = x4
    final5, d5 = x5
    final6, d6 = x6
    svg_decreasing_table_rows.append(
        (
            g(final1, decreasing=True),
            d1[0],
            g(d1[1], decreasing=True),
            g(final2, decreasing=True),
            d2[0],
            g(d2[1], decreasing=True),
            g(final3, decreasing=True),
            d3[0],
            g(d3[1], decreasing=True),
            g(final4, decreasing=True),
            d4[0],
            g(d4[1], decreasing=True),
            g(final5, decreasing=True),
            d5[0],
            g(d5[1], decreasing=True),
            g(final6, decreasing=True),
            d6[0],
            g(d6[1], decreasing=True),
        )
    )

context = {
    "equal": {
        "coloured_examples": list(map(lambda x: g(x, colours=True), coloured_examples)),
        "numbered_examples": list(map(g, numbered_examples)),
        "options": list(map(g, results.keys())),
        "table": svg_table_rows,
    },
    "decreasing": {
        "options": list(
            map(lambda x: g(x, decreasing=True), results_decreasing.keys())
        ),
        "table": svg_decreasing_table_rows,
    },
}

output = template.render(context)
