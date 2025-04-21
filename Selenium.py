import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def run_jupyter_with_selenium():
    jupyter_url = "http://localhost:8880/lab"
    jupyter_token = "1f5bbcfefa752866ca6f553a9ecbc125e8b51970c2674560"
    full_url = f"{jupyter_url}/?token={jupyter_token}"

    # Configure and start Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        # Open Jupyter Notebook
        print(f"Open Jupyter Notebook by the link: {full_url}")
        driver.get(full_url)

        # Waiting for UI loading
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jp-DirListing-content"))
        )
        print(" Jupyter Notebook was successfully loaded.")

        # Searching for the file
        file_name = "FinalTask_updated.ipynb"
        file_xpath = "//*[@id='filebrowser']/div/div/div[2]/ul/li[1]/span[1]/span[2]/span"
        file_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, f"{file_xpath}[text()='{file_name}']"))
        )

        # Scrolling to element
        driver.execute_script("arguments[0].scrollIntoView(true);", file_element)

        # Click with JavaScript
        driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('dblclick', {bubbles: true}));", file_element)
        print(f"Trying to open file: {file_name}")

        # Waiting for notebook loading
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jp-DirListing-content"))
        )
        print("File was successfully opened.")

        print("Executing all cells in the notebook...")
        run_all_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//jp-button[@title='Restart the kernel and run all cells']"))
        )

        # Click "Restart & Run All"  Restart the kernel and run all cells
        run_all_button.click()

        # Waiting for the Restart confirmation popup dialog and click "Restart"
        print("Handling the Restart confirmation dialog...")
        restart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Restart']"))
        )
        restart_button.click()
        print("Confirmed 'Restart'.")

        # Waiting for execution to complete
        # Execution is tracked by waiting for all cells to finish executing
        print("Waiting for cells to execute...")
        WebDriverWait(driver, 300).until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//div[@class='jp-InputArea-editor' and contains(@class, 'jp-mod-pending')]"))
        )
        print("All cells were executed successfully!")

        # Saving the notebook
        print("Saving the notebook...")
        save_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//jp-button[@title='Save and create checkpoint (⌘ S)']"))
        )
        save_button.click()
        print("Notebook was saved!")

        # idle for 10 secs
        time.sleep(10)

    except Exception as e:
        print(f"Error in interacting with Jupyter Notebook: {e}")

    finally:
        # Quit Selenium
        driver.quit()
        print("Job is completed.")


run_jupyter_with_selenium()