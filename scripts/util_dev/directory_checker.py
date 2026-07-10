import os

# def get_directory_structure(rootdir):
#     """
#     Tạo cấu trúc thư mục dưới dạng dictionary
#     """
#     structure = {}
#     rootdir = rootdir.rstrip(os.sep)
#     start = rootdir.rfind(os.sep) + 1
#     for path, dirs, files in os.walk(rootdir):
#         folders = path[start:].split(os.sep)
#         subdir = dict.fromkeys(files)
#         parent = reduce(dict.get, folders[:-1], structure)
#         parent[folders[-1]] = subdir
#     return structure

# Hoặc đơn giản hơn - in ra cây thư mục


def print_directory_tree(rootdir, prefix=''):
    print(prefix + os.path.basename(rootdir) + '/')
    prefix += '    '
    for item in os.listdir(rootdir):
        path = os.path.join(rootdir, item)
        if os.path.isdir(path):
            if path.endswith('.git') or path.endswith('__pycache__') or item.startswith('node_modules'):
                continue
            print_directory_tree(path, prefix)
        else:
            print(prefix + item)


# Sử dụng
print_directory_tree('.')  # In cây thư mục từ thư mục hiện tại
