"""Test `nth-last-col` selectors."""
from .. import util


class TestNthLastCol(util.TestCase):
    """Test `nth-last-col` selectors."""

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
    """

    def test_nth_last_col(self):
        """Test `nth-last-col` with a specific column."""

        for flags in (util.HTML, util.HTML | util.NOCACHE):
            self.assert_selector(
                self.MARKUP,
                "td:nth-last-col(1)",
                ["c4", "d4", "e4"],
                flags=flags
            )

    def test_nth_last_col_spanning_cell(self):
        """Test that a cell that spans columns matches for each column it covers."""

        self.assert_selector(
            self.MARKUP,
            "td:nth-last-col(3)",
            ["c12", "d2", "e2"],
            flags=util.HTML
        )

        self.assert_selector(
            self.MARKUP,
            "td:nth-last-col(4)",
            ["c12", "d1"],
            flags=util.HTML
        )

    def test_nth_last_col_pattern(self):
        """Test `nth-last-col` with an `an+b` pattern."""

        # With four columns, even from the end is columns one and three.
        self.assert_selector(
            self.MARKUP,
            "td:nth-last-col(2n)",
            ["c12", "c3", "d1", "d3", "e3"],
            flags=util.HTML
        )

        self.assert_selector(
            self.MARKUP,
            "td:nth-last-col(even)",
            ["c12", "c3", "d1", "d3", "e3"],
            flags=util.HTML
        )

    def test_nth_last_col_header(self):
        """Test `nth-last-col` on table header cells."""

        self.assert_selector(
            self.MARKUP,
            "th:nth-last-col(1)",
            ["h4"],
            flags=util.HTML
        )

    def test_nth_last_col_nested_tables(self):
        """Test that the last column is counted within each table, not the document."""

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

        self.assert_selector(
            markup,
            "#inner td:nth-last-col(1)",
            ["i3"],
            flags=util.HTML
        )

        self.assert_selector(
            markup,
            "#outer td:nth-last-col(1)",
            ["o2", "i3"],
            flags=util.HTML
        )
