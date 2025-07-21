import pytest
from playwright.async_api import async_playwright

@pytest.mark.asyncio
async def test_browser_launch():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com")
        assert await page.title() == "Example Domain"
        await browser.close()
