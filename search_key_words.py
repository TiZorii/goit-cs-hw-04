import os
import time
import threading
from multiprocessing import Process, Queue
from queue import Queue as ThreadQueue
from colorama import Fore, Style, init

# Ініціалізація Colorama для роботи з кольоровим текстом у консолі
init(autoreset=True)

# Функція для пошуку ключових слів у файлі


def search_keywords_in_file(file_path, keywords, result_dict, identifier):
    """
    Пошук ключових слів у текстовому файлі.

    Параметри:
    - file_path: шлях до файлу
    - keywords: список ключових слів для пошуку
    - result_dict: словник для зберігання результатів
    - identifier: унікальний ідентифікатор потоку або процесу

    Результат:
    - Оновлює result_dict, додаючи знайдені ключові слова та відповідні файли.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Повідомлення про успішне прочитання файлу
            print(f"{Fore.GREEN}{identifier}: File '{
                  file_path}' read.{Style.RESET_ALL}")
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    if keyword not in result_dict:
                        result_dict[keyword] = []
                    result_dict[keyword].append(file_path)
    except Exception as e:
        # Повідомлення про помилку
        print(f"{Fore.RED}{identifier}: Error reading file {
              file_path}: {e}{Style.RESET_ALL}")

# Функція для обробки файлів з використанням потоків


def threading_approach(file_paths, keywords):
    """
    Пошук ключових слів у текстових файлах з використанням потоків.

    Параметри:
    - file_paths: список файлів
    - keywords: список ключових слів для пошуку

    Результат:
    - Повертає словник із ключовими словами та відповідними файлами.
    """
    threads = []
    results = ThreadQueue()  # Потокова черга для зберігання результатів
    results_dict = {}

    def worker(file_paths_chunk, thread_id):
        """
        Робоча функція для потоків.
        Пошук ключових слів у частині файлів.
        """
        local_results = {}
        for file_path in file_paths_chunk:
            search_keywords_in_file(
                file_path, keywords, local_results, f"Thread-{thread_id}")
        results.put(local_results)

    # Розподіл файлів між потоками
    num_threads = min(len(file_paths), 3)  # Ліміт потоків до 3
    chunk_size = len(file_paths) // num_threads
    for i in range(num_threads):
        chunk = file_paths[i * chunk_size:(
            i + 1) * chunk_size] if i < num_threads - 1 else file_paths[i * chunk_size:]
        thread = threading.Thread(target=worker, args=(chunk, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Об'єднання результатів із потоків
    while not results.empty():
        partial_result = results.get()
        for keyword, paths in partial_result.items():
            if keyword not in results_dict:
                results_dict[keyword] = []
            results_dict[keyword].extend(paths)

    return results_dict

# Глобальна функція для роботи з процесами


def multiprocessing_worker(file_paths_chunk, keywords, queue, process_id):
    """
    Робоча функція для процесів.
    Пошук ключових слів у частині файлів і передача результатів через чергу.
    """
    local_results = {}
    for file_path in file_paths_chunk:
        search_keywords_in_file(file_path, keywords,
                                local_results, f"Process-{process_id}")
    queue.put(local_results)

# Функція для обробки файлів з використанням багатопроцесорності


def multiprocessing_approach(file_paths, keywords):
    """
    Пошук ключових слів у текстових файлах з використанням багатопроцесорності.

    Параметри:
    - file_paths: список файлів
    - keywords: список ключових слів для пошуку

    Результат:
    - Повертає словник із ключовими словами та відповідними файлами.
    """
    processes = []
    queue = Queue()  # Черга для результатів
    results_dict = {}

    # Розподіл файлів між процесами
    num_processes = min(len(file_paths), 3)  # Ліміт процесів до 3
    chunk_size = len(file_paths) // num_processes
    for i in range(num_processes):
        chunk = file_paths[i * chunk_size:(
            i + 1) * chunk_size] if i < num_processes - 1 else file_paths[i * chunk_size:]
        process = Process(target=multiprocessing_worker,
                          args=(chunk, keywords, queue, i))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    # Об'єднання результатів із процесів
    while not queue.empty():
        partial_result = queue.get()
        for keyword, paths in partial_result.items():
            if keyword not in results_dict:
                results_dict[keyword] = []
            results_dict[keyword].extend(paths)

    return results_dict

# Основна функція програми


def main():
    """
    Основна функція, яка запускає підходи з потоками та багатопроцесорністю
    для пошуку ключових слів у текстових файлах.
    """
    # Ключові слова для пошуку
    keywords = ["error", "keyword", "test"]

    # Пошук файлів з розширенням .txt
    file_paths = [f for f in os.listdir(".") if f.endswith(".txt")]
    print(f"{Fore.YELLOW}Found text files: {file_paths}{Style.RESET_ALL}\n")

    if not file_paths:
        print(f"{Fore.RED}No .txt files found. Exiting.{Style.RESET_ALL}")
        return

    # Підхід з потоками
    print(f"{Fore.MAGENTA}--- Threading Approach ---{Style.RESET_ALL}")
    start_time = time.time()
    threading_results = threading_approach(file_paths, keywords)
    threading_time = time.time() - start_time
    print(f"{Fore.MAGENTA}Threading results:{Style.RESET_ALL}")
    for keyword, files in threading_results.items():
        print(f"{Fore.LIGHTCYAN_EX}{keyword}: {files}")
    print(f"{Fore.YELLOW}Time taken: {
          threading_time:.2f} seconds{Style.RESET_ALL}\n")

    # Підхід з багатопроцесорністю
    print(f"{Fore.MAGENTA}--- Multiprocessing Approach ---{Style.RESET_ALL}")
    start_time = time.time()
    multiprocessing_results = multiprocessing_approach(file_paths, keywords)
    multiprocessing_time = time.time() - start_time
    print(f"{Fore.MAGENTA}Multiprocessing results:{Style.RESET_ALL}")
    for keyword, files in multiprocessing_results.items():
        print(f"{Fore.LIGHTCYAN_EX}{keyword}: {files}")
    print(f"{Fore.YELLOW}Time taken: {
          multiprocessing_time:.2f} seconds{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
