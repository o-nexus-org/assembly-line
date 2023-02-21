from src.checks import raise_err_if_file_is_filled_in


def test_fun_gives_none_when_good_file():
    file = 'testing/data/correct_prov_template.xlsx'
    assert raise_err_if_file_is_filled_in(file) is None


def test_fun_gives_error_when_already_filled_in_file():
    file = 'testing/data/filled_in_prov_template.xlsx'
    err_msg = raise_err_if_file_is_filled_in(file)
    assert isinstance(err_msg, str)