

class TailwindMapper:
    """converting CSS styles into Tailwind classes"""

    def __init__(self):

        ## Mapping table of standard values 
        
        self.exact_map = {
            "display": {
                "flex": "flex",
                "inline-flex": "inline-flex",
                "block": "block",
                "inline-block": "inline-block",
                "grid": "grid",
                "none": "hidden",
                "inline": "inline",
            },
            "position": {
                "static": "static",
                "fixed": "fixed",
                "absolute": "absolute",
                "relative": "relative",
                "sticky": "sticky",
            },
            "text-align": {
                "left": "text-left",
                "center": "text-center",
                "right": "text-right",
                "justify": "text-justify",
            },
            "justify-content": {
                "flex-start": "justify-start",
                "flex-end": "justify-end",
                "center": "justify-center",
                "space-between": "justify-between",
                "space-around": "justify-around",
                "space-evenly": "justify-evenly",
            },
            "align-items": {
                "flex-start": "items-start",
                "flex-end": "items-end",
                "center": "items-center",
                "baseline": "items-baseline",
                "stretch": "items-stretch",
            },
            "flex-direction": {
                "row": "flex-row",
                "row-reverse": "flex-row-reverse",
                "column": "flex-col",
                "column-reverse": "flex-col-reverse",
            },
            "font-weight": {
                "bold": "font-bold",
                "normal": "font-normal",
                "100": "font-thin",
                "300": "font-light",
                "500": "font-medium",
                "600": "font-semibold",
                "700": "font-bold",
                "900": "font-black",
            },
        }

        #--------------------------------------------------------#
        #                     Arbitrary Values                   #
        #  key: CSS property name | value: Tailwind class prefix #
        #--------------------------------------------------------#
        self.prefix_map = {
            "color": "text",
            "background-color": "bg",
            "width": "w",
            "height": "h",
            "margin": "m",
            "margin-top": "mt",
            "margin-bottom": "mb",
            "margin-left": "ml",
            "margin-right": "mr",
            "padding": "p",
            "padding-top": "pt",
            "padding-bottom": "pb",
            "padding-left": "pl",
            "padding-right": "pr",
            "border-radius": "rounded",
            "font-size": "text",
            "gap": "gap",
            "top": "top",
            "bottom": "bottom",
            "left": "left",
            "right": "right",
            "z-index": "z",
            "opacity": "opacity",
            "border-width": "border",
            "border-color": "border",
        }

    def _sanitize(self, value: str) -> str:
        """
            '10px 20px' -> '10px_20px'
        """
        return value.strip().replace(" ", "_")

    def map_property(self, prop_name: str, prop_value: str) -> str:
        """ Convert CSS property into a Tailwind class"""

        prop_name = prop_name.strip().lower()
        prop_value = prop_value.strip().lower()

        # 
        if prop_name in self.exact_map and prop_value in self.exact_map[prop_name]:
            return self.exact_map[prop_name][prop_value]

        # 
        if prop_name in self.prefix_map:
            prefix = self.prefix_map[prop_name]
            return f"{prefix}-[{self._sanitize(prop_value)}]"

        # 
        return f"[{prop_name}:{self._sanitize(prop_value)}]"


if __name__ == "__main__":
    mapper = TailwindMapper()

    tests = [
        ("display", "flex"),
        ("justify-content", "space-between"),
        ("font-weight", "600"),
        ("color", "#FF0000"),
        ("padding", "10px 20px"),  
        ("margin-top", "1rem"),
        ("cursor", "pointer"),      
    ]

    for prop, value in tests:
        print(f"{prop}: {value} -> {mapper.map_property(prop, value)}\n")