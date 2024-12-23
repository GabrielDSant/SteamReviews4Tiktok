import json
import os
from pathlib import Path
import time
from playwright.sync_api import sync_playwright
import translators as ts  # Biblioteca para tradução
from datetime import datetime

# Utility Functions
def add_transparency(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
    img[:, :, 3] = 240
    cv2.imwrite(img_path, img)



def save_text(review_texts):
    with open("review_texts.txt", "w", encoding="utf-8") as file:
        for idx, text in enumerate(review_texts):
            file.write(f"Review {idx}:\n{text}\n\n")



# Main Function
def download_funny_steam_reviews(app_id, thread_title):
    review_texts = {"thread_id": app_id, "thread_title": thread_title, "comments": [], "intro": False}
    folder_path = f"/steam/assets/{app_id}"
    os.makedirs(folder_path, exist_ok=True)  # Garante que a pasta existe

    with sync_playwright() as p:
        print("Launching Headless Browser")
        browser = p.chromium.launch(headless=True)  # Set to False to see the browser
        page = browser.new_page()
        page.set_viewport_size({"width": 414, "height": 896})

        page.goto(f"https://store.steampowered.com/app/{app_id}/")
        page.wait_for_load_state()

        # Handle age verification if necessary
        if page.locator('#ageYear').is_visible():
            page.select_option('#ageYear', '1990')
            page.click('text="View Page"')
            time.sleep(5)

        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        page.evaluate('document.querySelector("#review_context_funny").click();')
        page.evaluate('ShowFilteredReviews()')
        time.sleep(5)
        # page.screenshot(path=f"./steam_page.png")
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        # display_as_dropdown.click()
        # print("waiti g for funyny to load")
        # time.sleep(2)
        # display_as_dropdown.locator('option[value="funny"]').click(force=True)
        # # Wait for the reviews to load
        # #page.wait_for_selector('.apphub_CardContentMain')

        # # Scroll to load more reviews
        # print("Scrolling to load all reviews")
        # while True:
        #     page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        #     page.wait_for_timeout(2000)  # Wait for new content to load
        #     new_height = page.evaluate("document.body.scrollHeight")
        #     if new_height == previous_height:
        #         break
        #     previous_height = new_height
        review_elements = page.locator("#Reviews_funny .review_box").all()
        review_elements = review_elements[:15]

        for idx, element in enumerate(review_elements):
            if "partial" in element.get_attribute("class"):
                continue

            print("Translating and updating text on page...")
            review_text = element.locator('.content').inner_text()

            # Traduz o texto usando a biblioteca `translators`
            translated_text = ts.translate_text(
                review_text,
                to_language='pt',
                translator="google",
            )

            # Atualiza o texto visível no DOM antes de tirar a screenshot
            page.evaluate(
                """
                ({ elementSelector, newText }) => {
                    const element = document.querySelector(elementSelector);
                    if (element) {
                        element.innerHTML = newText;
                    }
                }
                """,
                {"elementSelector": f"#Reviews_funny .review_box:nth-child({idx + 1}) .content", "newText": translated_text}
            )

            # Captura a screenshot após a tradução
            screenshot_path = f'{folder_path}/{idx}.png'
            element.screenshot(path=screenshot_path)
            print(f"Saved screenshot: {screenshot_path}")

            # Adiciona ao dicionário
            review_texts["comments"].append({
                "comment_body": translated_text,
                "screenshot_path": screenshot_path,
                "original_text": review_text,
                "thread_id": app_id,
                "thread_title": "steam"
            })

        # Salva os dados traduzidos em um arquivo JSON
        with open(f"{folder_path}/review_data.json", "w", encoding="utf-8") as json_file:
            json.dump(review_texts, json_file, ensure_ascii=False, indent=4)
        
        browser.close()

    print("Done!")
