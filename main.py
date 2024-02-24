from tasks.scrape_offer import Task

if __name__ == "__main__":
    task = Task()
    task.scrape_main_offer()
    task.read()
