import svgwrite

PIXELS = 100
WOOD_COLOUR = "#73461F"
BASE_COLOUR = "#2d5725"
# CIRCLE_COLOUR = "#B95D2C"
TEXT_COLOUR = "#354212"
BALL_COLOURS = ("#EF3636", "#30C953", "#2C7FB7")


def generate(configuration, decreasing=False, colours=False):
    dwg = svgwrite.Drawing(**{"viewBox": "0 0 100 100"})

    # poles
    for i in range(3):
        THICKNESS = 0.08 * PIXELS
        BORDER = 0.1 * PIXELS
        REST = PIXELS - (2 * BORDER)
        X_COORD = BORDER + REST / 6 - THICKNESS / 2 + i * REST / 3
        RADIUS = 0.1 * PIXELS
        CIRCLE_THICKNESS = 2
        DECREASING = decreasing * 2 * RADIUS * i
        dwg.add(
            dwg.rect(
                insert=(X_COORD, 0.25 * PIXELS + DECREASING),
                size=(THICKNESS, 0.65 * PIXELS + THICKNESS / 2 - DECREASING),
                rx=THICKNESS / 2,
                ry=THICKNESS / 2,
                **{"fill": WOOD_COLOUR}
            )
        )
        for j, n in enumerate(configuration[i]):
            dwg.add(
                dwg.circle(
                    center=(
                        X_COORD + THICKNESS / 2,
                        0.9 * PIXELS - RADIUS - 2 * j * RADIUS,
                    ),
                    r=RADIUS - CIRCLE_THICKNESS / 2,
                    **{
                        "stroke": "black" if colours else "black",
                        "stroke-opacity": 0.7 if colours else 0.7,
                        "stroke-width": CIRCLE_THICKNESS,
                        "fill": BALL_COLOURS[n - 1] if colours else "white",
                    }
                )
            )
            if not colours:
                dwg.add(
                    dwg.text(
                        str(n),
                        insert=(
                            X_COORD + THICKNESS / 2 + 0.4,
                            0.9 * PIXELS - RADIUS - 2 * j * RADIUS + 1,
                        ),
                        **{
                            "text-anchor": "middle",
                            "font-size": 16,
                            "dominant-baseline": "middle",
                            "font-family": "Noto Serif Kannada",
                            "font-weight": "bold",
                            "fill": TEXT_COLOUR,
                        }
                    )
                )

    # base
    dwg.add(
        dwg.rect(
            insert=(4, 0.9 * PIXELS),
            size=(PIXELS - 8, 0.08 * PIXELS),
            rx=0.03 * PIXELS,
            ry=0.03 * PIXELS,
            **{"fill": BASE_COLOUR}
        )
    )

    return dwg.tostring()
