import h5py

# HDF5 파일 열기
with h5py.File('demo/model_demo.h5', 'r') as file:
    # 파일 내의 그룹 및 데이터셋 리스트 확인
    def print_attrs(name, obj):
        print(name)
        for key, val in obj.attrs.items():
            print("    %s: %s" % (key, val))

    file.visititems(print_attrs)