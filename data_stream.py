from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self):
        self.nb = 0
        self.data = list

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self.data:
            return (-1, "Nothing to output")
        rt = (self.nb, self.data[0])
        del self.data[0]
        self.nb += 1
        return rt


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if not isinstance(data, list):
            return False
        for element in data:
            if not isinstance(element, (int, float)):
                return False
        return True

    def ingest(self, data: int | float | list) -> None:
        if not self.validate(data):
            raise Exception("Improper numeric data")
        if isinstance(data, (int, float)):
            self.data = [str(data)]
            return
        self.data = []
        for element in data:
            self.data.append(str(element))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if not isinstance(data, list):
            return False
        for element in data:
            if not isinstance(element, str):
                return False
        return True

    def ingest(self, data: str | list) -> None:
        if not self.validate(data):
            raise Exception("Improper text data")
        if isinstance(data, str):
            self.data = [data]
        else:
            self.data = data


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            for key in data.keys():
                if not isinstance(key, str):
                    return False
                if not isinstance(data.get(key), str):
                    return False
            return True
        if not isinstance(data, list):
            return False
        for element in data:
            if not isinstance(element, dict):
                return False
            for key in element.keys():
                if not isinstance(key, str):
                    return False
                if not isinstance(element.get(key), str):
                    return False
        return True

    def ingest(self, data: dict | list) -> None:
        if not self.validate(data):
            raise Exception("Improper log data")
        if isinstance(data, dict):
            self.data = [f"{data.get('log_level')}: {data.get('log_message')}"]
            return
        self.data = []
        for element in data:
            self.data.append(f"{element.get('log_level')}: "
                             f"{element.get('log_message')}")


class DataStream():
	def __init__(self):
		self.processors = []

	def register_processor(self, proc: DataProcessor) -> None:
		self.processors.append(proc)
	
	def process_stream(self, stream: list[typing.Any]) -> None:
		for element in stream:
			check = 0
			for processor in self.processors:
				try:
					processor(element)
				except Exception:
					pass
				else:
					check = 1
					break
			if check == 0:
				print(f"DataStream - Can't process element in stream: {element}")

	def print_processors_stats(self) -> None:
		pass


if __name__ == "__main__":
    print("=== Code Nexus - Data Stream ===\n")
