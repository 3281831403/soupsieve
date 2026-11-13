"""Test column combinators."""
from .. import util
from soupsieve import SelectorSyntaxError


class TestColumn(util.TestCase):
    """Test column combinators."""

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

    def test_column(self):
        """Test the column combinator."""

        for flags in (util.HTML, util.HTML | util.NOCACHE):
            self.assert_selector(
                self.MARKUP,
                "col.first || td",
                ["c12", "d1"],
                flags=flags
            )

    def test_column_spanning_col(self):
        """Test that a `col` with a `span` represents each of its columns."""

        self.assert_selector(
            self.MARKUP,
            "col.price || td",
            ["c12", "c3", "d2", "d3", "e2", "e3"],
            flags=util.HTML
        )

    def test_column_no_spaces(self):
        """Test the column combinator with no spaces."""

        self.assert_selector(
            self.MARKUP,
            "col.price||td",
            ["c12", "c3", "d2", "d3", "e2", "e3"],
            flags=util.HTML
        )

    def test_column_header(self):
        """Test the column combinator on table header cells."""

        # The second `colgroup` declares a column with no `col` element,
        # so the fourth column cannot be matched through a `col`.
        self.assert_selector(
            self.MARKUP,
            "col || th",
            ["h1", "h2", "h3"],
            flags=util.HTML
        )

    def test_column_complex_left(self):
        """Test the column combinator with a complex selector on the left."""

        self.assert_selector(
            self.MARKUP,
            "colgroup col.price || td",
            ["c12", "c3", "d2", "d3", "e2", "e3"],
            flags=util.HTML
        )

    def test_column_no_col_elements(self):
        """Test that a table without `col` elements matches nothing."""

        self.assert_selector(
            self.MARKUP,
            "#plain col || td",
            [],
            flags=util.HTML
        )

    def test_column_not_in_table(self):
        """Test that elements that are not cells in a table match nothing."""

        self.assert_selector(
            self.MARKUP,
            "col || div",
            [],
            flags=util.HTML
        )

    def test_column_nested_tables(self):
        """Test that the column combinator uses the table the cell belongs to."""

        markup = """
        <table id="outer">
        <colgroup><col class="outer-col"></colgroup>
        <tr>
        <td id="o1">1</td>
        <td id="o2">
        <table id="inner">
        <colgroup><col class="inner-col" span="2"></colgroup>
        <tr>
        <td id="i1">1</td>
        <td id="i2">2</td>
        </tr>
        </table>
        </td>
        </tr>
        </table>
        """

        self.assert_selector(
            markup,
            "col.inner-col || td",
            ["i1", "i2"],
            flags=util.HTML
        )

        self.assert_selector(
            markup,
            "col.outer-col || td",
            ["o1"],
            flags=util.HTML
        )

    def test_column_invalid(self):
        """Test invalid column combinator syntax."""

        self.assert_raises('|| td', SelectorSyntaxError)
        self.assert_raises('col ||', SelectorSyntaxError)
        self.assert_raises('col || || td', SelectorSyntaxError)
