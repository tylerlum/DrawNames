from DrawNames import draw_names, is_valid_drawn_names


def test_draw_names():
    TEST_NUM_TESTS = 20
    TEST_NAMES = ["Ben", "Aaron", "Joel", "Angela", "Zoe", "Ken"]
    TEST_RECIPIENTS_PER_BUYER_MIN = 1
    TEST_RECIPIENTS_PER_BUYER_MAX = 4
    for n_recipients_per_buyer in range(
        TEST_RECIPIENTS_PER_BUYER_MIN, TEST_RECIPIENTS_PER_BUYER_MAX
    ):
        for _ in range(TEST_NUM_TESTS):
            test_results = draw_names(TEST_NAMES, n_recipients_per_buyer)
            assert is_valid_drawn_names(test_results, n_recipients_per_buyer)
