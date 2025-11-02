import os
from PIL import Image
from pillow_heif import register_heif_opener
from datetime import datetime

# HEIC 포맷 지원 등록
register_heif_opener()


def view_heic_metadata(file_path):
    """
    HEIC 파일의 메타데이터 출력
    
    Args:
        file_path: HEIC 파일 경로
    """
    if not os.path.exists(file_path):
        print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
        return
    
    try:
        # HEIC 파일 열기
        img = Image.open(file_path)
        
        print("\n" + "=" * 70)
        print(f"📸 HEIC 메타데이터: {os.path.basename(file_path)}")
        print("=" * 70)
        
        # 기본 정보
        print("\n[기본 정보]")
        print(f"파일 크기: {os.path.getsize(file_path) / 1024:.2f} KB")
        print(f"이미지 크기: {img.size[0]} x {img.size[1]} pixels")
        print(f"포맷: {img.format}")
        print(f"모드: {img.mode}")
        
        # EXIF 데이터
        exif = img.getexif()
        if exif:
            print("\n[EXIF 데이터]")
            exif_data = {}
            
            # EXIF 태그 매핑
            from PIL.ExifTags import TAGS, GPSTAGS
            
            for tag_id, value in exif.items():
                tag_name = TAGS.get(tag_id, tag_id)
                
                # GPS 정보 처리
                if tag_name == "GPSInfo":
                    # GPSInfo가 딕셔너리인 경우만 처리
                    if isinstance(value, dict):
                        gps_data = {}
                        for gps_tag_id, gps_value in value.items():
                            gps_tag_name = GPSTAGS.get(gps_tag_id, gps_tag_id)
                            gps_data[gps_tag_name] = gps_value
                        exif_data[tag_name] = gps_data
                    else:
                        # 딕셔너리가 아니면 그냥 값 저장
                        exif_data[tag_name] = value
                else:
                    exif_data[tag_name] = value
            
            # 주요 정보만 출력
            important_tags = [
                "Make", "Model", "DateTime", "DateTimeOriginal",
                "Orientation", "Software", "ExposureTime", "FNumber",
                "ISO", "FocalLength", "Flash", "WhiteBalance",
                "GPSInfo", "LensModel", "LensMake"
            ]
            
            for tag in important_tags:
                if tag in exif_data:
                    value = exif_data[tag]
                    
                    # GPS 정보 포맷팅
                    if tag == "GPSInfo" and isinstance(value, dict):
                        print(f"\n{tag}:")
                        for gps_key, gps_val in value.items():
                            print(f"  {gps_key}: {gps_val}")
                    else:
                        # 바이트 데이터는 디코딩
                        if isinstance(value, bytes):
                            try:
                                value = value.decode('utf-8').strip('\x00')
                            except:
                                value = str(value)
                        print(f"{tag}: {value}")
            
            # 전체 태그 보기 (선택적)
            print("\n[전체 EXIF 태그]")
            for tag_name, value in sorted(exif_data.items()):
                if tag_name not in important_tags:
                    if isinstance(value, bytes):
                        try:
                            value = value.decode('utf-8').strip('\x00')
                        except:
                            value = f"<bytes: {len(value)} bytes>"
                    elif isinstance(value, dict):
                        continue
                    print(f"{tag_name}: {value}")
        else:
            print("\n⚠️ EXIF 데이터가 없습니다.")
        
        # 추가 정보
        if hasattr(img, 'info'):
            print("\n[추가 정보]")
            for key, value in img.info.items():
                if key != 'exif':
                    print(f"{key}: {value}")
        
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()


def extract_gps_coordinates(file_path):
    """
    HEIC 파일에서 GPS 좌표 추출
    
    Returns:
        (latitude, longitude) or None
    """
    try:
        img = Image.open(file_path)
        exif = img.getexif()
        
        if not exif:
            return None
        
        gps_info = exif.get_ifd(0x8825)  # GPS IFD
        
        if not gps_info:
            return None
        
        def convert_to_degrees(value):
            """DMS (Degrees, Minutes, Seconds)를 십진수로 변환"""
            d, m, s = value
            return d + (m / 60.0) + (s / 3600.0)
        
        lat = gps_info.get(2)  # GPSLatitude
        lat_ref = gps_info.get(1)  # GPSLatitudeRef
        lon = gps_info.get(4)  # GPSLongitude
        lon_ref = gps_info.get(3)  # GPSLongitudeRef
        
        if lat and lon:
            latitude = convert_to_degrees(lat)
            if lat_ref == 'S':
                latitude = -latitude
            
            longitude = convert_to_degrees(lon)
            if lon_ref == 'W':
                longitude = -longitude
            
            return (latitude, longitude)
        
        return None
        
    except Exception as e:
        print(f"GPS 추출 오류: {str(e)}")
        return None


def batch_view_metadata(directory):
    """
    폴더 내 모든 HEIC 파일의 메타데이터 출력
    
    Args:
        directory: 폴더 경로
    """
    if not os.path.isdir(directory):
        print(f"❌ 폴더를 찾을 수 없습니다: {directory}")
        return
    
    heic_files = [f for f in os.listdir(directory) 
                  if f.lower().endswith(('.heic', '.heif'))]
    
    if not heic_files:
        print(f"⚠️ HEIC 파일이 없습니다: {directory}")
        return
    
    print(f"\n📂 총 {len(heic_files)}개의 HEIC 파일 발견")
    
    for i, filename in enumerate(heic_files, 1):
        file_path = os.path.join(directory, filename)
        print(f"\n[{i}/{len(heic_files)}]")
        view_heic_metadata(file_path)
        
        # GPS 좌표 추출
        coords = extract_gps_coordinates(file_path)
        if coords:
            print(f"\n🗺️ GPS 좌표: {coords[0]:.6f}, {coords[1]:.6f}")
            print(f"   Google Maps: https://www.google.com/maps?q={coords[0]},{coords[1]}")


# 사용 예시
if __name__ == "__main__":
    # 필요한 패키지 설치 안내
    print("📦 필요한 패키지:")
    print("   pip install pillow pillow-heif")
    print()
    
    # 단일 파일 메타데이터 보기
    file_path = "../202511__/IMG_0972.heic"  # 여기에 파일 경로 입력
    
    if os.path.exists(file_path):
        view_heic_metadata(file_path)
        
        # GPS 좌표 추출
        coords = extract_gps_coordinates(file_path)
        if coords:
            print(f"\n🗺️ GPS 좌표: {coords[0]:.6f}, {coords[1]:.6f}")
            print(f"   Google Maps: https://www.google.com/maps?q={coords[0]},{coords[1]}")
    else:
        print(f"⚠️ 파일을 찾을 수 없습니다: {file_path}")
        print("\n💡 사용법:")
        print("   # 단일 파일")
        print('   view_heic_metadata("your_photo.heic")')
        print("\n   # 폴더 전체")
        print('   batch_view_metadata("./photos")')