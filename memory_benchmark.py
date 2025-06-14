import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://humanbenchmark.com/tests/memory")

        container_selector = ".css-hvbk5q.eut2yre0"
        container = page.locator(container_selector)

        while True:
            active_cells = page.locator(".css-lxtdud.eut2yre1.active")
            count = await active_cells.count()
            if count == 0:
                await asyncio.sleep(0.1)
                continue

            container_box = await container.bounding_box()
            if container_box is None:
                print("Done")
                break

            positions = []
            for i in range(count):
                cell = active_cells.nth(i)
                cell_box = await cell.bounding_box()
                if cell_box is None:
                    continue
                rel_x = cell_box["x"] - container_box["x"] + cell_box["width"] / 2
                rel_y = cell_box["y"] - container_box["y"] + cell_box["height"] / 2
                positions.append({"x": rel_x, "y": rel_y})

            print(f"Detected {len(positions)} active elements, click in 3s...")

            await asyncio.sleep(3)

            # click
            for pos in positions:
                print(f"Click: x={pos['x']}, y={pos['y']}")
                try:
                    await container.click(position=pos, timeout=3000)
                    await asyncio.sleep(0.2)
                except Exception as e:
                    print(f"Failed to click: {e}")

            await asyncio.sleep(0.8)

if __name__ == "__main__":
    asyncio.run(main())
