from storage.history import load_all


class Check:

    @staticmethod
    def is_posted(title: str):
        return title in load_all()
