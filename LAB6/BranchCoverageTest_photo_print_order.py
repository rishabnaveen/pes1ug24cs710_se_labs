import pytest
from photo_print_order import extra_print_charge, order_valid, dispatch_status


# --- Branch Tests for extra_print_charge ---
def test_branch_invalid_print_size():
    with pytest.raises(ValueError, match="unknown print size"):
        extra_print_charge("invalid", 10, "matte", False)


def test_branch_negative_copies():
    with pytest.raises(ValueError, match="invalid copies"):
        extra_print_charge("4x6", -1, "matte", False)


def test_branch_extra_zero_or_negative():
    # Boundary: copies == included (20) -> extra = 0 -> returns 0
    assert extra_print_charge("4x6", 20, "matte", False) == 0


def test_branch_is_member_true_not_8x10():
    # is_member True AND size != "8x10": included = 15 + 5 = 20; copies = 30 -> extra = 10; rate = 4
    assert extra_print_charge("5x7", 30, "matte", True) == 10 * 4


def test_branch_is_member_true_is_8x10():
    # is_member True AND size == "8x10": included stays 10; copies = 20 -> extra = 10; rate = 7
    assert extra_print_charge("8x10", 20, "glossy", True) == 10 * 7


def test_branch_is_member_false():
    # is_member False: included stays 20; copies = 30 -> extra = 10; rate = 7
    assert extra_print_charge("4x6", 30, "glossy", False) == 10 * 7


def test_branch_extra_greater_than_50_matte():
    # extra = 60 > 50, finish != "canvas" (matte) -> rate = 4 + 2 = 6
    assert extra_print_charge("4x6", 80, "matte", False) == 60 * 6


def test_branch_extra_greater_than_50_canvas():
    # extra = 60 > 50, finish == "canvas" -> rate = 7 + 2 + 5 = 14
    assert extra_print_charge("4x6", 80, "canvas", False) == 60 * 14


# --- Branch Tests for order_valid ---
def test_branch_rush_true_copies_le_50():
    assert order_valid(10, 50, True) is True


def test_branch_rush_true_copies_gt_50():
    assert order_valid(10, 51, True) is False


def test_branch_rush_false_file_mb_gt_25():
    assert order_valid(26, 100, False) is False


def test_branch_rush_false_file_mb_le_25_copies_le_500():
    assert order_valid(25, 500, False) is True


def test_branch_rush_false_file_mb_le_25_copies_gt_500():
    assert order_valid(25, 501, False) is False


# --- Branch Tests for dispatch_status ---
def test_branch_dispatch_framed_international_on_time():
    # framed (24) + intl (24) = cutoff 48. hours = 48 >= 48 -> "on_time"
    assert dispatch_status(48, True, True) == "on_time"


def test_branch_dispatch_unframed_domestic_on_time():
    # unframed (12) + domestic (0) = cutoff 12. hours = 12 >= 12 -> "on_time"
    assert dispatch_status(12, False, False) == "on_time"


def test_branch_dispatch_tight():
    # cutoff = 12. hours = 6 (cutoff - 6 is 6; 6 >= 6) -> "tight"
    assert dispatch_status(6, False, False) == "tight"


def test_branch_dispatch_missed():
    # cutoff = 12. hours = 5 (< 6) -> "missed"
    assert dispatch_status(5, False, False) == "missed"