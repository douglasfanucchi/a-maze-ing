from mazegen.cell import Cell


class Edge:
    """A weighted reference to a cell, ordered by weight.

    Wraps a cell together with the random cost of reaching it so that
    instances can be stored in a min-heap. All comparisons delegate to
    the weight; the cell itself is never part of the ordering.

    Attributes:
        weight: The cost of the edge leading to the cell.
        cell: The cell this edge points to.
    """

    def __init__(self, weight: int, cell: Cell):
        """Initialize the edge.

        Args:
            weight: The cost of the edge leading to the cell.
            cell: The cell this edge points to.
        """
        self.weight = weight
        self.cell = cell

    def __eq__(self, other: object) -> bool:
        """Check whether two edges have the same weight.

        Args:
            other: The object to compare against.

        Returns:
            True if both edges share the same weight.

        Raises:
            ValueError: If other is not an Edge.
        """
        if not isinstance(other, Edge):
            raise ValueError("Invalid comparision")
        return self.weight == other.weight

    def __lt__(self, other: object) -> bool:
        """Check whether this edge is cheaper than another.

        Args:
            other: The object to compare against.

        Returns:
            True if this edge's weight is lower than other's.

        Raises:
            ValueError: If other is not an Edge.
        """
        if not isinstance(other, Edge):
            raise ValueError("Invalid comparision")
        return self.weight < other.weight

    def __gt__(self, other: object) -> bool:
        """Check whether this edge is more expensive than another.

        Args:
            other: The object to compare against.

        Returns:
            True if this edge's weight is higher than other's.

        Raises:
            ValueError: If other is not an Edge.
        """
        if not isinstance(other, Edge):
            raise ValueError("Invalid comparision")
        return self.weight > other.weight
