from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configure WebDriver options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/opt/google/chrome/google-chrome"  # Path to Google Chrome

# Set up the WebDriver service
service = Service('/usr/local/bin/chromedriver')  # Ensure this path is correct

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to log into LinkedIn
def login_linkedin(username, password):
    driver.get("https://www.linkedin.com/login")
    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    email_input.send_keys(username)
    password_input.send_keys(password)
    driver.find_element(By.XPATH, '//*[@type="submit"]').click()
    time.sleep(5)  # Wait for login to complete

# Function to extract information from a LinkedIn profile
def extract_info(profile_url):
    try:
        driver.get(profile_url)
        wait = WebDriverWait(driver, 10)
        
        # Extract username
        try:
            username_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.text-body-medium.break-words')))
            username = username_element.text
        except:
            username = 'N/A'
        
        # Extract education level
        try:
            education_element = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.pv-entity__comma-item')))
            education = ', '.join([e.text for e in education_element])
        except:
            education = 'N/A'
        
        # Extract college attended
        try:
            college_element = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h3.pv-entity__school-name')))
            college = ', '.join([c.text for c in college_element])
        except:
            college = 'N/A'
        
        # Extract career progression
        try:
            career_element = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h3.t-16.t-black.t-bold')))
            career = ', '.join([c.text for c in career_element])
        except:
            career = 'N/A'
        
        # Print or save the extracted data
        data = {
            'Username': username,
            'Education Level': education,
            'College Attended': college,
            'Career Progression': career
        }
        print(f'Scraped data from {profile_url}: {data}')
        return data

    except Exception as e:
        print(f'Error scraping {profile_url}: {e}')
        return None

# Your LinkedIn credentials
linkedin_username = 'your-email@example.com'
linkedin_password = 'your-password'

# Log into LinkedIn
login_linkedin(linkedin_username, linkedin_password)

# List of LinkedIn profile URLs to scrape
profile_urls = [
    
]

# Loop through each profile URL and extract information
for url in profile_urls:
    extract_info(url)

# Close the WebDriver
driver.quit()
