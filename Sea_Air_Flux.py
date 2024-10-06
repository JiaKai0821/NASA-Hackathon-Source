import rasterio
import matplotlib.pyplot as plt
from rasterio.plot import show
import numpy as np
from matplotlib.colors import LogNorm

# 讀取 GeoTIFF 文件
tiff_file = 'ECCO-Darwin_CO2_flux_202212.tif'

# 使用 rasterio 打開 GeoTIFF 文件
with rasterio.open(tiff_file) as src:
    data = src.read(1)  # 讀取第一個波段
    
    data[data == -9999] = np.nan
    max_value = np.max(data)
    min_value = np.min(data)
    print(f"Maximum value : {max_value}")
    print(f"Minimum value : {min_value}")
    
    #data = np.abs(data) #數值轉換成正值
    data = data*86400 #換成每天的排放量從s->day
    
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
    cax = ax.imshow(data,extent=[lon.min(), lon.max(), lat.min(), lat.max()], cmap='plasma', vmin=-20, vmax=20)

    # 添加顏色條，設置位置為右側
    cbar = fig.colorbar(cax, ax=ax, orientation='vertical', shrink=0.8)
    cbar.set_label(r'$mmol /\, m^{2} \,day$')

    # 添加標題
    plt.title("2022 December Sea - Air CO2 Flux")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    plt.savefig("2020 December CO2_flux.png", dpi=600, bbox_inches='tight')
    # 顯示圖像
    plt.show()
