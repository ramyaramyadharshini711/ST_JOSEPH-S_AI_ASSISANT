# website_scraper.py
import requests
from bs4 import BeautifulSoup
import json

# List of all college URLs
college_urls = [
    "https://stjosephcollegetup.edu.in/",
"https://stjosephcollegetup.edu.in/submenu.php?slug=research",
"https://stjosephcollegetup.edu.in/submenu.php?slug=iic",
"https://stjosephcollegetup.edu.in/submenu.php?slug=nirf",
"https://stjosephcollegetup.edu.in/submenu.php?slug=iqac",
"https://stjosephcollegetup.edu.in/submenu.php?slug=aishe",
"https://stjosephcollegetup.edu.in/submenu.php?slug=nad",
"https://stjosephcollegetup.edu.in/submenu.php?slug=naac",
"https://stjosephcollegetup.edu.in/fee-payment.php",
"https://stjosephcollegetup.edu.in/ug-admission.php",
"https://stjosephcollegetup.edu.in/pg-admission.php",
"https://stjosephcollegetup.edu.in/index.php",
"https://stjosephcollegetup.edu.in/submenu.php?slug=about-sjc",
"https://stjosephcollegetup.edu.in/submenu.php?slug=history",
"https://stjosephcollegetup.edu.in/submenu.php?slug=emblem",
"https://stjosephcollegetup.edu.in/submenu.php?slug=milestones",
"https://stjosephcollegetup.edu.in/submenu.php?slug=infrastructure",
"https://stjosephcollegetup.edu.in/submenu.php?slug=secretary-desk",
"https://stjosephcollegetup.edu.in/submenu.php?slug=principal-desk",
"https://stjosephcollegetup.edu.in/submenu.php?slug=governing-body",
"https://stjosephcollegetup.edu.in/submenu.php?slug=prospectus",
"https://stjosephcollegetup.edu.in/submenu.php?slug=admission-procedure",
"https://stjosephcollegetup.edu.in/submenu.php?slug=programmes-offered",
"https://stjosephcollegetup.edu.in/submenu.php?slug=departments",
"https://stjosephcollegetup.edu.in/submenu.php?slug=library",
"https://stjosephcollegetup.edu.in/submenu.php?slug=syllabus",
"https://stjosephcollegetup.edu.in/submenu.php?slug=teaching-faculty",
"https://stjosephcollegetup.edu.in/submenu.php?slug=non-teaching-staff",
"https://stjosephcollegetup.edu.in/submenu.php?slug=research",
"https://stjosephcollegetup.edu.in/submenu.php?slug=physical-education",
"https://stjosephcollegetup.edu.in/submenu.php?slug=association",
"https://stjosephcollegetup.edu.in/submenu.php?slug=register-here",
"https://stjosephcollegetup.edu.in/submenu.php?slug=alumnae-video",
"https://stjosephcollegetup.edu.in/gallery.php",
"https://stjosephcollegetup.edu.in/submenu.php?slug=grievance-cell",
"https://stjosephcollegetup.edu.in/submenu.php?slug=anti-ragging",
"https://stjosephcollegetup.edu.in/submenu.php?slug=icc",
"https://stjosephcollegetup.edu.in/submenu.php?slug=counselling-cell",
"https://stjosephcollegetup.edu.in/submenu.php?slug=feedback",
"https://stjosephcollegetup.edu.in/submenu.php?slug=examination",
"https://stjosephcollegetup.edu.in/submenu.php?slug=placement",
"https://stjosephcollegetup.edu.in/contact.php",
"https://stjosephcollegetup.edu.in/submenu.php?slug=students-union",
"https://stjosephcollegetup.edu.in/submenu.php?slug=sjc-clubs",
"https://stjosephcollegetup.edu.in/submenu.php?slug=code-of-conduct",
"https://stjosephcollegetup.edu.in/submenu.php?slug=scholarships",
"https://stjosephcollegetup.edu.in/submenu.php?slug=academic-calendar#cal-2025-2026",
"https://stjosephcollegetup.edu.in/submenu.php?slug=academic-calendar#cal-2024-2025",
"https://stjosephcollegetup.edu.in/submenu.php?slug=academic-calendar#cal-2023-2024",
"https://stjosephcollegetup.edu.in/submenu.php?slug=academic-calendar#cal-2022-2023",
"https://stjosephcollegetup.edu.in/submenu.php?slug=cocurricular#nss",
"https://stjosephcollegetup.edu.in/submenu.php?slug=cocurricular#yrc-rrc",
"https://stjosephcollegetup.edu.in/submenu.php?slug=cocurricular#campus-ministry",
"https://stjosephcollegetup.edu.in/submenu.php?slug=cocurricular#sports",
"https://stjosephcollegetup.edu.in/submenu.php?slug=cocurricular#womens-cell",
"https://stjosephcollegetup.edu.in/submenu.php?slug=cocurricular#aicuf",
"https://stjosephcollegetup.edu.in/submenu.php?slug=cocurricular#fine-arts",
"https://stjosephcollegetup.edu.in/submenu.php?slug=cocurricular#elc",
"https://stjosephcollegetup.edu.in/submenu.php?slug=download-forms#form-01",
"https://stjosephcollegetup.edu.in/submenu.php?slug=download-forms#form-02",
"https://stjosephcollegetup.edu.in/submenu.php?slug=download-forms#form-03",
"https://stjosephcollegetup.edu.in/submenu.php?slug=download-forms#form-04",
"https://stjosephcollegetup.edu.in/submenu.php?slug=download-forms#form-05",
"https://stjosephcollegetup.edu.in/submenu.php?slug=download-forms#form-06"
    # ... all URLs from the comprehensive list above
]

def fetch_page_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted tags
        for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            tag.decompose()

        content = soup.get_text(separator="\n", strip=True)

        return content

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def save_all_pages():
    all_text = ""

    for url in college_urls:
        print("Fetching:", url)

        text = fetch_page_content(url)

        if text:
            all_text += "\n\n"
            all_text += "=" * 80 + "\n"
            all_text += url + "\n"
            all_text += "=" * 80 + "\n"
            all_text += text

    with open(
        "knowledge_base/college_info.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(all_text)

    print("Knowledge base saved successfully!")

if __name__ == "__main__":
    save_all_pages()