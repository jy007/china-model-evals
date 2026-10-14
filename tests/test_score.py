from cme.score import classify

TRUTH = {"value": 281724.0, "prior": 245122.0, "unit": "usd_millions"}


def test_exact_match_is_correct():
    assert classify(281724, TRUTH) == "correct"


def test_rounding_within_half_a_million_is_correct():
    assert classify(281724.4, TRUTH) == "correct"


def test_thousand_x_off_is_unit_error():
    assert classify(281724000, TRUTH) == "unit_error"


def test_prior_year_value_is_wrong_period():
    assert classify(245122, TRUTH) == "wrong_period"


def test_negated_value_is_sign_error():
    assert classify(-281724, TRUTH) == "sign_error"


def test_none_is_missing():
    assert classify(None, TRUTH) == "missing"


def test_unrelated_value_is_wrong_value():
    assert classify(123, TRUTH) == "wrong_value"


def test_eps_compares_to_the_cent():
    eps = {"value": 13.64, "prior": 11.80, "unit": "usd_per_share"}
    assert classify(13.64, eps) == "correct"
    assert classify(13.6, eps) == "wrong_value"
