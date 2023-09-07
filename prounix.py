from conftest import (passing_basic_auth, login_to_web_personal_account, select_draft_offer,
                      open_easy_automation_funding_offer, open_spending_and_financing_plan, add_material_costs)


def test_create_easy_automation_offer(browser):
    # steps
    passing_basic_auth(browser)
    login_to_web_personal_account(browser)
    select_draft_offer(browser)
    open_easy_automation_funding_offer(browser)
    open_spending_and_financing_plan(browser)


def test_fill_material_costs(browser):
    # steps
    passing_basic_auth(browser)
    login_to_web_personal_account(browser)
    select_draft_offer(browser)
    open_easy_automation_funding_offer(browser)
    open_spending_and_financing_plan(browser)
    add_material_costs(browser, '1000000,00')
