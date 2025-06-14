import asyncio
from playwright.async_api import async_playwright

async def auto_click_until_disappear(url: str, selector: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto(url)

        while True:
            container = page.locator(".css-1k4dpwl")
            point = page.locator(".css-17nnhwz").first

            await container.wait_for()
            await point.wait_for()

            container_box = await container.bounding_box()
            point_box = await point.bounding_box()

            if container_box is None or point_box is None:
                print("Completed")
                return

            relative_x = point_box["x"] - container_box["x"] + point_box["width"] / 2
            relative_y = point_box["y"] - container_box["y"] + point_box["height"] / 2

            print(f"Click: x={relative_x}, y={relative_y}")

            await container.click(position={"x": relative_x, "y": relative_y}, force=True)

        # await browser.close()

if __name__ == "__main__":
    url = "https://humanbenchmark.com/tests/aim"
    selector = ".e6yfngs1"
    asyncio.run(auto_click_until_disappear(url, selector))
