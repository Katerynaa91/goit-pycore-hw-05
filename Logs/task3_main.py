from prettytable import PrettyTable
from sys import argv
from task3_modules import load_logs, parse_log_line, filter_logs_by_level
from task3_modules import logs_to_table, count_logs_by_level, display_log_counts


if __name__ == "__main__":

    """Команди для командного рядка:
    python file_name.py log_file_name.extension 
                    Виводить у командний рядок усі записи лог-файлу у вигляді таблиці 
                    та таблицю з кількістю входжень кожного рівня.
    python file_name.py log_file_name.extension level_name (INFO or DEBUG or ERROR or WARNING) 
                    Виводить у командний рядок записи лог-файлу, прив'язані до окремого рівня, що відповідає останньому аргументу
                    у вигляді таблиці та таблицю з кількістю входжень кожного рівня."""
    try: 
        if len(argv) > 3:
            raise ValueError ("Cannot read arguments. Please recheck if the data was entered correctly.")

        filename = argv[1]
        level = None if len(argv) < 3 else argv[2]

        status_logs = load_logs(filename)
        all_statuses = [parse_log_line(line) for line in status_logs]

        logsTable = PrettyTable()
        columns = [key for key in all_statuses[0].keys()]
        print(logs_to_table(filter_logs_by_level(all_statuses, level), logsTable, columns)) if len(argv) == 3\
        else print(logs_to_table(all_statuses, logsTable, columns))

        levelsTable = display_log_counts(count_logs_by_level(all_statuses))
        print(levelsTable)
        
    except Exception:
        print("Cannot read arguments. Please re-check the entered params")

    