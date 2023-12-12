import os
import arcpy


arcpy.env.overwriteOutput = True
arcpy.env.workspace = r'D:\我的论文\中国河流水化学组成的时空变化特征及其影响因素的研究\河流水化学组成的时空变化特征及其影响因素的研究\data\陆地蒸散发与GPP.gdb'
path = r'I:\DATA\全球PML_V2陆地蒸散发与GPP（2002.07-2019.08）'

for year_index in range(2003, 2020):
    if not os.path.isdir(os.path.join(path, str(year_index))):
        print(f'The file {year_index} is note a dir.')
        continue
    else:
        sub_path = os.path.join(path, str(year_index))
        for file in os.listdir(sub_path):
            in_raster = os.path.join(sub_path, file)
            for i in range(0, 5):
                band_index = i
                if i == 0:
                    out_rasterlayer = f'GPP{file[: -4]}'
                elif i == 1:
                    out_rasterlayer = f'Ec{file[: -4]}'
                elif i == 2:
                    out_rasterlayer = f'Ei{file[: -4]}'
                elif i == 3:
                    out_rasterlayer = f'Es{file[: -4]}'
                else:
                    out_rasterlayer = f'ET_water{file[: -4]}'

                arcpy.management.MakeRasterLayer(in_raster, out_rasterlayer, band_index=band_index)

                in_copy_raster = out_rasterlayer
                if 'GPP' in in_copy_raster:
                    out_copy_raster = rf'D:\我的论文\中国河流水化学组成的时空变化特征及其影响因素的研究\河流水化学组成的时空变化特征及其影响因素的研究\data\GPP\GPP{file}'
                elif 'Ec' in in_copy_raster:
                    out_copy_raster = rf'D:\我的论文\中国河流水化学组成的时空变化特征及其影响因素的研究\河流水化学组成的时空变化特征及其影响因素的研究\data\Ec\Ec{file}'
                elif 'Ei' in in_copy_raster:
                    out_copy_raster = rf'D:\我的论文\中国河流水化学组成的时空变化特征及其影响因素的研究\河流水化学组成的时空变化特征及其影响因素的研究\data\Ei\Ei{file}'
                elif 'Es' in in_copy_raster:
                    out_copy_raster = rf'D:\我的论文\中国河流水化学组成的时空变化特征及其影响因素的研究\河流水化学组成的时空变化特征及其影响因素的研究\data\Es\Es{file}'
                else:
                    out_copy_raster = rf'D:\我的论文\中国河流水化学组成的时空变化特征及其影响因素的研究\河流水化学组成的时空变化特征及其影响因素的研究\data\ET_water\ET_water{file}'

                pixel_type = '16_BIT_UNSIGNED'
                format = 'Tiff'
                arcpy.management.CopyRaster(in_copy_raster, out_copy_raster, pixel_type=pixel_type, format=format)
                print(f'Copying {file} successfully.')
print('done!')


