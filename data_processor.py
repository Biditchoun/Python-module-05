import abc


class DataProcessor(ABC):
	def validate(self, data: Any) -> bool:
		pass
	
	def ingest(self, data: Any) -> None:
		pass
	
	def output(self) -> tuple[int, str]:
		print(data)
		return


class NumericProcessor(DataProcessor):
	pass


class TextProcessor(DataProcessor):
	pass


class LogProcessor(DataProcessor):
	pass
