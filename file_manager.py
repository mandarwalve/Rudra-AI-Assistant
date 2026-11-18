import os

def search_files(directory, keyword):
    results = []

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith("$")]

        for filename in files:
            if keyword.lower() in filename.lower():
                results.append(os.path.join(root, filename))

    return results


if __name__ == "__main__":
    folder = input("Enter folder path: ")
    keyword = input("Enter filename to search: ")

    matches = search_files(folder, keyword)

    print(f"\nFound {len(matches)} file(s):")

    for file in matches:
        print(file)