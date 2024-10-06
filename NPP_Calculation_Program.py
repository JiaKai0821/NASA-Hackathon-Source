import rasterio
import matplotlib.pyplot as plt
from rasterio.plot import show
import numpy as np
from matplotlib.colors import LogNorm

year = 2023
date_list = []

# 每個月的起始和結束日期
month_days = {
    1: (101, 131),   # 1月從 0101 到 0131
    2: (202, 228),   # 2月從 0202 到 0228 (不考慮閏年)
    3: (301, 331),   # 3月從 0301 到 0331
    4: (401, 430),   # 4月從 0401 到 0430
    5: (501, 531),   # 5月從 0501 到 0531
    6: (601, 630),   # 6月從 0601 到 0630
    7: (701, 731),   # 7月從 0701 到 0731
    8: (801, 831),   # 8月從 0801 到 0831
    9: (901, 930),   # 9月從 0901 到 0930
    10: (1001, 1031),# 10月從 1001 到 1031
    11: (1101, 1130),# 11月從 1101 到 1130
    12: (1201, 1231) # 12月從 1201 到 1231
}

# 根據每個月的天數生成對應的日期
for month, (start, end) in month_days.items():
    for day in range(start, end + 1):
        # 將日期轉換為2023開頭的8位數格式並加入列表
        date_str = f"{year}{str(day).zfill(4)}"
        date_list.append(date_str)
        
for i in range(len(date_list)):
    file_name = 'MiCASA_v1_NPP_x3600_y1800_daily_' + date_list[i] + '.tif'
    
    
    # 讀取 GeoTIFF 文件
    tiff_file = file_name
    
    # 使用 rasterio 打開 GeoTIFF 文件
    with rasterio.open(tiff_file) as src:
        data = src.read(1)  # 讀取第一個波段
        
        #data[data == -9999] = np.nan
        max_value = np.max(data)
        min_value = np.min(data)
        print(f"Maximum value : {max_value}")
        print(f"Minimum value : {min_value}")
        
        #data = np.abs(data) #數值轉換成正值
        #data = data*86400 #換成每天的排放量從s->day
        
        #data[data >= 1e7] = np.nan
        
        #計算出最大數值與最小數值
        max_value = np.max(data)
        min_value = np.min(data)
        print(f"Maximum value : {max_value}")
        print(f"Minimum value : {min_value}")
        
        #norm=LogNorm(vmin=1e-4, vmax=1e9)
        #變換矩陣
        transform = src.transform
        rows, cols = data.shape #(721, 1440)
        row_indices, col_indices = np.meshgrid(np.arange(rows), np.arange(cols), indexing="ij")
        
        def pixel_to_coords(row, col):
            x, y = transform * (col, row)
            return x,y
        
        lon, lat = pixel_to_coords(row_indices, col_indices)
        
    
        # 創建繪圖窗口
        fig, ax = plt.subplots(figsize=(10, 6))
        # 繪製 GeoTIFF 數據並設置顏色映射
        cax = ax.imshow(data,extent=[lon.min(), lon.max(), lat.min(), lat.max()], cmap='plasma', norm=LogNorm(1e-6, 1e2))
    
        # 添加顏色條，設置位置為右側
        cbar = fig.colorbar(cax, ax=ax, orientation='vertical', shrink=0.8)
        cbar.set_label(r'$g \,Carbon/\, m^{2} \,day$')
    
        # 添加標題
        title = date_list[i] + "NPP CO2 Flux"
        fig_name = date_list[i] + "NPP CO2 Flux.png"
        plt.title(title)
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
    
        plt.savefig(fig_name, dpi=300, bbox_inches='tight')
        # 顯示圖像
        plt.show()

