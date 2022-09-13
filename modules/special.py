class StringEditor:

    @staticmethod
    def censor_word(string: str) -> str:
        return f"{string[0]}{'*' * 3}{string[-1:]}"

    @staticmethod
    def censor_email(email: str) -> str:
        arr = email.split("@")
        return f"{StringEditor.censor_word(arr[0])}@{arr[1]}"
