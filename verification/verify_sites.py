from playwright.sync_api import sync_playwright

def verify_sites():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Verify ahigovernance.com (Banner and Pricing)
        print("Verifying ahigovernance.com...")
        page.goto("http://localhost:8080/sitios-web/ahigovernance.com/index.html")

        # Screenshot Banner (Search for "ECP-1 Captcha Ético")
        banner = page.get_by_text("ECP-1 Captcha Ético").first
        if banner.is_visible():
            banner.scroll_into_view_if_needed()
            page.screenshot(path="verification/ahigovernance_banner.png")
            print("Captured ahigovernance_banner.png")
        else:
            print("Banner NOT found!")

        # Screenshot Pricing (Search for "Inversión en Fiabilidad")
        pricing = page.get_by_text("Inversión en Fiabilidad").first
        if pricing.is_visible():
            pricing.scroll_into_view_if_needed()
            page.screenshot(path="verification/ahigovernance_pricing.png")
            print("Captured ahigovernance_pricing.png")
        else:
            print("Pricing NOT found!")

        # 2. Verify sovereignsymbiosis.com (Timeline)
        print("Verifying sovereignsymbiosis.com...")
        page.goto("http://localhost:8080/sitios-web/sovereignsymbiosis.com/index.html")

        # Screenshot Timeline (Search for "ELIZA Translator")
        timeline = page.get_by_text("ELIZA Translator").first
        if timeline.is_visible():
            timeline.scroll_into_view_if_needed()
            page.screenshot(path="verification/sovereign_timeline.png")
            print("Captured sovereign_timeline.png")
        else:
            print("Timeline item NOT found!")

        # 3. Verify eliza.html
        print("Verifying eliza.html...")
        page.goto("http://localhost:8080/sitios-web/sovereignsymbiosis.com/eliza.html")
        page.screenshot(path="verification/eliza_page.png")
        print("Captured eliza_page.png")

        # 4. Verify ethic-check (Footer)
        print("Verifying ethic-check...")
        page.goto("http://localhost:8080/sitios-web/ethic-check/index.html")

        # Scroll to bottom
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.screenshot(path="verification/ethic_check_footer.png")
        print("Captured ethic_check_footer.png")

        browser.close()

if __name__ == "__main__":
    verify_sites()
