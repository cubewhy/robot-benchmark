from playwright.sync_api import sync_playwright
from random import randint

def main():
    with sync_playwright() as p:
        b = p.chromium.launch(headless=False)
        page = b.new_page()
        page.goto("https://humanbenchmark.com/tests/typing")
        page.wait_for_load_state("domcontentloaded")
        end = page.locator("//*[@id=\"root\"]/div/div[4]/div[1]/div/div[3]/button[1]")
        print("start")
        while True:
            letter = page.locator('span.incomplete.current')
            content = letter.text_content()
            if content is None:
                continue
            page.keyboard.type(content)
            # delay = randint(10, 30)
            print(content, end=" ")
            # page.wait_for_timeout(delay)
            if end.is_visible():
                print("\nend")
                break
        page.wait_for_timeout(30000)


if __name__ == "__main__":
    main()
