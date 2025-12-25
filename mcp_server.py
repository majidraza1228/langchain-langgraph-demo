import math
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Area")

@mcp.tool()
def circle_area(radius: float) -> float: 
    """Return the area of a circle for a given radius."""
    return math.pi * radius * radius


if __name__ == "__main__":
    mcp.run(transport="stdio")