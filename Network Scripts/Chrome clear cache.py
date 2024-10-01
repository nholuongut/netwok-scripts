import subprocess
import os
import threading

def clear_chrome_cache():
    try:
        # Replace this path with the actual path to your Chrome executable
        chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        
        # Ensure Chrome is not running before clearing the cache
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Build the command to clear the cache
        cache_clear_command = [
            chrome_path,
            "--user-data-dir=TempProfile",
            "--disk-cache-size=1",
            "--media-cache-size=1",
            "--disable-application-cache",
        ]
        
        # Execute the command
        subprocess.run(cache_clear_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Clean up temporary profile directory
        temp_profile_dir = os.path.join(os.path.expanduser('~'), 'TempProfile')
        if os.path.exists(temp_profile_dir):
            os.rmdir(temp_profile_dir)
        
        print("Chrome cache has been cleared.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    num_threads = 2  # Number of threads to use
    
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=clear_chrome_cache)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
if __name__ == "__main__":
    main()