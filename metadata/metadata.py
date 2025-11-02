import os
from PIL import Image
from pillow_heif import register_heif_opener
from datetime import datetime

# HEIC 포맷 지원 등록
register_heif_opener()


def quick_photo_summary(file_path):
    """
    HEIC/JPEG 파일의 촬영 시각 + GPS 좌표 + BBox 유효성 + 오늘 여부 출력
    """
    try:
        img = Image.open(file_path)
        exif = img.getexif()

        # 날짜
        date_str = None
        if exif:
            from PIL.ExifTags import TAGS

            for tag_id, value in exif.items():
                tag_name = TAGS.get(tag_id, tag_id)
                if tag_name in ("DateTimeOriginal", "DateTime"):
                    date_str = value
                    break

        # GPS 추출
        coords = extract_gps_coordinates(file_path)
        if not coords:
            print("\n⚠️ GPS 정보 없음 (좌표 없음)")
            return

        lat, lon = coords
        inside = is_in_bbox(lat, lon)

        # 오늘 날짜 비교
        today_str = datetime.now().strftime("%Y:%m:%d")  # exif 날짜 포맷과 동일하게
        is_today = date_str and date_str.startswith(today_str)

        # 결과 출력
        print("\n" + "=" * 60)
        print(f"📸 파일명: {os.path.basename(file_path)}")
        print(f"🕒 촬영 시각: {date_str if date_str else '(정보 없음)'}")
        print(
            f"📅 오늘 여부: {'✅ PASS (오늘 촬영)' if is_today else '❌ NON PASS (오늘 아님)'}"
        )
        print(f"📍 좌표: {lat:.6f}, {lon:.6f}")
        print(f"🌐 지도: https://www.google.com/maps?q={lat},{lon}")
        print(f"📦 위치 판정: {'✅ BBox 내부' if inside else '❌ BBox 외부'}")
        print("=" * 60)

    except Exception as e:
        print(f"❌ 처리 중 오류: {str(e)}")


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
            if lat_ref == "S":
                latitude = -latitude

            longitude = convert_to_degrees(lon)
            if lon_ref == "W":
                longitude = -longitude

            return (latitude, longitude)

        return None

    except Exception as e:
        print(f"GPS 추출 오류: {str(e)}")
        return None


# ============================================
# ✅ BBox 유효성 검사 함수
# ============================================

# BBox 경계 (위도/경도)
MIN_LAT = 37.704316
MAX_LAT = 37.719660
MIN_LON = 126.683397
MAX_LON = 126.690022


def is_in_bbox(lat, lon):
    """주어진 위도(lat), 경도(lon)가 BBox 내부에 있으면 True"""
    return (MIN_LAT <= lat <= MAX_LAT) and (MIN_LON <= lon <= MAX_LON)


def check_gps_in_bbox(file_path):
    """HEIC 또는 JPG 파일 GPS가 지정된 BBox 내부인지 확인"""
    coords = extract_gps_coordinates(file_path)
    if not coords:
        print("⚠️ GPS 정보가 없습니다.")
        return

    # 날짜/시간 추출
    img = Image.open(file_path)
    exif = img.getexif()
    date_str = None
    if exif:
        for tag_id, value in exif.items():
            from PIL.ExifTags import TAGS

            tag_name = TAGS.get(tag_id, tag_id)
            if tag_name in ("DateTimeOriginal", "DateTime"):
                date_str = value
                break

    lat, lon = coords
    inside = is_in_bbox(lat, lon)

    # ===========================
    # 깔끔한 결과 출력
    # ===========================
    print("\n" + "=" * 50)
    print(f"📸 파일명: {os.path.basename(file_path)}")
    if date_str:
        print(f"🕒 촬영 시각: {date_str}")
    else:
        print("🕒 촬영 시각: (정보 없음)")
    print(f"📍 GPS: {lat:.6f}, {lon:.6f}")
    print(f"🌐 지도: https://www.google.com/maps?q={lat},{lon}")
    print(f"📦 위치 판정: {'✅ BBox 내부' if inside else '❌ BBox 외부'}")
    print("=" * 50)


# 사용 예시
if __name__ == "__main__":

    file_path = "your image path"

    # "C:/Users/Seung/Desktop/Dacon/dataset/photo/IMG_0954.HEIC"
    # "C:/Users/Seung/Documents/카카오톡 받은 파일/test4.jpg"

    if os.path.exists(file_path):
        quick_photo_summary(file_path)
    else:
        print(f"⚠️ 파일을 찾을 수 없습니다: {file_path}")
