import sys

if __name__ == '__main':
    path_to_append = 'D:\\PycharmProjects\\PunishmentBook'  # Use double backslashes for Windows paths

    try:
        # Add the path to sys.path
        sys.path.append(path_to_append)
        print(f'Successfully appended path: {path_to_append} to sys.path')
    except Exception as e:
        print(f'An error occurred while appending the path to sys.path: {e}')
