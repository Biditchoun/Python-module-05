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


def testnumeric():
    print("Testing Numeric Processor...")
    test = NumericProcessor()
    val_test = test.validate(42)
    if val_test == 0:
        print(" Trying to validate input '42': False")
    if val_test == 1:
        print(" Trying to validate input '42': True")
    val_test = test.validate("Hello")
    if val_test == 0:
        print(" Trying to validate input 'Hello': False")
    if val_test == 1:
        print(" Trying to validate input 'Hello': True")
    print(" Test invalid ingestion of string 'foo' without prior validation:")
    try:
        test.ingest("foo")
    except Exception as err:
        print(f" Got exception: {err}")
    else:
        print(" Did not get any exception")
    data = [1, 2, 3, 4, 5]
    print(f" Processing data: {data}")
    if not test.validate(data):
        print(" Data was not validated")
        return
    test.ingest(data)
    print(" Extracting 3 values...")
    for i in range(0, 3):
        output_test = test.output()
        print(f" Numeric value {output_test[0]}: {output_test[1]}")


def testtext():
    print("Testing Text Processor...")
    test = TextProcessor()
    val_test = test.validate(42)
    if val_test == 0:
        print(" Trying to validate input '42': False")
    if val_test == 1:
        print(" Trying to validate input '42': True")
    val_test = test.validate("Hello")
    if val_test == 0:
        print(" Trying to validate input 'Hello': False")
    if val_test == 1:
        print(" Trying to validate input 'Hello': True")
    print(" Test invalid ingestion of int '42' without prior validation:")
    try:
        test.ingest(42)
    except Exception as err:
        print(f" Got exception: {err}")
    else:
        print(" Did not get any exception")
    data = ["Hello", "Nexus", "World"]
    print(f" Processing data: {data}")
    if not test.validate(data):
        print(" Data was not validated")
        return
    test.ingest(data)
    print(" Extracting 1 value...")
    output_test = test.output()
    print(f" Text value {output_test[0]}: {output_test[1]}")


def testlog():
    print("Testing Log Processor...")
    test = LogProcessor()
    val_test = test.validate("Hello")
    if val_test == 0:
        print(" Trying to validate input 'Hello': False")
    if val_test == 1:
        print(" Trying to validate input 'Hello': True")
    print(" Test invalid ingestion of string 'foo' without prior validation:")
    try:
        test.ingest("foo")
    except Exception as err:
        print(f" Got exception: {err}")
    else:
        print(" Did not get any exception")
    data = [{"log_level": "NOTICE", "log_message": "Connection to server"},
            {"log_level": "ERROR", "log_message": "Unauthorized access!!"}]
    print(f" Processing data: {data}")
    if not test.validate(data):
        print(" Data was not validated")
        return
    test.ingest(data)
    print(" Extracting 2 values...")
    for i in range(0, 2):
        output_test = test.output()
        print(f" Log entry {output_test[0]}: {output_test[1]}")


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===\n")
    testnumeric()
    print()
    testtext()
    print()
    testlog()
