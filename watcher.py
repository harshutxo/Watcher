import psutil
import time
import datetime
import csv
import os

# --- Configuration ---
LOG_INTERVAL_SECONDS = 5  # How often to log data (in seconds)
LOG_FILE_NAME = 'system_performance_log.csv'
CSV_HEADER = ['Timestamp', 'CPU Usage (%)', 'Memory Usage (%)']

def get_system_stats():
    """
    Retrieves current CPU and memory usage.

    Returns:
        tuple: A tuple containing CPU usage percentage and memory usage percentage.
               Returns (None, None) if an error occurs.
    """
    try:
        # Get CPU usage percentage
        # interval=1 means it will block for 1 second to measure CPU usage.
        # Using interval=None or 0.0 makes it non-blocking but can result in less accurate initial readings.
        cpu_usage = psutil.cpu_percent(interval=1)

        # Get virtual memory usage (RAM)
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent
        return cpu_usage, memory_usage
    except Exception as e:
        print(f"Error getting system stats: {e}")
        return None, None

def write_log_entry(file_writer, cpu_usage, memory_usage):
    """
    Writes a new entry to the CSV log file.

    Args:
        file_writer: The csv.writer object for the log file.
        cpu_usage (float): Current CPU usage percentage.
        memory_usage (float): Current memory usage percentage.
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        file_writer.writerow([timestamp, cpu_usage, memory_usage])
        print(f"{timestamp} - CPU: {cpu_usage}%, Memory: {memory_usage}% - Logged.")
    except Exception as e:
        print(f"Error writing to log file: {e}")

def main():
    """
    Main function to start monitoring and logging.
    """
    print(f"Starting system performance monitoring. Logging to '{LOG_FILE_NAME}' every {LOG_INTERVAL_SECONDS} seconds.")
    print("Press Ctrl+C to stop.")

    # Check if the log file exists to write the header
    file_exists = os.path.isfile(LOG_FILE_NAME)

    try:
        with open(LOG_FILE_NAME, mode='a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)

            # Write header only if the file is new or empty
            if not file_exists or os.path.getsize(LOG_FILE_NAME) == 0:
                csv_writer.writerow(CSV_HEADER)
                print("CSV header written.")

            while True:
                cpu_usage, memory_usage = get_system_stats()

                if cpu_usage is not None and memory_usage is not None:
                    write_log_entry(csv_writer, cpu_usage, memory_usage)
                else:
                    # Optionally, log an error marker or skip
                    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Failed to retrieve stats.")


                # Wait for the specified interval
                time.sleep(LOG_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Exiting script.")

if __name__ == "__main__":
    # Before running, ensure you have psutil installed:
    # pip install psutil
    main()
