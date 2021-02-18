import importlib
from concurrent.futures import ThreadPoolExecutor
from utils import Database, Data, Metadata, ObjectStorage
from constants import Constants


class Parameters:
    __DATASET_KEY_CHARACTER = "$"
    __DATASET_WITH_OBJECT_KEY_CHARACTER = "."
    __REMOVE_KEY_CHARACTER = ""

    def __init__(self, database: Database, data: Data):
        self.__database_connector = database
        self.__data = data

    def treat(self, method_parameters: dict) -> dict:
        parameters = method_parameters.copy()

        for name, value in parameters.items():
            if self.__is_dataset(value):
                dataset_name = self.__get_dataset_name_from_value(
                    value)
                if self.__has_dot_in_dataset_name(value):
                    object_name = self.__get_name_after_dot_from_value(value)

                    parameters[name] = self.__data.get_object_from_dataset(
                        dataset_name, object_name)

                else:
                    parameters[name] = self.__data.get_dataset_content(
                        dataset_name)

        return parameters

    def __is_dataset(self, value: str) -> bool:
        return self.__DATASET_KEY_CHARACTER in value

    def __get_dataset_name_from_value(self, value: str) -> str:
        dataset_name = value.replace(self.__DATASET_KEY_CHARACTER,
                                     self.__REMOVE_KEY_CHARACTER)
        return dataset_name.split(self.__DATASET_WITH_OBJECT_KEY_CHARACTER)[
            Constants.FIRST_ARGUMENT]

    def __has_dot_in_dataset_name(self, dataset_name: str) -> bool:
        return self.__DATASET_WITH_OBJECT_KEY_CHARACTER in dataset_name

    def __get_name_after_dot_from_value(self, value: str) -> str:
        return value.split(
            self.__DATASET_WITH_OBJECT_KEY_CHARACTER)[Constants.SECOND_ARGUMENT]


class Execution:
    __DATASET_KEY_CHARACTER = "$"
    __REMOVE_KEY_CHARACTER = ""

    def __init__(self,
                 database_connector: Database,
                 executor_name: str,
                 executor_service_type: str,
                 parent_name: str,
                 parent_name_service_type: str,
                 metadata_creator: Metadata,
                 class_method: str,
                 parameters_handler: Parameters,
                 storage: ObjectStorage,
                 ):
        self.__metadata_creator = metadata_creator
        self.__thread_pool = ThreadPoolExecutor()
        self.__database_connector = database_connector
        self.__storage = storage
        self.__parameters_handler = parameters_handler
        self.executor_name = executor_name
        self.parent_name = parent_name
        self.class_method = class_method
        self.executor_service_type = executor_service_type
        self.parent_name_service_type = parent_name_service_type

    def create(self,
               module_path: str,
               class_name: str,
               method_parameters: dict,
               description: str) -> None:

        self.__metadata_creator.create_file(self.parent_name,
                                            self.executor_name,
                                            module_path,
                                            class_name,
                                            self.class_method,
                                            self.executor_service_type)

        self.__thread_pool.submit(self.__pipeline,
                                  module_path,
                                  method_parameters,
                                  description)

    def update(self,
               module_path: str,
               method_parameters: dict,
               description: str) -> None:
        self.__metadata_creator.update_finished_flag(self.executor_name, False)

        self.__thread_pool.submit(self.__pipeline,
                                  module_path,
                                  method_parameters,
                                  description)

    def __pipeline(self,
                   module_path: str,
                   method_parameters: dict,
                   description: str) -> None:
        try:
            importlib.import_module(module_path)
            model_instance = self.__storage.read(self.parent_name,
                                                 self.parent_name_service_type)
            method_result = self.__execute_a_object_method(model_instance,
                                                           self.class_method,
                                                           method_parameters)
            self.__storage.save(method_result, self.executor_name,
                                self.executor_service_type)
            self.__metadata_creator.update_finished_flag(self.executor_name,
                                                         flag=True)

        except Exception as exception:
            self.__metadata_creator.create_execution_document(
                self.executor_name,
                description,
                method_parameters,
                repr(exception))
            return None

        self.__metadata_creator.create_execution_document(self.executor_name,
                                                          description,
                                                          method_parameters,
                                                          )

    def __execute_a_object_method(self, class_instance: object, method: str,
                                  parameters: dict) -> object:
        model_method = getattr(class_instance, method)

        treated_parameters = self.__parameters_handler.treat(parameters)
        return model_method(**treated_parameters)