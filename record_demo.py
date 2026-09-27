import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ARTIFACT_DIR = Path("/config/.gemini/antigravity/brain/4cb2f6c1-1ed7-498a-b950-8cf7899ae5bb")
URL = "https://travel-concierge-frontend-1026981673167.us-east1.run.app"

async def record_demo():
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="/usr/bin/google-chrome",
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            record_video_dir=str(ARTIFACT_DIR),
            record_video_size={"width": 1280, "height": 800}
        )
        page = await context.new_page()
        
        print("Navigating to frontend...")
        await page.goto(URL, wait_until="networkidle")
        await page.wait_for_timeout(2000)
        
        print("Sending Prompt 1: Destinations in France...")
        # Click example prompt chip 1
        chip = page.locator("button.chip", has_text="Destinations in France")
        if await chip.count() > 0:
            await chip.click()
        else:
            await page.fill("#input", "Find top destinations in France")
            await page.click("button[type='submit']")
            
        # Wait for agent response
        await page.wait_for_selector(".msg.agent .bubble p, .msg.agent .bubble .a2card", timeout=30000)
        await page.wait_for_timeout(5000)
        
        print("Sending Prompt 2: Generate a photo of Santorini at sunset...")
        await page.fill("#input", "Generate a photo of Santorini at sunset")
        await page.click("button[type='submit']")
        
        # Wait for agent response with generated image
        await page.wait_for_timeout(10000)
        
        # Look for generated image and click it to demonstrate Lightbox Modal
        a2img = page.locator("img.a2img")
        if await a2img.count() > 0:
            print("Opening image lightbox modal...")
            await a2img.first.click()
            await page.wait_for_timeout(3000)
            await page.click("#lightbox")
            await page.wait_for_timeout(2000)
            
        print("Demo flow complete. Finalizing video recording...")
        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(record_demo())
