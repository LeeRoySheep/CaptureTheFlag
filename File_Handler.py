
class FileHandler:
    def __init__(self, file_path=None):
        '''
        standardconstructor to create FileHandler object
        from FileHandler class
        '''
        self.file_path = file_path


    def txt_file_to_str(self):
        '''
        method to create string from txt file content
        return: file_content as str
        '''
        with open(self.file_path, 'r') as file:
            file_content = file.read()
        file.close()
        return file_content


def main():
    '''
    main function as usage example and for testing
    '''
    print(FileHandler("rules.txt").txt_file_to_str())

#dunder main for testing
if __name__ == "__main__":
    main()
