import os
from typing import Dict
from core.saltlux.utils import generate_key, get_dir_name, get_path, remove_dirs, run_container_fg, CustomError
from core.saltlux.resource import DataResource, PreprocessResource


class Prepare():
    def __init__(self, data_resource: DataResource, preprocess_resource: PreprocessResource):
        self.data_resource = data_resource
        self.preprocess_resource = preprocess_resource
        self.data_dir = self.data_resource.working_dir
        self.preprocess_dir = self.preprocess_resource.working_dir
        self.config = self.preprocess_resource.configs['prepare']
        self.metadata = 'data.lst'

    def __call__(self, param: Dict) -> Dict:
        dataset_key_list = param["datasetKeyList"]
        # dataset_name_list = param["datasetNameList"] # deprecated parameter
        pre_dataset_name = param["preDatasetName"]

        pre_dataset_key = generate_key('preDataset')
        pre_dataset_dir_name = get_dir_name(pre_dataset_key, pre_dataset_name)

        prepare_path = get_path(self.preprocess_dir, pre_dataset_dir_name, makedir=True)

        try:
            dataset_name_list = []
            for dataset_key in dataset_key_list:
                if not self.data_resource.is_valid_key(dataset_key):
                    raise CustomError(-950, 'invalid dataset key : {}'.format(dataset_key))

                dataset_name_list.append(self.data_resource.get_dataset_name(dataset_key))

            metadata_path = get_path(prepare_path, self.metadata)
            metadatas = []
            for dataset_name, dataset_key in zip(dataset_name_list, dataset_key_list):
                dataset_dir = get_dir_name(dataset_key, dataset_name)
                dataset_metadata_path = get_path(self.data_dir, dataset_dir, self.metadata)
                with open(dataset_metadata_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                for line in lines:
                    metadatas.append(line.strip().replace('.wav', '.pcm'))

            with open(metadata_path, 'w', encoding='utf-8') as f:
                for data in metadatas:
                    f.write(data + '\n')

            container_data_dir = self.config['docker']['dataset_dir']
            container_preprocess_dir = self.config['docker']['preprocess_dir']
            container_metadata_path = metadata_path.replace(self.preprocess_dir, container_preprocess_dir)
            container_image = self.config['docker']['image']
            container_wd = self.config['docker']['working_dir']
            container_command = './{} {}'.format(self.config['docker']['run_script'], container_metadata_path)

            container_volumes = {self.data_dir: {'bind': container_data_dir, 'mode': 'rw'},
                       self.preprocess_dir: {'bind': container_preprocess_dir, 'mode': 'rw'}}

            _ = run_container_fg(name=pre_dataset_key, command=container_command, image=container_image,
                                    working_dir=container_wd, volumes=container_volumes)

            self.preprocess_resource.refresh()

        except Exception as e:
            remove_dirs(prepare_path)
            return {"result": None, "errorCode": -1 if not isinstance(e, CustomError) else e.get_code(), "errorMessage": str(e)}

        return {"result": pre_dataset_key, "errorCode": 0, "errorMessage": ""}
