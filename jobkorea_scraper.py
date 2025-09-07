from playwright.sync_api import sync_playwright
import time
import os

def capture_developer_jobs_screenshot():
    """
    잡코리아에서 '개발자' 채용 공고를 각각 스크린샷으로 찍는 함수
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        keyword = "개발자"
        url = f"https://www.jobkorea.co.kr/Search/?stext={keyword}"

        print(f"Navigating to job search results for: {keyword}")
        page.goto(url, wait_until='domcontentloaded')

        # 페이지 로드를 위해 잠시 대기
        time.sleep(5)

        # 스크린샷을 저장할 디렉토리 생성
        output_dir = "job_postings_screenshots"
        os.makedirs(output_dir, exist_ok=True)

        # 공고 목록 가져오기 (contains selector)
        job_postings = page.query_selector_all('div[class*="h7nnv10"]')

        if not job_postings:
            print("No job postings found with the new selector.")
            browser.close()
            return

        print(f"Found {len(job_postings)} job postings. Taking screenshots...")

        for i, post in enumerate(job_postings):
            try:
                screenshot_path = os.path.join(output_dir, f"job_posting_{i+1}.png")
                post.screenshot(path=screenshot_path)
                print(f"Screenshot saved to {screenshot_path}")
            except Exception as e:
                print(f"Could not take screenshot for posting {i+1}: {e}")

        browser.close()

if __name__ == '__main__':
    capture_developer_jobs_screenshot()