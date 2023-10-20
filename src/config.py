# config.py 
# 컴파일러, 생성기, 옵션을 설정할 수 있습니다.
import os
import platform
from datetime import datetime

# 텔레그램 Chat ID 와 Token 값으로 직접 넣어주어야 합니다!
CHAT_ID = ""
HIGH_SEVERITY_CHAT_ID = ""
TOKEN = ""

# 수행 횟수 및 타임아웃 설정
total_tasks = 100 
generator_time_out = 10
compile_time_out = 30
binary_time_out = 10

# output 디렉토리 양식
BASE_DIR = f'output_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'

# catch시 결과 txt, json 이름 양식
def get_result_file_names(id):
    return {
        "txt": f"{id}_result.txt",
        "json": f"{id}_result.json"
    }

# linux 생성기 설정
linux_generators_config = {
    'csmith': {
        'name': 'csmith',
        'binary_path': 'csmith',
        'language': 'c',
        'options': [
            "--max-array-dim 3", 
            "--max-array-len-per-dim 10",
            "--max-block-depth 3",
            "--max-block-size 5",
            "--max-expr-complexity 10",
            "--max-funcs 4",
            "--max-pointer-depth 3",
            "--max-struct-fields 10",
            "--max-union-fields 10",
            "--muls",
            "--safe-math",
            "--no-packed-struct",
            "--pointers",
            "--structs",
            "--unions",
            "--volatiles",
            "--volatile-pointers",
            "--const-pointers",
            "--global-variables",
            "--no-builtins",
            "--inline-function",
            "--inline-function-prob 50"
        ],
        'output_format': '{generator} {options} -o {filepath} --seed {random_seed}',
        'src_files': ['{path}/random_program_{id}.c'],
        'src_files_to_send': ['{path}/random_program_{id}.c'],
        'zip_required': False,
        'zip_name': None,
        'include_dir': '/usr/local/include/',
        'path_type': 'filepath'
    },
    'yarpgen': {
        'name': 'yarpgen',
        'binary_path': 'yarpgen',
        'language': 'c',
        'options': [
            "--std=c",
            "--mutate=all"
        ],
        'output_format': '{generator} {options} -o {dir_path} --seed={random_seed} --mutation-seed={random_seed}',
        'src_files': ['{path}/driver.c', '{path}/func.c'],
        'src_files_to_send': ['{path}/driver.c', '{path}/func.c', '{path}/init.h'],
        'zip_required': True,
        'zip_name': "yarpgen_{id}.zip",
        'include_dir': '{path}',
        'path_type': 'dirpath'
    },
    'yarpgen_scalar': {
        'name': 'yarpgen_scalar',
        'binary_path': 'yarpgen_scalar',
        'language': 'c',
        'options': [
            "--std=c99"
        ],
        'output_format': '{generator} {options} -d {dir_path} --seed={random_seed}',
        'src_files': ['{path}/driver.c', '{path}/func.c'],
        'src_files_to_send': ['{path}/driver.c', '{path}/func.c', '{path}/init.h'],
        'zip_required': True,
        'zip_name': "yarpgen_scalar_{id}.zip",
        'include_dir': '{path}',
        'path_type': 'dirpath'
    }
}

# 리눅스 리틀 엔디안 컴파일러 설정
linux_little_endian_compilers = {
    "emcc": {
        "name": "emscription",
        "file_name": "emcc",
        "options": ["-O0", "-O1", "-O2", "-O3"],
        "output_format": "{compiler_path} {src_files} -o {exe_path}.html -s STANDALONE_WASM {optimization} -I {include_dir}",
        "language": {
            "c": {
                "binary_path": "emcc",
                "runners": {
                    "wasmer": "wasmer {exe_path}.wasm",
                    "wasmtime": "wasmtime {exe_path}.wasm",
                    "node": "node {exe_path}.js"
                }  
            },
            "cpp": {
                "binary_path": "em++",
                "runners": {
                    "wasmer": "wasmer {exe_path}.wasm",
                    "wasmtime": "wasmtime {exe_path}.wasm",
                    "node": "node {exe_path}.js"
                }  
            }
        }
    },
    "wasicc": {
        "name": "wasienv",
        "file_name": "wasicc",
        "options": ["-O0", "-O1", "-O2", "-O3"],
        "output_format": "{compiler_path} {src_files} -o {exe_path} {optimization} -I {include_dir}",
        "language": {
            "c": {
                "binary_path": "wasicc",
                "runners": {
                    "wasmer": "wasmer {exe_path}.wasm",
                    "wasmtime": "wasmtime {exe_path}.wasm",
                    "wasirun": "wasirun {exe_path}.wasm"
                }
            },
            "cpp": {
                "binary_path": "wasic++",
                "runners": {
                    "wasmer": "wasmer {exe_path}.wasm",
                    "wasmtime": "wasmtime {exe_path}.wasm",
                    "wasirun": "wasirun {exe_path}.wasm"
                }
            }
        }
    }
}

# platform에 따라서 생성기 설정 결정
if platform.system() == 'Linux':
    generators_config = linux_generators_config


# 결정된 생성기에 따라서 output 디렉토리의 트리 구조 결정
GENERATOR_DIRS = {key: os.path.join(BASE_DIR, config['name']) for key, config in generators_config.items()}
CATCH_DIRS = {key: os.path.join(GENERATOR_DIRS[key], 'catch') for key in generators_config.keys()}
TEMP_DIRS = {key: os.path.join(GENERATOR_DIRS[key], 'temp') for key in generators_config.keys()}