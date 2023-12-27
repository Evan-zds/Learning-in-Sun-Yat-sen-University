import os
import re
import sys
import glob
import datetime
import numpy as np
from osgeo import gdal


class RasterTiff:
    """创建Raster类"""
    gdal.AllRegister()

    def read_img(self, filename):
        """读取栅格文件"""
        dataset = gdal.Open(filename)
        im_width = dataset.RasterXSize
        im_height = dataset.RasterYSize
        im_bands = dataset.RasterCount

        im_geotrans = dataset.GetGeoTransform()
        im_proj = dataset.GetProjection()
        im_data = dataset.ReadAsArray(0, 0, im_width, im_height)

        print(type(im_data), im_data.shape)

        del dataset
        return im_height, im_width, im_bands, im_geotrans, im_proj, im_data

    def write_img(self, filename, im_geotrans, im_proj, im_data):
        """写入栅格数据"""
        # 判断栅格数据类型
        if 'int8' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32

        # 判断数组维数
        if len(im_data.shape) == 3:
            im_bands, im_height, im_width = im_data.shape
        elif len(im_data.shape) == 2:
            im_bands, (im_height, im_width) = 1, im_data.shape

        ## 创建文件
        # 定义数据类型
        driver = gdal.GetDriverByName('GTiff')
        dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)

        dataset.SetGeoTransform(im_geotrans)
        dataset.SetProjection(im_proj)

        # 根据波段写入数据
        if im_bands == 1:
            dataset.GetRasterBand(1).WriteArray(im_data)
        else:
            for i in range(0, im_bands):
                dataset.GetRasterBand(i + 1).WriteArray(im_data[i])

        del dataset


def month_statistics(year_param, month_param):
    """获取当月第一天，最后一天和当月天数"""
    first_day_this_month = datetime.date(year_param, month_param, day=1)
    if month_param == 12:
        first_day_next_month = datetime.date(year_param + 1, month=1, day=1)
    else:
        first_day_next_month = datetime.date(year_param, month_param + 1, day=1)

    last_day_this_month = first_day_next_month - datetime.timedelta(days=1)
    days_this_month = last_day_this_month.day

    return first_day_this_month, last_day_this_month, days_this_month


path = r'E:\Data\光合有效辐射PAR'
for year_folder in os.listdir(path):
    year_index = int(year_folder)
    if 2004 <= year_index <= 2016:
        print(f'Year: {year_folder}')
        year_folder_path = os.path.join(path, year_folder)
        all_tif_files_list = sorted(glob.glob(os.path.join(year_folder_path, '*.tif')))

        for month_index in range(1, 13):
            monthly_tif_list = []
            for file in all_tif_files_list:
                name_date_file = re.findall('GLASS04B01.V42.A(\d{7})', file)[0]
                datetime_date_file = datetime.datetime.strptime(name_date_file, '%Y%j')
                year_date_file, month_date_file = datetime_date_file.year, datetime_date_file.month
                if year_index == year_date_file and month_index == month_date_file:
                    monthly_tif_list.append([os.path.join(year_folder_path, file)])
            # print(monthly_tif_list)
            raster = RasterTiff()
            new_monthly_tif_list = []
            for monthly_tif in monthly_tif_list:
                rows, columns, bands, geotrans, proj, pixel_data = raster.read_img(monthly_tif[0])
                pixel_data = pixel_data.astype(np.float32)
                monthly_tif.extend([rows, columns, bands, geotrans, proj, pixel_data])
                new_monthly_tif_list.append(monthly_tif)

            data_month_aggregation = np.zeros(shape=(new_monthly_tif_list[0][1], new_monthly_tif_list[0][2]), dtype=np.float32)
            for new_monthly_tif in new_monthly_tif_list:
                new_monthly_tif[-1][np.where((new_monthly_tif[-1] < 0) | (new_monthly_tif[-1] > 130000))] = np.nan
                data_month_aggregation += new_monthly_tif[-1]

            scale_factor = 0.01
            data_month_aggregation = data_month_aggregation * scale_factor
            raster.write_img(os.path.join(path, year_folder, f'PAR{year_index}_{month_index}.tif'), new_monthly_tif_list[0][4], new_monthly_tif_list[0][5], data_month_aggregation)
            print(f'Converting PAR{year_index}_{month_index}.tif successfully.')
print('done!')