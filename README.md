# encrypt_decrypt_files
encrypt: encrypt a file.
        encrypt.py encrypt $file_name
        OR
        encrypt.py encrypt $file_name $key

decrypt: decrypt a file.
        encrypt.py decrypt $file_name
        OR
        encrypt.py decrypt $file_name $key

generate: generate keys.
        encrypt.py generate
        OR
        encrypt.py generate $nb_of_keys

help:
        encrypt.py help
