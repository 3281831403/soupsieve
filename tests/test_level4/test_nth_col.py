"""Test `nth-col` selectors."""
from .. import util
from soupsieve import SelectorSyntaxError


class TestNthCol(util.TestCase):
    """Test `nth-col` selectors."""

    MARKUP = """
    <table id="table">
    <colgroup>
    <col class="first">
    <col class="price" span="2">
    </colgroup>
    <colgroup span="1"></colgroup>
    <tr>
    <th id="h1">H1</th>
    <th id="h2">H2</th>
    <th id="h3">H3</th>
    <th id="h4">H4</th>
    </tr>
    <tr>
    <td id="c12" colspan="2">1-2</td>
    <td id="c3">3</td>
    <td id="c4">4</td>
    </tr>
    <tr>
    <td id="d1" rowspan="2">1</td>
    <td id="d2">2</td>
    <td id="d3">3</td>
    <td id="d4">4</td>
    </tr>
    <tr>
    <td id="e2">2</td>
    <td id="e3">3</td>
    <td id="e4">4</td>
    </tr>
    </table>
    <table id="plain">
    <tr>
    <td id="p1">1</td>
    <td id="p2">2</td>
    </tr>
    </table>
    <div id="outside"></div>
    """

    def test_nth_col(self):
        """Test `nth-col` with a specific column."""

        for flags in (util.HTML, util.HTML | util.NOCACHE):
            self.assert_selector(
                self.MARKUP,
                "td:nth-col(1)",
                ["c12", "d1", "p1"],
                flags=flags
            )

    def test_nth_col_spanning_cell(self):
        """Test that a cell that spans columns matches for each column it covers."""

        self.assert_selector(
            self.MARKUP,
            "td:nth-col(2)",
            ["c12", "d2", "e2", "p2"],
            flags=util.HTML
        )

    def test_nth_col_rowspan(self):
        """Test that a `rowspan` holds its columns for the rows that follow."""

        self.assert_selector(
            self.MARKUP,
            "td:nth-col(3)",
            ["c3", "d3", "e3"],
            flags=util.HTML
        )

        self.assert_selector(
            self.MARKUP,
            "td:nth-col(4)",
            ["c4", "d4", "e4"],
            flags=util.HTML
        )

    def test_nth_col_header(self):
        """Test `nth-col` on table header cells."""

        self.assert_selector(
            self.MARKUP,
            "th:nth-col(3)",
            ["h3"],
            flags=util.HTML
        )

    def test_nth_col_pattern(self):
        """Test `nth-col` with an `an+b` pattern."""

        self.assert_selector(
            self.MARKUP,
            "td:nth-col(2n)",
            ["c12", "c4", "d2", "d4", "e2", "e4", "p2"],
            flags=util.HTML
        )

        self.assert_selector(
            self.MARKUP,
            "td:nth-col(odd)",
            ["c12", "c3", "d1", "d3", "e3", "p1"],
            flags=util.HTML
        )

        self.assert_selector(
            self.MARKUP,
            "td:nth-col(-n+2)",
            ["c12", "d1", "d2", "e2", "p1", "p2"],
            flags=util.HTML
        )

    def test_nth_col_out_of_range(self):
        """Test that `nth-col` past the width of the table matches nothing."""

        self.assert_selector(
            self.MARKUP,
            "td:nth-col(5)",
            [],
            flags=util.HTML
        )

    def test_nth_col_no_col_elements(self):
        """Test that `nth-col` does not require `col` elements."""

        self.assert_selector(
            self.MARKUP,
            "#plain td:nth-col(2)",
            ["p2"],
            flags=util.HTML
        )

    def test_nth_col_not_a_cell(self):
        """Test that elements that are not table cells do not match `nth-col`."""

        self.assert_selector(
            self.MARKUP,
            "div:nth-col(1)",
            [],
            flags=util.HTML
        )

        self.assert_selector(
            self.MARKUP,
            "tr:nth-col(1)",
            [],
            flags=util.HTML
        )

    def test_nth_col_nested_tables(self):
        """Test that nested tables each have their own columns."""

        markup = """
        <table id="outer">
        <tr>
        <td id="o1">1</td>
        <td id="o2">
        <table id="inner">
        <tr>
        <td id="i1">1</td>
        <td id="i2">2</td>
        <td id="i3">3</td>
        </tr>
        </table>
        </td>
        </tr>
        </table>
        """

        # The inner table has three columns, the outer only two.
        self.assert_selector(
            markup,
            "#outer td:nth-col(3)",
            ["i3"],
            flags=util.HTML
        )

        self.assert_selector(
            markup,
            "#inner td:nth-col(2)",
            ["i2"],
            flags=util.HTML
        )

    def test_nth_col_rowspan_zero(self):
        """Test that a `rowspan` of zero spans the rows to the end of the table."""

        markup = """
        <table>
        <tr>
        <td id="z1" rowspan="0">1</td>
        <td id="z2">2</td>
        </tr>
        <tr>
        <td id="z3">3</td>
        </tr>
        </table>
        """

        self.assert_selector(
            markup,
            "td:nth-col(2)",
            ["z2", "z3"],
            flags=util.HTML
        )

    def test_nth_col_invalid(self):
        """Test invalid `nth-col` syntax."""

        self.assert_raises('td:nth-col()', SelectorSyntaxError)
        self.assert_raises('td:nth-col(2 of td)', SelectorSyntaxError)
        self.assert_raises('td:nth-col(foo)', SelectorSyntaxError)
