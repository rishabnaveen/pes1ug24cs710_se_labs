import pytest
from photo_print_order import extra_print_charge, order_valid, dispatch_status


# --- Tests for extra_print_charge ---
def test_extra_print_charge_invalid_size():
    with pytest.raises(ValueError, match="unknown print size"):
        extra_print_charge("invalid_size", 10, "matte", False)


def test_extra_print_charge_negative_copies():
    with pytest.raises(ValueError, match="invalid copies"):
        extra_print_charge("4x6", -5, "matte", False)


def test_extra_print_charge_within_included():
    assert extra_print_charge("4x6", 15, "matte", False) == 0


def test_extra_print_charge_member_not_8x10():
    # 5x7 member included = 15 + 5 = 20; copies = 25 -> extra = 5; matte rate = 4
    assert extra_print_charge("5x7", 25, "matte", True) == 5 * 4


def test_extra_print_charge_member_with_8x10():
    # 8x10 member: included stays 10; copies = 20 -> extra = 10; glossy rate = 7
    assert extra_print_charge("8x10", 20, "glossy", True) == 10 * 7


def test_extra_print_charge_extra_greater_than_50_non_canvas():
    # 4x6 non-member included = 20; copies = 80 -> extra = 60; matte rate = 4 + 2 = 6
    assert extra_print_charge("4x6", 80, "matte", False) == 60 * 6


def test_extra_print_charge_extra_greater_than_50_canvas():
    # 4x6 non-member included = 20; copies = 80 -> extra = 60; canvas rate = 7 + 2 + 5 = 14
    assert extra_print_charge("4x6", 80, "canvas", False) == 60 * 14


# --- Tests for order_valid ---
def test_order_valid_rush_allowed():
    assert order_valid(10, 30, True) is True


def test_order_valid_rush_exceeded():
    assert order_valid(10, 60, True) is False


def test_order_valid_file_too_large():
    assert order_valid(30, 100, False) is False


def test_order_valid_standard_allowed():
    assert order_valid(20, 200, False) is True


def test_order_valid_standard_copies_exceeded():
    assert order_valid(20, 600, False) is False


# --- Tests for dispatch_status ---
def test_dispatch_status_framed_international_on_time():
    # cutoff = 24 + 24 = 48; hours = 50 >= 48 -> "on_time"
    assert dispatch_status(50, True, True) == "on_time"


def test_dispatch_status_unframed_domestic_tight():
    # cutoff = 12 + 0 = 12; hours = 8 (cutoff - 6 is 6; 8 >= 6) -> "tight"
    assert dispatch_status(8, False, False) == "tight"


def test_dispatch_status_unframed_domestic_missed():
    # cutoff = 12; hours = 4 (< 6) -> "missed"
    assert dispatch_status(4, False, False) == "missed"